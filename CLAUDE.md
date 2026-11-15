# Curta 3D no PC — instruções da sessão

Você está no PC do Moroni (Windows, AMD Radeon RX 7600 XT de 16 GB). Este repositório foi preparado no Mac dele em 15/11/2026. Sua tarefa é executar `PLANO-CURTA-PC-1511.md`: uma escada de validação que termina, se tudo passar, na amostra da tomada T1 do curta D22 "A festa".

Fale com o Moroni em português do Brasil, com acentos corretos. Use `/model opus`: as decisões de arquitetura já estão no plano.

## Como começar

1. Leia `PLANO-CURTA-PC-1511.md` e `pesquisa/PESQUISA-1511.md` inteiros.
2. Rode `powershell -ExecutionPolicy Bypass -File scripts\diagnostico.ps1` e leia `relatorio/maquina.md`.
3. Diga ao Moroni, em poucas linhas, o que a máquina tem e se o portão da fase A passou. Siga para a fase B sem esperar, a menos que o portão tenha falhado.

## Regras de execução

- **Escada, não pipeline.** Um degrau por vez. Cada portão reprovado depois de três configurações diferentes encerra a escada: registre e reporte. Não repita a mesma configuração esperando outro resultado.
- **Confira antes de instalar.** Os fatos da pesquisa são de 15/11/2026 e vieram da web: nomes de arquivo, versões e endereços podem ter mudado. Abra a página oficial (repositório, release, model card) antes de cada download e use o que ela diz hoje.
- **Instalações fora do repositório**, em `C:\curta\` (ComfyUI, modelos, ambientes). Nada de modelo, ambiente virtual ou vídeo bruto dentro do git.
- **Disco.** Antes de cada download acima de 5 GB, diga o tamanho e o total acumulado. Teto: 120 GB, salvo outra ordem do Moroni.
- **Mudanças de sistema pedem ok antes:** driver da placa, variável de ambiente permanente, arquivo de paginação, WSL, qualquer coisa que exija reiniciar ou administrador. Variável só na sessão do terminal não precisa de ok.
- **Nada pago.** Nenhum serviço com cobrança, nenhuma conta nova, nenhum cartão. ElevenLabs e Replicate ficam fora desta rodada. Higgsfield está vetado pelo Moroni para este curta.
- **Segredos.** Nenhuma chave ou token em arquivo, log ou relatório.
- **Saída pesada vai para arquivo.** Downloads, instalações e gerações com saída redirecionada; leia só o final. Geração longa roda em segundo plano.
- **Olhe o resultado.** Imagem e vídeo se conferem abrindo a imagem ou a folha de quadros (`scripts/folha.py`), nunca só pelo código de saída.

## Regras de conteúdo (valem para todo prompt)

- Animação 3D estilizada com acabamento de longa-metragem; nunca low-poly, plástico, mascote ou fotorrealista. A referência é `referencia/onibus-folha-de-quadros.jpg`.
- Sem texto, letras, números, logos, marcas ou marca d'água na imagem. Telas sempre de costas para a câmera.
- Sem pessoas reais reconhecíveis. Os prompts nunca citam filmes, estúdios, jogos ou personagens existentes.
- Falas exatamente como no roteiro, em português do Brasil.
- As folhas de personagem são referência de identidade: nunca aparecem no quadro final.

## Adaptação dos prompts

Os prompts em `curta/d22-festa/prompts/` foram escritos para o Seedance 2.0, que recebe quatro referências e gera seis planos com fala em uma chamada. Modelo aberto não faz isso. Aqui:

- **Um plano por geração.** O roteiro lista os planos da T1 com duração e fala.
- **Identidade pelo quadro inicial.** Cada plano começa de uma imagem feita na fase C a partir das folhas; o vídeo só anima.
- **Fala pelo áudio.** Planos falados usam o arquivo de `audio-teste/` correspondente; planos mudos usam imagem-para-vídeo simples.
- **Prompt curto e literal.** Descreva o plano, o gesto e a câmera; reaproveite as descrições fixas dos personagens de `base_video.txt`.
- Os marcadores `{K1}`…`{K4}` são do cliente do Replicate; aqui as imagens entram como entrada do fluxo.

## Relato

Depois de cada fase, atualize `relatorio/RELATORIO.md` (modelo no próprio arquivo), faça commit e push. Imagens de conferência pequenas (JPG) e a amostra final (se tiver menos de 25 MB) entram em `saida/` e no commit; o resto fica fora.

Quando a escada terminar ou parar, entregue ao Moroni:
1. Feito × planejado, com evidência por fase.
2. O que ele precisa assistir e onde está.
3. Pedidos e decisões pendentes.
4. Uso real da sessão.
5. O que a próxima rodada precisa.

## Rota de reserva

`scripts/gerar_replicate.py` é o cliente do Seedance 2.0 pelo Replicate (pago, cerca de US$ 6 pela amostra). Só usar se o Moroni pedir; lê o token da variável `REPLICATE_API_TOKEN`.
