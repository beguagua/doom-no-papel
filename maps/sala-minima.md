# Sala mínima do PaperDOOM-1

**Versão:** 1.0  
**Dimensões:** `x=0..6`, `y=0..4`  
**Objetivo:** derrotar `G`.

```text
      0123456
y=0   #######
y=1   #.....#
y=2   #.....#
y=3   #P..G.#
y=4   #######
```

- `#` é parede sólida.
- `.` é piso.
- `P` começa em `(1,3)`, olhando para leste (`E`).
- `G` começa em `(4,3)`, com `HP=20`, estado `ALIVE` e cooldown `0`.
- O jogador começa com `HP=100`, `MUNIÇÃO=3`, nenhuma chave e `phase=PLAY`.
- As únicas ações da versão mínima são `F` (avançar), `T` (virar no sentido horário) e `A` (atacar).
- A fita de dano começa em `2,1,3`, convertida por `1=5`, `2=10`, `3=15`.
- Uma entidade sólida não pode ocupar a célula de outra entidade sólida.
- O objetivo é `WON` quando `G` passa a `DEAD`.

## Arestas

Toda passagem interna entre células adjacentes é `OPEN`. A borda externa é `WALL`. A linha central do ataque percorre no máximo cinco células e termina na primeira parede ou ator vivo.

## Traço dourado

```text
F F A A A
```

O traço esperado termina em `WON` com o jogador em `(3,3)`, `HP=95`, `MUNIÇÃO=0`, `G=DEAD` e checksums `23, 27, 80, 91, 83`.
