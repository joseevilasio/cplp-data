import re

from PyPDF2 import PdfReader
from rich import print

from app.utils import if_age_is_valid, remove_space_between_digit


def extract_text_pdf(file: str, verbose: bool = False) -> list:
    """Extract name and date of birth from PDF"""

    reader = PdfReader(file)  # instance
    number_of_pages = len(reader.pages)

    pattern_date = r"(\d{1,2}\s?\d{0,1}\s?/\s?\d{2}\s?/\s?\d{4})"
    pattern_name = r"^[a-zA-ZÀ-ÖØ-öø-ÿ\s]+$"
    pattern_split = r"data\s*d[et]?\s*nascimento|datade\s*nascimento|data\s*nascimento"

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
            .replace("Nome", "")
            .replace("nome", "")
        )  # remove line break and symbol dot

        list_text = re.split(
            pattern_split, text, flags=re.IGNORECASE
        )  # list of text

        if verbose:
            print(f"[green]{list_text}[/green]")

        for extract_infor in list_text:
            extract_infor = remove_space_between_digit(extract_infor)
            extract_infor = extract_infor.replace("-", "/")

            list_infor_split = re.split(
                pattern_date, extract_infor
            )  # regex split with pattern date

            if verbose:
                print(f"[blue]{list_infor_split}[/blue]\n")
                print(
                    f"[bold]Extract start-> pg:{number + 1} path:{file}[/bold]"
                )

            for item in list_infor_split:
                if re.search(pattern_name, item.replace("/", "")):
                    name.append(item.strip().replace("/", "-"))
                    if verbose:
                        print(
                            f"Name: {item.strip().replace('/','-')} --- ",
                            end="",
                        )
                elif re.search(pattern_date, item) and if_age_is_valid(item):
                    birth_date.append(item)
                    if verbose:
                        print(f"Date: {item}")

    return [name, birth_date, number_of_pages]
