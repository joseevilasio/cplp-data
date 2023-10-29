from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os
import math
import pandas as pd


# Path
here = os.path.dirname(os.path.abspath(__file__))
raw_path = "".join([here, "/assets/raw_pdf"])

# Dict model data
data = {
    "description": [],  # description
    "link_page": [],  # link page 'despacho'
    "link_pdf": [],  # link page file download
    "name_pdf": [],  # name pdf file
}

# Config webdriver
options = webdriver.FirefoxOptions()
options.set_preference("headless", True)

# Instance
browser = webdriver.Firefox(options=options)

# Get initial
browser.get("https://diariodarepublica.pt/dr/home")

sleep(3)

# Search
text_for_research = "Concede o estatuto de igualdade de direitos e deveres a vários cidadãos brasileiros"
input_place = browser.find_element(By.TAG_NAME, "input")  # Find the search box
input_place.send_keys(text_for_research)  # Insert text

buttom_search = browser.find_element(By.ID, "b2-b2-myButton2")  # Find the buttom submit
buttom_search.click()  # Submit

sleep(3)

# Search filter
checkbox_legislacao = browser.find_elements(
    By.CLASS_NAME, "checkbox"
)  # Find the checkbox 'Legislação'
checkbox_legislacao[1].click()  # Check

sleep(3)

checkbox_serie_plus = browser.find_element(
    By.XPATH, "//*[@id='Serie_Titulo']/div[1]/span"
)  # Find area to expand option 'Série'
checkbox_serie_plus.click()

sleep(2)

checkbox_serie = browser.find_elements(
    By.CLASS_NAME, "checkbox"
)  # Find the checkbox 'Série II'
checkbox_serie[4].click()  # Check

sleep(2)

# Filter date
date_published = browser.find_element(By.ID, "Input_dataPublicacaoDe") # Find box filter date
date_published.send_keys("2020-01-01") # Insert date fmt AAAA-MM-DD
exit_calendar = browser.find_element(By.XPATH, "//*[@id='FiltrarResultados']/div[1]/span").click()
date_published_submit = browser.find_element(By.XPATH, "//*[@id='Pesquisa2']/div[3]/button/span")
date_published_submit.click()

sleep(2)

# Check amount pages
amount_search = browser.find_element(By.ID, "b3-Titulo")
extract_number = amount_search.find_elements(By.CSS_SELECTOR, "span")[3].text.split(" ")[0]
amount_search_number = int(extract_number)
total_pages = math.ceil(amount_search_number / 200)

# Expand results 200
if amount_search_number > 25:
    expand_list = browser.find_element(By.XPATH, "//*[@id='ResultadosEncontrados']/div[2]/div[2]/div/div/span").click()
    select_200_items = browser.find_element(By.XPATH, "//*[@id='transitionContainer']/div/div[2]/div/div/div[3]/a/span").click()
    sleep(2)

# Data extraction

# Navigate between the pages
i = total_pages # initial countdown

for page in range(total_pages):
    
    body_results = browser.find_element(By.ID, "ListaResultados")  # Find data
    list_href_page = body_results.find_elements(
        By.CLASS_NAME, "title"
    )  # Find element in data (create list)

    # Collects links from the current page
    for item_href in list_href_page:
        link_page = item_href.get_attribute("href")  # Link for page 'despacho'
        text_page = item_href.find_element(
            By.CSS_SELECTOR, "span"
        ).text  # Extraction text 'despacho'

        data["description"].append(text_page)
        data["link_page"].append(link_page)

    i -= 1 # countdown

    # next page
    if total_pages > 1 and i != 0:
        next_page = browser.find_element(By.ID, "b27-Next").click()
        sleep(2)


for link in data["link_page"]:
    # Get link page 'despacho'
    browser.get(f"{link}")

    sleep(3)

    list_elements_page_download = browser.find_elements(
        By.CLASS_NAME, "ThemeGrid_MarginGutter"
    )  # List of elements in page
    download_link_pdf = list_elements_page_download[-1].get_attribute(
        "href"
    )  # Extraction link file pdf
    parser_name_pdf = download_link_pdf.split("/")[
        -1
    ]  # Parser link file pdf to pdf name

    data["link_pdf"].append(download_link_pdf)
    data["name_pdf"].append(parser_name_pdf)

# Close webdriver
browser.quit()

# Export data for spreadsheet
data_for_csv = pd.DataFrame(data)
data_for_csv.to_csv("".join([raw_path, "/data_scraping_raw.csv"]), sep=";", index=False)
