import re

import pandas as pd
from PyPDF2 import PdfReader

from utils import (
    PROCESSED_PATH,
    RAW_PATH,
    if_age_is_valid,
    remove_space_between_digit,
)


def extract_text_pdf(file) -> list:
    """Extract name and date of birth from PDF"""

    reader = PdfReader(file)  # instance
    number_of_pages = len(reader.pages)

    pattern_date = r"(\d{1,2}\s?\d{0,1}\s?/\s?\d{2}\s?/\s?\d{4})"
    pattern_name = r"^[a-zA-ZÀ-ÖØ-öø-ÿ\s]+$"

    name = []
    birth_date = []

    for number in range(number_of_pages):
        page = reader.pages[number]

        text = (
            page.extract_text()
            .replace("\n", "")
            .replace(".", "")
            .replace("//", "/")
            .replace("’", "")
        )  # remove line break and symbol dot
        word_initial_point = "nascimento"  # starting point for cutting

        amount_word_initial_point = len(word_initial_point)
        index_initial = (
            text.lower().find(word_initial_point) + amount_word_initial_point
        )

        extract_infor = text[index_initial:]  # information after index initial
        extract_infor = remove_space_between_digit(extract_infor)
        extract_infor = extract_infor.replace("-", "/")

        list_infor_split = re.split(
            pattern_date, extract_infor
        )  # regex split with pattern date

        print(f"Extract start -> page: {number + 1} path: {file}")

        for item in list_infor_split:
            if re.search(pattern_name, item):
                name.append(item.strip())
                print(f"Name: {item.strip()} --- ", end="")
            elif re.search(pattern_date, item) and if_age_is_valid(item):
                birth_date.append(item)
                print(f"Date: {item}")

    return name, birth_date


data_scraping_complete = pd.read_csv(
    "".join([RAW_PATH, "/data_scraping_raw_complete.csv"]), sep=";"
)

data = {
    "description": [],
    "link_page": [],
    "name": [],
    "birth_date": [],
    "extract_complete": [],
}

for index in range(len(data_scraping_complete)):
    name_pdf = data_scraping_complete.name_pdf[index]
    file_pdf = "".join([RAW_PATH, f"/{name_pdf}"])
    exist_file = data_scraping_complete.pdf_ok[index]
    description = data_scraping_complete.description[index]
    link_page = data_scraping_complete.link_page[index]

    if exist_file:
        list_name, list_birth_date = extract_text_pdf(file=file_pdf)

        [data["name"].append(name) for name in list_name]
        [
            data["birth_date"].append(birth_date)
            for birth_date in list_birth_date
        ]
        [
            data["description"].append(description)
            for x in range(len(list_name))
        ]
        [data["link_page"].append(link_page) for x in range(len(list_name))]
        [data["extract_complete"].append(True) for x in range(len(list_name))]

    else:
        print(f"File no exist -> {file_pdf}")

        data["extract_complete"].append(False)
        data["name"].append(None)
        data["birth_date"].append(None)
        data["description"].append(description)
        data["link_page"].append(link_page)


data_extract = pd.DataFrame(data)
data_extract.to_csv(
    "".join([PROCESSED_PATH, "/processed_data_extract.csv"]),
    sep=";",
    index=False,
)

print(len(data["extract_complete"]))
print(len(data["birth_date"]))
print(len(data["description"]))
print(len(data["link_page"]))
print(len(data["name"]))
