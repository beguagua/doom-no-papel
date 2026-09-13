# DOOM em meios improváveis

## Escopo e método

Este relatório investiga precedentes verificáveis de **DOOM** executado ou apresentado em formatos e plataformas incomuns. O recorte exigido cobre PDF, bactéria, calculadora, planilha, navegador e hardware mínimo. A análise privilegia fontes primárias ou técnicas: repositórios de código, READMEs, documentação de portabilidade, páginas dos autores e documentação institucional. Matérias jornalísticas foram usadas para contextualizar e, sobretudo, para conferir afirmações que aparecem repetidas de forma imprecisa.

A palavra “rodar” é ambígua neste tema. Para evitar misturas, uso quatro categorias:

1. **Execução real do motor ou de um port:** o código que implementa o jogo é executado no alvo ou no runtime que o alvo oferece, processa entradas e produz novos frames. Um port compilado para WebAssembly, por exemplo, é execução real no navegador, embora dependa do motor WebAssembly do navegador.
2. **Execução híbrida ou front-end:** o jogo é executado por um processo externo ou por uma extensão da plataforma, enquanto o formato improvável fornece a janela, o desenho ou a interface. O Excel com Python/PyXLL é deste tipo.
3. **Emulação:** o alvo executa um emulador de outra máquina ou sistema operacional, e o DOOM original roda dentro desse ambiente emulado. O Google Sheets com js-dos é o exemplo mais claro.
4. **Exibição, simulação ou clone:** o alvo apenas exibe frames calculados fora dele, ou implementa um jogo “Doom-like” sem ser o motor/ativos do DOOM original. Isto é importante para a bactéria e para o arquivo Doom.xls baseado somente em fórmulas.

## Conclusão

Há precedentes sólidos para afirmar que o motor clássico de DOOM pode ser transportado para runtimes e dispositivos muito diferentes do PC original. Os casos mais fortes são o **DoomPDF**, o port nativo **nDoom** para calculadoras TI-Nspire, o port **RP2040 Doom** para Raspberry Pi Pico e os ports de **WebAssembly** para navegadores. Neles, existe código de jogo executável, há uma ponte explícita para entrada e framebuffer, e os autores fornecem requisitos ou código reproduzível.

O caso do **PDF** é execução real, mas não significa que o formato PDF tenha virado uma CPU autônoma. O PDF contém JavaScript e código asm.js; o motor PDF do Chromium fornece o runtime. A renderização é feita escrevendo caracteres ASCII em campos de texto, com resolução e desempenho severamente reduzidos. O demo público informa que funciona apenas em navegadores baseados em Chromium [1] [2].

O caso da **bactéria** não é um port de DOOM para um computador biológico. A fonte técnica consultada afirma que o jogo roda em um computador convencional e que as células de *E. coli* funcionam como uma tela de baixa resolução; a página da autora descreve o trabalho como uma simulação de quanto tempo levaria para usar bactérias como display [5] [6] [7]. Portanto, a formulação “DOOM rodando em bactérias” é uma metáfora de exibição biológica, não um fato verificado de execução do motor dentro das células.

As **planilhas** formam três situações diferentes. No Excel com PyXLL, o motor DOOM é executado por Python/Cython e o Excel recebe frames para colorir células; é um front-end de planilha, não um motor feito pelas fórmulas. No Google Sheets, o navegador executa js-dos para emular a versão DOS e o Apps Script atualiza as cores das células; é emulação mais renderização remota. Já o arquivo **Doom.xls** executa fórmulas e ray casting dentro do Excel, mas é explicitamente um jogo “Doom-like”, não o DOOM original [12] [13] [14].

O melhor precedente de **hardware mínimo verificável** é o RP2040. O port executa DOOM derivado de Chocolate Doom em um microcontrolador com 264 KB de RAM, usando dois Cortex-M0+, flash de 2 MB no Raspberry Pi Pico para o DOOM1.WAD shareware comprimido e periféricos externos para VGA, áudio e teclado. O port sacrifica memória, coloca dados comprimidos em flash e usa otimizações agressivas, mas preserva uma parcela incomumente grande da experiência original [9] [10] [11]. Isso é uma demonstração de engenharia de portabilidade, não um limite matemático inferior para “o menor hardware possível”.

A implicação central para qualquer projeto inspirado nesses precedentes é separar **onde o jogo calcula**, **onde os dados do jogo vivem** e **onde o frame aparece**. Os projetos mais convincentes não fazem o formato improvável realizar tudo sozinho: eles reduzem a interface ao mínimo, deslocam dados para armazenamento disponível, ou usam o alvo como display. Esta decomposição permite uma demonstração honesta sem chamar de “DOOM rodando no alvo” algo que é apenas vídeo, simulação ou emulação.

## Evidências

### 1. Matriz comparativa

| Precedente | O que foi verificado | Mecanismo | Requisitos/limites registrados | Classificação |
|---|---|---|---|---|
| **DoomPDF** | O repositório se identifica como um port de DOOM que roda dentro de um PDF. O demo público limita o uso a navegadores Chromium-based [1] [2]. | C/C do port compilado com Emscripten antigo para **asm.js**, executado pelo JavaScript do motor PDF. Entrada por campos de texto/botões; saída por um campo de texto por linha, contendo caracteres ASCII [1]. | Atualizar as 200 linhas leva cerca de 80 ms por frame, aproximadamente 13 fps; a imagem é monocromática com seis cores efetivas. Build requer Linux, Python, dependências e Emscripten 1.39.20 baixado pelo script [1] [3]. | **Execução real**, em runtime JavaScript/PDF; não é emulação de DOS. O PDF é o contêiner e a interface. |
| **E. coli / DOOM biológico** | O material técnico diz que o jogo roda em um computador padrão e que uma grade 32×48 de células pode ser usada como display 1-bit. A página da autora descreve o trabalho como simulação de tempo de execução [5] [6] [7]. | Computador calcula os frames; um controlador traduz bits em presença/ausência de um repressor que controla fluorescência. A bactéria representa pixels, não o motor do jogo [5] [6]. | Cerca de 70 min para atingir o pico de iluminação e 8 h 20 min para voltar ao estado inicial; a estimativa divulgada é aproximadamente um frame a cada 8–9 h e cerca de 599 anos para uma partida completa [6]. | **Simulação/exibição biológica**, não execução do motor dentro de bactérias. O qualificativo “em tempo real” em matéria jornalística não deve ser lido como port computacional. |
| **nDoom em TI-Nspire** | O repositório fornece código-fonte, binário `ndoom.tns`, instruções e suporte a modelos TI-Nspire ClickPad, TouchPad, CX, CX CR4 e CX II [8]. | Port nativo do motor clássico para o ambiente da calculadora, instalado como aplicação `.tns` por meio de **Ndless**. O usuário fornece IWAD/PWAD compatível; a calculadora lê WAD, inicializa vídeo e aceita teclado/touchpad [8]. | Ndless é requisito. IWADs precisam ser copiados e renomeados para `.wad.tns`; há suporte principal a IWADs e suporte parcial a PWADs. Vários jogos são selecionáveis, incluindo DOOM shareware, DOOM, Ultimate DOOM e DOOM II [8]. | **Execução real nativa** na calculadora; não é vídeo e não depende de emulador de PC. |
| **DOOM em Excel com PyXLL** | O repositório inclui `doom.py`, requisitos e a referência ao WAD. O código chama `cydoomgeneric`, inicia o jogo em thread e fornece callbacks de frame e entrada [12] [13]. | O motor C/Cython `cydoomgeneric` roda por Python; PyXLL expõe uma função ao Excel. O callback converte o framebuffer em cores BGR e o `Formatter` pinta o interior das células [12] [13]. | Requer Microsoft Excel/ambiente PyXLL, Python, `pyxll` e `cydoomgeneric`; o WAD está incluído no repositório. A resolução é reduzida com `scipy.ndimage.zoom`, e a atualização célula a célula é o gargalo [12] [13]. | **Execução híbrida real**: o jogo roda em Python/C, enquanto o Excel é display e interface. Não é “DOOM implementado em fórmulas”. |
| **Doom.xls por fórmulas** | A fonte descreve um engine 3D feito com fórmulas Excel, ray casting por pixel, mapa procedural, inimigos e iluminação, e o chama explicitamente de “Doom-like game” [14]. | Cálculos de células, formatação condicional e shaders/funções de planilha. Macros são opcionais para capturar teclas; o artigo afirma que o engine não usa macro [14]. | O mapa é um labirinto procedural plano, com mecânicas simplificadas e inimigos procedurais. Há arquivos `.xlsx`/`.xlsm` para download, mas não são WAD nem o motor original do DOOM [14]. | **Clone/arte computacional executado em planilha**, não port de DOOM. |
| **DOOM em Google Sheets** | O README fornece `Code.gs` e `Index.html`, instruções de instalação e limitações. O projeto diz que executa DOOM na planilha, mas identifica o uso de js-dos para emular a versão DOS [15]. | HTML/JavaScript carrega **js-dos**, que emula o ambiente DOS; frames são capturados em 120×80, diferenças são detectadas e o Apps Script atualiza a cor de fundo das células [15]. | É preciso criar uma planilha, instalar o Apps Script, ajustar grade de 120×80 e lançar o menu. Atualizações célula a célula são muito lentas e a planilha não oferece true color [15]. | **Emulação + exibição híbrida**. A planilha não executa diretamente o motor original; o navegador executa o emulador e a planilha recebe uma representação do frame. |
| **Doom.wasm no navegador** | O projeto fornece módulo WebAssembly, exemplo de browser e interface mínima. O README registra 10 imports, 4 exports e memória máxima de cerca de 16 MB com o WAD shareware [16]. | Código DOOM compilado para WebAssembly; o JavaScript cria um `Canvas`, copia o framebuffer, encaminha eventos de teclado e chama `initGame()`/`tickGame()` em 35 Hz [16]. | Navegador com WebAssembly e Canvas; o exemplo carrega o WAD shareware por padrão. O projeto não usa DOSBox/js-dos para o exemplo de browser. O build completo requer Python, Docker, Make, curl e git [16]. | **Execução real direta no runtime WebAssembly**, não emulação de DOS. |
| **D3Wasm / DOOM 3** | A página técnica documenta o port funcional do id Tech 4/DOOM 3 para Emscripten/WebAssembly e WebGL, com demonstração online, saves e navegadores desktop principais [17]. | Código do engine id Tech 4 compilado para Wasm; backend refeito para WebGL/GLSL. Dados são baixados e armazenados em IndexedDB [17]. | WebAssembly, WebGL e IndexedDB; CPU moderno, aproximadamente 850 MB de RAM e 400 MB de dados baixados/cacheados. Desempenho citado: aproximadamente 30–40 fps em desktop moderno, variando por navegador [17]. | **Execução real direta no navegador**, em escala muito mais pesada que DOOM clássico. |
| **RP2040 Doom / Raspberry Pi Pico** | Código-fonte, UF2s, ferramenta de conversão de WAD e documentação fornecem um port do DOOM derivado de Chocolate Doom para RP2040/RP2350 [9] [10] [11]. | Execução nativa em dois Cortex-M0+; WAD é convertido para formatos compactados WHX/WHD e lido diretamente da flash. PIO gera sinais VGA; áudio e teclado usam periféricos/placas externas [9] [10]. | RP2040 tem 264 KB de RAM. O Pico com 2 MB de flash acomoda DOOM1.WAD shareware comprimido; placas de 8 MB acomodam Ultimate DOOM e DOOM II. O projeto cita saída 320×200 a 60 Hz, áudio OPL2, rede I2C de até quatro jogadores e normalmente 30–35+ fps, com overclock de 270 MHz [9] [10] [11]. | **Execução real nativa em hardware mínimo documentado**, embora não seja um limite inferior absoluto. |

### 2. PDF: código de jogo dentro de um contêiner de documento

O README primário é explícito:

> “This is a Doom source port that runs inside a PDF file.” — README do projeto DoomPDF [1].

A arquitetura descrita no README é tecnicamente consistente com a demonstração. O padrão PDF suporta JavaScript com uma biblioteca própria. O PDFium, usado pelo Chromium, implementa apenas uma parte mais restrita dessa superfície por razões de segurança. O projeto compila C para asm.js com uma versão antiga do Emscripten. O JavaScript do PDF fornece o loop e a ponte de entrada/saída; não há necessidade de emular DOS.

A restrição dominante é o framebuffer. Um framebuffer 320×200 teria 64.000 pixels. Alternar um campo de texto por pixel a cada frame seria inviável. O autor usa um campo por linha, totalizando 200 campos, e converte cada linha em caracteres ASCII. O resultado é uma imagem legível, monocromática de seis cores efetivas, com aproximadamente 80 ms de custo de atualização por frame [1] [3].

A página pública do projeto registra uma limitação de compatibilidade mais estreita do que a descrição genérica do JavaScript em PDF:

> “Note: the PDF only works inside Chromium-based browsers.” — página pública DoomPDF [2].

Esta diferença é relevante para um relatório de projeto. A existência de APIs de JavaScript em PDF não implica que Acrobat, Firefox e Chromium tenham o mesmo comportamento. A demonstração verificável deve fixar o runtime, a versão do navegador, o modo de abertura do PDF e a política de segurança aplicada pelo engine PDF.

### 3. Bactéria: o caso mais importante de correção terminológica

O material de Ars Technica é a fonte mais clara para corrigir o slogan. Ele informa que o trabalho não codifica todo o DOOM no DNA bacteriano e que o jogo roda em um computador padrão, enquanto as células servem como display de baixa resolução [5]. O MIT resume a arquitetura como uma placa de poços 32×48 ligada a um controlador que traduz código binário em adição ou omissão de um repressor que controla a fluorescência [7].

O mecanismo proposto é um display biológico de 1 bit por célula/poço. A bactéria não calcula BSP, colisão, IA, leitura de WAD, renderização ou mistura de áudio. O computador convencional calcula a imagem e o controlador decide quais pixels biológicos devem fluorescer. Isso torna o precedente valioso para um projeto de **saída lenta, física ou viva**, mas não para alegar computação completa em organismos.

As fontes públicas divergem na escolha de verbos. Uma matéria usa “programmed Doom to run on a display made from E. coli” [6], enquanto a fonte da autora chama o projeto de simulação [7]. O relatório adota a interpretação mais conservadora: houve um projeto técnico de display/feasibility study com células e um modelo de tempo de resposta; não foi verificada uma implementação do motor DOOM dentro da bactéria. A manchete “DOOM em bactéria” deve, portanto, ser rotulada como **exibição bacteriana simulada ou assistida por computador**, não como port biológico.

### 4. Calculadora: nDoom como port nativo verificável

O nDoom é um caso limpo porque o repositório fornece código C, Makefile, binários e instruções específicas do dispositivo. O fluxo requer instalar Ndless, transferir `ndoom.tns`, transferir o IWAD e iniciar o aplicativo na calculadora [8]. O port conhece tela, memória, endereçamento e controles TI-Nspire; não está abrindo um DOS emulado dentro da calculadora.

A dependência de um IWAD é conceitualmente importante. O executável é o motor; o WAD contém dados de jogo. O próprio repositório oficial do código de DOOM explica que o código aberto precisa dos dados reais do jogo [18]. Assim, uma demonstração reproduzível precisa separar o binário do port, o sistema de extensão Ndless e a licença/proveniência do WAD.

### 5. Planilhas: três alegações que não devem ser colapsadas

#### Excel com PyXLL

A implementação do repositório `DOOM-in-excel` é particularmente útil como evidência de leitura de fonte. `doom.py` chama `cydoomgeneric`, inicializa o jogo em uma thread, aponta para `Doom1.WAD`, recebe pixels por callback e usa um `Formatter` do PyXLL para definir `interior_color` das células [12]. O pacote `cydoomgeneric` documenta as funções de callback `draw_frame` e `get_key` e afirma que roda em Linux, macOS e Windows [13].

A conclusão precisa ser qualificada: é possível **jogar DOOM com a janela/planilha do Excel como display**, mas o cálculo do jogo ocorre na extensão Python/C. Não é uma CPU construída com células nem uma implementação do engine em fórmulas. Como precedente de integração, é real e interessante; como precedente de “DOOM rodando no Excel”, é híbrido.

#### Doom.xls baseado apenas em fórmulas

O projeto de fórmulas tem mérito diferente. O artigo descreve ray casting pixel a pixel, mapa procedural, oclusão, iluminação, inimigos, colisão e formatação condicional, com a afirmação de que o engine não usa macro [14]. A entrada por teclado é uma camada separada e pode usar VBA. O resultado é um jogo tridimensional executado pela recalculação do Excel, mas o próprio artigo o chama de “Doom-like game”.

Não há base para tratá-lo como port do DOOM. O mapa é procedural, as regras e inimigos são simplificados, e não há leitura de IWAD nem o renderer original. É melhor classificado como **clone técnico/arte computacional em planilha**.

#### Google Sheets

O repositório de Google Sheets informa o encadeamento completo: `Index.html` carrega DOOM por js-dos, reduz o frame para 120×80, detecta pixels alterados e `Code.gs` colore células [15]. O uso de js-dos é decisivo. Um emulador de DOS executa a versão DOS; Google Sheets é usado como camada de menu, sincronização e display.

O projeto é uma demonstração real de integração entre browser, emulador, Apps Script e planilha. É, porém, uma alegação diferente de “o Apps Script executa DOOM”. O motor DOOM é executado pelo ambiente DOS emulado no JavaScript, e as células recebem apenas uma imagem reduzida. A lentidão da atualização célula a célula e a perda de cores são limitações estruturais, não simples problemas de otimização.

### 6. Navegador: WebAssembly direto versus DOS emulado

O navegador não é um único tipo de precedente. O `doom.wasm` fornece uma interface pequena: inicializar o jogo, avançar um tick e informar teclas. O exemplo de browser instancia WebAssembly, lê o framebuffer exportado, copia os pixels para um Canvas e chama `tickGame` 35 vezes por segundo [16]. O README estima até cerca de 16 MB de memória WebAssembly com o WAD shareware. Isso é port direto para Wasm, não emulação de DOS.

O D3Wasm demonstra uma versão mais exigente: o engine id Tech 4/DOOM 3, compilado com Emscripten, usa WebGL/GLSL e IndexedDB. A página documenta 400 MB de dados, cerca de 850 MB de RAM e desempenho de 20–50 fps dependendo de navegador e cenário [17]. Este caso comprova a viabilidade de levar engines 3D substanciais ao browser, mas não deve ser usado como requisito para DOOM clássico.

A distinção entre `doom.wasm` e o Google Sheets é útil para o projeto:

| Aspecto | WebAssembly direto | Google Sheets com js-dos |
|---|---|---|
| Código do jogo | Compilado para Wasm | Binário/versão DOS dentro de um emulador |
| Runtime | WebAssembly do navegador | JavaScript + emulador de DOS |
| Framebuffer | Canvas HTML | Cores de células via Apps Script |
| Emulação de hardware | Não necessária para o motor | Necessária para a camada DOS |
| Controle de desempenho | Loop/ticks e Canvas | Latência de API e atualização de células |
| Classificação | Port real no browser | Emulação e renderização híbrida |

### 7. Hardware mínimo: por que o RP2040 é um precedente forte

A documentação do RP2040 Doom registra o conflito de recursos. A compilação direta de Chocolate Doom exigiria cerca de 300 KB de dados mutáveis estáticos e ao menos mais 700 KB de memória dinâmica, enquanto o RP2040 tem 264 KB de RAM [11]. O port resolve o problema movendo dados constantes para flash, reduzindo tipos e precisão, sobrepondo buffers, usando bitsets e índices/pointers de 16 bits, e mantendo WAD e gráficos comprimidos em flash.

O port também altera a ordem de renderização para permitir uso dos dois cores e acesso direto a dados comprimidos. A saída VGA e o áudio não são recursos multimídia integrados do RP2040; o PIO é programado para gerar sinais digitais e placas externas fazem as conexões necessárias [9] [10]. Esta ressalva impede uma descrição enganosa como “Pico sozinho com HDMI e som”. O microcontrolador executa o jogo, mas precisa de circuito/periféricos de saída e entrada.

A documentação registra que o `DOOM1.WAD` shareware tem aproximadamente 4 MB, mas uma versão WHX comprimida e o executável cabem nos 2 MB do Pico; versões completas Ultimate DOOM e DOOM II exigem placas de 8 MB [9] [10]. O compartilhamento de rede de até quatro jogadores via I2C e a reprodução de demos originais são sinais de que não se trata apenas de um vídeo pré-gravado [9] [10].

O resultado é um ponto de referência de engenharia: **264 KB de RAM não é uma barreira absoluta para a lógica e renderização do DOOM clássico**, desde que o port aceite uma arquitetura radicalmente especializada. O requisito de 270 MHz, o armazenamento externo ou a placa VGA/áudio e o trabalho de compressão são parte do custo real.

## Implicações para o projeto

### 1. Escolher a afirmação correta antes de escolher a plataforma

O projeto deve decidir qual demonstração quer produzir:

- Se o objetivo é provar que o motor executa em um formato documental, o PDF é o precedente mais direto. O mínimo honesto é fornecer o PDF, fixar Chromium, explicar o JavaScript do PDF e medir resolução, fps e latência.
- Se o objetivo é provar portabilidade de software, WebAssembly direto ou nDoom são melhores. Eles permitem inspeção de código, callbacks claros e separação entre engine, dados e display.
- Se o objetivo é provar hardware restrito, RP2040 é a referência. É necessário publicar mapa de memória, frequência, tamanho de WAD, periféricos e imagem/UF2 reproduzível.
- Se o objetivo é explorar saída física viva, a bactéria é uma referência de display e cinética, não de computação. O relatório deve declarar “o computador executa; a bactéria exibe”.
- Se o objetivo é explorar planilhas, escolher entre um front-end real com PyXLL, um emulador com Google Sheets ou um clone em fórmulas. Cada um demonstra uma competência distinta.

### 2. Arquitetura recomendada: engine, dados, runtime e display separados

Uma arquitetura de projeto robusta deve ter quatro interfaces explícitas:

1. **Engine:** código do jogo, com entrada, tempo, simulação e renderização.
2. **Dados:** IWAD/PWAD, assets, música e sons, tratados separadamente do executável e com a licença documentada.
3. **Runtime:** browser Wasm, JavaScript em PDF, Python/Cython, Ndless ou firmware RP2040.
4. **Display/input:** Canvas, campos PDF, células, LCD/VGA, ou uma matriz bacteriana.

A interface mínima de `doomgeneric` ilustra essa decomposição com `DG_Init`, `DG_DrawFrame`, `DG_SleepMs`, `DG_GetTicksMs` e `DG_GetKey` [19]. O projeto pode adotar a mesma disciplina e registrar, para cada alvo, quais callbacks são reais, quais são simulados e onde ocorre a conversão de pixels.

### 3. Critérios de verificação e prova

Para evitar um vídeo que pareça execução sem ser execução, cada demonstração deve incluir:

- **Código fonte e commit/tag** do port, com licença e dependências.
- **Dados de jogo** separados do código e com procedência legal; o código-fonte original de id Software não substitui o IWAD [18].
- **Entrada ao vivo**, como teclado, touchpad, tecla em PDF ou controle externo; vídeo pré-renderizado não é suficiente.
- **Estado variável**, por exemplo abrir uma porta, mudar o frame por input, morrer ou reiniciar. Isto distingue execução de reprodução de vídeo.
- **Medições**, incluindo fps, resolução, latência, memória, armazenamento e tempo de inicialização.
- **Descrição da camada de execução**, dizendo literalmente “port direto”, “emulador”, “front-end”, “display remoto” ou “clone”.
- **Reprodução**, com instruções, versão do runtime, arquivos e limitações conhecidas.

### 4. Métricas específicas por meio

| Meio | Métricas mínimas recomendadas |
|---|---|
| PDF | navegador e versão, tamanho do PDF, tempo por frame, número de campos, caracteres/cores e comportamento de segurança. |
| Bactéria | número de poços/pixels, bit depth, tempo de fluorescência ligado/desligado, se a placa é física ou modelada, e qual computador calcula os frames. |
| Calculadora | modelo, sistema/Ndless, RAM/flash quando disponíveis, WAD, resolução, fps e mapeamento de teclas. |
| Excel/Sheets | processo que executa o engine, emulador ou extensão, resolução da célula, atualizações por frame, latência da API e dependência de macros. |
| Navegador | Wasm direto ou emulação, Canvas/WebGL, memória, tamanho do WAD, taxa de ticks e suporte a custom WAD. |
| RP2040 | frequência, distribuição de RAM/flash, formato comprimido, pinos, periféricos, fps e se áudio/entrada são internos ou externos. |

### 5. O que não deve ser prometido

Não se deve dizer que “qualquer coisa roda DOOM” sem declarar qual camada está executando o jogo. Um vídeo de um display bacteriano, um clone de ray casting feito em fórmulas e uma sessão do DOSBox em uma planilha podem ser trabalhos válidos, mas são evidências de naturezas diferentes. O valor técnico aumenta quando a descrição é mais específica, não quando o slogan é mais amplo.

Também não se deve usar o RP2040 como “hardware mínimo absoluto”. O projeto é uma implementação altamente otimizada e com overclock. Outros ports podem usar menos memória, resolução inferior, sem som, sem assets completos ou sem compatibilidade com demos. O fato verificável é o alvo documentado de 264 KB de RAM e 2 MB de flash para DOOM1.WAD comprimido, não uma prova de impossibilidade abaixo disso.

## Limites

**Limites da evidência bacteriana.** As fontes públicas consultadas são suficientes para negar a interpretação forte de que todo o motor DOOM foi codificado em E. coli, mas não permitem reconstruir todos os detalhes experimentais da placa. Há tensão entre a linguagem popular de “display feito de células” e a descrição da autora como simulação. O relatório, por isso, não afirma que cada poço foi demonstrado em uma partida interativa completa. A conclusão segura é que o trabalho modela/projeta uma tela bacteriana e deixa o jogo em um computador convencional [5] [6] [7].

**Limites de compatibilidade do PDF.** A página do demo diz Chromium-based. A documentação do projeto descreve APIs de PDF e menciona implementações parciais em navegadores modernos, mas não garante que o arquivo concreto funcione em Firefox, Acrobat ou leitores móveis [1] [2]. O resultado deve ser reproduzido no runtime declarado, e não generalizado para “qualquer leitor PDF”.

**Limites dos repositórios de terceiros.** Alguns projetos têm README curto, binários pré-gerados ou dependências antigas. O port Excel depende de PyXLL e de um módulo Python/C; o Google Sheets depende de APIs e permissões do Apps Script; o WebDOOM e outros ports Wasm podem exigir toolchains de 32 bits ou ativos que não são distribuídos pelo repositório. A existência de código e uma demo não garante que uma build atual seja trivial.

**Limites da palavra DOOM.** O relatório separa o motor clássico, ports que preservam o engine ou sua lógica, emuladores que executam o binário DOS e clones “Doom-like”. Sem essa separação, o mesmo rótulo mistura uma partida original em um microcontrolador, um ray caster em fórmulas e um display de caracteres em PDF.

**Limites legais e de dados.** A liberação do código-fonte por id Software não libera automaticamente todos os dados comerciais. O repositório original informa que ainda é necessário possuir dados reais do DOOM [18]. Qualquer protótipo público deve distribuir apenas dados autorizados, usar a versão shareware quando apropriado ou instruir o usuário a fornecer seu próprio IWAD.

**Limites de atualidade.** Navegadores, PDFium, Apps Script, Emscripten e toolchains mudam. Números de fps, compatibilidade e URLs de demonstração são propriedades das versões consultadas e devem ser rechecados antes de uma apresentação pública.

## Referências

[1]: https://github.com/ading2210/doompdf "GitHub — ading2210/doompdf: Doom running inside a PDF file"

[2]: https://doompdf.pages.dev/ "DoomPDF — demonstração e nota de compatibilidade"

[3]: https://arstechnica.com/gaming/2025/01/this-pdf-contains-a-playable-copy-of-doom/ "This PDF contains a playable copy of Doom — Ars Technica"

[4]: https://github.com/id-Software/DOOM "id Software — DOOM Open Source Release"

[5]: https://arstechnica.com/gaming/2024/01/can-it-run-doom-gut-bacteria-edition/ "Can it run Doom? Gut bacteria edition — Ars Technica"

[6]: https://www.popsci.com/science/doom-e-coli-cells/ "Running 'Doom' on E. coli cells… very, very slowly — Popular Science"

[7]: https://www.laurenramlan.com/portfolio/project-two-llrgk-wff4y "Lauren Ramlan — Doom on Bacteria"

[8]: https://github.com/critor/ndoom "GitHub — critor/ndoom: Doom port for the TI-Nspire"

[9]: https://github.com/kilograham/rp2040-doom "GitHub — kilograham/rp2040-doom: Fully-featured Doom port for Raspberry Pi RP2040/RP2350"

[10]: https://kilograham.github.io/rp2040-doom/ "RP2040 Doom — desenvolvimento, resultados e requisitos"

[11]: https://kilograham.github.io/rp2040-doom/speed_and_ram.html "RP2040 Doom — Making It Run Fast And Fit in RAM"

[12]: https://github.com/Pranshul-Thakur/DOOM-in-excel "GitHub — Pranshul-Thakur/DOOM-in-excel"

[13]: https://github.com/wojciech-graj/cydoomgeneric "GitHub — cyDoomGeneric: Python bindings for doomgeneric"

[14]: https://www.gamedeveloper.com/design/3d-engine-entirely-made-of-ms-excel-formulae-enjoy-this-doom-xls-file- "3D engine entirely made of MS Excel formulae: Enjoy this Doom.xls file — Game Developer"

[15]: https://github.com/moses297/doom-on-google-sheets "GitHub — moses297/doom-on-google-sheets"

[16]: https://github.com/jacobenget/doom.wasm "GitHub — jacobenget/doom.wasm: Doom as a small WebAssembly module"

[17]: http://www.continuation-labs.com/projects/d3wasm/ "D3wasm — port of id Tech 4 / Doom 3 engine to WebAssembly and WebGL"

[18]: https://github.com/id-Software/DOOM "id Software — DOOM Open Source Release (código exige dados do jogo)"

[19]: https://github.com/ozkl/doomgeneric "GitHub — ozkl/doomgeneric: Make porting Doom easier"

[20]: https://www.raspberrypi.com/news/doom-comes-to-raspberry-pi-pico/ "Doom comes to Raspberry Pi Pico — Raspberry Pi News"

*Autor padrão do relatório: Manus AI.*
Documentação preparada a partir da leitura das páginas, READMEs, árvores de código e scripts de build citados nas referências; snippets de busca não foram tratados como evidência final.
