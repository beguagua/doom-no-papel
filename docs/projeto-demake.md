# Projeto de um DOOM de papel

**Identificador do projeto:** PaperDOOM-1  
**Escopo:** jogo de ação inspirado em DOOM, executável manualmente com folhas, lápis, marcadores e um baralho ou fita de números.  
**Natureza da proposta:** demake jogável, não uma implementação completa do motor original.

## conclusão

É viável projetar um jogo manual inspirado em DOOM, mas não é honesto chamar o resultado de “DOOM completo em papel”. O DOOM original combina coordenadas contínuas, alturas de setores, colisão geométrica, objetos com estados e temporizadores, ataques hitscan, sprites, planos de piso e teto, e uma árvore BSP pré-computada para ordenar a visibilidade. O papel não precisa reproduzir todas essas estruturas para produzir uma experiência jogável. Ele precisa preservar um contrato menor e explícito: explorar um mapa oculto, virar e avançar, abrir portas, coletar chaves e munição, enfrentar inimigos, receber dano e alcançar a saída.

A arquitetura recomendada é o **PaperDOOM-1**, um demake determinístico de um jogador com estas restrições: mapa ortogonal de 9 × 6 células, quatro orientações cardeais, no máximo oito atores, até três tipos de item, uma arma hitscan principal, portas discretas e um renderer frontal de cinco “raios” quantizados. Um tick não representa 1/35 de segundo em tempo físico; representa uma rodada manual. Essa separação é deliberada. O código original fixa sua lógica em 35 tics por segundo [3], mas tentar contar 35 atualizações por segundo em papel tornaria o jogo impraticável sem acrescentar fidelidade relevante.

O estado canônico deve existir em uma **folha de estado**. O mapa, a ficha de atores, o log de ações e o desenho frontal são apenas vistas desse estado. Ao final de cada tick, o jogador atualiza o log, recalcula o estado e desenha o quadro. Essa regra evita que uma ilustração inconsistente passe a ser tratada como verdade.

O resultado preserva, por inferência de projeto, cinco propriedades percebidas de DOOM: movimentação em primeira pessoa, combate rápido de linha de visão, pressão de inimigos, portas e chaves como controle espacial, e feedback visual frontal. Ele não preserva a geometria, o timing ou a renderização originais. A conclusão prática é: **PaperDOOM-1 é um jogo jogável inspirado no modelo de dados e no ritmo de DOOM, não um port fiel nem um formato para executar mapas WAD originais**.

| Decisão | Especificação de PaperDOOM-1 | Motivo |
|---|---|---|
| Unidade espacial | Uma célula quadrada; movimento de uma célula por ação | Elimina coordenadas fracionárias e cálculos trigonométricos |
| Orientação | Norte, leste, sul ou oeste | Permite uma tabela de rotação única |
| Estado temporal | Um tick por ação do jogador | Mantém a execução manual reproduzível |
| Mapa | Células de piso mais arestas de parede, porta ou passagem | Separa ocupação de conectividade |
| Renderer | Cinco vetores de célula, profundidade máxima cinco | Mantém a sensação frontal sem BSP ou seno/cosseno |
| Combate | Pistola hitscan com dano 5, 10 ou 15; inimigos com pontos de vida | Mantém a ideia de tiro instantâneo e é fácil de auditar |
| Aleatoriedade | Fita ou baralho d3 pré-escrito | Dois jogadores podem reproduzir o mesmo cenário |
| Vitória | Alcançar a célula de saída com a chave exigida e todos os objetivos definidos | Fornece um fim verificável |

## evidências

### Método e distinção entre fato e inferência

As afirmações sobre o DOOM original abaixo foram verificadas lendo o repositório oficial do código-fonte liberado pela id Software, os arquivos C e headers correspondentes e duas descrições técnicas independentes. A coluna “Tipo” separa fatos observados nas fontes de decisões que são inferências de engenharia para o jogo de papel.

| Afirmação | Tipo | Evidência lida | Consequência para o projeto |
|---|---|---|---|
| Um mapa DOOM é descrito por `THINGS`, `LINEDEFS`, `SIDEDEFS`, `VERTEXES`, `SEGS`, `SSECTORS`, `NODES`, `SECTORS`, `REJECT` e `BLOCKMAP`; os headers oficiais definem esses registros | **Fato verificado** | `doomdata.h` [2] e a especificação técnica EDGE [12] | Não é necessário copiar o WAD para o papel; é melhor escolher uma codificação tabular menor e declarar a perda de fidelidade |
| A geometria do nível é essencialmente 2D em planta; setores carregam piso, teto, luz e texturas, e a estrutura original não suporta “salas acima de salas” | **Fato verificado** | Artigo técnico “The Doom rendering engine” [11] | Uma grade 2D de células é uma aproximação estrutural coerente para o núcleo do demake |
| O renderer original percorre uma árvore BSP, visita primeiro o lado da câmera e testa a caixa delimitadora do outro lado antes de visitá-lo | **Fato verificado** | `r_bsp.c`, especialmente `R_RenderBSPNode`, `R_CheckBBox` e `R_AddLine` [10] | Um renderer manual não deve fingir que está executando BSP; deve usar uma tabela fixa de visibilidade por células |
| A lógica original usa 35 tics por segundo | **Fato verificado** | `TICRATE 35` em `doomdef.h` [3]; a contagem de `leveltime` ocorre em `P_Ticker` [5] | O tick manual deve ser uma unidade lógica, com uma nota explícita de que não equivale a 28,57 ms físicos |
| O comando por tic original contém movimento para frente, movimento lateral, giro, consistência, caractere de chat e botões | **Fato verificado** | `ticcmd_t` em `d_ticcmd.h` [4] e construção do comando em `g_game.c` [14] | O log de papel deve ter uma linha de comando por tick, mas pode reduzir os campos àqueles que o jogador realmente usa |
| A ordem central de `P_Ticker` é pensar nos jogadores, executar thinkers, atualizar especiais, processar respawn e incrementar `leveltime` | **Fato verificado** | `p_tick.c`, função `P_Ticker` [5] | O protocolo manual precisa ter ordem fixa; inverter jogador e inimigos mudaria o resultado |
| O objeto móvel original guarda posição x/y/z, ângulo, momento, raio, altura, estado, contador de estado, flags, vida, alvo e tempos de reação | **Fato verificado** | `mobj_t` em `p_mobj.h` [15] e movimentação/estados em `p_mobj.c` [16] | A ficha de ator deve guardar somente os campos que afetam regras e renderer, mas a seleção deve ser explícita |
| O movimento aplica impulso conforme comando e ângulo, depois tenta uma nova posição; a colisão verifica coisas e linhas, e subir um degrau acima de 24 unidades é rejeitado | **Fato verificado** | `p_user.c` [6] e `p_map.c`, `P_CheckPosition`/`P_TryMove` [7] | Uma célula bloqueada e uma porta fechada substituem a geometria contínua; não se deve permitir “diagonal implícita” |
| O ataque de pistola é hitscan: `P_GunShot` sorteia dano 5 vezes um valor entre 1 e 3 e chama `P_LineAttack`; a rotina para no primeiro alvo ou parede relevante | **Fato verificado** | `p_pspr.c` [9] e `p_map.c`, `P_AimLineAttack`/`P_LineAttack` [7] | A pistola de papel pode usar uma fita d3 e resolver a linha de visão por células |
| O objeto `MT_POSSESSED` possui 20 de vida, e `MT_SHOTGUY` possui 30 de vida, além de flags de solidez e de alvo atingível | **Fato verificado** | Tabela `mobjinfo` em `info.c` [13] | Esses valores podem ser usados como referência de escala, desde que a tabela de papel seja marcada como uma adaptação |
| O dano reduz a vida, pode aplicar armadura e, quando a vida chega a zero, muda o ator para estado morto e contabiliza a morte | **Fato verificado** | `P_DamageMobj` e `P_KillMobj` em `p_inter.c` [8] | O ledger precisa registrar vida atual e `ALIVE/DEAD`; não basta apagar a miniatura do inimigo |

### O que foi verificado e o que foi inferido

**Fatos verificados:** o código original é dirigido por tics; o nível é uma planta 2D com setores; os atores têm estado, vida e movimento; a colisão é separada da renderização; a pistola usa uma linha de ataque; e o renderer usa BSP, segmentos, clipping e planos. Esses fatos são descrições do artefato original, não regras obrigatórias para um jogo de papel.

**Inferências de projeto:** a grade de células, as quatro direções, os cinco vetores, a redução a uma pistola, o inimigo sentinela, o formato das folhas, o checksum, a fita d3 e a regra de um comando principal por tick são escolhas novas. Elas são justificadas por auditabilidade e manuseio humano. Não devem ser apresentadas como funcionamento interno de DOOM.

## implicações para o projeto

### 1. Contrato operacional

O jogo usa uma separação em quatro camadas:

1. **Modelo:** estado canônico, mapa, regras e fonte de aleatoriedade.
2. **Entrada:** uma ação escrita pelo jogador no log.
3. **Simulação:** transição determinística de um estado para o próximo.
4. **Apresentação:** HUD, mapa descoberto e quadro frontal de cinco colunas.

A apresentação nunca modifica o estado. Um ator morto continua registrado como `DEAD`; uma porta continua tendo um estado; e um item coletado recebe `COLLECTED`. Essa redundância evita erros de apagar e recolocar marcadores.

### 2. Páginas e materiais

Use uma pasta com páginas numeradas. Os números são referências entre folhas, não páginas descartáveis.

| Página | Conteúdo | Regra de uso |
|---|---|---|
| P0 — regras | Legenda, ações permitidas, tabela de dano, tipos de ator, condição de vitória | Não alterar durante uma partida |
| P1 — mapa-mestre | Grade completa, coordenadas, paredes e arestas identificadas | Fica com o árbitro ou dobrada; o jogador recebe apenas o mapa descoberto |
| P2 — estado | Tick, posição e direção do jogador, vida, armadura, arma, munição, chaves, flags e RNG | É a fonte de verdade do jogador |
| P3 — atores | Uma linha por ator, com ID, tipo, posição, vida, estado, cooldown, alerta e drop | Atualizar na ordem crescente de ID |
| P4 — eventos | Portas, elevadores simplificados, saída, dano ambiental e itens | Registrar a causa, não apenas o novo valor |
| P5 — log de ticks | Uma linha por tick: entrada, movimento, alvo, dano, inimigo, resultado, checksum | Nunca apagar linhas; corrigir com uma nova linha marcada |
| P6 — renderer | Grade de cinco colunas e tabela de profundidade | Redesenhar depois de cada tick concluído |
| P7 — validação | Cenários de teste, resultado esperado e assinatura do estado | Usar antes de jogar uma campanha |

Materiais mínimos: lápis, borracha, régua, seis marcadores de papel para atores e itens, um marcador para a posição do jogador e um baralho d3 ou uma fita contendo uma sequência fixa de `1, 2, 3`. Um dado d3 também serve, mas uma fita pré-escrita fornece reprodutibilidade.

### 3. Representação de estado

A notação abaixo é a especificação do estado, não código executável.

```text
S = {
  tick: inteiro >= 0,
  phase: PLAY | WON | LOST,
  rng_index: inteiro,
  player: {
    cell: (x, y),
    facing: N | E | S | W,
    hp: 0..100,
    armor: 0..100,
    weapon: PISTOL,
    ammo_clip: inteiro >= 0,
    keys: conjunto de BLUE | YELLOW | RED,
    attack_cooldown: inteiro >= 0,
    used_down: booleano
  },
  map: {
    cells[x,y]: FLOOR | EXIT | HAZARD,
    edges[x,y,dir]: OPEN | WALL | DOOR(id),
    doors[id]: CLOSED | OPEN,
    items[id]: PRESENT | COLLECTED
  },
  actors[id]: {
    type: SENTINEL | GRUNT,
    cell: (x,y),
    facing: N | E | S | W,
    hp: inteiro,
    state: IDLE | ALERT | ATTACK | DEAD,
    cooldown: inteiro >= 0,
    drops: NONE | AMMO | KEY
  }
}
```

O mapa distingue **célula** de **aresta**. A célula diz onde se pode estar; a aresta diz se duas células são conectadas. Essa escolha permite que uma porta seja uma barreira entre duas células, em vez de uma ocupação ambígua de célula. Para reduzir escrita, uma folha pode desenhar a porta na célula adjacente, mas o ledger deve registrar a aresta canônica, por exemplo `edge(3,1,E)=DOOR(D1)`.

A ocupação é exclusiva: duas entidades sólidas não podem terminar o mesmo tick na mesma célula. Um item pode compartilhar a célula do jogador apenas durante a coleta; ao final do tick ele deve ficar `COLLECTED`. O mapa-mestre contém todas as entidades, mas a folha do jogador só mostra células já descobertas e símbolos que o renderer autorizou revelar.

#### Checksum manual

O checksum detecta, mas não corrige, erros de transcrição. Ao final de cada tick, calcule:

```text
CHK = (tick + 3*x + 5*y + 7*dir + 11*hp + 13*ammo_clip
       + 17*nr_chaves + 19*nr_atores_vivos + 23*rng_index) mod 97
```

Codifique `dir` como N=0, E=1, S=2 e W=3. `nr_atores_vivos` inclui somente atores com estado diferente de `DEAD`. Se um checksum divergir, compare o log a partir do primeiro tick divergente. Este checksum é uma inferência simples de engenharia; não é o checksum de rede de DOOM.

### 4. Mapa e legenda

O mapa de PaperDOOM-1 usa nove colunas e seis linhas úteis, cercadas por parede. A legenda do exemplo é:

```text
# = parede sólida
P = início do jogador
K = chave azul
D = porta D1
G = sentinela inimiga
M = inimigo de referência
E = saída
. = piso
```

Mapa completo de teste, com coordenadas `x=0..8` e `y=0..5`:

```text
      012345678
 y=0  #########
 y=1  #PK.D..G#
 y=2  #...#...#
 y=3  #...#..E#
 y=4  #...#...#
 y=5  #########
```

O ponto `D` em `(4,1)` é a aresta `edge(3,1,E)=DOOR(D1)`, não uma célula transitável enquanto estiver fechada. A parede vertical em `x=4`, de `y=2` a `y=4`, separa os dois lados. A porta é, portanto, o único cruzamento. `K` está em `(2,1)`; `G` está em `(7,1)`; e `E` está em `(7,3)`. O objetivo deste cenário mínimo é coletar `K`, abrir `D1`, derrotar `G` e chegar a `E`.

A convenção de setores é reduzida, mas explícita: cada grupo conectado de células tem `floor=0`, `ceiling=2` e `light=normal`. Uma porta fechada tem `ceiling=0` na passagem e é bloqueio; uma porta aberta herda `floor=0`, `ceiling=2`. Isso não modela um elevador ou alturas contínuas; apenas conserva a ideia de uma abertura que muda a conectividade.

### 5. Renderer por células

O renderer escolhido não é o renderer original. Ele é uma aproximação frontal quantizada, desenhada com cinco colunas. Não há perspectiva contínua, textura, sprite animado, visplane ou BSP. O papel precisa responder a uma pergunta limitada: “o que há nas cinco direções grosseiras à frente do jogador?”.

Para o jogador voltado para leste, use estes vetores de célula, em ordem de `r=-2` a `r=+2`:

```text
r=-2: ( 0,-1)   lateral esquerda distante
r=-1: (+1,-1)   diagonal esquerda
r= 0: (+1, 0)   centro
r=+1: (+1,+1)   diagonal direita
r=+2: ( 0,+1)   lateral direita distante
```

Para cada coluna, inspecione `n=1..5` e visite `cell + n*v`. Para N, S e W, gire o vetor com a tabela de rotação da página P6. Uma diagonal que atravessa um canto é conservadora: se qualquer uma das duas arestas ortogonais estiver fechada, a célula diagonal é tratada como bloqueada. Essa regra evita que o jogador atravesse o canto de duas paredes.

A primeira parede, porta fechada ou ator atingível encerra a coluna. Um item ou saída aparece antes da parede se a célula for atingida. A altura gráfica é uma função discreta da profundidade:

| Distância `n` | Parede ou porta | Espaço aberto | Símbolo sugerido |
|---:|---|---|---|
| 1 | faixa de 4 unidades | 4 unidades | `████` |
| 2 | faixa de 3 unidades | 3 unidades | `▓▓▓` |
| 3 | faixa de 2 unidades | 2 unidades | `▒▒` |
| 4–5 | faixa de 1 unidade | 1 unidade | `░` |
| nenhum bloqueio | vazio | vazio | `.` |

O ator substitui a faixa da coluna na mesma profundidade: `G` para sentinela, `M` para inimigo, `*` para item e `E` para saída. O quadro mínimo tem esta forma:

```text
P6 — QUADRO t=6, jogador (6,1), olhando E
             r=-2   r=-1    r=0    r=+1   r=+2
céu            .      .       .      .      .
alvo         ████   ████      G      ▓▓      ░
piso           .      .       .      .      .
HUD       HP 100 | ARM 0 | PISTOLA | MUNIÇÃO 12 | CHAVE AZUL
```

No exemplo, o centro encontra `G` em uma célula adjacente. Os vetores laterais encontram paredes ou profundidades diferentes. O quadro é informativo; a posição e a vida do ator continuam vindo de P2 e P3.

Uma alternativa mais próxima da aparência de um raycaster seria usar sete ou nove vetores e uma tabela de alturas maior. Isso aumenta o custo de cópia e não recupera a geometria contínua do DOOM. Portanto, a proposta usa cinco colunas como contrato de usabilidade, não como alegação de equivalência visual.

### 6. Regras do núcleo jogável

#### Entrada

O jogador escreve exatamente uma ação principal por tick:

| Código | Ação |
|---|---|
| `F` | Avançar uma célula na direção atual |
| `B` | Recuar uma célula |
| `SL` / `SR` | Deslocar uma célula para a esquerda/direita sem virar |
| `L` / `R` | Virar 90 graus |
| `U` | Usar a porta, interruptor ou saída adjacente |
| `A` | Atacar com a arma atual |
| `W` | Esperar |

A ação de papel é intencionalmente mais restrita que o `ticcmd_t` original, que pode combinar movimento, giro e botões [4]. Se o protótipo precisar de mais velocidade, uma edição futura pode aceitar `F+A`, mas isso deve ser uma regra nova e testada, não uma combinação informal.

#### Movimento

O movimento calcula a célula destino. A ação falha se a aresta de saída for `WALL` ou `DOOR(CLOSED)`, se a célula destino estiver fora da grade ou se estiver ocupada por um ator sólido. A ação também falha se o jogador estiver `DEAD`, `WON` ou `LOST`. Não há deslocamento parcial, empurrão ou aceleração. Essa é a redução de `P_TryMove` para uma unidade discreta.

Ao entrar em uma célula, o jogador coleta imediatamente itens presentes. A coleta é registrada antes da ação do inimigo. Uma saída só encerra o jogo se as condições de vitória estiverem satisfeitas.

#### Portas e chaves

`U` procura uma porta ou interruptor na célula adjacente na direção atual. `D1` exige `BLUE`. Se o jogador possuir a chave, `CLOSED` vira `OPEN`; sem a chave, o estado não muda e o log recebe `LOCKED`. Uma porta aberta permanece aberta neste núcleo. Fechamento temporizado pode ser adicionado apenas depois de os testes básicos passarem.

#### Pistola

A pistola tem munição de pente e consome uma unidade por ataque. O ataque percorre a coluna central `r=0` até a distância cinco. Se encontrar primeiro uma parede ou porta fechada, não atinge atores atrás dela. Se encontrar um ator vivo, retira dano e termina. Retire o próximo número da fita d3:

```text
d3 = 1 -> 5 de dano
d3 = 2 -> 10 de dano
d3 = 3 -> 15 de dano
```

A tabela é equivalente em forma ao dano do `P_GunShot` original, que usa `5*(P_Random()%3+1)` [9], mas a fita de papel torna a aleatoriedade auditável. Não se deve afirmar que a sequência da fita reproduz o gerador pseudoaleatório original.

O ator `G` deste cenário é um **sentinela de 20 HP**, usando a vida de `MT_POSSESSED` como referência do código [10]. O ator `M` é um **grunt de 30 HP**, usando a vida de `MT_SHOTGUY` como referência [10]. Os nomes e o comportamento são adaptações. Um ator morto passa a `DEAD`, não bloqueia movimento, não recebe novos ataques e não age.

#### IA mínima

Cada ator possui um modo. `IDLE` não se move até detectar o jogador; `ALERT` tenta aproximar-se; `ATTACK` ataca; `DEAD` é terminal. Para manter o jogo manual, a percepção é cardinal: há linha de visão quando ator e jogador estão na mesma linha ou coluna, todas as arestas intermediárias estão abertas e a distância é no máximo cinco. Uma porta fechada bloqueia a percepção.

A IA do `G` é `SENTINEL`: ele não se desloca e ataca apenas quando o jogador estava adjacente no início do tick, causando 5 de dano e entrando em cooldown 2. Avaliar a adjacência no início evita que um monstro ataque imediatamente depois de o jogador entrar em seu alcance. O movimento do `G` é sempre nulo. O movimento de um eventual `GRUNT` segue a menor distância Manhattan, com desempate na ordem N, E, S, W; se estiver adjacente no início do tick, ataca por 5 de dano e entra em cooldown 2. O movimento de um monstro falha se a célula estiver ocupada ou bloqueada. Essas regras são inferências de projeto e não a IA completa do DOOM.

#### Dano, morte e derrota

O jogador começa com `HP=100`, `ARM=0` e `MUNIÇÃO=12`. O dano do inimigo reduz primeiro armadura, na proporção de 1 ponto de armadura para 1 ponto de dano nesta versão simples, e depois vida. Ao chegar a zero, o jogador fica `LOST`. O modelo original possui armadura, vida espelhada no objeto e estado de morte [8]; a proporção usada aqui é deliberadamente simplificada.

A vitória ocorre quando `phase=PLAY`, o jogador está em `E`, possui `BLUE` e `G` está `DEAD` — ou quando o mapa declara explicitamente que não exige limpeza. A condição precisa estar escrita em P0 para que uma partida possa ser auditada.

### 7. Protocolo de cada tick

O árbitro ou jogador segue sempre esta ordem. Uma linha de P5 deve existir para cada etapa relevante.

1. **Ler o estado anterior.** Copie `S_t` e confirme o checksum anterior.
2. **Registrar a entrada.** Escreva `t`, ação e o índice atual da fita d3.
3. **Validar a ação.** Rejeite códigos inválidos, ações durante `WON/LOST` e ataques sem munição.
4. **Aplicar a ação do jogador.** Resolva virar, mover, usar ou atacar. Atualize posição, porta, munição, item e vida do alvo.
5. **Resolver coleta e saída.** Colete itens da célula nova e verifique se a saída pode terminar o jogo.
6. **Atualizar atores.** Percorra IDs em ordem crescente. Para cada ator vivo, reduza cooldown; se puder atacar, ataque; caso contrário, execute a regra de movimento. Um ator morto por um ataque do jogador não age neste mesmo tick.
7. **Resolver ambiente.** Aplique dano de hazard, temporizadores e transições definidas em P4. O mapa de teste não tem hazard.
8. **Resolver terminalidade.** Marque `WON` ou `LOST`. Se ambos parecerem ocorrer no mesmo tick, a derrota prevalece, pois a regra de dano de ator vem antes da vitória; a situação deve ser registrada como conflito de cenário.
9. **Incrementar o tick.** Faça `tick := tick + 1` e `rng_index` avançar somente quando uma regra consumiu a fita.
10. **Calcular checksum e renderizar.** Escreva `CHK`, atualize P2/P3 e desenhe P6 a partir de `S_(t+1)`.

A ordem preserva a ideia geral observada em `P_Ticker` — jogador, thinkers, especiais, respawn e tempo [5] — mas não afirma reproduzir todos os subsistemas. O protocolo é a parte mais importante da arquitetura: sem ele, dois jogadores podem interpretar o mesmo mapa de maneiras diferentes.

### 8. Exemplo mínimo executado

Use a fita d3 começando por `2, 1, 3, ...`. Estado inicial: `t=0`, jogador `(1,1)` olhando E, `HP=100`, `MUNIÇÃO=12`, nenhuma chave; `D1=CLOSED`; `G=(7,1), HP=20, ID=01`.

| Tick | Entrada | Resultado do jogador | Resultado dos atores | Estado relevante após o tick |
|---:|---|---|---|---|
| 0 | `F` | Vai de `(1,1)` para `(2,1)` e coleta `BLUE` | Nenhuma ação ofensiva | chave azul; munição 12 |
| 1 | `F` | Vai para `(3,1)` | Nenhuma ação ofensiva | diante da porta D1 |
| 2 | `U` | Abre `D1` porque possui `BLUE` | Nenhuma ação ofensiva | `D1=OPEN` |
| 3 | `F` | Entra em `(4,1)` | Nenhuma ação ofensiva | lado direito do mapa |
| 4 | `F` | Vai para `(5,1)` | `G` continua sentinela | `G` ainda com 20 HP |
| 5 | `F` | Vai para `(6,1)` | `G` estava a duas células no início do tick; não ataca | quadro central mostra `G` |
| 6 | `A` | Usa munição; fita=2; causa 10 | `G` permanece vivo com 10 HP e ataca por 5; cooldown 2 | munição 11; `G=10`; `HP=95` |
| 7 | `A` | Usa munição; fita=1; causa 5 | `G=5`; cooldown do G cai para 1 e ele não ataca | munição 10; `G=5`; `HP=95` |
| 8 | `A` | Usa munição; fita=3; causa 15 | `G` passa a `DEAD` antes de poder agir | munição 9; `G=DEAD`; `HP=95` |
| 9 | `F` | Vai para `(6,2)` | Nenhuma ação ofensiva | corredor inferior direito |
| 10 | `F` | Vai para `(6,3)` | Nenhuma ação ofensiva | ao lado de E |
| 11 | `F` | Vai para `(7,3)` | Nenhuma ação ofensiva | entra na célula E |
| 12 | `U` | Verifica saída, chave e objetivos | Nenhuma ação ofensiva | `phase=WON` |

Como o jogador ainda está olhando E em `(6,3)`, a entrada correta para a saída em `(7,3)` é `F`; o protocolo define `SR` como strafe relativo, mas ele não é necessário nesta sequência. A tabela consolidada é:

| Tick | Entrada | Resultado |
|---:|---|---|
| 9 | `F` | `(6,2)` |
| 10 | `F` | `(6,3)` |
| 11 | `F` | `(7,3)=E` |
| 12 | `U` | `WON` |

O primeiro quadro frontal após `t=6` pode ser desenhado como:

```text
             r=-2   r=-1    r=0    r=+1   r=+2
alvo         ████   ████      G      ▓▓      ░
```

A versão final do log deve usar apenas a tabela corrigida. A presença da correção no relatório é intencional: ela ilustra por que a execução precisa de coordenadas, definição de strafe e testes de aceitação, em vez de depender de linguagem informal.

### 9. Plano de validação

A validação deve começar pelo núcleo determinístico, antes de acrescentar armas, pisos especiais ou mapas maiores.

| ID | Teste | Preparação | Resultado esperado |
|---|---|---|---|
| V1 | Limites da grade | Tentar `F` contra a parede externa | Posição não muda; nenhum ator age fora da ordem normal; checksum muda apenas pelo tick |
| V2 | Parede interna | Jogador à esquerda de `x=4`, porta fechada | `F` falha; `D1` continua `CLOSED` |
| V3 | Chave e porta | Coletar K e executar `U` | Item vira `COLLECTED`; porta vira `OPEN`; sem chave, `LOCKED` |
| V4 | Linha de tiro bloqueada | Ator atrás de parede ou porta fechada | Ataque consome munição, mas não altera HP do ator |
| V5 | Linha de tiro aberta | G no centro, distância 1–5 | Primeiro ator vivo recebe o dano e nenhum ator atrás recebe dano |
| V6 | Fita de dano | Três ataques com d3 `1,2,3` | Danos exatos 5, 10 e 15; `rng_index` avança três vezes |
| V7 | Morte | Ator com HP 5, ataque com d3=1 | HP=0, estado `DEAD`, não bloqueia célula e não age no mesmo tick |
| V8 | Colisão de atores | Grunt tenta entrar em célula ocupada | Movimento falha; não há sobreposição ao final do tick |
| V9 | Ordem | Inimigo que morreria no ataque do jogador | Inimigo não realiza ação posterior nesse mesmo tick |
| V10 | Derrota | Jogador com HP 5 recebe 5 de dano | `phase=LOST`; entradas seguintes são rejeitadas |
| V11 | Vitória | Limpar G, possuir chave e entrar em E | `phase=WON` somente após `U` na saída, conforme P0 |
| V12 | Reprodutibilidade | Reexecutar a sequência do exemplo com a mesma fita | Cada posição, HP, porta, estado e checksum deve coincidir |
| V13 | Renderer | Avaliar cada uma das cinco colunas em posições conhecidas | Cada coluna identifica a primeira obstrução correta; diagonal de canto não atravessa parede |
| V14 | Integridade do mapa | Verificar toda aresta em ambos os lados | `OPEN` é simétrico; uma porta tem um único ID; toda célula transitável está dentro dos limites |

Os testes V1–V12 são testes de regras. V13 é teste da apresentação. V14 é teste de dados. Um cenário só é considerado pronto quando a sequência de entrada, a fita e o estado final estão anexados à P7. Para uma campanha, cada mapa deve vir com pelo menos um traço dourado (“golden trace”) contendo a entrada e os estados esperados em todos os ticks.

Critérios práticos de aceitação, propostos e não derivados do DOOM original, são: um jogador deve conseguir resolver dez ticks sem consultar o mapa-mestre; um árbitro deve conseguir localizar a primeira divergência comparando P2, P3 e P5; e dois jogadores com o mesmo estado inicial e a mesma fita devem alcançar o mesmo checksum final. Se qualquer um desses critérios falhar, reduza o número de campos ou de vetores antes de aumentar o conteúdo.

## limites

### Limites de fidelidade

PaperDOOM-1 não executa arquivos WAD, não percorre a árvore BSP original, não desenha texturas por colunas, não calcula planos de piso e teto, não implementa alturas contínuas, não suporta salas sobre salas, não simula a física de momentum e atrito, não reproduz os `thinkers` ou estados de animação completos, não reproduz todas as armas, monstros, pickups, segredos, scripts, sons, multiplayer ou demos. O mapa de nove por seis é um formato novo. A existência dos lumps, dos setores e do BSP é uma evidência para entender o problema, não uma promessa de compatibilidade [2] [10] [11].

### Limites de execução manual

O renderer de cinco vetores pode mostrar uma parede ou ator em uma coluna que não corresponde a uma projeção perspectiva contínua. A IA cardinal pode parecer previsível. A regra conservadora de cantos pode bloquear uma célula que uma geometria contínua permitiria atravessar. A fita d3 reproduz a distribuição escolhida de dano, mas não o estado interno do gerador aleatório do código original. O checksum não prova a correção do estado; apenas ajuda a encontrar divergências.

Um jogo maior exige mais folhas e mais disciplina. O custo cresce com o número de atores, portas e efeitos temporizados. A primeira versão deve limitar deliberadamente o conteúdo. Só depois de os testes passarem vale acrescentar uma segunda arma, uma segunda chave ou um inimigo com projétil.

### Limites de segurança e licenciamento

A proposta usa apenas a ideia de um jogo de tiro em primeira pessoa e referências técnicas ao código-fonte. Não pressupõe copiar sprites, sons, texturas ou mapas comerciais. Para uma publicação, use arte original e confirme a licença e os termos dos materiais que forem efetivamente distribuídos. O repositório oficial declara GPL 2.0 para o código liberado [1], mas isso não transforma automaticamente todos os dados audiovisuais de qualquer versão de DOOM em material livre.

### Evolução recomendada

A ordem de extensão mais segura é: (1) mapa maior mantendo células ortogonais; (2) segundo tipo de porta e chave; (3) shotgun com sete pellets usando uma fita separada; (4) inimigo móvel com tabela de caminho; (5) hazard e elevador em estados discretos; (6) renderer de sete vetores; e somente então (7) tentativa de importar uma geometria externa. Em cada passo, preserve o protocolo de tick e adicione testes dourados. Não tente começar com a totalidade do WAD ou com uma emulação manual do BSP.

## referências

[1]: https://github.com/id-Software/DOOM "id Software/DOOM: DOOM Open Source Release"
[2]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/doomdata.h "doomdata.h — estruturas de dados dos mapas DOOM"
[3]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/doomdef.h "doomdef.h — constantes e definições internas do DOOM"
[4]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/d_ticcmd.h "d_ticcmd.h — comando de entrada por tic"
[5]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/p_tick.c "p_tick.c — thinkers e protocolo de P_Ticker"
[6]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/p_user.c "p_user.c — movimento e pensamento do jogador"
[7]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/p_map.c "p_map.c — colisão, linha de ataque e interação com linhas"
[8]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/p_inter.c "p_inter.c — coleta, dano e morte de atores"
[9]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/p_pspr.c "p_pspr.c — estados de armas e ataques de pistola/shotgun"
[10]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/r_bsp.c "r_bsp.c — travessia BSP, clipping e subsectors"
[11]: https://soulsphere.org/apocrypha/doom-engine/ "The Doom rendering engine"
[12]: https://edge.sourceforge.net/edit_guide/doom_specs.htm "Unofficial Doom Specs - EDGE"
[13]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/info.c "info.c — estados e parâmetros de atores do DOOM"
[14]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/g_game.c "g_game.c — construção de comandos e processamento do jogo"
[15]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/p_mobj.h "p_mobj.h — estrutura de objetos móveis"
[16]: https://raw.githubusercontent.com/id-Software/DOOM/master/linuxdoom-1.10/p_mobj.c "p_mobj.c — movimento e ciclo de estados de objetos"

> **Resumo de proveniência:** as fontes [1]–[10] são arquivos e páginas do código-fonte oficial liberado pela id Software; [11] é uma descrição técnica independente do renderer; [12] é uma especificação técnica independente do formato de níveis. As regras de PaperDOOM-1, exceto quando explicitamente rotuladas como referência ou equivalência de forma, são propostas de design e não fatos sobre o DOOM original.

> **Resultado:** a arquitetura concreta mais defensável é uma máquina de estados discreta com mapa 2D por células e arestas, protocolo de tick escrito, renderer de cinco vetores e validação por traços dourados. Isso entrega um demake jogável e auditável; não entrega DOOM completo em papel.
