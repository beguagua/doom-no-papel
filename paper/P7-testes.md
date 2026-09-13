# P7 — Testes e auditoria

Execute os testes antes de inventar novos mapas ou inimigos.

| ID | Preparação | Entrada | Resultado esperado |
|---|---|---|---|
| T1 | `(1,3)`, olhando W | `F` | Posição não sai pela parede. |
| T2 | `(1,3)`, olhando E | `F` | Jogador vai para `(2,3)`. |
| T3 | qualquer posição | `T` | Direção gira 90 graus; posição não muda. |
| T4 | Jogador diante de parede | `A` | Munição diminui; nenhum ator atrás recebe dano. |
| T5 | G em linha aberta | `A` | Primeiro ator vivo recebe o dano da fita. |
| T6 | Fita `1,2,3` | `A,A,A` | Danos `5,10,15`; RNG avança 3. |
| T7 | G com HP 5 | `A` com fita 1 | G fica `DEAD` e não age. |
| T8 | Munição 0 | `A` | Ação rejeitada; fita não avança. |
| T9 | G adjacente e cooldown 0 | qualquer ação não letal | Jogador recebe 5; G vai a cooldown 2. |
| T10 | `phase=WON` | `F` | Estado permanece terminal. |
| T11 | Estado inicial | `F,F,A,A,A` | Checksums `23,27,80,91,83`; `WON`. |
| T12 | Dois operadores | mesmo traço | Mesmo estado final. |

## Critério de publicação

A sala mínima só está pronta quando:

1. o teste automatizado passa;
2. duas execuções manuais conferem com o traço dourado;
3. nenhum arquivo contém IWAD ou asset proprietário;
4. o README repete que o resultado é um demake independente;
5. as folhas têm versão e licença indicadas.
