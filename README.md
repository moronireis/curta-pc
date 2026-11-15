# Curta 3D no PC

Pacote para rodar no PC (Windows, RX 7600 XT) a validação da rota gratuita do curta D22 "A festa". Preparado no Mac em 15/11/2026.

## Como rodar no PC

1. Abra o PowerShell e baixe o repositório (público; baixar não pede login):

   ```powershell
   cd $HOME
   git clone https://github.com/moronireis/curta-pc.git
   cd curta-pc
   ```

   Para a sessão devolver o relatório por `git push`, o PC precisa estar logado no GitHub (`gh auth login`). Sem login ela trabalha igual e deixa o relatório na pasta.

2. Abra o Claude Code nessa pasta:

   ```powershell
   claude
   ```

3. Dentro dele, troque o modelo e dê a partida:

   ```
   /model opus
   Leia o CLAUDE.md e execute o PLANO-CURTA-PC-1511.md a partir da fase A.
   ```

A sessão instala tudo em `C:\curta\`, fora desta pasta, pergunta antes de mexer em driver ou no sistema, e grava o andamento em `relatorio/RELATORIO.md`.

## O que tem aqui

| Caminho | O que é |
|---|---|
| `PLANO-CURTA-PC-1511.md` | O plano: escada de validação em seis fases, barreiras e estimativa |
| `CLAUDE.md` | Regras da sessão do PC |
| `pesquisa/PESQUISA-1511.md` | O que a pesquisa achou, com fontes, e o que é aposta |
| `curta/d22-festa/` | Roteiro, folha do protagonista (`K1.png`), prompts e manifesto do curta |
| `audio-teste/` | Cinco falas da T1 em voz genérica, para o teste de boca sincronizada |
| `referencia/` | Trecho e folha de quadros do "Ônibus" (o alvo de qualidade) e os prompts dele |
| `scripts/diagnostico.ps1` | Levanta CPU, RAM, disco, placa e ferramentas; só lê |
| `scripts/folha.py` | Gera folha de quadros de um vídeo para conferência (precisa de Pillow e ffmpeg) |
| `scripts/gerar_replicate.py` | Rota paga de reserva (Seedance 2.0 pelo Replicate) |
| `relatorio/` | Preenchido pela sessão do PC |
| `saida/` | Imagens de conferência e a amostra final |
