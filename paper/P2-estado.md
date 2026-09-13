# P2 — Estado canônico

**Não desenhe a partir da memória; copie os valores após cada tick.**

| Campo | Inicial | Atual |
|---|---:|---:|
| `tick` | `0` | |
| `phase` | `PLAY` | |
| `player.x` | `1` | |
| `player.y` | `3` | |
| `facing` | `E` | |
| `HP` | `100` | |
| `MUNIÇÃO` | `3` | |
| `nr_chaves` | `0` | |
| `rng_index` | `0` | |
| `CHK` | `19` | |

## Linha de atualização

Preencha uma cópia ou uma nova linha por tick. Não apague linhas anteriores.

| Tick após | Ação | x | y | Direção | HP | Munição | rng | Atores vivos | Phase | CHK |
|---:|---|---:|---:|---|---:|---:|---:|---:|---|---:|
| 0 | inicial | 1 | 3 | E | 100 | 3 | 0 | 1 | PLAY | 19 |
| 1 | | | | | | | | | | |
| 2 | | | | | | | | | | |
| 3 | | | | | | | | | | |
| 4 | | | | | | | | | | |
| 5 | | | | | | | | | | |
| 6 | | | | | | | | | | |
| 7 | | | | | | | | | | |
| 8 | | | | | | | | | | |
| 9 | | | | | | | | | | |
| 10 | | | | | | | | | | |

## Fórmula

```text
CHK = (tick + 3*x + 5*y + 7*dir + 11*HP + 13*MUNIÇÃO
       + 17*nr_chaves + 19*atores_vivos + 23*rng_index) mod 97
```

`dir`: N=0, E=1, S=2, W=3.
