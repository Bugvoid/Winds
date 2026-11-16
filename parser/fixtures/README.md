# Fixtures reais da B3

Boletins diários "PROVENTOS DOS EMISSORES DEPOSITADOS NA FORMA "EX"" do Plantão de
Notícias da B3 (agência 18), de 19/10/2026 a 16/11/2026: 21 arquivos, um por dia útil.

- `boletins/Proventos-<data ex>-<id da notícia>.txt`: conteúdo de
  `<pre id="conteudoDetalhe">` da página `Noticias/Detail`, com as entidades HTML já
  decodificadas e quebra de linha LF. O texto está exatamente como a B3 publica,
  inclusive os espaços no fim das linhas, que importam para o corte por colunas.
  Por isso o `.gitattributes` marca esses arquivos como `-text`.
- `listagem-2026-10-17_2026-11-16.json`: resposta de `Noticias/ListarTitulosNoticias`
  com `palavra=Proventos` para o período, útil para os testes do coletor.

Coletados em 16/11/2026 na máquina do Luan, com o `robo-bra-b3-plantao-noticias` do
Pongo_Financy (uma requisição por vez, com pausa de 3 a 5 s entre os detalhes).

Particularidade do período: a data ex 03/11/2026 saiu em **duas notícias** (ids 3539164 e
3539165), com o mesmo `dateTime` e texto idêntico. O coletor e o pipeline precisam tratar
isso como um único boletim do dia.
