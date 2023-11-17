## Projeto

## Web Scraping com Selenium.

## Download de PDFs com urlib3.

## Parse PDF com PyPDF2Reader.

Parser inicial com string, "nascimento" utilizando lower() em todo texto extraído

problemas encontrados, fazer regex com data para separar dados

Formato de datas encontradas:['dd/mm/aaaa', 'd d/mm/aaaa', 'dd /mm/aaaa', 'dd/mm//aaaa', 'dd/mm/ aaaa','dd-mm-aaaa']
Formato de nomes encontrados: ['Jose Da`Silva', 'Jose Da-silva']

ATENÇÃO: Tratar os arquivos listados abaixo separados para consolidação de dados.

/home/josejunior/cplp-data/app/../assets/raw_data//pdf/despacho_5259-2023_dr_88-2023.pdf - (Maria clara de Araujo Souza) com ano de data nascimento 2022
/home/josejunior/cplp-data/app/../assets/raw_data//pdf/despacho_4757-2023_dr_78-2023.pdf - (Hugo Martins) com data de nascimento incorreta 5 digitos em ano
despacho_10384-2022_dr_164-2022.pdf (Melquizedeque dos Santos Martins ) data com mês incorreto 18
/home/josejunior/cplp-data/app/../assets/raw_data//pdf/despacho_8752-2021_dr_172-2021.pdf erro ao extrair dados bruto, verificar
/home/josejunior/cplp-data/app/../assets/raw_data//pdf/despacho_7729-2020_dr_152-2020.pdf (Maicon Sarte Miranda), data de nascimento 2019
/home/josejunior/cplp-data/app/../assets/raw_data//pdf/despacho_4833-2019_dr_92-2019.pdf (Raquel da Cunha Carboni Farias)  data de nascimento 2019
/home/josejunior/cplp-data/app/../assets/raw_data//pdf/despacho_1295-2020_dr_20-2020.pdf  Maria Liziane Pinto de Macêdo e Jaine com data sem /

Arquivos de 2019 com padrão diferente dos demais.
/home/josejunior/cplp-data/app/../assets/raw_data//pdf/despacho_6030-2019_dr_123-2019.pdf (Palavras chaves Nascimento aparecendo muitas vezes)


## TODO:

padrão na criação de name pdf 123/1234 ou 12/1234 ou 1234/1234
Inserir filtro de data final - feito
Criar log em arquivo
Arquivos serem criaados com data inicial e final de pesquisa, para ter comparação de janelas, criar banco csv com informações de intervalos e os onde pdfs
Criar controller para comandos em CLI - em andamento
