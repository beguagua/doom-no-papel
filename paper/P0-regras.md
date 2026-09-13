# P0 — Regras do PaperDOOM-1

**Versão 1.0 — não altere durante uma partida.**

## Declaração

PaperDOOM-1 é um demake manual e determinístico inspirado em DOOM. Não é o motor original, não lê WADs e não reproduz a renderização vanilla.

## Estado inicial

- Jogador: `(1,3)`, olhando para `E`.
- Jogador: `HP=100`, `MUNIÇÃO=3`, `tick=0`, `phase=PLAY`.
- Sentinela `G`: `(4,3)`, `HP=20`, `ALIVE`, `cooldown=0`.
- Fita: `2,1,3`; `1=5`, `2=10`, `3=15` de dano.

## Ações válidas

| Código | Efeito |
|---|---|
| `F` | Avança uma célula na direção atual, se livre. |
| `T` | Gira 90 graus no sentido horário, sem mover. |
| `A` | Dispara na linha central, consumindo uma munição e um valor da fita se houver ator atingível. |

Uma ação inválida não altera a posição, mas ainda produz uma linha de log e um novo tick.

## Ordem de um tick

1. Copie o estado anterior e confira o checksum.
2. Registre o tick, a ação e o índice da fita.
3. Rejeite entrada após `WON` ou `LOST` e ataque sem munição.
4. Aplique a ação do jogador.
5. Se o jogador matou `G`, marque `DEAD`; um ator morto neste passo não age.
6. Para cada ator vivo, em ordem de ID: reduza cooldown; se o jogador estava adjacente no início do tick e cooldown chegou a zero, cause 5 de dano e defina cooldown `2`; caso contrário, não faça nada nesta versão mínima.
7. Resolva derrota (`HP<=0`).
8. Resolva vitória (`G=DEAD`). Se ambas ocorrerem, derrota prevalece.
9. Incremente `tick`. Avance a fita somente quando um ataque consumiu dano.
10. Calcule o checksum e redesenhe P6.

## Ataque

O ataque percorre o eixo central na direção do jogador. A primeira parede encerra a busca. O primeiro ator vivo encontrado recebe o próximo dano da fita. A munição é consumida mesmo quando o tiro não encontra um ator, desde que o ataque tenha sido válido.

## Checksum

Codifique `N=0`, `E=1`, `S=2`, `W=3`.

```text
CHK = (tick + 3*x + 5*y + 7*dir + 11*hp + 13*ammo
       + 17*nr_chaves + 19*nr_atores_vivos + 23*rng_index) mod 97
```

O checksum detecta divergências, mas não as corrige. Ele é uma regra PaperDOOM-1, não o checksum de rede do DOOM.

## Vitória e derrota

- `WON`: `G` está `DEAD`.
- `LOST`: HP do jogador chegou a zero.
- Após um estado terminal, ações são rejeitadas.
