import os
from datetime import datetime
from typing import Optional

import pandas as pd

from extract_infor_pdf import extract_text_pdf
from utils import PROCESSED_PATH, RAW_PATH, download_pdf
from web_scraping import extract_data_from_search_page


def web_scraping(
    date_start: Optional[str] = None,
    date_end: Optional[str] = None,
    auto_mode: Optional[bool] = False,
):
    """Extract data from search page of the site diariodeportugal.pt
    for file.csv according to date information.
    Args:
    date_start -> None, filter search today
    date_end -> None, filter search today
    auto_mode -> If True filter search according to file logdatesearch.csv
    """

    # TODO: Implementar decisões

    # function extract, return file csv
    extract_data_from_search_page(date_start, date_end)


def download_pdf_(
    auto_mode: Optional[bool] = True, file_path: Optional[str] = None
):
    """"""

    data_download = {
        "date_save_pdf": [],  # Date when save pdf
        "pdf_ok": [],  # If the pdf has been saved (True or False)
    }

    data_links = pd.read_csv(
        "".join([RAW_PATH, "/data_scraping_raw.csv"]), sep=";"
    )

    for index in range(len(data_links)):
        link_pdf = data_links.link_pdf[index]
        name_pdf = data_links.name_pdf[index]
        path_pdf = "".join([RAW_PATH, f"/{name_pdf}"])

        if os.path.exists(path_pdf):
            result = True

        else:
            result = download_pdf(url=link_pdf, path=path_pdf)

        data_download["date_save_pdf"].append(
            datetime.now().strftime("%d/%m/%Y %H:%M")
        )
        data_download["pdf_ok"].append(result)

    data_download = pd.DataFrame(data_download)

    # Concat data download and data infor links
    data_complete = pd.concat([data_links, data_download], axis=1)
    data_complete.to_csv(
        "".join([RAW_PATH, "/data_scraping_raw_complete.csv"]),
        sep=";",
        index=False,
    )


def extract_infor(
    auto_mode: Optional[bool] = True, file_path: Optional[str] = None
):
    """"""
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
            [
                data["link_page"].append(link_page)
                for x in range(len(list_name))
            ]
            [
                data["extract_complete"].append(True)
                for x in range(len(list_name))
            ]

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
