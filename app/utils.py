import os
import re
from datetime import datetime
from time import sleep

import urllib3

# Path
ROOT_PATH: str = os.path.dirname(__file__)
RAW_PATH: str = os.path.join(ROOT_PATH, "..", "assets/raw_data")
PROCESSED_PATH: str = os.path.join(ROOT_PATH, "..", "assets/processed_data")


def create_pdf_name(text: str) -> str:
    """transforms the description into a name for pdf file"""

    pattern = r"(\b\d{3,5}/\d{4}\b)"
    list_re = re.split(pattern, text)
    pdf_name = "".join(["despacho_", list_re[1], "_dr_", list_re[3], ".pdf"])
    pdf_name = pdf_name.replace("/", "-")

    return pdf_name


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


def if_age_is_valid(date: str) -> bool:
    """Comparing dates to check if you are of legal age"""

    converted_date = datetime.strptime(date, "%d/%m/%Y").date()
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

    print(f"Get -> {url}")

    sleep(2)

    if content_type == "application/pdf":
        with open(path, "wb") as file:
            for chunk in response.stream(1024):
                file.write(chunk)

    else:
        print("Fail download")
        return False

    response.release_conn()
    print(f"Download Done -> {path}\n")
    return True
