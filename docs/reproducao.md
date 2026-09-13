# Reprodução do PaperDOOM-1

## Materiais

Use papel A4 ou carta, lápis, borracha, régua e um marcador pequeno. Para a versão mínima, não é necessário dado: a fita `2,1,3` está em P4. O simulador Python é opcional e serve apenas para conferência.

## Preparação

Imprima P0–P7. Preencha P2 com o estado inicial e P3 com o ator `G`. Copie o mapa de P1. Se houver duas pessoas, uma pode atuar como árbitro e manter P1/P4 enquanto a outra mantém P2/P3/P5.

## Uma rodada

O jogador anuncia uma ação válida. O árbitro registra o tick e o índice da fita. A ação é aplicada ao estado de P2. Em seguida, atualize atores em ordem de ID, resolva terminalidade, incremente o tick, calcule o checksum e redesenhe P6. Nunca use P6 para corrigir P2 ou P3.

## Traço dourado

Execute `F F A A A`. O resultado esperado é:

| Tick | Estado importante | CHK |
|---:|---|---:|
| 0 | `(2,3)`, HP 100, munição 3, G 20 | 23 |
| 1 | `(3,3)`, HP 100, munição 3, G 20 | 27 |
| 2 | `(3,3)`, HP 95, munição 2, G 10 | 80 |
| 3 | `(3,3)`, HP 95, munição 1, G 5 | 91 |
| 4 | `(3,3)`, HP 95, munição 0, G DEAD, WON | 83 |

## Validação opcional

Na raiz do repositório:

```bash
python3 -m unittest discover -s tests -v
python3 -m src.paperdoom.cli --trace F F A A A
```

Para gerar novamente os PDFs:

```bash
for f in paper/*.md; do manus-md-to-pdf "$f" "${f%.md}.pdf"; done
```

## Solução de problemas

Se um checksum divergir, compare primeiro a primeira linha divergente de P5. Os erros mais comuns são consumir a fita ao errar um tiro contra a parede, permitir que G aja depois de morrer ou alterar o estado diretamente a partir do desenho de P6. Se a divergência persistir, reinicie do último checkpoint correto; não edite linhas antigas do log.
