#!/usr/bin/env python3
"""Cliente de geração do Replicate para curtas animados.

Uso: python3 gerar.py <pasta-do-curta> <comando> [códigos...] [opções]

Comandos:
  listar                  itens, estado em disco, tamanho do prompt, custo, livro e teto
  simular <códigos>       imprime prompt final e payload (sem URLs), sem chamar a API
  gerar <códigos>         gera (paralelo); pula o que existe, salvo com --refazer
  gerar --teste-fumaca    1 vídeo de 5 s, 480p, 9:16, com áudio, ref K1 -> raw/_fumaca.mp4

Códigos: imagem = K2; vídeo = T1a, T1b (T1 = todas as versões).
Só biblioteca padrão (Python 3.9). O token nunca é impresso nem gravado.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor

API = "https://api.replicate.com/v1"
UA = "curta-gerar/1.0 (python-urllib)"
LOCK = threading.Lock()
PRINT_LOCK = threading.Lock()
LIMITE_UPLOAD_SEM_REDUZIR = 10 * 1024 * 1024  # acima disso, reduz para JPEG 2048


def log(msg):
    with PRINT_LOCK:
        print(msg, flush=True)


class Erro(Exception):
    pass


# ---------------------------------------------------------------- token / HTTP

_TOKEN = None


def token():
    global _TOKEN
    if _TOKEN:
        return _TOKEN
    t = os.environ.get("REPLICATE_API_TOKEN", "").strip()
    if not t:
        try:
            with open(os.path.expanduser("~/.zshrc"), encoding="utf-8") as f:
                for linha in f:
                    if linha.startswith("export REPLICATE_API_TOKEN="):
                        t = linha.split("=", 1)[1].strip().strip("'\"")
                        break
        except OSError:
            pass
    if not t:
        raise Erro("REPLICATE_API_TOKEN não encontrado (ambiente nem ~/.zshrc).")
    _TOKEN = t
    return t


def http(method, url, body=None, headers=None, timeout=120, raw=False):
    h = {"Authorization": "Bearer " + token(), "User-Agent": UA}
    if headers:
        h.update(headers)
    data = None
    if body is not None:
        if isinstance(body, (bytes, bytearray)):
            data = bytes(body)
        else:
            data = json.dumps(body).encode()
            h.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            conteudo = r.read()
            return conteudo if raw else (json.loads(conteudo) if conteudo else {})
    except urllib.error.HTTPError as e:
        try:
            detalhe = e.read().decode("utf-8", "replace")[:600]
        except Exception:
            detalhe = ""
        err = Erro("HTTP %s em %s %s: %s" % (e.code, method, url.split("?")[0], detalhe))
        err.status = e.code
        raise err
    except urllib.error.URLError as e:
        raise Erro("Falha de rede em %s %s: %s" % (method, url.split("?")[0], e.reason))


def baixar(url, destino):
    tmp = destino + ".parcial"
    h = {"User-Agent": UA}
    host = urllib.parse.urlparse(url).hostname or ""
    if host.endswith("replicate.delivery") or host.endswith("replicate.com"):
        h["Authorization"] = "Bearer " + token()
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=600) as r, open(tmp, "wb") as f:
            shutil.copyfileobj(r, f)
    except urllib.error.HTTPError as e:
        raise Erro("HTTP %s ao baixar a saída" % e.code)
    os.replace(tmp, destino)


import urllib.parse  # noqa: E402  (usado em baixar)


# ---------------------------------------------------------------- manifesto


class Curta:
    def __init__(self, pasta):
        self.pasta = os.path.abspath(pasta)
        with open(self.p("curta.json"), encoding="utf-8") as f:
            self.m = json.load(f)
        self.itens = {i["codigo"]: i for i in self.m["itens"]}
        self.precos = self.m.get("precos_usd", {})
        self.teto = float(self.m.get("teto_usd", 0))

    def p(self, *partes):
        return os.path.join(self.pasta, *partes)

    def ler(self, rel):
        with open(self.p(rel), encoding="utf-8") as f:
            return f.read().strip()

    # --- arquivos das referências e das saídas
    def arquivo_ref(self, cod):
        it = self.itens.get(cod)
        if it is None:
            raise Erro("Referência %s não existe no manifesto." % cod)
        if it["tipo"] == "pronta":
            return self.p(it["arquivo"])
        if it["tipo"] == "imagem":
            return self.p("assets", cod + ".png")
        raise Erro("Referência %s é do tipo %s, não é imagem." % (cod, it["tipo"]))

    def saida(self, job):
        if job["tipo"] == "imagem":
            return self.p("assets", job["codigo"] + ".png")
        return self.p("raw", job["codigo"] + ".mp4")

    # --- expandir códigos pedidos em tarefas
    def jobs(self, codigos):
        out = []
        for c in codigos:
            if c in self.itens:
                it = self.itens[c]
                if it["tipo"] == "video":
                    for v in it.get("versoes", [""]):
                        out.append(self._job(it, v))
                elif it["tipo"] == "imagem":
                    out.append(self._job(it, ""))
                else:
                    raise Erro("%s é uma imagem pronta; não se gera." % c)
                continue
            m = re.match(r"^(.*?)([a-z])$", c)
            if m and m.group(1) in self.itens and self.itens[m.group(1)]["tipo"] == "video":
                it = self.itens[m.group(1)]
                if m.group(2) not in it.get("versoes", []):
                    raise Erro("%s: versão '%s' não está em versoes %s." % (c, m.group(2), it.get("versoes")))
                out.append(self._job(it, m.group(2)))
                continue
            raise Erro("Código desconhecido: %s" % c)
        return out

    def _job(self, it, versao):
        j = {
            "codigo": it["codigo"] + versao,
            "item": it["codigo"],
            "tipo": it["tipo"],
            "refs": list(it.get("refs", [])),
            "proporcao": it.get("proporcao", "9:16"),
            "resolucao": it.get("resolucao"),
            "prompt_item": self.ler(it["prompt"]),
        }
        if it["tipo"] == "video":
            j["duracao"] = int(it.get("duracao", 5))
            j["audio"] = bool(it.get("audio", True))
            if "seed" in it:
                j["seed"] = it["seed"]
        return j

    def job_fumaca(self):
        return {
            "codigo": "_fumaca",
            "item": "_fumaca",
            "tipo": "video",
            "refs": ["K1"],
            "proporcao": "9:16",
            "resolucao": "480p",
            "duracao": 5,
            "audio": True,
            "sem_base": True,
            "prompt_item": (
                "{K1} is the model sheet of HE; it is an identity reference only and never appears on screen: "
                "no panels, no grey background. A stylised 3D animated feature film at feature-film render "
                "quality: sculpted, slightly exaggerated proportions, skin with soft subsurface scattering, "
                "hair in groomed clumps, real fabric texture, volumetric light, shallow depth of field. Never "
                "low-poly, plastic, game-like, photorealistic or 2D. One continuous close-up of HE, a lean young "
                "man of eighteen or nineteen with black wavy hair to his ears, in a plain charcoal-grey hoodie, "
                "sitting at his desk in his small bedroom at night; the room is cold blue from his monitor, "
                "whose screen never faces the camera. Slow push-in on his face. He types, then glances up and, "
                "only his mouth moving, says quietly in Brazilian Portuguese with a Brazilian accent: "
                "\"Tô trabalhando.\" Tô is one short syllable, never Estou. His voice is young, low and calm. "
                "Sound: soft fast typing and his one line; no music. No text, letters, subtitles, logos or watermarks."
            ),
        }

    # --- prompt
    def prompt(self, job):
        if job.get("sem_base"):
            texto = job["prompt_item"]
        else:
            base = self.ler(self.m["base_video" if job["tipo"] == "video" else "base_imagem"])
            texto = base + "\n\n" + job["prompt_item"]
        refs = job["refs"]

        def troca(mt):
            cod = mt.group(1)
            if cod not in refs:
                raise Erro("%s: marcador {%s} sem referência correspondente em refs %s." % (job["codigo"], cod, refs))
            n = refs.index(cod) + 1
            return ("[Image%d]" % n) if job["tipo"] == "video" else ("image %d" % n)

        texto = re.sub(r"\{([A-Za-z]+\d+)\}", troca, texto)
        sobra = re.findall(r"\{[^{}\s]{1,20}\}", texto)
        if sobra:
            raise Erro("%s: marcadores não resolvidos: %s" % (job["codigo"], ", ".join(sobra)))
        if job["tipo"] == "video":
            lim = int(self.m.get("limite_prompt_video", 4000))
            if len(texto) > lim:
                raise Erro("%s: prompt de vídeo com %d caracteres passa do limite %d." % (job["codigo"], len(texto), lim))
        return texto

    def custo(self, job):
        if job["tipo"] == "imagem":
            return float(self.precos["imagem"])
        chave = "video_%s_s" % job["resolucao"]
        if chave not in self.precos:
            raise Erro("Sem preço %s em precos_usd." % chave)
        return float(self.precos[chave]) * job["duracao"]

    def modelo(self, job):
        return self.m["modelo_video" if job["tipo"] == "video" else "modelo_imagem"]

    def payload(self, job, prompt, urls):
        if job["tipo"] == "video":
            d = {
                "prompt": prompt,
                "reference_images": urls,
                "duration": job["duracao"],
                "resolution": job["resolucao"],
                "aspect_ratio": job["proporcao"],
                "generate_audio": job["audio"],
            }
            if job.get("seed") is not None:
                d["seed"] = job["seed"]
            return d
        return {
            "prompt": prompt,
            "image_input": urls,
            "aspect_ratio": job["proporcao"],
            "resolution": job["resolucao"] or "2K",
            "output_format": "png",
        }

    # ------------------------------------------------------------ livro de gastos
    def livro(self):
        f = self.p("gastos.jsonl")
        if not os.path.exists(f):
            return []
        with open(f, encoding="utf-8") as fh:
            return [json.loads(l) for l in fh if l.strip()]

    def _grava_livro(self, linhas):
        f = self.p("gastos.jsonl")
        tmp = f + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            for l in linhas:
                fh.write(json.dumps(l, ensure_ascii=False) + "\n")
        os.replace(tmp, f)

    @staticmethod
    def conta(linha):
        # concluída com saída ou em curso conta; falha/cancelada sem saída conta zero
        if linha.get("estado") in ("failed", "canceled", "recusada", "erro_envio"):
            return 0.0
        return float(linha.get("custo_estimado_usd", 0))

    def total(self):
        return sum(self.conta(l) for l in self.livro())

    def reservar(self, job, payload_log):
        with LOCK:
            linhas = self.livro()
            soma = sum(self.conta(l) for l in linhas)
            custo = self.custo(job)
            if soma + custo > self.teto + 1e-9:
                raise Erro("%s recusado pelo teto: livro US$ %.2f + US$ %.2f > teto US$ %.2f."
                           % (job["codigo"], soma, custo, self.teto))
            linha = {
                "chamada": uuid.uuid4().hex[:12],
                "horario": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
                "codigo": job["codigo"],
                "modelo": self.modelo(job),
                "parametros": payload_log,
                "custo_estimado_usd": round(custo, 4),
                "predicao": None,
                "estado": "reservado",
                "metrics": None,
            }
            linhas.append(linha)
            self._grava_livro(linhas)
            return linha["chamada"]

    def atualizar(self, chamada, **campos):
        with LOCK:
            linhas = self.livro()
            for l in linhas:
                if l.get("chamada") == chamada:
                    l.update(campos)
            self._grava_livro(linhas)

    # ------------------------------------------------------------ referências (Files API)
    def _estado(self):
        f = self.p("estado.json")
        if os.path.exists(f):
            with open(f, encoding="utf-8") as fh:
                return json.load(fh)
        return {"arquivos": {}}

    def _grava_estado(self, e):
        f = self.p("estado.json")
        with open(f + ".tmp", "w", encoding="utf-8") as fh:
            json.dump(e, fh, ensure_ascii=False, indent=1)
        os.replace(f + ".tmp", f)

    def url_ref(self, cod, forcar=False):
        caminho = self.arquivo_ref(cod)
        if not os.path.exists(caminho):
            raise Erro("Referência %s ainda não existe em disco: %s" % (cod, caminho))
        with open(caminho, "rb") as fh:
            sha = hashlib.sha256(fh.read()).hexdigest()
        with LOCK:
            est = self._estado()
            reg = est["arquivos"].get(cod)
        if reg and not forcar and reg.get("sha256") == sha:
            exp = reg.get("expires_at")
            valido = True
            if exp:
                try:
                    t = dt.datetime.fromisoformat(exp.replace("Z", "+00:00"))
                    valido = t - dt.datetime.now(dt.timezone.utc) > dt.timedelta(minutes=30)
                except ValueError:
                    valido = True
            if valido:
                try:
                    http("GET", API + "/files/" + reg["id"], timeout=30)
                    return reg["url"]
                except Erro:
                    pass  # sumiu / expirou: sobe de novo
        enviar, mime, nome = caminho, "image/png", os.path.basename(caminho)
        tmpdir = None
        if os.path.getsize(caminho) > LIMITE_UPLOAD_SEM_REDUZIR:
            tmpdir = self.p(".tmp-upload")
            os.makedirs(tmpdir, exist_ok=True)
            enviar = os.path.join(tmpdir, cod + ".jpg")
            subprocess.run(["sips", "-Z", "2048", "-s", "format", "jpeg", "-s", "formatOptions", "92",
                            caminho, "--out", enviar], check=True, capture_output=True)
            mime, nome = "image/jpeg", cod + ".jpg"
        with open(enviar, "rb") as fh:
            dados = fh.read()
        limite = "----curta" + uuid.uuid4().hex
        corpo = (
            ("--%s\r\nContent-Disposition: form-data; name=\"content\"; filename=\"%s\"\r\n"
             "Content-Type: %s\r\n\r\n" % (limite, nome, mime)).encode() + dados +
            ("\r\n--%s\r\nContent-Disposition: form-data; name=\"type\"\r\n\r\n%s"
             "\r\n--%s\r\nContent-Disposition: form-data; name=\"filename\"\r\n\r\n%s"
             "\r\n--%s--\r\n" % (limite, mime, limite, nome, limite)).encode()
        )
        r = http("POST", API + "/files", body=corpo,
                 headers={"Content-Type": "multipart/form-data; boundary=" + limite}, timeout=300)
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)
        reg = {"id": r["id"], "url": r["urls"]["get"], "expires_at": r.get("expires_at"),
               "sha256": sha, "arquivo": os.path.relpath(caminho, self.pasta),
               "enviado": nome, "bytes": r.get("size")}
        with LOCK:
            est = self._estado()
            est["arquivos"][cod] = reg
            self._grava_estado(est)
        log("  ref %s enviada (%s, %.1f MB, expira %s)" % (cod, nome, len(dados) / 1e6, reg["expires_at"]))
        return reg["url"]


# ---------------------------------------------------------------- execução


def mover_antigo(caminho):
    base, ext = os.path.splitext(caminho)
    n = 1
    while os.path.exists("%s.antigo-%d%s" % (base, n, ext)):
        n += 1
    destino = "%s.antigo-%d%s" % (base, n, ext)
    os.rename(caminho, destino)
    return destino


def executar(curta, job, refazer):
    cod = job["codigo"]
    destino = curta.saida(job)
    if os.path.exists(destino):
        if not refazer:
            log("%s: já existe (%s), pulado." % (cod, os.path.relpath(destino, curta.pasta)))
            return {"codigo": cod, "estado": "pulado"}
    prompt = curta.prompt(job)
    payload_log = curta.payload(job, "<%d caracteres>" % len(prompt), ["<%s>" % r for r in job["refs"]])
    chamada = curta.reservar(job, payload_log)  # checa o teto antes de qualquer envio
    try:
        urls = [curta.url_ref(r) for r in job["refs"]]
    except Exception as e:
        curta.atualizar(chamada, estado="erro_envio", erro=str(e)[:300])
        raise
    payload = curta.payload(job, prompt, urls)
    if refazer and os.path.exists(destino):
        antigo = mover_antigo(destino)
        log("%s: anterior movido para %s" % (cod, os.path.basename(antigo)))
    t0 = time.time()
    try:
        pred = http("POST", API + "/models/%s/predictions" % curta.modelo(job), body={"input": payload}, timeout=120)
    except Erro as e:
        curta.atualizar(chamada, estado="erro_envio", erro=str(e)[:400])
        raise
    pid = pred["id"]
    curta.atualizar(chamada, predicao=pid, estado=pred.get("status"))
    log("%s: predição %s -> %s" % (cod, pid, pred.get("status")))
    intervalo = 8 if job["tipo"] == "video" else 4
    limite = 30 * 60 if job["tipo"] == "video" else 10 * 60
    ultimo = pred.get("status")
    while pred.get("status") not in ("succeeded", "failed", "canceled"):
        if time.time() - t0 > limite:
            curta.atualizar(chamada, estado="tempo_esgotado")
            raise Erro("%s: passou de %d min sem terminar (predição %s ainda pode concluir e cobrar)."
                       % (cod, limite // 60, pid))
        time.sleep(intervalo)
        try:
            pred = http("GET", API + "/predictions/" + pid, timeout=60)
        except Erro as e:
            log("%s: falha ao consultar (%s), tentando de novo" % (cod, str(e)[:80]))
            continue
        if pred.get("status") != ultimo:
            ultimo = pred.get("status")
            log("%s: %s (%.0f s)" % (cod, ultimo, time.time() - t0))
    dur = time.time() - t0
    estado = pred["status"]
    saida = pred.get("output")
    if isinstance(saida, list):
        saida = saida[0] if saida else None
    if estado == "succeeded" and saida:
        baixar(saida, destino)
        curta.atualizar(chamada, estado="succeeded", metrics=pred.get("metrics"), segundos=round(dur, 1),
                        saida=os.path.relpath(destino, curta.pasta))
        log("%s: salvo em %s (%.0f s)" % (cod, os.path.relpath(destino, curta.pasta), dur))
        return {"codigo": cod, "estado": "ok", "segundos": dur, "predicao": pid, "metrics": pred.get("metrics")}
    curta.atualizar(chamada, estado=estado if estado != "succeeded" else "failed",
                    metrics=pred.get("metrics"), erro=(pred.get("error") or "sem saída")[:500],
                    segundos=round(dur, 1))
    raise Erro("%s: predição %s terminou em %s: %s" % (cod, pid, estado, pred.get("error")))


def cmd_listar(curta):
    print("Curta %s  (%s)" % (curta.m.get("id"), curta.pasta))
    for it in curta.m["itens"]:
        if it["tipo"] == "pronta":
            c = curta.p(it["arquivo"])
            print("  %-8s pronta  %-9s %s" % (it["codigo"], "existe" if os.path.exists(c) else "FALTA", it["arquivo"]))
            continue
        for job in curta.jobs([it["codigo"]]):
            d = curta.saida(job)
            try:
                n = "%d car." % len(curta.prompt(job))
            except Erro as e:
                n = "ERRO: " + str(e)
            print("  %-8s %-7s %-9s prompt %-12s US$ %5.2f  refs %s" % (
                job["codigo"], job["tipo"], "existe" if os.path.exists(d) else "não existe", n,
                curta.custo(job), ",".join(job["refs"])))
    linhas = curta.livro()
    print("Livro: %d chamadas, US$ %.2f estimado; teto US$ %.2f; sobra US$ %.2f"
          % (len(linhas), curta.total(), curta.teto, curta.teto - curta.total()))


def cmd_simular(curta, jobs):
    for job in jobs:
        prompt = curta.prompt(job)
        payload = curta.payload(job, "<prompt abaixo>", ["<%s: %s>" % (r, os.path.relpath(curta.arquivo_ref(r), curta.pasta))
                                                          for r in job["refs"]])
        print("=" * 70)
        print("%s  modelo %s  custo est. US$ %.2f  prompt %d caracteres" % (
            job["codigo"], curta.modelo(job), curta.custo(job), len(prompt)))
        print("-" * 70)
        print(prompt)
        print("-" * 70)
        print(json.dumps(payload, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser(description="Gera imagens e vídeos de um curta pelo Replicate.")
    ap.add_argument("pasta")
    ap.add_argument("comando", choices=["listar", "simular", "gerar"])
    ap.add_argument("codigos", nargs="*")
    ap.add_argument("--refazer", action="store_true", help="refaz o que existe (move o antigo para .antigo-N)")
    ap.add_argument("--teste-fumaca", action="store_true", help="1 vídeo 5 s 480p com K1 -> raw/_fumaca.mp4")
    a = ap.parse_args()
    try:
        curta = Curta(a.pasta)
        if a.comando == "listar":
            cmd_listar(curta)
            return 0
        jobs = curta.jobs(a.codigos)
        if a.teste_fumaca:
            jobs.append(curta.job_fumaca())
        if not jobs:
            raise Erro("Nenhum código informado.")
        if a.comando == "simular":
            cmd_simular(curta, jobs)
            return 0
        for j in jobs:  # valida tudo antes de gastar
            curta.prompt(j)
        falhas = 0
        with ThreadPoolExecutor(max_workers=min(6, len(jobs))) as ex:
            futuros = {ex.submit(executar, curta, j, a.refazer): j for j in jobs}
            for f, j in futuros.items():
                try:
                    f.result()
                except Exception as e:
                    falhas += 1
                    log("ERRO %s: %s" % (j["codigo"], e))
        log("Livro: US$ %.2f estimado de US$ %.2f." % (curta.total(), curta.teto))
        return 1 if falhas else 0
    except Erro as e:
        print("ERRO: %s" % e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
