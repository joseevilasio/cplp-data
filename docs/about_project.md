## Projeto

**Estatuto de Direitos e Deveres**

## Web Scraping com Selenium.

Utilizando o Selenium como webdriver para acessar a página desejada e fazer o web scraping das informações, há outras abordagens que utilizam beautifulsoup + selenium ou scrapy + selenium, contudo para o objetivo do projeto apenas selenium e suas funcionalidades foi possível ter êxito na extração das informações e assim ter apenas uma biblioteca para lidar com as atualizações.

No script é possível manipular datas de início e fim para janela de pesquisa, assim conseguir um número de resultados menor para processamento. As informações coletadas para esse projeto são:

 - Descrição do despacho, onde há informações sobre o despacho como data de publicação e número.
 - Link para página do despacho.
 - Link para o PDF que contém as informações do despacho.

Com essas informações extraídas passamos para outras etapas, download e parser do PDF.

## Download de PDFs com urlib3.

Com a informação do link para download do PDF, utilizei a biblioteca urllib3 para fazer o request com método **GET** e passando o parâmetro de ```preload_content``` como False, essa foi a maneira mais viável até o momento, outras soluções que havia utilizado funcionava em alguns situações e outras apresentava falha e a questão do preload era um problema bem chato pois quando fazia o download era um PDF de um html. Dentro de um contexto faço um ```for``` no ```response``` utilizando ```stream``` e escrevo em um arquivo PDF. 

## Parser do PDF com PyPDF2Reader, REGEX e Pandas.

Extraindo os dados do PDF, a parte mais complexa fica por conta da enorme variedade de como a formação do texto foi realizada. A informação para o projeto que está no PDF é o nome e data de nascimento, com o PyPDF2 temos uma instanciar uma classe que recebe um arquivo PDF e temos um objeto que é possível extrair do texto do PDF que é uma única string, com essa string fazemos a extração dos dados.

O tratamento inicial na string é remover as quebras de linhas e retirar alguns caracteres desnecessários. Com regex utilizando um padrão para fazer um split na string, com o termo "Data de Nascimento" e tratar esses pedaços para identificar o que é nome e a data de nascimento também utilizando regex.


Formato de datas encontradas: ['dd/mm/aaaa', 'd d/mm/aaaa', 'dd /mm/aaaa', 'dd/mm//aaaa', 'dd/mm/ aaaa','dd-mm-aaaa', 'dd-mm-aa', 'dd-mmaaaa']
Formato de nomes encontrados: ['Jose Da`Silva', 'Jose Da-silva']

Utilizado pandas para criar dataframes e salvar os arquivos em csv e outros momentos para acessar esses csv e manipular algumas informações nas funções. 

***
**NOTA:** Alguns arquivos listados abaixo ainda não tive êxito no tratamento dentro pipeline do app.


***
