from selenium import webdriver  
from selenium.webdriver.common.by import By
from time import sleep
import os
from datetime import datetime
import pandas as pd
from urllib import request


here = os.path.dirname(os.path.abspath(__file__))
path_download = "".join([here, "/assets/raw_pdf"])

options = webdriver.FirefoxOptions()

# options.set_preference("browser.download.folderList", 2)
# options.set_preference("browser.download.manager.showWhenStarting",False)
# options.set_preference("browser.download.dir", path_download)
# options.set_preference("pdfjs.disabled", True)
options.set_preference("headless", True)

browser = webdriver.Firefox(options=options)

browser.get("https://diariodarepublica.pt/dr/home")

sleep(3)

input_place = browser.find_element(By.TAG_NAME, "input")
input_place.send_keys("Concede o estatuto de igualdade de direitos e deveres a vários cidadãos brasileiros")

buttom_search = browser.find_element(By.ID, "b2-b2-myButton2")
buttom_search.click()

sleep(3)

checkbox_legislacao = browser.find_elements(By.CLASS_NAME, "checkbox")
checkbox_legislacao[1].click()

sleep(3)

checkbox_serie_plus = browser.find_element(By.XPATH, "//*[@id='Serie_Titulo']/div[1]/span")
checkbox_serie_plus.click()

sleep(0.5)

checkbox_serie = browser.find_elements(By.CLASS_NAME, "checkbox")
checkbox_serie[4].click()

sleep(2)

#TODO: Configurar para ter 200 resultados na pagina e avançar para próxima paginas
#TODO: Filtar datas
#TODO: Ordenar resultado de pesquisa

body_results = browser.find_element(By.ID, "ListaResultados")
list_href = body_results.find_elements(By.CLASS_NAME, "title")

infor = {
    "index": [], #index
    "date_save": [], #saves date when the download
    "item": [], #description
    "link_page": [], #link page decreto
    "link_pdf": [], #link page file download
    "name_pdf": [] #name pdf file
}

index = 0

for item in list_href:
    link = item.get_attribute("href")
    text = item.find_element(By.CSS_SELECTOR, "span").text

    infor["item"].append(text)
    infor["link_page"].append(link)
    infor["index"].append(index)
    index += 1


# TODO: Concluir coleta de dados de link das paginas fazer for em cima de dict com as informações

for item in infor["link_page"]:

    print(f"Abrir pagina {item} - >")

    browser.get(f"{item}")

    print("Aberta!")

    sleep(3)

    download = browser.find_elements(By.CLASS_NAME, "ThemeGrid_MarginGutter")
    download_link_pdf = download[-1].get_attribute("href")

    parser_pdf_name = download_link_pdf.split("/")[-1]   

    request.urlretrieve(download_link_pdf, "".join([path_download, f"/{parser_pdf_name}"]))

    sleep(2)    

    infor["date_save"] = datetime.now()
    infor["name_pdf"] = parser_pdf_name
    infor["link_pdf"] = download_link_pdf

    print("Finalizado! - > Proximo")

    sleep(1)


data = pd.DataFrame(infor)
data.to_excel("/assets/data_scraping_raw.xlsx", index=False)

browser.quit()
