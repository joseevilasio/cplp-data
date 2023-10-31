from PyPDF2 import PdfReader
import re
import pandas as pd
import os


def extract_text_pdf(file) -> list:
    """Extract name and date of birth from PDF"""

    reader = PdfReader(file) # instance
    number_of_pages = len(reader.pages)

    pattern_date = r"(\d{2}/\d{2}/\d{4})"
    pattern_name = r"^[a-zA-ZÀ-ÖØ-öø-ÿ\s]+$"

    name = []
    birth_date = []

    for number in range(number_of_pages):

        page = reader.pages[number]

        text = page.extract_text().replace("\n", "").replace(" .", "") # remove line break and symbol dot
        word_initial_point = "nascimento" # starting point for cutting

        amount_word_initial_point = len(word_initial_point)
        index_initial = text.find(word_initial_point) + amount_word_initial_point

        extract_infor = text[index_initial:] # information after index initial       

        list_infor_split = re.split(pattern_date, extract_infor) # regex split with pattern date        

        for item in list_infor_split:
            if re.search(pattern_name, item):
                name.append(item.strip())
            elif re.search(pattern_date, item):
                birth_date.append(item)

    return name, birth_date


# Path
here = os.path.dirname(os.path.abspath(__file__))
raw_path = "".join([here, "/assets/raw_pdf"])
processed_data = "".join([here, "/assets/processed_data"])

data_scraping_complete = pd.read_csv("".join([raw_path, "/data_scraping_raw_complete.csv"]), sep=";")

data = {
    "description": [],
    "link_page": [],
    "name": [],
    "birth_date": [],
    "extract_complete": [],
}

for index in range(len(data_scraping_complete)):

    name_pdf = data_scraping_complete.name_pdf[index]
    file_pdf = "".join([raw_path, f"/{name_pdf}"])
    exist_file = data_scraping_complete.pdf_ok[index]

    data["description"].append(data_scraping_complete.description[index])
    data["link_page"].append(data_scraping_complete.link_page[index])

    if exist_file:
        name, birth_date = extract_text_pdf(file=file_pdf)
    else:
        print(f"File no exist -> {file_pdf}")

