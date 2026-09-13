# Dados externos e IWAD

PaperDOOM-1 não usa IWAD, PWAD ou qualquer arquivo de dados do DOOM. O mapa mínimo é um Markdown próprio e o renderer usa símbolos tipográficos.

O código-fonte publicado pela id Software separa o motor dos dados. Um port real de DOOM normalmente precisa de um IWAD externo, que pode conter mapas, sprites, texturas, sons, músicas e outros recursos. A publicação do código do motor não autoriza automaticamente a redistribuição desses dados.

Não coloque neste diretório `DOOM.WAD`, `DOOM1.WAD`, `DOOM2.WAD`, `TNT.WAD`, `PLUTONIA.WAD` ou dumps de assets. Se quiser testar um port real, forneça o arquivo por um caminho local autorizado e mantenha-o fora deste repositório.

Uma alternativa técnica é estudar um conteúdo livre como [Freedoom](https://freedoom.github.io/about.html), respeitando a licença e os créditos próprios. Isso seria outro experimento, separado do demake PaperDOOM-1.
