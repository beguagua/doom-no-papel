# Computação em papel: métodos executáveis, memória, lógica, autômatos e limites

## Escopo e critério de inclusão

Este relatório investiga computação que pode ser **executada, observada ou armazenada em papel, cartão ou dobradura**, distinguindo três casos que muitas vezes são chamados pelo mesmo nome:

1. **Computação manual simbólica:** uma pessoa atua como unidade de controle e aritmética, movimentando marcadores e escrevendo estados em uma folha ou dispositivo de cartão.
2. **Computação física no papel:** a geometria, a dobra, a perfuração, a posição de abas ou a deformação mecânica implementa estados e regras.
3. **Papel como substrato de eletrônica ou interface:** papel conduz sinais, sustenta componentes ou é lido por uma câmera, enquanto a lógica principal está em componentes eletrônicos ou em um computador externo.

A primeira e a segunda categorias são computadores de papel no sentido mais forte. A terceira é relevante para o projeto, mas não deve ser apresentada como computação feita somente pelo papel.

## Conclusão

Há métodos reais e reproduzíveis para executar computação em papel, mas eles têm naturezas diferentes.

O método mais simples e mais confiável é um **interpretador manual de máquina de registradores**. Uma folha contém o programa, os registradores e o estado; o lápis ou marcador representa o contador de programa. Em cada ciclo, o operador lê uma instrução, altera um valor, testa uma condição e move o marcador. O projeto Paper Computer documenta instruções como `CLR`, `INC`, `DEC`, `CPY`, `JZ` e `JE`, além de uma máquina de reescrita, aritmética desenhada e uma memória de 16 células feita com um mecanismo de papel dobrado [1]. O WDR/Know-how Computer reduz a ideia a cinco comandos e usa uma folha, caneta e, na versão mais simples, palitos de fósforo; a fonte de projeto afirma que o conjunto é Turing-completo [2]. Essa afirmação de completude deve ser entendida como uma propriedade do modelo de instruções, não como evidência de velocidade ou de uma execução automática.

O **CARDIAC**, criado pela Bell Telephone Laboratories em 1968, é a demonstração histórica mais completa. É um computador de papelão com CPU, memória, cartões de entrada e saída, slides e uma joaninha que marca o contador de programa. Possui 100 posições de memória, palavras decimais de três dígitos e dez opcodes para entrada, carga, soma, teste, deslocamento, saída, armazenamento, subtração, salto e parada [3]. O manual original deixa explícito que o operador é a “fonte de energia”: executa a aritmética, movimenta os slides e transfere dados entre as seções [4]. Portanto, o CARDIAC é uma máquina executável manualmente, não apenas um diagrama.

A **lógica em papel por dobradura** também é demonstrada tecnicamente. Os padrões de Inna Zakharevich fornecem folhas imprimíveis para portas OR, AND, NOR, NAND e NOT [5]. O artigo de Thomas C. Hull e Inna Zakharevich formaliza dobras opcionais como fios booleanos e constrói gadgets de lógica capazes de simular a regra 110 de autômato celular. O resultado é uma prova de que, no modelo matemático adotado, a dobradura plana tessellante é logspace-completa para P e, portanto, Turing-completa [6]. Isso é uma afirmação de computabilidade e complexidade sobre padrões de dobras, não uma medição de um computador de papel pequeno executando instruções em tempo humano.

Existe ainda uma forma física de **memória sequencial**. O trabalho “Origami mechanologic” demonstra, experimentalmente, uma unidade mecânica de um bit baseada em um origami waterbomb, capaz de escrever, apagar e reescrever o bit em resposta a um sinal variável. O mesmo trabalho acopla unidades para implementar AND, OR, maioria de três entradas e transmissão de sinais [7]. É o exemplo mais próximo de um flip-flop mecânico em papel dobrado, embora o dispositivo experimental use filme de polipropileno de 40 µm, e não uma folha comum de caderno.

O papel também funciona como **memória passiva**. Cartões perfurados codificam dados e programas pela presença ou ausência de furos. O Smithsonian registra que, após a Segunda Guerra Mundial, cartões passaram a ser usados para inserir tanto dados quanto programas em computadores [8]. A IBM descreve o cartão de 80 colunas e a convenção em que uma linha de programa ocupava um cartão [9]. O Computer History Museum registra um baralho de 62.500 cartões, equivalente a 5 MB, usado para armazenar o programa de controle da rede SAGE [10]. O cartão é memória e meio de entrada; sem um leitor e uma unidade de processamento, ele não executa a computação sozinho.

Por outro lado, **um circuito desenhado com lápis não foi verificado nas fontes primárias consultadas como uma porta lógica digital completa feita somente de grafite**. O Science Museum demonstra que um traço de lápis conduz corrente suficiente para acender um LED e que seu brilho varia com o comprimento do traço e a posição do contato [11]. O artigo técnico de Shekhawat mostra que grafite misturado com argila pode formar resistores e capacitores em papel e até ser usado para estimar eletricamente π [12]. Esses resultados sustentam o papel do grafite como condutor resistivo, sensor ou elemento analógico. Eles não sustentam, por si só, um AND, OR, NOT ou flip-flop digital robusto sem componentes adicionais, como bateria, LED, chaves, diodos, transistores ou uma ação manual.

A recomendação para o projeto é, portanto, separar explicitamente os níveis. Para uma demonstração **paper-only**, usar uma máquina manual de registradores ou o CARDIAC. Para demonstrar **lógica física**, usar padrões de origami e um pequeno conjunto de portas, com entradas e saídas visíveis. Para demonstrar **memória**, usar uma célula mecânica bistável ou uma grade de marcas/cartões. Para uma experiência híbrida de papel e eletrônica, usar cobre, grafite ou marcadores com componentes e declarar que o papel é substrato ou interface. Não misturar esses casos em uma única alegação de “computador feito só de papel”.

## Evidências

### 1. Máquina de registradores em uma folha

O Paper Computer de XXIIVV contém simultaneamente o programa e o estado da execução na mesma folha. O lápis representa o contador de programa. Cada instrução atua sobre registradores ou sobre a posição do contador:

| Instrução | Operação verificada | Estado alterado |
|---|---|---|
| `CLR(r)` | zera o registrador `r` | conteúdo de `r` |
| `INC(r)` | incrementa `r` | conteúdo de `r` |
| `DEC(r)` | decrementa `r` | conteúdo de `r` |
| `CPY(a,b)` | copia `a` para `b` | conteúdo de `b` |
| `JZ(r,i)` | salta para `i` se `r = 0` | contador de programa |
| `JE(a,b,i)` | salta se `a = b` | contador de programa |

O estado observável pode ser modelado como

```text
Estado = (PC, R1, R2, ..., Rn, marcas, saída)
```

Uma etapa consiste em ler a instrução na posição `PC`, aplicar sua regra, atualizar o estado e avançar ou saltar. O programa termina ao encontrar uma instrução vazia ou uma parada. Essa representação é reproduzível com papel quadriculado, lápis, uma tabela de registradores e uma lista de instruções.

A mesma página apresenta uma **máquina de reescrita**: há um conjunto ordenado de regras `LHS -> RHS` e um multiconjunto inicial de símbolos. Em cada etapa, procura-se a primeira regra cujo lado esquerdo esteja presente, substitui-se esse lado pelo direito e reinicia-se a busca. Essa variante desloca a memória dos registradores para marcas e símbolos escritos na folha. Ela é útil para um projeto que queira mostrar que “memória” não precisa ser uma matriz de bits: pode ser uma configuração textual ou geométrica.

### 2. WDR/Know-how Computer e instruções manuais

A documentação do WDR descreve cinco operações: `END`, `SKP(r)`, `JMP(z)`, `INC(r)` e `DEC(r)` [2]. `SKP` testa se um registrador é zero e altera o avanço do contador de programa. `JMP` escolhe diretamente a linha seguinte. O projeto também mostra uma codificação de oito bits com três bits de operação e cinco bits de valor, permitindo 32 linhas endereçáveis nessa representação.

O ponto técnico importante é a distinção entre **programa**, **estado** e **operador**. O programa está escrito na folha. Os registradores podem ser números escritos, marcas, palitos ou peças móveis. O operador realiza a transição. Nada no mecanismo básico fornece um relógio automático, um sinal elétrico ou uma unidade aritmética; a taxa de execução é a taxa de leitura, escrita, comparação e movimentação humana.

### 3. CARDIAC: arquitetura de papelão, memória e ISA

A documentação técnica da Drexel descreve o CARDIAC como um kit de papelão composto por uma seção de CPU e uma seção de memória. Cinco slides representam a entrada, o sinal do acumulador e os três dígitos da instrução. A memória tem um slide de saída e uma joaninha que marca a posição atual do programa [3]. O manual original é reproduzível a partir de scans e arquivos de texto no Internet Archive [4]. Uma reconstrução moderna fornece arte vetorial, arquivos para corte e instruções para construir o aparelho com três folhas de A4, impressora e tesoura ou estilete [13].

A arquitetura verificada é:

| Recurso | Limite ou comportamento |
|---|---|
| Memória | 100 células, endereços `00` a `99` |
| Palavra na memória | número decimal assinado de até três dígitos |
| Acumulador | aritmética manual, com um dígito extra para overflow intermediário |
| Entrada | cartões, cada um carregando um número assinado de três dígitos |
| Saída | cartões de saída, um número assinado de três dígitos por operação |
| Instruções | 10 opcodes, cada instrução com três dígitos |
| Controle | contador de programa, saltos condicionais e incondicionais |
| Parada | `HRS`, que interrompe e reposiciona o contador |

A ISA é:

| Opcode | Nome | Ação |
|---:|---|---|
| 0 | `INP` | lê um cartão e grava em uma célula |
| 1 | `CLA` | carrega uma célula no acumulador |
| 2 | `ADD` | soma uma célula ao acumulador |
| 3 | `TAC` | salta se o acumulador for negativo |
| 4 | `SFT` | desloca dígitos à esquerda e à direita |
| 5 | `OUT` | escreve uma célula em um cartão de saída |
| 6 | `STO` | grava o acumulador em uma célula |
| 7 | `SUB` | subtrai uma célula do acumulador |
| 8 | `JMP` | salta e grava uma informação de retorno na célula 99 |
| 9 | `HRS` | para e reposiciona o programa |

A fonte primária do manual enfatiza que a memória é escrita e lida a lápis, e que o operador executa a aritmética. Isso é relevante para a definição de “executável”: o objeto não simula apenas a aparência de uma CPU; ele define uma transição precisa que uma pessoa pode aplicar ciclo a ciclo. O custo é que cada passo exige leitura, busca da célula, movimentação de slides, cálculo e atualização visual.

### 4. Dobragem como porta lógica e autômato celular

As folhas de padrões de Zakharevich contêm quatro cópias experimentais de cada porta OR, AND, NOR, NAND e NOT [5]. O valor lógico é codificado pela configuração das dobras. A página do projeto Paper Computer também aponta esses padrões como uma implementação funcional de portas em origami [1].

O artigo “Flat origami is Turing Complete” torna a alegação mais rigorosa. O modelo usa uma **trinca de dobras paralelas** como fio: a dobra central é obrigatória e uma das duas dobras laterais opcionais codifica o valor booleano. O artigo constrói gadgets de NOR e NAND, além de AND, OR, NOT, interseção, twist e eater. Esses gadgets são combinados para simular Rule 110, um autômato celular unidimensional cujo próximo estado depende de três células vizinhas [6].

A construção é uma ponte direta entre papel, lógica e autômatos:

```text
estado da célula na linha t-1
        ↓
wire de entrada A ─┐
wire de entrada B ─┼─> gadgets NOR/NAND ─> wire de saída
wire de entrada C ─┘
        ↓
estado da célula na linha t
```

A prova não significa que qualquer folha dobrada execute qualquer programa. Ela depende de padrões planejados, dobras opcionais, regras de planicidade e, na construção tessellante, de um modelo de grade que pode ser arbitrariamente grande. O próprio artigo afirma que as dobras fornecidas devem ser verificadas diretamente por dobragem e que a prova se concentra em impedir outras configurações de dobragem [6]. Portanto, é uma demonstração formal e parcialmente reproduzível, não um benchmark de tempo de execução de um objeto pequeno.

### 5. Memória mecânica, bits e lógica sequencial

Um flip-flop eletrônico é uma memória binária com dois estados estáveis. A documentação RealDigital explica que latches e flip-flops memorizam um sinal e o disponibilizam depois; um D-latch acompanha a entrada enquanto o controle está ativo, enquanto um D-flip-flop amostra a entrada na borda de subida [14]. A mesma documentação explica que a realimentação de portas NAND ou NOR cria dois estados estáveis.

No papel dobrado, a analogia mais forte não é um desenho de portas, mas uma **estrutura bistável**. Em “Origami mechanologic”, um waterbomb de origami funciona como armazenamento mecânico de um bit: a unidade muda entre duas configurações estáveis, pode ser escrita, apagada e reescrita, e pode ser acoplada a outras unidades para formar portas AND, OR e maioria [7]. O artigo também mostra transmissão de sinais entre unidades.

Há duas diferenças importantes em relação a um flip-flop eletrônico. Primeiro, o estado mecânico é uma configuração geométrica, não uma tensão lógica. Segundo, o dispositivo necessita de força, deslocamento ou sinal ambiental para mudar de estado. A mudança pode ser deliberadamente lenta e depender de atrito, rigidez, alinhamento e fadiga do material. Ainda assim, é uma demonstração real de memória sequencial mecânica, e não apenas uma tabela-verdade desenhada.

### 6. Lápis, grafite e circuitos elétricos em papel

O Science Museum apresenta um experimento no qual uma linha desenhada com lápis conduz corrente suficiente para acender um LED. A composição é grafite misturado com argila; lápis macios possuem maior proporção de grafite; traços mais longos oferecem maior resistência; e mudar o ponto de contato altera o brilho [11].

O artigo de Shekhawat, publicado em *The Physics Teacher*, usa lápis de diferentes graus, papel A4, garras jacaré e um medidor LCR. O trabalho demonstra o uso do traço de grafite como elemento resistivo e capacitivo e inclui uma estimativa elétrica de π [12]. Esses materiais são baratos e reproduzíveis.

A conclusão técnica é restritiva: um traço de grafite é um **condutor resistivo variável**, não uma porta lógica ideal. Para obter lógica digital, é necessário um mecanismo que tenha ganho, limiar, isolamento e restauração do nível lógico. Um LED e uma bateria fornecem uma saída visual, mas não restauram automaticamente um nível para alimentar várias portas. Um contato manual, uma dobra ou uma aba pode fornecer uma chave; componentes ativos ou mecânicos adicionais podem então formar lógica. Não foi encontrada, nas fontes primárias e técnicas consultadas, uma demonstração confiável de AND/OR/NOT e memória sequencial feita somente por traços de lápis, sem componentes adicionais.

Os guias do Exploratorium e da SparkFun confirmam a arquitetura típica de circuitos em papel: fita de cobre ou tinta condutiva, LED, bateria tipo moeda e uma chave que pode ser uma aba de alumínio ou uma dobra [15] [16]. A SparkFun salienta que conexões por fita, tinta, adesivo condutivo, linha ou solda têm confiabilidades diferentes e que dobras e tinta podem falhar sob movimento repetido [16]. Assim, papel pode ser um excelente substrato de circuito, mas o comportamento lógico depende dos componentes e das conexões.

### 7. Cartões perfurados como memória, instrução e fluxo serial

O cartão perfurado fornece um caso histórico em que o papel é efetivamente uma memória codificada por estados discretos. No sistema de Hollerith, furos em posições específicas representavam dados. O Smithsonian registra que cartões perfurados passaram a ser o meio preferido para entrada de programas e dados em computadores eletrônicos do pós-guerra [8].

A IBM descreve cartões com 80 colunas e 10 linhas, e observa que cada cartão de programa correspondia aproximadamente a uma linha de código [9]. O Computer History Museum documenta o uso de baralhos de cartões para armazenar programas e observa que cartões e fita de papel dominaram o processamento de dados antes de memórias magnéticas de maior capacidade [10].

Nesse modelo, o estado físico do cartão é binário por posição: furo ou ausência de furo. O estado global é uma sequência ordenada de cartões. A memória é persistente enquanto o papel não for danificado, mas o acesso é predominantemente **serial**: para ler o cartão seguinte, é preciso avançar no baralho. Um mecanismo de leitor converte essa configuração em sinais e então executa a lógica. A memória em papel é, portanto, real, durável e regravável por perfuração, mas não é memória de acesso aleatório sem uma máquina auxiliar.

### 8. Papel como interface de visão computacional: caso híbrido

O Paper Playground é um projeto recente que usa papel e cartão como interfaces tangíveis, mas faz a computação com câmera, navegador/computador e micro:bit. A plataforma detecta sequências de pontos coloridos nas bordas dos cartões, rastreia marcadores e executa programas associados aos papéis. Os autores demonstram uma estação musical, um jogo espacial e monitoramento de plantas [17].

A fonte é particularmente útil para estabelecer o limite da categoria. O papel simplifica a criação de grades, sliders, sensores de sopro e mecanismos de estiramento, mas a câmera faz a detecção e o micro:bit ou computador produz a resposta. O artigo relata oclusão por mãos e cabeças, necessidade de calibração da iluminação e limite de quatro marcadores únicos. Portanto, o sistema é uma interface computacional em papel, não uma máquina paper-only.

## Implicações para o projeto

### Arquitetura recomendada

Para um protótipo cujo requisito seja “executar sem eletrônica”, a opção com maior relação entre confiabilidade, clareza e esforço é uma máquina de registradores inspirada no Paper Computer e no CARDIAC. A implementação mínima precisa de uma folha de programa, uma tabela de registradores, um marcador de `PC`, uma regra de parada e uma convenção de atualização. A implementação didática mais completa deve acrescentar memória endereçável, entrada, saída, salto condicional e pelo menos uma operação aritmética.

Uma arquitetura recomendada para a primeira versão é:

| Módulo | Implementação em papel | Estado que deve ser visível |
|---|---|---|
| Controle | seta, clipe ou lápis sobre a linha atual | `PC` |
| Memória | tabela de 16 a 100 células | conteúdo por endereço |
| Acumulador | caixa separada com sinal e valor | valor atual |
| Instrução | cartões ou linhas numeradas | opcode e operando |
| Entrada | cartões com números ou símbolos | fila de entrada |
| Saída | cartões ou uma área de resultados | sequência produzida |
| Parada | `HALT`/`HRS` ou célula vazia | condição terminal |
| Auditoria | tabela de rastreamento | histórico de cada ciclo |

Para manter a execução verificável, cada ciclo deve registrar `PC` anterior, instrução, memória lida, valor do acumulador, decisão de salto, memória escrita, saída e `PC` seguinte. Isso permite comparar a execução manual com um emulador independente, sem transformar o emulador no mecanismo principal.

### Progressão experimental

A progressão mais segura é começar com um contador, depois implementar soma por repetição, um teste condicional e uma saída. Em seguida, adicionar subrotina, memória indireta ou uma máquina de reescrita. O CARDIAC fornece exemplos históricos de loops, multiplicação, subrotinas, bootstrap e o jogo NIM [3] [4].

Para a parte de lógica, fabricar primeiro uma única porta NAND ou NOR de origami a partir dos padrões imprimíveis. Marcar as duas entradas e a saída com convenções inequívocas, testar as quatro combinações e fotografar cada configuração. Só depois combinar portas em um somador de um bit ou em uma célula de autômato celular.

Para a memória, comparar três mecanismos:

| Mecanismo | Vantagem | Risco ou custo |
|---|---|---|
| marca escrita a lápis | barato, arbitrário e persistente | execução lenta e sujeita a erro de cópia |
| aba/slider/cartão | estado visual e reversível | desgaste, folga e ambiguidade de posição |
| dobra bistável | memória física sem leitura textual | exige geometria, força e material adequados |

A parte de grafite deve ser tratada como experimento elétrico separado. Medir resistência em função de comprimento, largura, grau do lápis e pressão do contato. Em seguida, adicionar uma chave ou componente ativo se a meta for lógica. Não declarar que o grafite implementa sozinho uma porta digital sem medir níveis lógicos, fan-out, repetibilidade e comportamento sob carga.

### Limite de estado e escolha do formato

Para uma folha finita, o estado observável é finito. Se há `N` células, cada uma com `K` valores, `R` registradores com `V` valores e um contador com `P` posições, o número máximo de configurações distintas, ignorando detalhes de escrita, é aproximadamente:

```text
P × K^N × V^R
```

Essa expressão não é uma medição do CARDIAC; é uma forma de dimensionar o protótipo. A memória pode crescer anexando folhas ou cartões, mas o tempo de acesso e a chance de erro também crescem. Se o operador puder anexar papel indefinidamente, uma máquina manual pode simular uma fita não limitada; em um artefato físico finito, há apenas um prefixo finito dessa fita.

## Limites

### Limites verificados nas fontes

O CARDIAC tem 100 células e palavras de três dígitos [3] [4]. Ele não possui execução automática: o operador move slides e faz a aritmética [4]. O WDR tem cinco comandos no projeto consultado e usa um modelo deliberadamente pequeno [2]. O Paper Computer em uma folha possui a memória e o programa escritos no mesmo suporte [1].

As portas de origami e a simulação de Rule 110 dependem de padrões de dobras bem especificados e de um modelo de planicidade [5] [6]. O artigo de Hull e Zakharevich não demonstra que a fabricação comum, a espessura, a deformação ou a fadiga de uma folha produzam automaticamente a mesma computação em escala arbitrária.

A memória do trabalho de Treml et al. é mecânica e experimental, mas usa waterbomb em filme de polipropileno e parâmetros estruturais específicos [7]. Ela não deve ser tratada como evidência de que qualquer folha de papel sulfite seja um flip-flop durável.

Grafite conduz, mas é resistivo, dependente da composição do lápis e sensível ao comprimento e ao ponto de contato [11] [12]. Circuitos de papel com cobre, tinta ou fita também dependem da qualidade de conexão e podem falhar com dobra ou movimento [15] [16].

O Paper Playground exige câmera, computador e micro:bit, além de calibração e marcadores; o artigo relata oclusão, iluminação e limite de quatro marcadores [17]. Ele é uma plataforma híbrida, não uma solução paper-only.

### Inferências de engenharia

A velocidade de um computador manual é dominada pelo operador. Não foi encontrada uma taxa universal de instruções por minuto para CARDIAC, WDR ou Paper Computer; qualquer número apresentado como benchmark seria uma nova medição, não um fato das fontes. Para um protótipo, o tempo de execução deve ser medido separando leitura da instrução, busca da memória, aritmética, movimentação do marcador e registro do traço.

O tempo de uma máquina manual cresce aproximadamente com o número de transições executadas e com o custo físico de localizar e atualizar o estado. Loops curtos podem ser rápidos; saltos longos, tabelas grandes e cópia de dados aumentam o custo humano. Uma máquina pode não terminar se o programa entra em loop, mesmo que cada transição isolada seja bem definida.

A completude de Turing não implica capacidade prática ilimitada. Ela significa que, sob as convenções do modelo, a família de dispositivos pode representar computações arbitrárias com recursos que crescem. Em papel finito, o tamanho, a precisão da dobra, a fadiga do material, a legibilidade e a memória disponível impõem limites concretos.

Um flip-flop exige dois estados distinguíveis e uma regra de atualização. Uma marca apagável ou um slider pode representar esses estados, mas não fornece automaticamente temporização, isolamento ou restauração de sinal. Para reivindicar “flip-flop de papel”, o projeto deve especificar a entrada de escrita, a condição de retenção, a saída e o comportamento quando duas entradas chegam simultaneamente.

## Referências

[1]: https://wiki.xxiivv.com/site/paper_computer.html "Paper Computer — XXIIVV"

[2]: https://wiki.xxiivv.com/site/wdr_computer.html "WDR paper computer — XXIIVV"

[3]: https://www.cs.drexel.edu/~bls96/museum/cardiac.html "CARDIAC — Department of Computer Science, Drexel University"

[4]: https://archive.org/details/CardiacCardboardIllustrativeAidToComputation "CardIAC Cardboard Illustrative Aid to Computation — Bell Telephone Laboratories manual archive"

[5]: https://pi.math.cornell.edu/~zakh/crease-patterns.pdf "Origami logic gadgets — crease patterns, Inna Zakharevich"

[6]: https://arxiv.org/html/2309.07932v4 "Flat origami is Turing Complete — Thomas C. Hull and Inna Zakharevich"

[7]: https://www.pnas.org/doi/10.1073/pnas.1805122115 "Origami mechanologic — Benjamin Treml et al., Proceedings of the National Academy of Sciences"

[8]: https://www.si.edu/spotlight/punch-cards/punch-cards-data-processing "Punch Cards for Data Processing — Smithsonian Institution"

[9]: https://www.ibm.com/history/punched-card "The IBM punched card — IBM History"

[10]: https://www.computerhistory.org/revolution/memory-storage/8/326 "Punched Cards & Paper Tape — Computer History Museum"

[11]: https://www.sciencemuseumgroup.org.uk/learning/resources/graphite-circuits "Graphite Circuits — Science Museum Group"

[12]: https://pubs.aip.org/aapt/pte/article/61/2/154/2866861/Graphite-paper-circuit-elements-Resistor-capacitor "Graphite-paper circuit elements: Resistor, capacitor, and π value estimation — Vibhooti Shekhawat"

[13]: https://vonkonow.com/cardiac-recreating-an-educational-paper-computer-from-1968/ "CARDIAC — Recreating an educational paper computer from 1968 — von Konow"

[14]: https://realdigital.org/doc/74cd33aeb02d913233a0254f76857207 "Project 7: Flip-flops and Latches — Real Digital"

[15]: https://www.exploratorium.edu/tinkering/projects/paper-circuits "Paper Circuits — Exploratorium Tinkering"

[16]: https://learn.sparkfun.com/tutorials/the-great-big-guide-to-paper-circuits/all "The Great Big Guide to Paper Circuits — SparkFun Learn"

[17]: https://dl.acm.org/doi/10.1145/3689050.3705981 "Physical Computing with Paper Playground: Exploring a Multimodal Platform — Krithik Ranjan et al."

[18]: https://cs.stanford.edu/people/eroberts/courses/soco/projects/2004-05/automata-theory/basics.html "Basics of Automata Theory — Stanford Computer Science"

[19]: https://faculty.fairfield.edu/cstaecker/machines/instructo.html "The Instructo Paper Computer — Fairfield University"

## Síntese final de fatos e inferências

**Fatos verificados:** (a) o Paper Computer implementa uma máquina de registradores manual com programa e estado em papel [1]; (b) o CARDIAC tem 100 células, dez instruções e execução manual por slides [3] [4]; (c) existem padrões imprimíveis de OR, AND, NOR, NAND e NOT em origami [5]; (d) a construção formal de Hull e Zakharevich simula Rule 110 com fios e gadgets de dobras [6]; (e) origami mechanologic demonstra um bit mecânico regravável e portas AND/OR [7]; (f) cartões perfurados foram usados para armazenar e inserir programas e dados [8] [9]; (g) traços de grafite conduzem e podem funcionar como elementos resistivos/capacitivos [11] [12].

**Inferências de engenharia:** (a) o tempo de uma máquina de papel é dominado pela execução serial humana; (b) o estado de uma folha finita é finito, embora folhas e cartões possam ser anexados; (c) completude de Turing não significa velocidade nem tamanho físico práticos; (d) grafite sozinho não foi demonstrado nas fontes consultadas como lógica digital completa; (e) Paper Playground deve ser classificado como interface híbrida, pois a câmera e o microcontrolador fazem parte do ciclo computacional.

> A separação entre fatos e inferências é essencial: o papel pode carregar instruções, memória, geometria e sinais, mas “computar em papel” não designa um único mecanismo físico.

— Relatório preparado por Manus AI.
