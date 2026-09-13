# PaperDOOM-1

**Um demake manual e determinístico inspirado em DOOM.**

PaperDOOM-1 é um experimento de computação em papel: o jogador mantém um estado explícito, aplica uma regra por tick, registra o resultado e redesenha uma visão frontal reduzida. O kit foi desenhado para ser reproduzível com lápis, folhas e uma fita fixa de dano.

> **Limite essencial:** este projeto **não é o DOOM original**, não lê WADs, não executa o motor da id Software, não reproduz o renderer vanilla e não distribui IWADs, sprites, texturas, músicas ou sons proprietários. Ele é um demake independente que preserva algumas ideias perceptíveis: exploração em primeira pessoa, linha de tiro, inimigo, munição e estado terminal.

## Comece em cinco minutos

1. Imprima `paper/P0-regras.pdf` até `paper/P7-testes.pdf`, ou use os arquivos Markdown equivalentes.
2. Coloque o jogador em `(1,3)`, olhando para leste, com `HP=100`, `MUNIÇÃO=3`; coloque o sentinela `G` em `(4,3)` com `HP=20`.
3. Use a fita de dano `2, 1, 3`, onde `1=5`, `2=10` e `3=15` de dano.
4. Execute `F, F, A, A, A`. Os checksums esperados são `23, 27, 80, 91, 83`, terminando em `WON`.
5. Para conferir a execução com uma máquina comum, rode:

```bash
python3 -m unittest discover -s tests -v
python3 -m src.paperdoom.cli --trace F F A A A
```

O simulador é **validador independente**. Ele não é necessário para jogar no papel e não transforma o projeto em um port do DOOM.

## O kit

| Arquivo | Função |
|---|---|
| `paper/P0-regras.md` | Contrato imutável: ações, ordem do tick, dano e vitória. |
| `paper/P1-mapa.md` | Mapa-mestre com coordenadas, células e arestas. |
| `paper/P2-estado.md` | Folha de estado canônico. |
| `paper/P3-atores.md` | Fichas de atores e cooldowns. |
| `paper/P4-eventos.md` | Registro de eventos e terminalidade. |
| `paper/P5-log.md` | Log de uma linha por tick e checksum. |
| `paper/P6-renderer.md` | Renderer frontal de cinco vetores. |
| `paper/P7-testes.md` | Testes, traço dourado e auditoria. |
| `maps/sala-minima.md` | Especificação do mapa de uma sala. |
| `src/paperdoom/` | Simulador/validador novo e independente. |
| `tests/` | Testes automatizados e traço dourado. |
| `docs/plano-tecnico.md` | Relatório de pesquisa e plano de evolução. |

PDFs para impressão são gerados a partir dos Markdown em `paper/` com `manus-md-to-pdf`.

## O que foi estudado

O plano técnico compara a arquitetura do código-fonte publicado pela id Software — WAD, mapas, BSP, colunas, spans, tics e `ticcmd_t` — com computação em papel, CARDIAC, máquinas de registradores, lógica de dobradura e precedentes como DoomPDF, DOOM em planilhas, WebAssembly e RP2040 Doom. O resultado é uma decisão de escopo: um DOOM completo executado manualmente em papel não é um objetivo operacional razoável; um demake determinístico e auditável é.

Leia [`docs/plano-tecnico.md`](docs/plano-tecnico.md) para as fontes, limites, licenças e fases futuras.

## Licenças e proveniência

- O código novo em `src/` é disponibilizado sob [`LICENSE-CODE.txt`](LICENSE-CODE.txt).
- A documentação e as folhas são disponibilizadas sob [`LICENSE-DOCS.md`](LICENSE-DOCS.md).
- A licença GPLv2 do código-fonte publicado pela id Software é reproduzida somente como referência em [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md); nenhum código do repositório oficial é necessário para executar este demake.
- Nenhum IWAD ou asset proprietário está incluído. Consulte `data/README-IWAD.md` se quiser comparar este projeto com um port real.

**PaperDOOM-1 é um projeto independente e não é afiliado, patrocinado ou endossado pela id Software, ZeniMax, Bethesda ou pelos autores dos source ports citados.**
