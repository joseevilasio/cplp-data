import os
import re
from datetime import datetime
from time import sleep

import pandas as pd
import urllib3

# Path
ROOT_PATH: str = os.path.dirname(__file__)
LOG_PATH: str = os.path.join(ROOT_PATH, "/log/")
RAW_PATH: str = os.path.join(ROOT_PATH, "..", "assets/raw_data/")
PROCESSED_PATH: str = os.path.join(ROOT_PATH, "..", "assets/processed_data/")
MERGE: str = os.path.join(ROOT_PATH, "..", "assets/merge/")


def create_pdf_name(text: str) -> str:
    """transforms the description into a name for pdf file"""

    pattern = r"(\b\d{1,5}/\d{4}\b)"
    list_re = re.split(pattern, text)
    pdf_name = "".join(["despacho_", list_re[1], "_dr_", list_re[3], ".pdf"])
    pdf_name = pdf_name.replace("/", "-")

    return pdf_name


def remove_space_between_digit(text: str) -> str:
    """Removes spaces between digits, before and after."""

    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    i = 0
    length = len(text)
    text_compile = []

    for character in text:
        if (length - 1) == i:
            pass
        elif character == " " and text[i - 1] in numbers:
            pass
        elif character == " " and text[i + 1] in numbers:
            pass
        else:
            text_compile.append(character)
        i += 1
    result = "".join(text_compile)

    return result


def if_age_is_valid(date: str) -> bool:
    """Comparing dates to check if you are of legal age"""

    try:
        converted_date = datetime.strptime(date, "%d/%m/%Y").date()
    except:
        print(f"Not added. Error with date -> '{date}'")
        return False

    today = datetime.now().strftime("%d/%m/%Y")
    converted__today = datetime.strptime(today, "%d/%m/%Y").date()

    age = converted__today.year - converted_date.year

    if age >= 18:
        return True
    else:
        return False


def download_pdf(url: str, path: str) -> bool:
    """Receive a pdf file link and download"""

    http = urllib3.PoolManager()

    response = http.request("GET", url, preload_content=False)
    content_type = response.headers["content-type"]

    sleep(2)

    if content_type == "application/pdf":
        with open(path, "wb") as file:
            for chunk in response.stream(1024):
                file.write(chunk)

    else:
        print("Fail download")
        return False

    response.release_conn()
    return True


def automode(phase: str) -> list:
    """Check the standard mode and start the phase according to the data
    already collected.
    param phase: Type mode `scraping`, `get_pdf`, `extract`
    """
    default = pd.read_csv("./app/log/default.csv", sep=";")

    for index in range(len(default)):
        if default.length_of_pages[index] <= 0 and phase == "scraping":
            search_range = default.search_range[index].split("]-[")
            date_start = search_range[0].replace("[", "")
            date_end = search_range[1].replace("]", "")

            return [date_start, date_end]

        elif default.download_of_pdf[index] <= 0 and phase == "get_pdf":
            search_range = default.search_range[index]
            file_path = "".join([RAW_PATH, f"{search_range}-web-scraping.csv"])

            return [file_path, True]

        elif default.pdf_pages_extracted[index] <= 0 and phase == "extract":
            search_range = default.search_range[index]
            file_path = "".join(
                [RAW_PATH, f"{search_range}-path-pdf-to-extract.csv"]
            )

            return [file_path, True]

    if phase == "scraping":
        print("There are search range to web scraping!")
        return False

    if phase == "get_pdf":
        print("There are no PDFs to download!")
        return False

    if phase == "extract":
        print("There are no PDFs to extract!")
        return False


def update_default(data: list, range: str, phase: str):
    """Insert new data the phase according to the data
    already collected.
    param data: list of data.
    param range: search range.
    param phase: Type mode `scraping`, `get_pdf`, `extract`.
    """

    df = pd.read_csv("./app/log/default.csv", sep=";")
    row = df.index[df.eq(range).any(axis=1)].values[0]

    if phase == "scraping":
        df.at[row, "length_of_pages"] = data[0]

    elif phase == "get_pdf":
        df.at[row, "download_of_pdf"] = data[0]

    elif phase == "extract":
        df.at[row, "pdf_pages_extracted"] = data[0]
        df.at[row, "length_of_name_extracted"] = data[1]

    df.to_csv("./app/log/default.csv", sep=";", index=False)
