from selenium import webdriver  
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import os

# options = Options()
# options.add_argument("window-size=400,800")

HERE = os.path.dirname(os.path.abspath(__file__))
path_download = "".join([HERE, "/assets"])


options = webdriver.FirefoxOptions()

# Exemplo de configuração de opções:
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting",False)
options.set_preference("browser.download.dir", path_download)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

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

body_results = browser.find_element(By.ID, "ListaResultados")
list_href = body_results.find_elements(By.CLASS_NAME, "title")

infor = {
    "index": [],
    "date_save": [],
    "item": [],
    "link_page": [],
    "link_pdf": [],
    "name_pdf": []
}

index = 0

for item in list_href:
    link = item.get_attribute("href")
    text = item.find_element(By.CSS_SELECTOR, "span").text

    infor["item"].append(text)
    infor["link_page"].append(link)
    infor["index"].append(index)
    index += 1


browser.get(f"{infor['link_page'][0]}")

sleep(3)

download = browser.find_elements(By.CLASS_NAME, "ThemeGrid_MarginGutter")
download_link_pdf = download[-1].get_attribute("href")

parser_pdf_name = download_link_pdf.split("/")[-1]
print(parser_pdf_name)

browser.get(download_link_pdf)

sleep(1)

button_save = browser.find_element(By.ID, "download")
button_save.click()
# print(infor)

# browser.quit()
