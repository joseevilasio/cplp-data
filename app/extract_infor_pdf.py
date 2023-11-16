import re

from PyPDF2 import PdfReader

from app.utils import if_age_is_valid, remove_space_between_digit


def extract_text_pdf(file: str, verbose: bool = False) -> list:
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
            .replace(" ‘ ", "")
        )  # remove line break and symbol dot

        word = ["nascimento", "nasc"]
        word = word[1] if text.lower().find(word[0]) == -1 else word[0]

        word_initial_point = word # starting point for cutting

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

        if verbose:
            print(extract_infor)
            print(list_infor_split)
            print(f"Extract start -> page: {number + 1} path: {file}")

        for item in list_infor_split:
            if re.search(pattern_name, item.replace("/", "")):
                name.append(item.strip().replace("/", "-"))
                if verbose:
                    print(f"Name: {item.strip().replace('/','-')} --- ", end="")
            elif re.search(pattern_date, item) and if_age_is_valid(item):
                birth_date.append(item)
                if verbose:
                    print(f"Date: {item}")

    return [name, birth_date, number_of_pages]
