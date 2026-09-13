# P6 — Renderer frontal

Este renderer é uma aproximação manual quantizada. Ele **não** é o BSP, o ray caster por pixel ou o renderer de colunas do DOOM original.

## Vetores relativos quando olhando para leste

| Coluna | Vetor base |
|---:|---|
| `r=-2` | `(0,-1)` |
| `r=-1` | `(+1,-1)` |
| `r=0` | `(+1,0)` |
| `r=+1` | `(+1,+1)` |
| `r=+2` | `(0,+1)` |

Para N, S e W, gire esses vetores 90 graus conforme a tabela de orientação. Para cada coluna, avance `n=1..5`. A primeira parede ou ator encerra a coluna.

## Símbolos por profundidade

| Distância | Parede | Espaço livre |
|---:|---|---|
| 1 | `████` | `....` |
| 2 | `▓▓▓` | `...` |
| 3 | `▒▒` | `..` |
| 4–5 | `░` | `.` |
| nenhuma | `.` | `.` |

O ator vivo substitui a parede pela letra (`G`). A saída, se existisse, seria `E`; itens usam `*`.

## Quadro

```text
P6 — QUADRO t=2
        r=-2   r=-1    r=0    r=+1   r=+2
alvo       .      .       G      .      .
HUD    HP 100 | PISTOLA | MUNIÇÃO 3 | G=20
```

O quadro é uma vista derivada. Se o desenho divergir de P2/P3, mantenha P2/P3 e redesenhe P6.
