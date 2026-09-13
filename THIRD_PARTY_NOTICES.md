# Avisos de terceiros e proveniência

## id Software / DOOM Open Source Release

O projeto foi estudado a partir do repositório [id-Software/DOOM](https://github.com/id-Software/DOOM). A árvore publicada contém código-fonte do motor clássico, `LICENSE.TXT` com GNU GPL versão 2 e `README.TXT` que informa que os dados reais do jogo são externos. Este repositório **não copia nem redistribui** essa árvore, e o simulador PaperDOOM-1 não depende dela.

As referências de arquitetura incluem `r_bsp.c`, `r_draw.c`, `r_plane.c`, `r_things.c`, `w_wad.c`, `doomdata.h`, `d_main.c`, `d_ticcmd.h`, `p_tick.c`, `p_pspr.c` e `p_inter.c`. A documentação deste projeto resume os conceitos com links e texto próprio.

## Fontes de pesquisa

As fontes consultadas e os títulos estão listados em [`docs/plano-tecnico.md`](docs/plano-tecnico.md). Elas incluem a documentação técnica do código-fonte, Chocolate Doom, Crispy Doom, Calico, Paper Computer, CARDIAC, padrões de lógica em origami, cartões perfurados, DoomPDF, nDoom, Doom-in-Excel, Google Sheets, WebAssembly e RP2040 Doom.

## Dados e assets

Nenhum `IWAD`, `PWAD`, sprite, textura, música, som, fonte, screenshot ou trecho extenso de texto narrativo do DOOM é distribuído neste repositório. “DOOM” é usado apenas para descrever a inspiração e o contexto técnico. O projeto não afirma compatibilidade com WAD.

Para uma experiência com conteúdo livre, investigue separadamente um pacote como [Freedoom](https://freedoom.github.io/about.html) e respeite os avisos e a licença dele. A licença de Freedoom não é a licença do código do motor DOOM.

## Conteúdo próprio

O mapa de `maps/sala-minima.md`, as regras PaperDOOM-1, o simulador e as folhas são conteúdo novo deste projeto, licenciados conforme os arquivos na raiz.
