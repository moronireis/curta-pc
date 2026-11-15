# PLANO — Curta 3D falado no PC (RX 7600 XT), rota gratuita

> Rodada única, 15/11/2026. Pedido do Moroni: gerar o curta D22 "A festa" (molde do D20 "O ônibus") sem Higgsfield e sem crédito pago, usando o PC dele. Este plano é executado por uma sessão do Claude Code aberta **no PC**, dentro deste repositório.
> Fases expressam ordem de dependência, não calendário.

## 1. Objetivo + o que já existe

Descobrir, com o menor esforço possível, se a RX 7600 XT de 16 GB entrega de graça um clipe 3D falado em português aceitável ao lado do Ônibus; se entregar, gerar a amostra da tomada T1 no PC.

| Já existe (neste repositório) | Falta |
|---|---|
| Roteiro D22 com falas e planos (`curta/d22-festa/roteiro.md`) | Tudo que roda no PC: ComfyUI para AMD, modelos, fluxos |
| Folha do protagonista `K1.png` e prompts das folhas K2, K3 e do quarto K4 | Folhas K2, K3 e quadro K4 gerados |
| Prompts de vídeo da T1 escritos para o Seedance (`prompts/T1.txt`, `base_video.txt`) | Versão desses prompts plano a plano, para modelo aberto |
| Referência de qualidade: trecho e folha de quadros do Ônibus (`referencia/`) | Medição real de tempo e memória na placa |
| Cinco falas de teste em voz genérica do macOS (`audio-teste/`, custo zero) | Vozes definitivas (só depois da amostra aprovada) |
| Pesquisa de 15/11 com fontes (`pesquisa/PESQUISA-1511.md`) | Confirmação de quase tudo que ela marca como aposta |
| Cliente do Replicate (`scripts/gerar_replicate.py`), rota paga de reserva | Crédito na conta (não é desta rodada) |

## 2. Escopo executável agora

Uma escada de validação. Cada degrau tem um portão; se o portão falha depois de três configurações diferentes, a sessão para, registra e reporta. Não se monta o degrau seguinte sobre um degrau reprovado.

**Fase A — Máquina.** Rodar `scripts/diagnostico.ps1`; gravar `relatorio/maquina.md` (CPU, RAM, disco livre, placa, driver, Windows, Python, git, ffmpeg).
Portão: RAM de 16 GB ou mais e 80 GB livres em disco. Abaixo disso, parar e reportar.

**Fase B — Base (depende de A).** ComfyUI portable para AMD (ROCm nativo no Windows) em `C:\curta\ComfyUI`, fora do repositório. Conferir que o PyTorch enxerga a placa; se não enxergar, tentar `HSA_OVERRIDE_GFX_VERSION=11.0.0` só na sessão.
Portão: uma imagem qualquer gerada na GPU, com tempo e pico de VRAM anotados.

**Fase C — Imagem com referência (depende de B).** Modelo de edição com imagem de entrada (Qwen-Image-Edit ou FLUX.2 klein, quantizado). Gerar: folha K2 (amigo), folha K3 (amiga), quadro K4 (quarto) a partir de `K1.png` e dos prompts; depois o quadro inicial do plano 3 da T1 (ele olhando por cima do ombro) usando K1 e K4.
Portão: o protagonista do quadro inicial é reconhecível como o do K1 e o acabamento 3D é o mesmo. A sessão olha a imagem e confere contra a lista `conferir` do `curta.json`.

**Fase D — Vídeo mudo (depende de C).** Wan 2.2 imagem-para-vídeo quantizado com LoRA de 4 passos, 480×832, 5 s, a partir do quadro inicial da fase C. Reserva: Wan 2.2 de 5B.
Portão: clipe gerado sem travar, com movimento coerente e identidade preservada; tempo por clipe e pico de memória anotados.

**Fase E — Fala (depende de D).** Vídeo guiado por áudio com `audio-teste/ele-1-nao-vai-dar.wav` sobre o mesmo quadro inicial: InfiniteTalk quantizado; reserva: Wan 2.2 S2V quantizado. Depois, um plano com dois personagens na porta e uma fala do amigo.
Portão: boca em sincronia visível com a fala, rosto estável, sem boca mexendo em quem não fala.

**Fase F — Amostra T1 (depende de E).** Os seis planos da T1 gerados um a um (quadro inicial → vídeo; planos falados pelo caminho da fase E), unidos com corte seco no ffmpeg em 9:16. Entrega: `saida/T1-pc.mp4`, folha de quadros e comparação lado a lado com `referencia/onibus-folha-de-quadros.jpg`.

**Fase G — Relato (depende do ponto em que a escada parou).** `relatorio/RELATORIO.md` preenchido, commit e push. A sessão do Mac lê e decide o próximo passo com o Moroni.

Fora desta rodada, por barreira real e não por falta de fôlego: tomadas T2 a T5, vozes definitivas, telas, montagem final, publicação. Dependem do veredito do Moroni sobre a amostra.

## 3. Barreira

**O que bloqueia testar (o Moroni faz):**
- Assistir a `saida/T1-pc.mp4` (ou ao clipe do último degrau aprovado) ao lado de `referencia/onibus-trecho-12s.mp4` e dizer se a qualidade serve.

**O que bloqueia continuar (pedidos explícitos):**
- Repositório privado: o PC precisa estar autenticado no GitHub (`gh auth login`) para clonar e para devolver o relatório.
- Atualização do driver da placa, se a fase B pedir: a sessão pergunta antes; é mudança de sistema.
- Se o Windows falhar na fase B ou D: decidir entre Linux em dual boot, WSL2, ou encerrar a rota. Recomendação: encerrar a rota e pôr US$ 10 no Replicate; dual boot só se o Moroni quiser investir nisso.
- Vozes: a amostra usa voz genérica gratuita. ElevenLabs entra só com a amostra aprovada e com o gasto avisado antes (regra do Moroni).

**Decisões do Moroni, com recomendação:**
1. Modelo da sessão do PC — recomendo Opus 5.5 (`/model opus`); as decisões já estão neste plano.
2. Teto de disco para modelos — recomendo 120 GB; a sessão avisa antes de cada download acima de 5 GB.
3. Se a escada parar antes da fase E — recomendo a rota paga de reserva (Replicate, cerca de US$ 6 pela amostra).

## 4. Critérios de pronto + autotestes

- Cada fase deixa em `relatorio/RELATORIO.md`: o que foi instalado (com versão e endereço de origem), a configuração usada, o tempo por geração, o pico de VRAM e de RAM, e o veredito do portão.
- Imagens: conferidas pela sessão contra a lista `conferir` do item; no máximo uma repetição por item antes de registrar a falha.
- Vídeos: folha de quadros com `scripts/folha.py`; a sessão olha a folha, não só o código de saída.
- Fala: transcrição do áudio do clipe comparada com a fala escrita; sincronia julgada em quadros consecutivos da boca.
- Nenhuma chave, token ou caminho com credencial em arquivo do repositório; `git status` limpo de modelos e de saídas grandes antes do push.
- Divergência entre o plano e o que foi feito vira item do relatório.

## 5. Estimativa de uso

Referência: `claude-usage --estimate 70` (medida no Mac em 15/11/2026).

| Como executar | Custo API-equiv | % Fable semanal | % geral semanal |
|---|---|---|---|
| Tudo em Fable | ~US$ 70 | ~4,0% | ~2,1% |
| **Fable decide (este plano, feito no Mac) + Opus 5.5 executa no PC — recomendado** | ~US$ 30–40 | ~1,0–1,4% | ~1,0–1,2% |
| Tudo em Opus 5.5 / Sonnet 5 | ~US$ 25–35 | 0% | ~0,7–1,1% |

Janela no momento da medida: geral 33%, Fable 49%, ritmo 72%.

Otimizações: sessão do PC em Opus 5.5; downloads e gerações com saída redirecionada para arquivo e leitura só do final; pesquisa já feita vem no repositório e não se refaz; a escada para no primeiro portão reprovado em vez de montar o pipeline inteiro; custo de geração zero (GPU local) e custo de voz zero (voz genérica).
