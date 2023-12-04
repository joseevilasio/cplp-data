# CPLP DATA

## Compilação de informações sobre a Comunidade dos Países de Língua Portuguesa

A Comunidade dos Países de Língua Portuguesa (CPLP) é uma organização de cooperação entre os estados membros de países e povos que partilham a língua portuguesa, com o objetivo de promoção da cooperação mutuamente vantajosa, desenvolvimento e reciprocidade de tratamento. Para saber mais visite o [site oficial](https://www.cplp.org/).

## Objetivo

O projeto tem como objetivo compilar informações resultantes das ações da CPLP para servir de apoio para estudos, análise de dados e facilitar a consulta dos dados por parte dos cidadãos da CPLP.

## Primeiro Projeto - Estatuto de Igualdade de Direitos e Deveres [Em desenvolvimento]

O estatuto de igualdade é acordo bilateral entre Brasil e Portugual. Que de acordo com as informações do site ePortugal: "O Estatuto de Igualdade de Direitos e Deveres confere a cidadãos brasileiros residentes em Portugal um conjunto de direitos nas áreas do trabalho, economia, política, entre outras. Este estatuto pode ser pedido pelo correio ou presencialmente."

*Na primeira fase a coleta de informações vai se concentar do lado de Portugal.*

O estatuto há três possibilidades de solicitação: 
1) Estatuto de Igualdade de Direitos e Deveres;
2) Estatuto de Igualdade de Direitos Políticos;
3) Estatuto de Igualdade de Direitos e Deveres e de Direitos Políticos.

Cada solicitação tem seus requisitos, o principal requisito é o título residência para morar em Portugal, com a nova residência em vigor que é a **Autorização de Residência CPLP** que teve um elevado número de emissões por conta da facilidade. Isso levou ao aumento de solicitações do Estatuto de Igualdade de Direitos e Deveres, o projeto consiste na coleta dessas informações.

1) Fazer um web scraping da página [*Diário da República*](https://diariodarepublica.pt/dr/home) para coletar arquivos em PDF dos estatutos concedidos a brasileiros;
2) Extrair as informações desses arquivos PDFs de forma nominal a quem foi concedido, data, despacho;
3) Gerar insights a partir do dados.

Utilizado as seguintes ferramentas:
```
- Python
- Selenium
- Pandas
- PyPDF2
- Typer
```

Informações mais detalhadas sobre implementação, a utilização da tecnologias e dificuldades encontradas, [veja aqui!](https://github.com/joseevilasio/cplp-data/blob/main/docs/about_project.md)

### 📋 Pré-requisitos

```
Python
Poetry
```
### 🔧 Instalação

Fazer um clone do repositório do projeto:
```
$ gh repo clone joseevilasio/cplp-data
```
Instalar as dependências do projeto com o Poetry:
```
$ poetry install
```

### 📦 Como funciona

A utilização é realizada através do CLI. É possível utilizar a função 'automode' para de acordo o arquivo *default.csv* buscar os intervalos prédefinidos de pesquisa, ou inserir a data inicial/final com o 'start-web-scraping'. Com as informações do web-scraping inicia o download dos arquivos PDFs com a função 'start-download-pdf' ao passar o caminho do arquivo que deseja fazer o download ou ativar o automode que busca referência no em *default.csv*, em seguida a função 'start-extract-pdf' extrai as informações para um arquivo csv.

```
$ poetry run cplpdata --help
```

![cplp-data/assets/imgs/cli-help.png](https://github.com/joseevilasio/cplp-data/blob/main/assets/imgs/cli-help.png)

Comandos:
 - report
 - start-automode
 - start-download-pdf
 - start-extract-pdf
 - start-web-scraping

![cplp-data/assets/imgs/cli-help.png](https://github.com/joseevilasio/cplp-data/blob/main/assets/imgs/cli-screenrecord.gif)

