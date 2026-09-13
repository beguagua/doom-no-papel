# P5 — Log de ticks

Uma linha por tick. Nunca apague a linha antiga; registre correções como uma nova linha com `CORREÇÃO`.

| Tick inicial | Ação | Resultado do jogador | Resultado do ator | HP | Munição | G HP | G estado | rng | Phase | CHK |
|---:|---|---|---|---:|---:|---:|---|---:|---|---:|
| 0 | `F` | `(1,3)` → `(2,3)` | nenhum | 100 | 3 | 20 | ALIVE | 0 | PLAY | 23 |
| 1 | `F` | `(2,3)` → `(3,3)` | nenhum | 100 | 3 | 20 | ALIVE | 0 | PLAY | 27 |
| 2 | `A` | acerta; dano 10 | G ataca; dano 5 | 95 | 2 | 10 | ALIVE | 1 | PLAY | 80 |
| 3 | `A` | acerta; dano 5 | cooldown 1 | 95 | 1 | 5 | ALIVE | 2 | PLAY | 91 |
| 4 | `A` | acerta; dano 15 | G não age | 95 | 0 | 0 | DEAD | 3 | WON | 83 |

## Checkpoint

Ao terminar cada linha, compare posição, direção, HP, munição, HP de G, estado de G, índice da fita, fase e checksum. A primeira divergência é o ponto de investigação.
