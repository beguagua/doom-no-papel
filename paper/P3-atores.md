# P3 — Atores

Atualize atores em ordem crescente de ID. Não apague atores mortos.

| ID | Tipo | x | y | HP inicial | HP atual | Estado | Cooldown |
|---:|---|---:|---:|---:|---:|---|---:|
| 01 | SENTINEL `G` | 4 | 3 | 20 | 20 | ALIVE | 0 |

## Regra da sentinela

No início do tick, se `G` estiver vivo, adjacente ao jogador e o cooldown for zero, causa 5 de dano. O cooldown é reduzido em um antes da verificação; quando ataca, volta a `2`. A sentinela não se move.

Se o jogador matar `G` durante a ação do jogador, `G` vira `DEAD` e não age nesse mesmo tick.

## Ledger

| Tick | ID | Evento | HP antes | Cooldown antes | HP depois | Estado depois | Cooldown depois |
|---:|---:|---|---:|---:|---:|---|---:|
| inicial | 01 | inicialização | 20 | 0 | 20 | ALIVE | 0 |
| 0 | 01 | sem ação | | | | | |
| 1 | 01 | sem ação | | | | | |
| 2 | 01 | contra-ataque | 10 | 0 | 10 | ALIVE | 2 |
| 3 | 01 | cooldown | 5 | 2 | 5 | ALIVE | 1 |
| 4 | 01 | morto antes da IA | 0 | 1 | 0 | DEAD | 1 |
