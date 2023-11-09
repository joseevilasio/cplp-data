# CPLP DATA

## Compilação de informações sobre a Comunidade dos Países de Língua Portuguesa

A Comunidade dos Países de Língua Portuguesa (CPLP) é uma organização de cooperação entre os estados membros de países e povos que partilham a língua portuguesa, com o objetivo de promoção da cooperação mutuamente vantajosa, desenvolvimento e reciprocidade de tratamento. Para saber mais visite o [site oficial](https://www.cplp.org/).

## Objetivo

O projeto tem como objetivo compilar informações resultantes das ações da CPLP para servir de apoio para estudos, análise de dados e facilitar a consulta dos dados por parte dos cidadãos da CPLP.

## Primeiro Projeto - Estatuto de Igualdade de Direitos e Deveres

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

Informações mais detalhadas sobre implementação, a utilização da tecnologias e dificuldades encontradas, consulte o [about](ABOUT.md)
