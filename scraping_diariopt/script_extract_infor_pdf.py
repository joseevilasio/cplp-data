from PyPDF2 import PdfReader
import re

# TODO: Fazer um for com arquivos pdf

reader = PdfReader("scraping_diariopt/assets/raw_pdf/0004400044.pdf")
page = reader.pages[0] # Pode haver mais de uma pagina
num_pages = len(reader.pages)


text = page.extract_text().replace("\n", "").replace(" .", "") #retirar quebra de linhas e retirar "."
texto_para_ponto_inicial = "nascimento"
tam_texto_para_ponto_inicial = len(texto_para_ponto_inicial)
indice_inicial = text.find(texto_para_ponto_inicial) + tam_texto_para_ponto_inicial

extract = text[indice_inicial:]

date = r"(\d{2}/\d{2}/\d{4})"
name = r"^[a-zA-ZÀ-ÖØ-öø-ÿ\s]+$"

list_objs_re = re.split(date, extract)

data = {
    "name": [],
    "date_born": []
}

for item in list_objs_re:
    if re.search(name, item):
        data["name"].append(item.strip())
    elif re.search(date, item):
        data["date_born"].append(item)

print(data)
