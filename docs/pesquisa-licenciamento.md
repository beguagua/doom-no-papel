# Código-fonte e licenças do DOOM

## Conclusão

O repositório público `id-Software/DOOM` deve ser tratado como uma distribuição do **código-fonte do motor clássico sob GNU General Public License versão 2 (GPLv2)**, e não como uma distribuição do jogo completo. A página do repositório informa que o código está sob GPL 2.0, o `README.TXT` atual repete essa declaração e a raiz contém o texto integral da GPLv2 em `LICENSE.TXT`.[1] [2] [3] O repositório, contudo, preserva nos arquivos C e H os cabeçalhos históricos que mencionam a antiga DOOM Source Code License (DSL). Essa inconsistência documental não deve ser apagada: a prática prudente é manter `LICENSE.TXT`, manter os avisos de copyright e licença já presentes, declarar claramente a GPLv2 no README do projeto derivado e pedir esclarecimento jurídico ao titular se o projeto precisar de uma posição formal sobre a interação entre os dois textos.

A GPLv2 permite copiar, modificar e redistribuir o código, inclusive por remuneração, desde que sejam preservados os avisos, a licença e a ausência de garantia; que alterações sejam identificadas; e que obras derivadas distribuídas como um todo satisfaçam as condições de copyleft da GPLv2.[3] [8] Ela não concede direitos sobre o **IWAD** — o arquivo de dados que contém mapas, gráficos, sons, músicas e outros recursos do jogo — nem sobre as marcas, o manual, os textos narrativos ou assets proprietários de DOOM. O próprio lançamento original diz que é necessário obter dados reais de DOOM, e os arquivos técnicos informam que arte e WADs não foram incluídos.[2] [4] A documentação de source ports confirma que o executável e o IWAD são componentes distintos.[9]

Para um GitHub público, a configuração de menor risco é: publicar somente o código e os arquivos de build que pertencem à release; não versionar `DOOM.WAD`, `DOOM1.WAD`, `DOOM2.WAD`, `TNT.WAD`, `PLUTONIA.WAD`, texturas, sprites, sons, músicas, screenshots ou trechos extensos de manuais sem uma licença específica; fornecer instruções para o usuário obter legalmente o IWAD; e oferecer, como alternativa, um IWAD livre como Freedoom, sempre com a licença e os créditos correspondentes.[4] [9] [10] [11]

> **Síntese jurídica:** a GPLv2 resolve a redistribuição do código GPL. Ela não transforma os dados comerciais de DOOM em conteúdo livre. “Código aberto” do motor não significa “jogo completo aberto”.

## Evidências

### 1. O que o espelho oficial contém e qual é a licença atual

**Fatos verificados.** O repositório `id-Software/DOOM` se identifica como “DOOM Open Source Release”. A descrição pede uso não lucrativo e diz que é necessário possuir dados reais de DOOM, mas o mesmo README atual termina com “Licensed under the GNU General Public License 2.0”. A raiz contém `LICENSE.TXT`, com o texto integral da GNU GPL versão 2, de junho de 1991.[1] [2] [3]

Há também um fato histórico relevante no próprio espelho: o commit oficial `Add GPL information`, de 16 de janeiro de 2024, adiciona `LICENSE.TXT` e acrescenta ao `README.TXT` o copyright da ZeniMax Media Inc. e a declaração GPL 2.0.[5] Isso documenta a apresentação atual do repositório, mas não deve ser confundido com a data histórica da primeira relicença: a documentação técnica do ecossistema registra a relicença para GPLv2 em 3 de outubro de 1999.[6]

Os arquivos-fonte ainda não foram uniformizados. Por exemplo, `linuxdoom-1.10/d_main.c` e `linuxdoom-1.10/w_wad.c` mantêm cabeçalho com copyright de id Software e a frase de que o código só estaria disponível sob a DOOM Source Code License.[7] O estado observável é, portanto, uma árvore com licença GPLv2 na raiz e avisos históricos DSL em muitos arquivos. Não é seguro interpretar a ausência de uma alteração nos cabeçalhos como autorização para removê-los.

**Interpretação técnica, não parecer jurídico.** A fonte técnica que transcreve a DSL explica que ela foi a licença original de 1997 e que o código foi depois relicenciado sob GPL; também observa que licenças anteriores não são simplesmente apagadas e descreve uma situação de dupla base de autorização.[6] Essa leitura explica por que o projeto deve conservar os avisos antigos e a GPLv2. Ela não substitui uma confirmação do titular nem uma análise de cada contribuição incorporada.

### 2. Licença original de 1997 versus GPLv2

O pacote original `doomsrc.zip`, datado de 23 de dezembro de 1997, contém `README.TXT`, `linuxdoom-1.10.src.tgz` e `sndserv.tgz`; não contém um IWAD. O README original diz que o código foi liberado para uso não lucrativo e que o usuário ainda precisava de dados reais de DOOM.[4] A árvore técnica do pacote também preserva os cabeçalhos que apontam para a DSL.

A DSL histórica se intitula **Limited Use Software License Agreement**. A transcrição técnica informa que ela:

* concede uso educacional de porções do código, sem conceder propriedade;
* proíbe duplicar o código-fonte fora das exceções indicadas;
* proíbe exploração comercial do software, embora contenha uma exceção específica para software próprio desenvolvido no exercício do uso educacional;
* proíbe vender, alugar, sublicenciar, distribuir por dinheiro ou outra contraprestação, ou explorar comercialmente o software; e
* afirma que o software inclui, no texto da licença histórica, código-fonte, dados de arte, música e ferramentas.

Essas regras são muito mais restritivas que a GPLv2 e descrevem a situação do lançamento histórico, não a licença que um novo clone deve inventar para a árvore atual. A licença atual que aparece no repositório oficial é GPLv2. Ao redistribuir uma cópia derivada, não se deve reintroduzir uma restrição “somente não comercial” sobre o código que o titular apresenta sob GPLv2, porque isso seria incompatível com a permissão GPL de cobrar pela transferência e com a proibição de impor restrições adicionais ao destinatário.[3] [6] [8]

### 3. Arquivos necessários para compilar e executar a release clássica

A tabela abaixo separa o que é código/build do que é dado externo. Os caminhos são os caminhos observados no repositório oficial.

| Componente | Evidência no repositório | Função prática | Situação de redistribuição |
|---|---|---|---|
| `LICENSE.TXT` | Arquivo de raiz com GPLv2 integral.[3] | Licença que deve acompanhar o código GPLv2. | Deve permanecer no repositório e nas redistribuições. |
| `README.TXT` | Declara GPL 2.0 e avisa que dados reais são necessários.[2] | Contexto, limitações e instruções da release. | Preservar aviso e copyright; revisar o texto se o fork modificar a finalidade. |
| `linuxdoom-1.10/*.c` e `*.h` | Árvore principal do motor, com avisos históricos nos cabeçalhos.[7] | Renderização, jogo, rede, leitura de WAD e sistema Linux. | Redistribuir com GPLv2 e sem remover avisos históricos. |
| `linuxdoom-1.10/Makefile` | Usa GCC, define `NORMALUNIX` e `LINUX`, vincula X11/Xext, `libm` e `libnsl`.[7] | Build do executável `linux/linuxxdoom`. | O projeto deve documentar dependências; bibliotecas do sistema são componentes externos. |
| `sndserv/` | Tem Makefile e fontes do servidor de som, separado do motor.[1] | Servidor de som da release Linux original. | Tratar como parte do código publicado, mantendo seus avisos/licenças. |
| `ipx/` e `sersrc/` | READMEs os identificam como drivers IPX e serial/modem.[1] | Drivers de rede e comunicação da release. | Incluir na auditoria de copyright e licença; não presumir que código de terceiros seja GPL sem verificar. |
| IWAD externo | `d_main.c` procura `doom1.wad`, `doom.wad`, `doomu.wad`, `doom2.wad`, `doom2f.wad`, `tnt.wad` e `plutonia.wad`; a variável `DOOMWADDIR` pode indicar o diretório.[7] | Dados necessários para um jogo completo. | Não vem do repositório e não deve ser incluído sem autorização própria. |
| Bibliotecas e ambiente | O Makefile referencia X11/Xext, `libnsl`, `libm` e GCC.[7] | Dependências de compilação e execução. | Licenças devem ser verificadas separadamente; não são cobertas automaticamente pela GPL do motor. |

A documentação de `README.b` é especialmente explícita: o lançamento Linux não continha suporte SVGA, Windows ou DOS completo; ferramentas que geravam certas tabelas foram omitidas; e “artwork” e WADs não foram incluídos. Ela acrescenta que pelo menos o WAD shareware seria necessário para executar o binário.[4] Isso prova a separação técnica entre engine e dados, mas a menção histórica ao shareware não é, por si só, uma licença moderna para publicar `DOOM1.WAD` no GitHub.

### 4. IWAD, PWAD e assets

Um IWAD é o arquivo WAD principal que contém os dados externos de um jogo completo. A documentação técnica lista mapas, texturas, sprites, gráficos de interface, sons, músicas e outros lumps como conteúdo típico de um IWAD.[10] O código de `w_wad.c` abre arquivos externos, reconhece cabeçalhos `IWAD` e `PWAD`, lê seus diretórios de lumps e permite que arquivos posteriores substituam recursos anteriores.[7]

Um PWAD é normalmente um arquivo de complemento criado por um autor de mod. Ele pode conter mapas próprios ou substituir recursos do IWAD, e frequentemente é pequeno porque depende de recursos que continuam no IWAD.[11] Isso tem duas consequências legais distintas:

1. Um PWAD integralmente criado pelo autor pode ter uma licença própria, mas o autor deve ter direitos sobre todos os recursos que incluiu.
2. Um PWAD que incorpora sprites, texturas, sons, música, mapas ou trechos de outros jogos não se torna redistribuível apenas por ser chamado de “mod” ou “PWAD”.

O projeto Freedoom oferece um contraste verificável: ele diz que o código do motor DOOM foi liberado, mas que o conteúdo original — gráficos, áudio, níveis, cenário e personagens — permaneceu proprietário; o objetivo do projeto é fornecer uma substituição livre.[12] A página do projeto descreve seus assets como licenciados sob BSD, com a exigência de incluir o aviso de copyright e creditar Freedoom.[12] O README do repositório Freedoom também exige permissão ou licença livre para tudo que for submetido e alerta que não se deve basear arte e sons em obras restritas.[13]

**Regra operacional:** não incluir no GitHub nenhum IWAD comercial ou shareware, nem extratos de assets, salvo se houver uma autorização específica, atual e verificável para aquela forma de distribuição. Se o objetivo é fornecer uma experiência executável sem exigir uma cópia comercial, usar um IWAD livre como Freedoom, separado e claramente identificado, é a alternativa tecnicamente apropriada; a licença de Freedoom não é a licença do código DOOM.

### 5. O que a GPLv2 permite e exige

A GPLv2 oficial permite cópias literais do código, desde que cada cópia preserve o aviso de copyright, o disclaimer de garantia, os avisos de licença e uma cópia da GPL.[8] Ela permite modificar o programa e distribuir a obra derivada sob os termos da GPLv2, exigindo avisos destacados nos arquivos modificados com a alteração e a data.[8]

Se uma obra distribuída contém ou deriva do programa, a GPLv2 exige que a obra como um todo seja licenciada, sem cobrança de royalties de licença, sob os termos da GPLv2, ressalvadas as seções independentes que possam ser consideradas obras separadas. A GPLv2 também esclarece que a mera agregação de outra obra independente no mesmo meio não coloca automaticamente essa outra obra sob a GPL.[8] Essa regra é importante para pacotes que colocam um engine GPL ao lado de um IWAD livre com licença própria, mas não resolve os direitos de um IWAD comercial.

Na distribuição de executáveis, a seção 3 exige o código-fonte correspondente completo, ou uma oferta escrita válida nas condições descritas pela licença. Em um GitHub, publicar no mesmo local a revisão exata do código correspondente é uma forma operacional usual de atender ao acesso equivalente, mas o projeto deve vincular explicitamente a versão do binário à revisão e conservar todos os scripts necessários de compilação e instalação.[8]

A GPLv2 não autoriza remover marcas, transformar dados não GPL em dados GPL, omitir créditos de terceiros ou adicionar uma cláusula “não comercial” à parte GPL. Ela também fornece o software sem garantia.[8]

### 6. Tutorial, documentação, nomes e conteúdo textual

Um tutorial novo, escrito pelo projeto, pode ser licenciado separadamente, por exemplo sob CC BY-SA 4.0 para documentação ou sob uma licença permissiva adequada. O GitHub alerta que, sem licença, o copyright padrão permanece e terceiros não recebem automaticamente permissão para reproduzir, distribuir ou criar derivados.[14] Por isso, o tutorial deve ter um aviso explícito, um arquivo de licença ou uma seção de termos documentais; a GPLv2 do código não deve ser usada como atalho para licenciar automaticamente textos de terceiros.

A política de copyright do DoomWiki informa que seus textos são CC BY-SA 4.0, exige atribuição por backlink ou histórico de revisões e requer a mesma licença ou uma licença compatível para reutilização.[15] A mesma política diz que o wiki não tem permissão para reproduzir extensamente textos de jogo, codex, cutscenes ou diálogos da Bethesda; apenas citações breves em contexto apropriado são tratadas como potencialmente justificáveis por fair use.[15] A política do wiki não é uma decisão judicial nem substitui a lei aplicável, mas é uma orientação técnica prudente: escrever explicações próprias, citar fontes com links e não copiar manuais, diálogos, textos de interface ou narrativa original em bloco.

A documentação atual do repositório e os textos do source port também não concedem uma licença geral para usar as marcas DOOM, id Software, ZeniMax ou Bethesda como se o projeto fosse oficial. O README do fork deve dizer que o projeto é independente, evitar logotipos oficiais e não sugerir endosso. Essa é uma recomendação de gestão de risco de marca, não uma conclusão sobre cada jurisdição.

## Implicações para o projeto

### Estrutura recomendada do GitHub

A estrutura recomendada é separar claramente código, documentação, dados e arte. Um exemplo mínimo é:

```text
LICENSE.TXT                 # GPLv2 do código do DOOM
README.md                   # escopo, créditos, aviso de não-afiliação e build
THIRD_PARTY_NOTICES.md      # inventário de componentes e licenças
COPYING-DOCS.md             # se a documentação usar licença própria
src/                        # código derivado do DOOM
platform/                   # adaptações novas, com autoria e licença declaradas
docs/                       # tutorial próprio e instruções de build
assets/                     # somente assets próprios ou sob licença verificada
```

O arquivo de licença deve ficar na raiz. A documentação do GitHub recomenda `LICENSE`, `LICENSE.txt` ou `LICENSE.md` e explica que uma licença detectável aparece no topo da página do repositório.[14] [16] A detecção do GitHub é um auxílio de descoberta, não uma auditoria de titularidade; a própria documentação recomenda consultar um profissional para questões jurídicas.[14]

### Checklist de publicação

| Verificação | Ação recomendada | Motivo |
|---|---|---|
| Código original do DOOM | Preservar `LICENSE.TXT`, os copyrights, os cabeçalhos DSL e as notas existentes. | Evita apagar avisos e registra a proveniência histórica. |
| Alterações | Marcar cada arquivo modificado com aviso de alteração e data; manter um CHANGELOG. | É exigência expressa da GPLv2 para arquivos modificados.[8] |
| Licença do fork | Declarar GPLv2 para a parte derivada do código e não adicionar “não comercial”. | A restrição não comercial é incompatível com a permissão GPLv2 de redistribuição, inclusive por cobrança.[3] [8] |
| Build reproduzível | Publicar Makefiles, scripts, patches e a revisão correspondente a cada binário. | A GPLv2 define o código correspondente como a forma preferida para modificar, incluindo scripts de compilação e instalação.[8] |
| IWAD | Excluir todos os IWADs proprietários do Git e das releases. | IWAD contém o conteúdo do jogo, não apenas o motor.[9] [10] [12] |
| Shareware | Não presumir que “shareware” equivale a licença livre para hospedar `DOOM1.WAD`; direcionar o usuário a uma fonte autorizada ou usar Freedoom. | A evidência histórica consultada mostra necessidade de dados, mas não uma autorização atual inequívoca para bundling no GitHub.[2] [4] |
| PWADs | Aceitar apenas arquivos cujo autor e todos os componentes tenham licença verificável. | PWAD pode conter recursos substitutos ou cópias de dados do IWAD.[11] |
| Freedoom | Distribuir separado, com sua própria licença BSD, aviso de copyright e créditos. | Freedoom é uma substituição de conteúdo, não parte da GPL do engine.[12] [13] |
| Tutorial | Escrever texto próprio, citar URLs e licenciar a documentação; para conteúdo do DoomWiki, cumprir CC BY-SA 4.0. | Copyright de código não licencia automaticamente manuais e textos de terceiros.[14] [15] |
| Terceiros | Manter `THIRD_PARTY_NOTICES.md` com componente, versão, URL, licença, copyright e caminho. | Torna auditável a origem de bibliotecas, drivers, fontes e assets. |
| Marca | Usar “compatível com DOOM” de forma descritiva e incluir aviso de projeto independente. | Reduz risco de confusão sobre endosso ou afiliação. |

### Decisão sobre binários e releases

Um release que contém apenas o executável do engine ainda precisa cumprir a GPLv2. Deve incluir a licença, avisos, o código-fonte correspondente e as instruções de obtenção ou compilação. O pacote não deve incluir um IWAD comercial para “facilitar o primeiro uso”. Em vez disso, o README deve explicar que o usuário fornece um IWAD autorizado ou escolhe Freedoom.

Se o projeto distribuir um pacote com engine GPL e Freedoom BSD, manter os componentes em arquivos identificáveis e distribuir os avisos de ambas as licenças. Se o projeto desenvolver um IWAD próprio, a licença dos mapas, gráficos, sons, músicas e textos deve ser declarada separadamente. A licença do engine não é suficiente para cobrir a criação ou a redistribuição desses dados.

## Limites

Este relatório é uma investigação técnica de fontes públicas, não um parecer jurídico. Direitos autorais, contratos antigos de shareware, marcas e exceções de citação variam conforme a jurisdição. A análise não determina se uma cópia específica de um WAD, screenshot, música, textura, sprite, mapa, tutorial ou arquivo de terceiros é licenciada; essa determinação exige verificar a origem e os termos daquele item.

A evidência mais forte para o estado atual do código é o próprio repositório da id Software, seu `LICENSE.TXT`, seu `README.TXT`, os fontes e o commit que adicionou a informação GPL.[1] [2] [3] [5] A data de relicença de 1999 e a transcrição da DSL vêm de uma fonte técnica comunitária que se apresenta como referência do ecossistema, não de um instrumento de concessão assinado publicado pela id Software.[6] Por isso, a data e a interpretação de dupla licença devem ser registradas como evidência técnica secundária, e não como substitutas de confirmação do titular.

A documentação histórica do lançamento diz “uso não lucrativo” e “dados reais de DOOM”, enquanto a apresentação atual diz GPLv2.[2] [4] Não se deve misturar essas frases para concluir que o código atual continua limitado a uso não comercial. A leitura operacional mais segura é usar a licença GPLv2 atual, conservar os avisos históricos e evitar qualquer distribuição de dados ou documentação cuja licença não esteja demonstrada.

A menção de que o WAD shareware era necessário para executar a release Linux é uma afirmação do pacote histórico, não uma autorização contemporânea de hospedagem pública.[4] O relatório deliberadamente não afirma que `DOOM1.WAD` é livremente redistribuível. Na ausência de uma licença explícita e atual para o uso planejado, a recomendação é não incluí-lo.

Por fim, GitHub é um meio público de hospedagem, não uma garantia de titularidade. O fato de um arquivo estar disponível em outro repositório, em um espelho ou em uma release não prova que o redistribuidor possui direitos para incluí-lo. A auditoria deve ser feita arquivo por arquivo.

## Referências

[1]: https://github.com/id-Software/DOOM "id-Software/DOOM — DOOM Open Source Release"

[2]: https://github.com/id-Software/DOOM/blob/master/README.TXT "README.TXT — id-Software/DOOM"

[3]: https://github.com/id-Software/DOOM/blob/master/LICENSE.TXT "LICENSE.TXT — GNU General Public License v2 — id-Software/DOOM"

[4]: https://www.doomworld.com/idgames/idstuff/source/doomsrc "DOOM source code — idgames archive entry and 23 December 1997 release notes"

[5]: https://github.com/id-Software/DOOM/commit/a77dfb96cb91780ca334d0d4cfd86957558007e0 "Add GPL information — id-Software/DOOM commit"

[6]: https://doomwiki.org/wiki/Licences "Licences — The Doom Wiki"

[7]: https://github.com/id-Software/DOOM/tree/master/linuxdoom-1.10 "linuxdoom-1.10 source tree, Makefile, d_main.c and w_wad.c — id-Software/DOOM"

[8]: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html "GNU General Public License, version 2 — Free Software Foundation"

[9]: https://www.chocolate-doom.org/wiki/index.php/FAQ "FAQ — Chocolate Doom: IWAD requirements and source-port status"

[10]: https://doomwiki.org/wiki/IWAD "IWAD — The Doom Wiki"

[11]: https://doomwiki.org/wiki/PWAD "PWAD — The Doom Wiki"

[12]: https://freedoom.github.io/about.html "About Freedoom — a free replacement for DOOM game content"

[13]: https://github.com/freedoom/freedoom "Freedoom — complete free content first-person shooter game"

[14]: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository "Licensing a repository — GitHub Docs"

[15]: https://doomwiki.org/wiki/Doom_Wiki:Copyrights "Doom Wiki:Copyrights — reuse, attribution and in-game text policy"

[16]: https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository "Adding a license to a repository — GitHub Docs"

---

**Nota de escopo.** As afirmações classificadas como “fatos verificados” são diretamente apoiadas pelos arquivos/páginas citados. As orientações sobre não distribuir IWADs, separar documentação e preservar os avisos são recomendações de conformidade baseadas nesses fatos e devem ser validadas por advogado quando houver distribuição comercial, integração de código de terceiros ou lançamento em jurisdições específicas.

**Autor:** Manus AI

**Data da pesquisa:** 13 de setembro de 2026
