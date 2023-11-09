import os
from datetime import datetime
from typing import Optional

import pandas as pd

from app.extract_infor_pdf import extract_text_pdf
from app.utils import PROCESSED_PATH, RAW_PATH, automode, download_pdf
from app.web_scraping import extract_data_from_search_page


def web_scraping(
    date_start: Optional[str] = None,
    date_end: Optional[str] = None,
    auto_mode: Optional[bool] = False,
):
    """Extract data from search page of the site diariodeportugal.pt
    for file.csv according to date information.
    param date_start: `Default - None`, filter search today
    param date_end: `Default - None`, filter search today
    param auto_mode: `Default - False`If True filter search according
                    to setting default
    """

    if auto_mode is False:
        if date_start and date_end:
            pass
        elif date_start and date_end is None:
            date_end = datetime.now().strftime("%Y-%m-%d")
        elif date_start is None and date_end:
            date_start = datetime.now().strftime("%Y-%m-%d")
        else:
            date_start = date_end = datetime.now().strftime("%Y-%m-%d")
    elif auto_mode:
        date_start, date_end = automode("scraping")

    # function extract, return file csv
    data = extract_data_from_search_page(date_start, date_end)

    # Export data for csv
    web_scraping = pd.DataFrame(data)
    web_scraping.to_csv(
        "".join([RAW_PATH, f"[{date_start}]-[{date_end}]-web-scraping.csv"]),
        sep=";",
        index=False,
    )


def get_pdf(auto_mode: Optional[bool] = True, file_path: Optional[str] = None):
    """Receive a pdf file link and download, save infor in file csv
    param auto_mode: `Default - True` If True get pdf according
                    to setting default
    param file_path: `Default - None` Get pdf according to file
    """

    if auto_mode:
        file_path = automode("get_pdf")

    data_download = {
        "date_save_pdf": [],  # Date when save pdf
        "pdf_ok": [],  # If the pdf has been saved (True or False)
    }

    web_scraping = pd.read_csv("".join([file_path]), sep=";")

    for index in range(len(web_scraping)):
        link_pdf = web_scraping.link_pdf[index]  # link download
        name_pdf = web_scraping.name_pdf[index]  # pdf name
        path_pdf = "".join([RAW_PATH, f"/pdf/{name_pdf}"])  # save
        search_range = web_scraping.search_range[index]

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
    path_pdf_to_extract = pd.concat([web_scraping, data_download], axis=1)
    path_pdf_to_extract.to_csv(
        "".join([RAW_PATH, f"{search_range}-path-pdf-to-extract.csv"]),
        sep=";",
        index=False,
    )


def extract_infor(
    auto_mode: Optional[bool] = True, file_path: Optional[str] = None
):
    """Extract infor PDF, save infor in file csv
    param auto_mode: `Default - True` If True extract infor according
                    to setting default
    param file_path: `Default - None` Extract infor according to file
    """

    if auto_mode:
        file_path = automode("extract")

    path_pdf_to_extract = pd.read_csv("".join([file_path]), sep=";")

    data = {
        "search_range": [],
        "description": [],
        "link_page": [],
        "name": [],
        "birth_date": [],
        "extract_complete": [],
    }

    for index in range(len(path_pdf_to_extract)):
        name_pdf = path_pdf_to_extract.name_pdf[index]
        file_pdf = "".join([RAW_PATH, f"/{name_pdf}"])
        exist_file = path_pdf_to_extract.pdf_ok[index]
        description = path_pdf_to_extract.description[index]
        link_page = path_pdf_to_extract.link_page[index]
        search_range = path_pdf_to_extract.search_range[index]

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
            [
                data["search_range"].append(search_range)
                for x in range(len(list_name))
            ]

        else:
            print(f"File no exist -> {file_pdf}")

            data["extract_complete"].append(False)
            data["name"].append(None)
            data["birth_date"].append(None)
            data["description"].append(description)
            data["link_page"].append(link_page)
            data["search_range"].append(search_range)

    data_extract = pd.DataFrame(data)
    data_extract.to_csv(
        "".join([PROCESSED_PATH, f"{search_range}-extract-pdf-complete.csv"]),
        sep=";",
        index=False,
    )

    print(len(data["extract_complete"]))
    print(len(data["birth_date"]))
    print(len(data["description"]))
    print(len(data["link_page"]))
    print(len(data["name"]))
