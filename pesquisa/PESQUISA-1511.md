# Pesquisa de 15/11/2026 — o que se sabe antes de instalar

Tudo aqui veio de leitura na web em 15/11/2026, sem teste nosso. Cada item diz se é confirmado ou aposta. Confira na página oficial antes de usar: este campo muda todo mês.

## Por que esta rota existe

- O curta de referência (D20 "O ônibus") foi feito com o Seedance 2.0, que gera vários planos com fala sincronizada e até nove imagens de referência em uma chamada.
- A conta do Replicate está sem crédito (HTTP 402). Seedance 2.0 não tem cota gratuita confirmada em nenhum serviço; na BytePlus só as versões 1.5 Pro e 1.0 Pro têm.
- Nenhum modelo aberto tem teste publicado com fala em português do Brasil, personagem 3D estilizado e dois ou três falantes. A qualidade desta rota é desconhecida até rodar.

## Base: ComfyUI em placa AMD no Windows

- **Confirmado (README do ComfyUI):** existe caminho oficial com ROCm nativo no Windows (PyTorch da AMD), Windows 11, driver atual, sem HIP SDK. Há build portable para AMD (`ComfyUI_windows_portable_amd.7z`) e o ComfyUI Desktop traz ROCm desde a v0.7.0. https://github.com/comfy-org/comfyui · https://blog.comfy.org/p/official-amd-rocm-support-arrives
- **Não oficial:** a RX 7600 XT é `gfx1102` e não está na lista oficial de placas do PyTorch para Windows; o README diz que `HSA_OVERRIDE_GFX_VERSION=11.0.0` pode ser necessário. https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/windows/windows_compatibility.html
- **Pouca memória (limitações oficiais):** `--lowvram` e `--disable-pinned-memory`. https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/limitations/limitationsrad.html
- **Bug conhecido:** no Windows com ROCm, a segunda geração do Wan 2.2 fica de quatro a cinco vezes mais lenta. Contorno relatado em 01/11/2026: variável `GPU_RESOURCE_CACHE_SIZE=0` e opção `--cache-none`. https://github.com/Comfy-Org/ComfyUI/issues/12672
- **Não usar:** ZLUDA (sem financiamento) e DirectML; as fontes apontam o ROCm nativo como melhor.
- **Não confirmado:** driver Adrenalin mínimo para a 7600 XT.

## Imagem com referência de personagem

- **Medido em RX 7800 XT de 16 GB, Windows 11, ROCm:** nós Nunchaku int4 — FLUX.2 klein 4B em 2,9 s e Qwen-Image Lightning em 11,6 s por imagem de 1024², depois de aquecido; a primeira execução compila por um bom tempo. https://github.com/TwelveNights/ComfyUI-nunchaku-rocm
- **Funciona, sem tempo medido:** Qwen-Image-Edit-2509 nos nós de edição do ComfyUI.
- **Aposta:** duas ou três imagens de referência ao mesmo tempo em placa AMD.

## Vídeo

- **LTX-2.5 com áudio junto: descartado nesta placa.** Na RX 7600 XT de 16 GB travou o sistema ou gerou ruído colorido; a Lightricks fechou o chamado em 04/11/2026 dizendo que AMD/ROCm não está nos planos. https://github.com/Lightricks/LTX-2/issues/325
- **Wan 2.2 imagem-para-vídeo 14B quantizado com LoRA de 4 passos:** existe em GGUF Q4_K_M, 9,66 GB cada modelo (ruído alto e ruído baixo). https://huggingface.co/jayn7/WAN2.2-I2V_A14B-DISTILL-LIGHTX2V-4STEP-GGUF — **aposta:** nenhum tempo medido em placa AMD de 16 GB.
- **MOVA e Ovi:** pedem mais VRAM ou RAM do que a máquina provavelmente tem. Não tentar.

## Fala com boca sincronizada

- **InfiniteTalk / MultiTalk (sobre Wan 2.1):** vídeo guiado por áudio a 480p; há modelo para vários falantes, com cada voz ligada a uma região da imagem; um autor relata pequena degradação com duas pessoas. https://github.com/MeiGen-AI/MultiTalk · https://dev.to/ai-ksk/infinitetalk-goes-native-in-comfyui-single-and-dual-lip-sync-loops-plus-the-ltx-2-distilled-route-2hcn
- **Wan 2.2 S2V:** existe em GGUF. https://huggingface.co/quantstack/wan2.2-s2v-14b-gguf
- **Aposta:** nenhum relato desses modelos em placa AMD, nem com personagem 3D estilizado.
- **Sincronia labial depois do vídeo (plano C):** em benchmark acadêmico o MuseTalk teve 67,8% de sucesso em personagem estilizado e o LatentSync falhou em mudar a boca. https://arxiv.org/html/2505.21448v1

## Voz

- A amostra usa as vozes genéricas de `audio-teste/` (macOS, custo zero).
- TTS aberto em português: nenhum teste publicado de sotaque brasileiro, deboche ou risada. Não é desta rodada.

## Memória e disco

- Uma receita de LTX em placa AMD pede 32 GB de RAM no mínimo e 64 GB recomendados; não há medição para Wan em 16 GB.
- Arquivo de paginação grande evita erro de memória comprometida, mas a geração fica muito lenta se houver troca real. https://runaihome.com/blog/comfyui-paging-file-too-small-os-error-1455-fix-2026/

## Ordem de instalação sugerida

1. Driver Adrenalin recente (perguntar antes de atualizar) e ComfyUI portable para AMD; validar com uma imagem.
2. Nós de imagem com referência (Nunchaku-ROCm ou GGUF) para os quadros iniciais.
3. Wan 2.2 imagem-para-vídeo GGUF Q4 com LoRA de 4 passos, com `--lowvram --disable-pinned-memory` e o contorno do bug.
4. InfiniteTalk em GGUF; se falhar, Wan 2.2 S2V em GGUF.
