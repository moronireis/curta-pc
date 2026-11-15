# D22 — A festa (curta falado, 3D estilizado)

> Estado: v0, 15/11/2026. Plano com GO ("go recomendado — faz uma amostra") do Moroni em 15/11/2026: `PLANO-CURTA-FESTA-1511.md`. Perfil @moronireis.
> Gate mkt-editor: PENDENTE. As falas da T1 foram para a amostra sem o gate; o roteiro inteiro passa por ele antes da rodada completa.
> Formato: 5 tomadas de 15 s, personagens falando em cena (fala gerada pelo Seedance junto com o vídeo). Sem narrador. Só a última fala olha para a câmera. Cada tomada gerada duas vezes (a, b).
> Molde: D20 "O ônibus" (`roteiros/D20-onibus.md`). Dele vêm a humilhação com plateia que ri, o herói que não responde na hora, a frase devolvida na virada e a chamada falada dentro do carro.
> Geração: API do Replicate, pasta `~/Videos/reels-ia/hf/d22-festa-1511/` (`curta.json`, `prompts/`), script `~/Agent System/video/scripts/curta/gerar.py`. Sem Higgsfield.

## História em uma frase
Os amigos chamam para a festa, ele fica trabalhando e ouve que os projetos dele nunca dão certo; tempos depois, quando perguntam se ele vem ou vai ficar com as "IAzinhas", ele encosta na porta da balada num carro esportivo e, ao "como você fez isso?", responde: "Com as minhas IAzinhas."

## História inteira
Noite. Ele, o mesmo rapaz do ônibus, de moletom, trabalha no computador no quarto. Os amigos aparecem na porta, arrumados para a festa, e chamam. Ele diz que não dá, está trabalhando. Eles debocham: ele nunca vai, e os projetos dele nunca dão certo. Riem. Ele fica. Nada funciona: erro na tela, zero venda, testa na mesa, madrugada virando manhã. Ele levanta o rosto: "É só questão de tempo." Começa a montar a IA, o celular vibra, venda aprovada, outra, outra. O tempo passa. Outra noite, os amigos ligam da porta da balada: "E aí, vem pra festa hoje ou vai ficar com as suas IAzinhas?". Ele: "Hmm... dessa vez eu dou um pulo." Um carro grafite encosta na porta da balada. Os queixos caem. O vidro desce: é ele, de moletom. "Como você fez isso?" "Com as minhas IAzinhas." Olha para a câmera: "Me segue pra aprender também."

## Decisões fechadas no GO (15/11/2026, todas as recomendadas)
1. Teto de gasto no Replicate: US$ 70.
2. Protagonista: o mesmo rapaz do ônibus (folha K1 do D20).
3. Frase da virada: "Com as minhas IAzinhas."
4. Convite da T1: amigos na porta do quarto.
5. Voz dele: voz jovem de biblioteca, fixa em todas as falas (ElevenLabs, depois da amostra aprovada).
6. Resolução: 720p.
7. Carro: o mesmo grafite sem emblema.
8. Rota: Fable decide e revisa, Opus 5.5 executa.

Mudança minha em relação ao plano: dois amigos com folha (o amigo e a amiga), não três. Dois já fazem a plateia que ri, cabem no quadro vertical da porta e o prompt cabe no limite de 4.000 caracteres da API.

## Regra de cor
- O quarto é azul frio: a única luz é a do monitor.
- Os amigos e a festa são quentes: âmbar do corredor na T1, néon quente na T4 e na T5. Ele termina dentro do mundo quente.

## Personagens e vozes (uma descrição fixa por personagem, repetida em todas as tomadas)
- **Ele:** 18 a 19 anos aparentes, magro, cabelo preto ondulado até a orelha, sobrancelha grossa, olho castanho, sem barba; moletom cinza-chumbo liso com capuz, sem estampa e sem cordão. Voz jovem, baixa e calma; nunca sobe o tom.
- **O amigo:** uns vinte anos, alto, ombro largo, cabelo castanho-escuro curto com topete, queixo quadrado, sorriso convencido; jaqueta bomber vinho aberta sobre camiseta branca, jeans escuro. Voz jovem, alta, clara e debochada.
- **A amiga:** uns vinte anos, magra, cabelo castanho-escuro comprido em rabo de cavalo alto, argola pequena; blusa de cetim coral, calça preta. Voz jovem, afiada e sarcástica.

Objetos sem número nem letra: o monitor aparece sempre de costas; teclado fora do quadro; celular de costas lisas, tela nunca virada para a câmera; carro sem placa e sem emblema; fachada da balada sem letreiro (só néon em formas).

## Falas por tomada

### T1 — O quarto, os amigos na porta (piloto)
1. Close dele digitando, rosto aceso pelo monitor (2 s). Sem fala.
2. A porta abre, luz âmbar; os dois amigos se debruçam, arrumados (2,5 s).
   - AMIGO: "Bora pra festa!"
3. Ele olha por cima do ombro, sem tirar a mão do teclado (2,5 s).
   - ELE: "Não vai dar. Tô trabalhando."
4. Close dela revirando os olhos (2 s).
   - AMIGA: "Você nunca vai!"
5. Close dele apontando a mesa; depois da fala, os dois caem na risada (3,5 s).
   - AMIGO: "E seus projetos nunca dão certo!"
6. Close enorme: o rosto dele cai; ele volta para a tela; a porta fecha e a luz quente some (2,5 s). Sem fala. Termina em movimento.

17 palavras.

### T2 — O quarto, nada dá certo
1. Brilho vermelho de erro no rosto; ele fecha os olhos (3 s). *Na edição entram as telas F1 e F2.*
2. Testa na mesa, copo vazio (2,5 s).
3. O celular vibra na mesa; ele vira o celular para baixo (2,5 s).
4. A janela passa de madrugada para manhã; ele segue digitando (3,5 s).
5. Close: ele ergue o rosto, firme (3,5 s).
   - ELE: "É só questão de tempo."

5 palavras.

### T3 — O quarto, a IA
1. Ele digita com foco, brilho azul no rosto (3 s). *Na edição entram S1 a S3.*
2. O celular vibra; olho arregala; sorriso abre (3 s). *Na edição entra S4.*
3. Soco no ar, gira na cadeira (2,5 s).
4. Outra noite, mesma mesa: o celular toca, ele atende e escuta, meio sorriso (3 s).
5. Close (3,5 s).
   - ELE: "Hmm... dessa vez eu dou um pulo."

7 palavras.

### T4 — A porta da balada (néon quente)
1. Os amigos na calçada, música abafada; o amigo ao celular, os outros rindo (4,5 s).
   - AMIGO: "E aí, vem pra festa hoje ou vai ficar com as suas IAzinhas?"
2. Ronco de motor; o farol varre os rostos (2 s).
3. Um carro grafite baixo, sem marca, desliza até o meio-fio (3 s).
4. Queixos caem, um depois do outro (2,5 s).
5. O vidro desce e revela ele, calmo, de moletom (3 s).

13 palavras.

### T5 — O carro na porta
1. O amigo inclinado na janela (3 s).
   - AMIGO: "Como você fez isso?"
2. Ele, meio sorriso (3 s).
   - ELE: "Com as minhas IAzinhas."
3. Reação dos amigos, sem graça (2 s).
4. Frontal dentro do carro, ele olha para a câmera (4 s).
   - ELE: "Me segue pra aprender também."
5. O carro arranca; no retrovisor os amigos ficam pequenos (3 s). Termina em movimento.

13 palavras.

## Total
55 palavras em 75 s brutos. Corte final perto de 55 a 60 s em 1,15×, com as telas dentro da T2 e da T3. Na montagem, a resposta dele da T3 ("dessa vez eu dou um pulo") entra logo depois da pergunta do amigo da T4.

Falas frágeis para o Seedance (rodar em dobro, conferir por transcrição): "Bora", "pra" (nunca "para"), "Tô" (nunca "Estou"), "IAzinhas" (i-a-ZI-nhas), "dou um pulo", o "E" inicial de "E seus projetos".

## Telas (feitas localmente, 1080×1920, português, sem emoji, sem logo)
- **F1:** "Falha ao publicar" com botão "Tentar de novo".
- **F2:** painel "Vendas hoje · R$ 0".
- **S1 a S4:** as do D20 (campo de pedido, "Criando seu robô…", conversa, três notificações "Venda aprovada").

## Legenda do post
A definir com o Moroni.
