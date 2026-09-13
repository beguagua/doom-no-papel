# P4 — Eventos e fita

## Fita de dano

Escreva a fita antes de começar. Não reordene nem reutilize uma posição consumida.

```text
índice:  0  1  2  3  4  5  6  7  ...
valor:   2  1  3  2  1  3  2  1  ...
dano:   10  5 15 10  5 15 10  5  ...
```

Nesta sala, apenas os três primeiros valores são necessários.

## Registro causal

| Tick | Evento | Causa | Estado anterior | Resultado |
|---:|---|---|---|---|
| 0 | movimento | `F`, destino livre | `(1,3)` | `(2,3)` |
| 1 | movimento | `F`, destino livre | `(2,3)` | `(3,3)` |
| 2 | dano ao G | `A`, alvo em linha | `G=20` | `G=10` |
| 2 | dano ao jogador | G adjacente, cooldown 0 | `HP=100` | `HP=95` |
| 3 | dano ao G | `A`, alvo em linha | `G=10` | `G=5` |
| 4 | morte do G | `A`, dano 15 | `G=5` | `G=DEAD` |
| 4 | vitória | objetivo cumprido | `PLAY` | `WON` |

## Terminalidade

Se o jogador chegar a HP zero no mesmo tick em que matar o inimigo, marque `LOST`, conforme P0. Não continue a partida depois de `WON` ou `LOST`.
