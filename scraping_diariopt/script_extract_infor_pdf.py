from PyPDF2 import PdfReader
import re
import pandas as pd
import os


def remove_space_between_digit(text: str) -> str:
    """Removes spaces between digits, before and after."""

    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    i = 0
    text_compile = []

    for character in text:        
        if character == " " and text[i - 1] in numbers:
            pass        
        elif character == " " and text[i + 1] in numbers:
            pass        
        else:
            text_compile.append(character)
        i += 1    
    result = "".join(text_compile)

    return result


def extract_text_pdf(file) -> list:
    """Extract name and date of birth from PDF"""

    reader = PdfReader(file) # instance
    number_of_pages = len(reader.pages)

    pattern_date = r"(\d{1,2}\s?\d{0,1}\s?/\s?\d{2}\s?/\s?\d{4})"
    pattern_name = r"^[a-zA-ZÀ-ÖØ-öø-ÿ\s]+$"

    name = []
    birth_date = []

    for number in range(number_of_pages):

        page = reader.pages[number]

        text = page.extract_text().replace("\n", "").replace(".", "").replace("//", "/").replace("’", "") # remove line break and symbol dot
        word_initial_point = "nascimento" # starting point for cutting

        amount_word_initial_point = len(word_initial_point)
        index_initial = text.find(word_initial_point) + amount_word_initial_point

        extract_infor = text[index_initial:] # information after index initial
        extract_infor = remove_space_between_digit(extract_infor)

        list_infor_split = re.split(pattern_date, extract_infor) # regex split with pattern date

        print(f"Extract start -> page: {number + 1} path: {file}")

        for item in list_infor_split:
            if re.search(pattern_name, item):
                name.append(item.strip())
                print(f"Name: {item.strip()} --- ", end="")
            elif re.search(pattern_date, item):
                birth_date.append(item.replace(" ", ""))
                print(f"Date: {item.strip()}")
            

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
    description = data_scraping_complete.description[index]
    link_page = data_scraping_complete.link_page[index]    

    if exist_file:
        list_name, list_birth_date = extract_text_pdf(file=file_pdf)
        
        [data["name"].append(name) for name in list_name]
        [data["birth_date"].append(birth_date) for birth_date in list_birth_date]
        [data["description"].append(description) for x in range(len(list_name))]
        [data["link_page"].append(link_page) for x in range(len(list_name))]
        [data["extract_complete"].append(True) for x in range(len(list_name))]

    else:
        print(f"File no exist -> {file_pdf}")
        
        data["extract_complete"].append(False)
        data["name"].append(None)
        data["birth_date"].append(None)
        data["description"].append(description)
        data["link_page"].append(link_page)


# data_extract = pd.DataFrame(data)
# data_extract.to_csv(
#     "".join([processed_data, "/processed_data_extract.csv"]), sep=";", index=False
# )

print(len(data["extract_complete"]))
print(len(data["birth_date"]))
print(len(data["description"]))
print(len(data["link_page"]))
print(len(data["name"]))
