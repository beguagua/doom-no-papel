# Plano técnico: DOOM no papel

**Versão:** 1.0  
**Escopo:** consolidação de cinco relatórios de pesquisa sobre arquitetura de DOOM, computação em papel, precedentes de DOOM em meios improváveis, licenciamento e projeto de um demake manual.  
**Conclusão executiva:** é viável executar em papel um **jogo determinístico inspirado em DOOM** e demonstrar computação manual auditável. Não é viável, em escala humana e com materiais simples, executar manualmente o DOOM completo com fidelidade ao motor, aos WADs, à renderização e aos 35 tics por segundo. Também é viável usar papel como memória, programa, mapa, entrada ou display enquanto um computador externo executa um port real; essa terceira modalidade não é computação *paper-only*.

> **Tese central.** “DOOM no papel” é uma expressão com três significados tecnicamente diferentes: executar manualmente uma representação fiel de contratos do motor; jogar um demake novo e determinístico; ou usar folhas e cartões como interface para um computador que executa DOOM. O projeto deve escolher uma dessas afirmações antes de escolher materiais, regras ou código.

## 1. Decisão de viabilidade e significado

O projeto é **viável** se o objetivo for construir um artefato físico com estado explícito, ações discretas, regras determinísticas, renderer simplificado e trilha de auditoria. O papel pode armazenar instruções, registradores, cartões, marcas, posições, tabelas, estados de atores e uma sequência de pseudoaleatoriedade. Máquinas manuais de registradores, o CARDIAC, cartões perfurados e padrões de lógica por dobradura demonstram que computação em papel pode ser executável, e não apenas uma ilustração de computador. [18] [19] [20]

A mesma conclusão não autoriza a alegação de que uma folha reproduz o DOOM original. O jogo da id Software combina um formato de dados indexado, mapas com setores e uma árvore BSP pré-calculada, projeção de segmentos, clipping por colunas, planos desenhados em *spans*, sprites mascarados, objetos com estados, colisão geométrica, entrada por comandos discretos, sincronização por tic e uma camada de sistema. [1] [3] [4] [5] [7] [8] A tradução fiel de todos esses mecanismos para execução manual exigiria muitas tabelas, cópias e decisões por passo, com custo incompatível com uma partida útil.

O resultado recomendado é o **PaperDOOM-1**: um demake manual de um jogador, com mapa 2D discreto, estado canônico em folhas, uma arma, um inimigo, ações limitadas, fonte de dano auditável, renderer frontal reduzido e checkpoints. A proposta preserva propriedades perceptíveis — exploração em primeira pessoa, linha de tiro, pressão de inimigo, portas ou objetivos espaciais e feedback frontal — mas não preserva a geometria contínua, a compatibilidade com WAD, o renderer vanilla ou a simulação completa.

### 1.1 Taxonomia operacional

| Rótulo | Onde a computação ocorre | O que pode ser chamado de DOOM | Fidelidade esperada | Verificabilidade | Decisão recomendada |
|---|---|---|---|---|---|
| **Execução manual fiel** | Pessoa, folhas, tabelas e marcadores | Uma emulação manual de contratos selecionados do motor; não necessariamente o jogo completo | Alta em um subsistema pequeno; muito baixa em escala completa | Alta quando cada transição é registrada, mas vulnerável a erro humano | Usar como experimento de renderer, tic ou formato, não como produto principal |
| **Demake determinístico** | Pessoa aplicando regras novas em papel | Jogo inspirado em DOOM, explicitamente não compatível com WAD | Baixa a média; alta apenas no ritmo e nas ideias escolhidas | Muito alta, porque o estado e o traço podem ser pequenos | **Escolha principal para um protótipo jogável** |
| **Papel como interface externa** | Computador, navegador, emulador ou microcontrolador; papel fornece entrada/saída | DOOM real ou um port, se o motor realmente executar no dispositivo externo | Pode ser alta no motor; baixa no papel como máquina autônoma | Média; exige auditar hardware, runtime, código e dados | Usar para uma instalação interativa, mantendo a alegação “híbrida” |

A distinção é necessária porque precedentes conhecidos não têm o mesmo mecanismo. DoomPDF executa um port compilado para asm.js dentro do runtime JavaScript do leitor PDF e usa campos de texto como display. nDoom é um port nativo para TI-Nspire. RP2040 Doom executa um port derivado de Chocolate Doom em microcontrolador com periféricos. Excel com PyXLL usa Python/C como motor e a planilha como display; Google Sheets usa js-dos para emular DOS; Doom.xls é um clone *Doom-like* em fórmulas, não o DOOM original. [24] [25] [26] [27] [28] [29]

## 2. O que é o DOOM original

### 2.1 Arquitetura de execução

O código publicado pela id Software é um motor de software 2.5D. O renderer não é um *ray caster* que lança um raio independente para cada pixel. Ele percorre `NODES` de uma árvore BSP pré-calculada, visita primeiro o lado frontal da câmera e usa `R_CheckBBox` para decidir se o lado posterior ainda pode conter colunas visíveis. Os `SSECTORS` fornecem segmentos, planos e objetos para essa travessia. [3]

Depois da projeção dos segmentos, paredes e sprites são desenhados como **colunas verticais**. Pisos e tetos são agrupados em **spans horizontais**. A aritmética de ponto fixo, as tabelas angulares e as tabelas de iluminação permitem que o backend escreva no framebuffer linear de resolução lógica 320×200. O renderer preserva listas de clipping, visplanes e máscaras de sprite; uma versão fiel não pode ser reduzida a “um quadrado por sala” sem declarar a perda de comportamento. [4] [5] [6]

O WAD é um contêiner de lumps. O cabeçalho contém identificação `IWAD` ou `PWAD`, número de lumps e deslocamento do diretório; cada entrada contém posição, tamanho e nome de até oito bytes. `W_InitMultipleFiles` agrega arquivos e a procura reversa dá precedência a lumps posteriores. O formato permite separar motor, dados principais e complementos, mas também exige que o projeto trate o WAD como dado externo, e não como código. [7]

Os mapas vanilla dependem da sequência de lumps `THINGS`, `LINEDEFS`, `SIDEDEFS`, `VERTEXES`, `SEGS`, `SSECTORS`, `NODES`, `SECTORS`, `REJECT` e `BLOCKMAP`. `NODES` aceleram a visibilidade; `BLOCKMAP` acelera colisões e consultas espaciais; `REJECT` pode evitar verificações de linha de visão entre setores. `P_SetupLevel` converte esses dados em estruturas internas relacionadas por referências e ponteiros. [8]

A simulação é dirigida por **tics**. `TICRATE` vale 35 tics por segundo. A entrada de teclado, mouse e joystick é convertida em um `ticcmd_t`, que contém movimento, giro e botões. `P_Ticker` atualiza jogadores, *thinkers*, especiais, respawn e tempo de nível em uma ordem definida. Rede e demos usam a representação de comandos por tic, portanto a lógica não deve receber eventos de plataforma diretamente como posições contínuas. [9] [10] [11]

O sistema de memória original usa uma zona contígua com blocos, tags de vida útil e purga. O cache de lumps integra-se ao alocador; dados de nível podem ser liberados na troca de mapa e recursos de cache podem ser recarregados. No backend Linux publicado, a zona reserva 6 MiB, mas isso é um fato daquele backend, não um requisito histórico universal do executável DOS. [7] [14]

### 2.2 O que pode ser transposto

A transposição mais defensável conserva **contratos observáveis**, não a aparência de cada arquivo C. Podem ser transpostos para papel: um relógio lógico por rodadas; uma folha de estado; um mapa 2D; ocupação e conectividade; atores com vida e estados; comandos discretos; ataques de linha de visão; uma fonte de dano pré-escrita; uma rotina de resolução; um quadro frontal reduzido; e um checksum que detecte divergências.

Não devem ser chamados de equivalentes ao DOOM original: uma grade de células no lugar de coordenadas contínuas; uma tabela de cinco vetores no lugar de BSP, projeção, clipping e spans; uma porta aberta permanentemente no lugar de todos os especiais; uma IA cardinal no lugar de *thinkers* e estados completos; ou uma fita `d3` no lugar do gerador pseudoaleatório vanilla. Essas escolhas são **inferências de engenharia para o demake**.

| Elemento do DOOM | Fato observado | Transposição para papel | Limite declarado |
|---|---|---|---|
| Tempo | 35 tics/s, com comandos construídos por tic | Um tick por ação principal | Um tick manual não equivale a 28,57 ms físicos |
| Mapa | Lumps de geometria, setores, BSP e aceleração 2D | Células, arestas e portas identificadas | Não lê WAD nem executa BSP |
| Visibilidade | BSP, segmentos, clipping, colunas, spans e sprites | Cinco vetores frontais quantizados | Não produz perspectiva contínua nem textura vanilla |
| Entrada | Eventos convertidos em `ticcmd_t` | Ação escrita em uma linha de log | Pode ter menos combinações que `ticcmd_t` |
| Combate | Pistola com dano `5*(P_Random()%3+1)` e linha de ataque | Fita `d3` com 5, 10 ou 15 de dano | A sequência não reproduz o RNG original |
| Atores | Posição, ângulo, estado, vida, alvo, flags e temporizadores | Ficha com posição, vida, estado e cooldown | IA e estados são reduzidos |
| Memória | Zona com tags, cache e purga | Folhas P2–P5 e cartões de estado | A organização física não é o alocador original |
| Dados | IWAD/PWAD externos e precedência de lumps | Mapa e regras próprios, em folhas | Compatibilidade com IWAD é excluída |

A tabela separa os fatos do motor das escolhas do demake. O propósito do papel não é esconder as diferenças, mas tornar cada redução explícita e verificável.

## 3. Três modos de execução e escolha de produto

### 3.1 Execução manual fiel

Neste modo, o papel tenta representar o máximo possível do contrato original: comandos por tic, mapa derivado de dados, tabelas de projeção, clipping, estado de objetos, dano, colisão e talvez um framebuffer de baixa resolução. Um protótipo fiel de um único subsistema é tecnicamente viável. Um jogo completo não é um objetivo operacional razoável: cada tic exigiria localizar estruturas, atualizar vários atores, resolver colisões, calcular visibilidade e desenhar ou transcrever muitas colunas.

O custo é alto em páginas, preparação, tempo de operador e probabilidade de erro. A fidelidade pode ser alta para um traço pequeno, como a leitura de uma sequência de comandos ou a travessia de um BSP simples, mas cai rapidamente quando mapas, atores e visibilidade crescem. A verificabilidade pode ser alta se cada campo tiver uma fonte e uma regra, mas a reprodutibilidade depende de treinamento, legibilidade e revisão independente.

**Uso adequado:** laboratório didático sobre um contrato específico, por exemplo WAD, ticcmd, BSP ou uma coluna projetada. **Uso inadequado:** prometer “o DOOM original inteiro em papel”.

### 3.2 Demake determinístico

Neste modo, o projeto define um novo estado discreto com mapa limitado e regras suficientes para produzir uma partida. A proposta PaperDOOM-1 usa células ortogonais, quatro direções, atores em quantidade limitada, uma arma hitscan, portas opcionais, fonte de dano pré-escrita e renderer frontal de cinco colunas. A regra de execução é determinística: dois operadores que recebem o mesmo estado inicial, as mesmas ações e a mesma fita devem obter o mesmo estado final.

O custo é baixo a médio e cresce de forma previsível com o número de células, atores, portas, ações e páginas. A fidelidade ao DOOM é conceitual: primeira pessoa, exploração, ameaça, tiro instantâneo e objetivos espaciais. A verificabilidade é a melhor das três modalidades, porque a fonte de verdade cabe em tabelas e o log pode ser comparado linha a linha.

**Uso adequado:** produto principal deste plano, oficina, jogo de mesa experimental, demonstração de computação manual e estudo de design determinístico.

### 3.3 Papel como interface para computador externo

Neste modo, o papel é um periférico físico: cartões representam comandos, marcadores indicam posição, uma câmera reconhece símbolos ou uma folha recebe o framebuffer reduzido. O motor real executa em um computador, navegador, calculadora, microcontrolador ou emulador. A fidelidade ao DOOM pode ser alta, mas a execução não é *paper-only*. O projeto deve dizer onde o motor calcula, onde o IWAD vive, qual runtime é usado e como o frame retorna ao papel.

O custo físico é baixo, mas o custo de engenharia externa pode ser alto. A verificabilidade depende de código-fonte, versão do runtime, entrada ao vivo, medição e procedência dos dados. A demonstração é forte para portabilidade ou instalação, mas não prova que uma folha seja uma CPU autônoma. Paper Playground, por exemplo, usa câmera, computador e micro:bit; é uma interface computacional em papel, não uma máquina apenas de papel. [23]

**Uso adequado:** instalação híbrida, exposição, interface tangível e comparação entre o estado físico e um port WebAssembly ou desktop. Deve ser apresentado como “DOOM controlado ou exibido por papel”.

## 4. Arquitetura faseada do PaperDOOM-1

### Fase 0 — contrato, escopo e proveniência

O projeto começa com uma declaração de uma página contendo quatro decisões: modalidade de execução; variante de fidelidade; conjunto de ações; e licença dos materiais. A versão inicial deve escolher o demake determinístico. O nome “PaperDOOM-1” deve aparecer como jogo inspirado e independente, sem sugerir que o projeto abre ou executa WADs do DOOM.

Nesta fase, separar código, documentação, regras, mapas e assets. O protótipo pode usar apenas símbolos tipográficos e desenhos próprios. Não incluir sprites, texturas, sons, músicas, mapas ou IWADs comerciais. Se algum código do repositório da id Software for copiado ou derivado, preservar a GPLv2 e os avisos históricos aplicáveis; se o motor do demake for novo, não rotulá-lo automaticamente como GPL apenas porque o tema é DOOM.

### Fase 1 — máquina manual mínima

Construir primeiro um interpretador de registradores com `PC`, estado, comando, transição e log. O Paper Computer demonstra que programa e estado podem ocupar a mesma folha com instruções de limpar, incrementar, decrementar, copiar e saltar. O CARDIAC demonstra uma arquitetura manual com memória, acumulador, entrada, saída e dez opcodes. [18] [19]

A finalidade desta fase é validar a disciplina de **estado antes de imagem**. Cada ciclo deve registrar estado anterior, entrada, regra aplicada, campos alterados e estado seguinte. Se o operador não consegue reproduzir uma soma ou uma condição de salto, não deve iniciar um jogo com combate.

### Fase 2 — núcleo do jogo

Adicionar uma folha P2 com o estado canônico, uma folha P3 com atores e uma folha P5 com o log. O mapa deve distinguir células de arestas. A célula define onde uma entidade pode estar; a aresta define se a passagem está aberta, fechada ou é uma porta. Essa separação permite modificar conectividade sem mover entidades ou redesenhar todo o mapa.

O estado mínimo é:

```text
S = {
  tick: inteiro >= 0,
  phase: PLAY | WON | LOST,
  rng_index: inteiro >= 0,
  player: {
    cell: (x, y),
    facing: N | E | S | W,
    hp: 0..100,
    ammo: inteiro >= 0
  },
  map: {
    cells[x,y]: FLOOR | WALL | EXIT,
    edges[x,y,dir]: OPEN | WALL | DOOR(id),
    doors[id]: CLOSED | OPEN
  },
  actors[id]: {
    type: SENTINEL | GRUNT,
    cell: (x,y),
    hp: inteiro >= 0,
    state: ALIVE | DEAD,
    cooldown: inteiro >= 0
  }
}
```

A apresentação não modifica esse estado. Um ator morto permanece na ficha como `DEAD`; uma porta permanece com seu estado; uma munição consumida não volta por causa de uma correção no desenho. O estado canônico é a fonte de verdade; mapa descoberto, HUD, quadro frontal e ilustrações são vistas derivadas.

### Fase 3 — mapa e renderer manual

O primeiro mapa deve ser uma sala única ou um corredor curto. O renderer não deve fingir executar o BSP. Ele deve declarar uma tabela fixa de vetores, por exemplo cinco colunas relativas à direção do jogador. Para cada coluna, percorrer distâncias discretas até encontrar parede, porta fechada, ator, item ou saída. Uma diagonal que cruza um canto é bloqueada se qualquer uma das duas arestas ortogonais estiver fechada.

A saída visual pode usar quatro símbolos de profundidade. Isso é uma aproximação de apresentação, não a rasterização original. Se o projeto quiser pesquisar fidelidade, deve criar uma trilha separada que compare uma cena simples do renderer vanilla com uma tabela manual, sem misturar o resultado com o demake jogável.

### Fase 4 — armas, inimigos e objetivos

Adicionar primeiro uma pistola hitscan, uma fita de dano e um inimigo sentinela. O ataque percorre a linha central até a primeira obstrução. O inimigo recebe 5, 10 ou 15 pontos de dano conforme o próximo valor da fita. Um inimigo morto muda para `DEAD`, deixa de bloquear movimento e não executa uma ação posterior no mesmo tick.

Depois de os testes básicos passarem, podem ser adicionados uma chave, uma porta, um segundo inimigo ou um objetivo de saída. Cada extensão exige uma nova regra, uma entrada na tabela de estado, um caso de teste e pelo menos um traço dourado. A ordem de extensão não deve ser confundida com a ordem de implementação do DOOM original.

### Fase 5 — validação, publicação e opção híbrida

Publicar apenas depois que duas pessoas independentes reproduzirem o mesmo cenário com o mesmo checksum. A documentação deve conter materiais para impressão, versão das regras, exemplos, limitações e uma classificação explícita entre fato do DOOM, referência de design e regra nova do PaperDOOM-1.

Somente depois pode ser criada uma interface híbrida. Nessa variante, um computador pode ler a ação escrita ou cartões, executar uma versão do demake ou um port real e devolver um frame reduzido. A documentação deve conservar duas linhas de proveniência: o estado físico do papel e o estado calculado pelo computador.

## 5. Protocolo operacional

### 5.1 Páginas

| Página | Conteúdo | Regra de integridade |
|---|---|---|
| **P0 — regras** | Ações, símbolos, dano, ordem do tick, vitória, derrota e limites | Imutável durante a partida |
| **P1 — mapa** | Grade, coordenadas, células e arestas | Uma única versão assinada |
| **P2 — estado** | Tick, jogador, vida, munição, direção, fase e RNG | Fonte de verdade |
| **P3 — atores** | ID, tipo, posição, vida, estado e cooldown | Atualizar por ID crescente |
| **P4 — eventos** | Portas, itens, hazards e terminalidade | Registrar causa e resultado |
| **P5 — log** | Uma linha por tick, entrada, efeitos e checksum | Nunca apagar; corrigir com nova linha |
| **P6 — renderer** | Cinco colunas, profundidades e legenda | Derivar apenas de P1–P3 |
| **P7 — testes** | Casos, traços dourados e resultados esperados | Usar antes de uma campanha |

### 5.2 Ordem fixa de um tick

1. Copiar o estado anterior e conferir o checksum.
2. Registrar o tick, a ação e o índice atual da fita.
3. Rejeitar ações inválidas, ataques sem munição e entradas após `WON` ou `LOST`.
4. Aplicar a ação do jogador.
5. Resolver coleta e condição de saída.
6. Atualizar atores vivos em ordem crescente de ID; um ator morto durante a ação do jogador não age nesse tick.
7. Aplicar ambiente e temporizadores.
8. Resolver terminalidade; se vitória e derrota parecerem ocorrer no mesmo tick, a derrota prevalece.
9. Incrementar `tick` e avançar `rng_index` somente quando uma regra consumiu a fita.
10. Calcular checksum, atualizar P2/P3 e redesenhar P6.

A ordem é inspirada na existência de uma sequência central em `P_Ticker`, mas não afirma reproduzir todos os subsistemas do motor. [11]

### 5.3 Checkpoint e checksum

Ao final de cada tick, o operador deve escrever um checkpoint com posição, direção, vida, munição, vida dos atores, estados de portas, índice da fita e fase. Para detectar erros de transcrição, usar:

```text
CHK = (tick + 3*x + 5*y + 7*dir + 11*hp + 13*ammo
       + 17*nr_chaves + 19*nr_atores_vivos + 23*rng_index) mod 97
```

Codificar `N=0`, `E=1`, `S=2`, `W=3`. O checksum detecta, mas não corrige, divergências. Ele é uma escolha de engenharia do PaperDOOM-1 e não é o checksum de rede do DOOM.

## 6. Protótipo mínimo: uma sala, um inimigo, uma arma e três ações

### 6.1 Contrato do protótipo

O cenário tem uma sala retangular sem portas, uma pistola e um sentinela. Há somente três ações válidas:

| Código | Ação | Regra |
|---|---|---|
| `F` | Avançar | Move uma célula na direção atual se o destino estiver livre |
| `T` | Virar | Gira 90 graus no sentido horário sem mover |
| `A` | Atacar | Dispara a pistola na linha central até a primeira obstrução |

Não há strafe, porta, chave, item, segundo inimigo ou projétil. Essa restrição é deliberada. O protótipo prova que papel pode executar uma transição com entrada, movimento, combate, dano, morte, checkpoint e renderer sem depender de uma lista aberta de exceções.

Mapa de teste, com coordenadas `x=0..6` e `y=0..4`:

```text
      0123456
y=0   #######
y=1   #.....#
y=2   #.....#
y=3   #P..G.#
y=4   #######
```

O jogador começa em `(1,3)`, olhando para leste. O sentinela `G` começa em `(4,3)` com 20 HP. A sala é piso em todas as células internas. O jogador começa com 100 HP e três munições. A fita de dano começa com `2, 1, 3`, que significam 10, 5 e 15 de dano. O sentinela tem cooldown inicial zero; quando vivo e adjacente no início de um tick, causa 5 de dano, entra em cooldown 2 e não se move. O cooldown é reduzido antes da verificação de ataque.

O objetivo do protótipo é marcar `WON` quando `G` estiver `DEAD`. Não é uma condição do DOOM original; é uma condição nova, suficiente para uma demonstração fechada.

### 6.2 Traço dourado

| Tick inicial | Ação | Transição do jogador | Resolução do sentinela | Estado após o tick | CHK |
|---:|---|---|---|---|---:|
| 0 | `F` | `(1,3)` → `(2,3)` | Distante; não ataca | HP 100, munição 3, G=20, fita 0 | 23 |
| 1 | `F` | `(2,3)` → `(3,3)` | Distante; não ataca | HP 100, munição 3, G=20, fita 0 | 27 |
| 2 | `A` | Dispara; primeiro alvo é G; consome fita 2 | G perde 10; contra-ataca por 5; cooldown 2 | HP 95, munição 2, G=10, fita 1 | 80 |
| 3 | `A` | Dispara; consome fita 1 | G perde 5; cooldown cai para 1; não ataca | HP 95, munição 1, G=5, fita 2 | 91 |
| 4 | `A` | Dispara; consome fita 3 | G perde 15 e passa a `DEAD`; não age | HP 95, munição 0, G=0, `WON` | 83 |

O checksum inicial, antes de qualquer ação, é 19. Os valores da tabela usam `dir=E`, nenhuma chave e um ator vivo até o terceiro disparo. Se o operador obter outro valor, deve comparar a primeira linha divergente, não corrigir apenas o checksum final.

O quadro frontal após o segundo `F`, olhando para leste, pode ser representado assim:

```text
r=-2     r=-1      r=0      r=+1     r=+2
  .        ░        G        ░        .

HUD: HP 100 | PISTOLA | MUNIÇÃO 3 | G=20
```

A altura dos símbolos é uma tabela do PaperDOOM-1. Ela não é uma coluna texturizada do renderer vanilla. O desenho pode ser ampliado com cinco profundidades, mas a fonte de verdade continua sendo a posição `(3,3)` e a ficha de `G` em P3.

### 6.3 O que o protótipo demonstra

O protótipo demonstra uma máquina manual com estado persistente, entrada finita, regras ordenadas, fonte de variação auditável, combate de linha de visão, morte terminal e saída verificável. Ele não demonstra leitura de WAD, compatibilidade com demos, BSP, setores, sprites, áudio, rede, aceleração ou o DOOM original. A descrição correta é: **demake determinístico de uma sala inspirado em DOOM e executável manualmente**.

## 7. Estrutura de arquivos para GitHub

A estrutura a seguir separa documentação, regras, código novo, testes e dados. Ela não pressupõe distribuição de IWAD proprietário:

```text
paperdoom/
├── README.md                         # escopo, classificação e instruções
├── LICENSE-DOCS.md                   # licença da documentação própria
├── LICENSE-CODE.txt                  # licença do código novo, se escolhida
├── LICENSE-GPL-2.0.txt               # somente se houver código derivado do DOOM GPL
├── THIRD_PARTY_NOTICES.md            # componentes, versões e licenças
├── CHANGELOG.md                      # alterações e datas
├── docs/
│   ├── FINAL-PLANO-DOOM-NO-PAPEL.md  # este plano consolidado
│   ├── conceitos.md                  # DOOM original versus demake
│   └── reproducao.md                 # materiais e procedimento
├── paper/
│   ├── P0-regras.pdf
│   ├── P1-mapa.pdf
│   ├── P2-estado.pdf
│   ├── P3-atores.pdf
│   ├── P4-eventos.pdf
│   ├── P5-log.pdf
│   ├── P6-renderer.pdf
│   └── P7-testes.pdf
├── src/
│   └── paperdoom/                    # validador ou emulador independente
├── maps/
│   ├── sala-minima.md
│   └── mapas-proprios/
├── tests/
│   ├── golden/
│   │   └── sala-minima.trace
│   ├── unit/
│   └── fixtures/
├── assets/
│   ├── OWNED_ORIGINAL.md             # arte própria, se houver
│   └── LICENSES.md                   # licença de cada asset
└── data/
    └── README-IWAD.md                # explica que IWAD comercial não é distribuído
```

Se uma versão futura usar código derivado do repositório oficial, `LICENSE-GPL-2.0.txt` deve acompanhar esse código, os avisos de copyright e os cabeçalhos históricos não devem ser removidos, e cada alteração deve ser identificada. O repositório oficial apresenta atualmente o código sob GPLv2, embora conserve cabeçalhos históricos que mencionam a DOOM Source Code License; essa situação exige preservação documental e, para um produto comercial ou juridicamente sensível, revisão profissional. [1] [30] [31]

Se o projeto for inteiramente novo, a licença do código novo e a licença da documentação podem ser escolhidas separadamente. A GPLv2 do motor oficial não licencia automaticamente texto novo, arte própria, regras novas ou um demake independente.

## 8. Licenciamento e separação entre código, IWAD e assets

O código publicado pela id Software contém `LICENSE.TXT` com GPLv2 e o README declara essa licença. A GPLv2 permite copiar, modificar e redistribuir o código sob as condições da licença, incluindo preservação de avisos, identificação de alterações e fornecimento do código-fonte correspondente para executáveis distribuídos. [1] [30] [31]

Isso não transforma o jogo completo em conteúdo livre. O IWAD contém mapas, gráficos, sprites, texturas, sons, músicas, fontes e outros lumps. O próprio lançamento informa que os dados reais do jogo são necessários e que arte e WADs não foram incluídos. IWAD, PWAD, marca, manual, textos narrativos e assets devem ser auditados separadamente. [1] [32] [33]

A política de publicação recomendada é:

| Componente | Tratamento no projeto |
|---|---|
| Código novo do demake | Licença escolhida pelo autor, declarada em arquivo próprio |
| Código copiado ou derivado do DOOM GPL | GPLv2, avisos preservados e alterações identificadas |
| Código de terceiros | Inventário em `THIRD_PARTY_NOTICES.md` e licença verificada |
| IWAD comercial | Não incluir no GitHub, no PDF de impressão nem na release |
| IWAD shareware | Não presumir que “shareware” autoriza hospedagem pública; usar fonte autorizada ou instrução para o usuário |
| Freedoom | Pode ser alternativa de conteúdo livre, com sua própria licença BSD, avisos e créditos; não é licença do motor DOOM |
| Assets próprios | Licença e autoria declaradas individualmente |
| Textos de terceiros | Não copiar extensamente; citar e respeitar a licença da fonte |
| Marca e identidade | Declarar projeto independente e evitar sugerir endosso oficial |

Freedoom é uma substituição de conteúdo com licença própria; sua existência permite testar um motor compatível sem tratar os assets comerciais como livres. [34] A análise é técnica, não parecer jurídico. Em caso de distribuição comercial, inclusão de código de terceiros, uso de marcas ou publicação de dados históricos, deve haver revisão jurídica específica.

## 9. Checklist de implementação e publicação

### 9.1 Escopo e terminologia

- [ ] O README declara se o projeto é execução manual fiel, demake ou interface híbrida.
- [ ] O texto diz explicitamente que PaperDOOM-1 não lê WADs e não é o DOOM completo.
- [ ] Fatos sobre o motor original estão separados de inferências e regras novas.
- [ ] A versão das regras e o estado inicial do protótipo estão fixados.
- [ ] O número de ações, ordem do tick e condição terminal estão escritos em P0.

### 9.2 Estado e execução

- [ ] Há uma única folha de estado canônico.
- [ ] Toda ação produz uma linha no log.
- [ ] A ordem de atualização do jogador e dos atores é fixa.
- [ ] A fita de dano é numerada e não pode ser reordenada.
- [ ] O checksum é calculado após cada tick.
- [ ] A apresentação nunca altera P2 ou P3.

### 9.3 Mapa e renderer

- [ ] Toda célula interna tem coordenada.
- [ ] Toda aresta é classificada como aberta, parede ou porta.
- [ ] A conectividade é simétrica quando aplicável.
- [ ] Diagonais não atravessam cantos fechados.
- [ ] O renderer usa somente o estado autorizado e sua legenda é completa.
- [ ] A documentação não chama o renderer de cinco vetores de BSP ou ray caster vanilla.

### 9.4 Reprodutibilidade

- [ ] O traço dourado da sala mínima está anexado.
- [ ] Duas pessoas executaram o traço sem consultar uma correção intermediária.
- [ ] O estado final e o checksum coincidem.
- [ ] A primeira divergência pode ser localizada em menos de cinco minutos.
- [ ] As folhas de impressão têm versão, escala e instruções de recorte.

### 9.5 Licenças

- [ ] O código oficial derivado mantém GPLv2 e avisos de copyright.
- [ ] A origem e a licença de cada componente de terceiros estão listadas.
- [ ] Nenhum IWAD proprietário ou asset não autorizado está no repositório.
- [ ] Freedoom, se usado, aparece como componente separado com créditos próprios.
- [ ] Documentação, código novo e assets próprios têm termos claros.
- [ ] O README contém aviso de projeto independente.

## 10. Testes e critérios de sucesso

### 10.1 Testes essenciais

| ID | Teste | Preparação | Resultado esperado |
|---|---|---|---|
| T1 | Parede externa | `F` contra a borda da sala | Posição não muda; tick ainda é registrado |
| T2 | Movimento válido | Jogador em piso livre | Posição avança uma célula, sem salto |
| T3 | Rotação | `T` em cada direção | Direção muda exatamente 90 graus; posição não muda |
| T4 | Linha bloqueada | Parede entre jogador e G | `A` consome munição, mas não altera HP de G |
| T5 | Linha aberta | G a distância 1–5 | Somente o primeiro ator recebe dano |
| T6 | Dano | Fita `1,2,3` | Danos exatos 5, 10 e 15 |
| T7 | Morte | G com HP 5 e dano 5 | G passa a `DEAD` e não age no mesmo tick |
| T8 | Munição | Munição zero e `A` | Ação rejeitada; fita não avança |
| T9 | Inimigo | Jogador adjacente e G vivo | Dano e cooldown seguem P0 |
| T10 | Terminalidade | Entrada após `WON` ou `LOST` | Entrada rejeitada e estado preservado |
| T11 | Checksum | Reexecutar traço dourado | Todos os CHK coincidem |
| T12 | Renderer | Posições conhecidas nas cinco colunas | Primeira obstrução e símbolo corretos |
| T13 | Auditoria | Dois operadores independentes | Mesmo estado final e mesma fase |
| T14 | Integridade do mapa | Conferir todas as arestas | Nenhuma passagem assimétrica não documentada |

### 10.2 Critérios de sucesso por estágio

| Estágio | Critério mínimo de aceitação |
|---|---|
| **Papel básico** | Um operador executa 20 ticks sem regra ambígua e registra todos os estados |
| **Protótipo mínimo** | Duas execuções do traço `F,F,A,A,A` produzem os cinco checkpoints esperados e `WON` |
| **Demake alfa** | Uma segunda sala ou objetivo é adicionada sem quebrar os testes T1–T14 |
| **Demake publicável** | Um terceiro operador consegue imprimir, iniciar e terminar a sala apenas com README e P0–P7 |
| **Estudo fiel de subsistema** | Um experimento separado compara uma regra manual com uma saída do código-fonte, sem chamar o demake de port completo |
| **Interface híbrida** | A instalação identifica motor externo, runtime, entrada, display, versão e dados usados; um vídeo pré-renderizado sozinho não é aceito como prova |

## 11. Riscos e mitigação

| Risco | Consequência | Mitigação |
|---|---|---|
| Confundir demake com DOOM original | Comunicação tecnicamente falsa | Usar a taxonomia da Seção 1 e repetir os limites no README |
| Estado espalhado em desenhos | Divergência silenciosa | P2/P3 são canônicos; P6 é sempre derivado |
| Regras implícitas | Dois operadores obtêm partidas diferentes | Registrar entradas, ordem, exceções e terminalidade em P0 |
| Fadiga e erro de cópia | Checkpoints incorretos | Tamanho pequeno, pausa por blocos, revisão independente e checksum |
| Aleatoriedade não reproduzível | Traços não comparáveis | Fita ou baralho d3 numerado e imutável |
| Renderer superestimado | Promessa de equivalência visual | Chamar cinco vetores de aproximação quantizada |
| Escopo crescente | Muitas páginas e baixa jogabilidade | Só adicionar conteúdo após todos os testes passarem |
| Dependência de IWAD | Distribuição potencialmente ilícita | Não incluir dados comerciais; usar assets próprios ou alternativa livre autorizada |
| Mistura de licenças | Release incompleta ou incompatível | Separar código, documentação, terceiros e assets em arquivos distintos |
| Interface híbrida rotulada como paper-only | Atribuição errada de computação | Declarar cada camada: engine, dados, runtime e display |
| Comparar 35 Hz físico com tick manual | Ritmo impraticável ou falsa fidelidade | Definir tick como unidade lógica e explicar a diferença |
| Confundir imagem com estado | Regras podem ser alteradas por ilustração | Sempre resolver a partir de P2/P3 e recalcular P6 |

## 12. Distinções finais

### DOOM original

É o motor e o conjunto de dados históricos definidos por uma arquitetura de software: WADs, mapas estruturados, BSP pré-calculado, renderer de colunas e spans, objetos, armas, colisão, tics, comandos, demos, rede e interfaces de sistema. O código-fonte publicado é uma fonte primária do motor Linux, mas não inclui automaticamente os dados comerciais nem prova todos os detalhes do executável DOS. [1] [3] [7] [9]

### Demake inspirado

É o PaperDOOM-1. Usa escolhas novas para produzir um jogo físico pequeno, determinístico e jogável. A relação com DOOM é de inspiração e seleção de propriedades percebidas. O demake não deve aceitar a etiqueta “compatível com WAD”, “port vanilla” ou “DOOM completo”.

### Experimento de computação em papel

É a investigação do papel como suporte de instruções, memória, lógica, estado ou interface. Pode usar uma máquina de registradores, CARDIAC, origami, cartões, grafite ou uma câmera. “Turing-completo” em um modelo formal não significa execução rápida, automática, infinita ou robusta em uma folha finita. O papel é um meio físico com limites de espaço, legibilidade, atrito, fadiga e intervenção humana. [18] [19] [20] [21] [22] [23]

A formulação pública recomendada é:

> **PaperDOOM-1 é um demake manual e determinístico, inspirado em DOOM, que executa regras de jogo e computação auditáveis em papel. Ele não é o DOOM original, não é compatível com WADs e não substitui um port executável. Uma instalação que use um computador externo deve ser chamada de interface híbrida.**

## Referências

[1]: https://github.com/id-Software/DOOM "id-Software/DOOM — DOOM Open Source Release, README e licença atual"

[2]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/doomdef.h "DOOM original — doomdef.h, constantes de resolução e TICRATE"

[3]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/r_bsp.c "DOOM original — r_bsp.c, BSP, R_CheckBBox, clipping e subsectors"

[4]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/r_draw.c "DOOM original — r_draw.c, colunas e spans no framebuffer"

[5]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/r_plane.c "DOOM original — r_plane.c, visplanes, pisos, tetos e spans"

[6]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/r_things.c "DOOM original — r_things.c, projeção e sprites mascarados"

[7]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/w_wad.c "DOOM original — w_wad.c, WAD, precedência e cache de lumps"

[8]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/doomdata.h "DOOM original — doomdata.h, registros e lumps de mapas"

[9]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/d_main.c "DOOM original — d_main.c, loop principal, tics e apresentação"

[10]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/d_ticcmd.h "DOOM original — d_ticcmd.h, comando de entrada por tic"

[11]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/p_tick.c "DOOM original — p_tick.c, ordem de atualização de jogadores e thinkers"

[12]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/p_pspr.c "DOOM original — p_pspr.c, ataque da pistola e dano"

[13]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/p_inter.c "DOOM original — p_inter.c, dano, morte e interação"

[14]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/i_system.c "DOOM original — i_system.c, relógio Linux e zona de memória do backend"

[15]: https://github.com/chocolate-doom/chocolate-doom "Chocolate Doom — fidelidade ao DOS e portabilidade"

[16]: https://github.com/fabiangreffrath/crispy-doom "Crispy Doom — resolução ampliada, widescreen e limites removidos"

[17]: https://github.com/team-eternity/calico-doom "Calico — backport do DOOM de Atari Jaguar e renderer específico de console"

[18]: https://wiki.xxiivv.com/site/paper_computer.html "Paper Computer — máquina de registradores manual em uma folha"

[19]: https://www.cs.drexel.edu/~bls96/museum/cardiac.html "CARDIAC — computador manual de papelão da Bell Telephone Laboratories"

[20]: https://arxiv.org/html/2309.07932v4 "Flat origami is Turing Complete — lógica e Rule 110 por dobraduras"

[21]: https://www.pnas.org/doi/10.1073/pnas.1805122115 "Origami mechanologic — memória mecânica regravável e portas físicas"

[22]: https://www.ibm.com/history/punched-card "The IBM punched card — cartões de 80 colunas e programação"

[23]: https://dl.acm.org/doi/10.1145/3689050.3705981 "Physical Computing with Paper Playground — papel como interface híbrida"

[24]: https://github.com/ading2210/doompdf "DoomPDF — port de DOOM em PDF com asm.js e campos de texto"

[25]: https://github.com/critor/ndoom "nDoom — port nativo de DOOM para calculadoras TI-Nspire"

[26]: https://github.com/kilograham/rp2040-doom "RP2040 Doom — port para RP2040/RP2350 e requisitos de memória"

[27]: https://github.com/jacobenget/doom.wasm "doom.wasm — DOOM compilado para WebAssembly com interface de browser"

[28]: https://github.com/Pranshul-Thakur/DOOM-in-excel "DOOM-in-excel — motor externo e Excel como display via PyXLL"

[29]: https://github.com/moses297/doom-on-google-sheets "doom-on-google-sheets — js-dos, Apps Script e atualização de células"

[30]: https://github.com/id-Software/DOOM/blob/master/LICENSE.TXT "LICENSE.TXT — GNU General Public License versão 2 no repositório oficial"

[31]: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html "GNU General Public License, version 2 — texto da licença"

[32]: https://doomwiki.org/wiki/IWAD "IWAD — conteúdo principal, mapas, gráficos e recursos de DOOM"

[33]: https://doomwiki.org/wiki/PWAD "PWAD — arquivos de complemento e substituição de recursos"

[34]: https://freedoom.github.io/about.html "Freedoom — conteúdo livre alternativo e licença própria"

---

**Nota metodológica.** Este documento consolida os cinco arquivos de pesquisa fornecidos. As afirmações sobre o motor original, seus formatos e seus contratos são tratadas como fatos apenas quando apoiadas pelas fontes primárias ou técnicas listadas. As decisões de PaperDOOM-1 — grade, três ações, fita de dano, checksum, sala mínima, IA e critérios de aceitação — são propostas novas de engenharia e não alegações sobre o funcionamento interno do DOOM.
