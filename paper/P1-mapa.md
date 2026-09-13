# P1 — Mapa-mestre

**Versão:** 1.0  |  **Mapa:** sala mínima 7×5

```text
      0123456
y=0   #######
y=1   #.....#
y=2   #.....#
y=3   #P..G.#
y=4   #######
```

## Legenda

| Símbolo | Significado |
|---|---|
| `#` | Parede sólida; não atravessar. |
| `.` | Piso livre. |
| `P` | Posição inicial do jogador; depois, use P2. |
| `G` | Sentinela; depois, use P3. |

## Regras espaciais

- As coordenadas aumentam para a direita (`x`) e para baixo (`y`).
- As direções são `N`, `E`, `S`, `W`.
- Toda célula interna é piso e toda borda externa é parede.
- Não há movimento diagonal.
- A ocupação é exclusiva: o jogador não pode entrar na célula de um ator vivo.
- O ator morto não bloqueia movimento, mas continua registrado como `DEAD` em P3.

## Células para conferir

| Elemento | Coordenada |
|---|---:|
| Jogador inicial | `(1,3)` |
| Sentinela `G` | `(4,3)` |
| Parede norte | `y=0` |
| Parede sul | `y=4` |
| Parede oeste | `x=0` |
| Parede leste | `x=6` |

Dobre ou cubra o mapa-mestre se quiser jogar apenas com a visão descoberta. A posição canônica continua em P2.
