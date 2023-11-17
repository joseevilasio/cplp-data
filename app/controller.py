import os
from datetime import datetime
from typing import Optional

import pandas as pd
import typer

from app.extract_infor_pdf import extract_text_pdf
from app.utils import (
    PROCESSED_PATH,
    RAW_PATH,
    automode,
    download_pdf,
    update_default,
)
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

    # decision tree to set date
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
        if automode("scraping") is False:
            return None
        else:
            date_start, date_end = automode("scraping")

    # function extract, return file csv
    data = extract_data_from_search_page(date_start, date_end)

    search_range = f"[{date_start}]-[{date_end}]"

    # Convert data in Dataframe
    web_scraping = pd.DataFrame(data)

    # update data in file default
    if auto_mode:
        length_of_pages = [web_scraping["link_page"].count()]
        update_default(length_of_pages, search_range, "scraping")
        print("Updated dafault data.")

    # Export Dataframe in csv
    file_path = "".join([RAW_PATH, search_range, "-web-scraping.csv"])
    web_scraping.to_csv(file_path, sep=";", index=False)
    print(f"Data saved in '{file_path}'")

    return file_path


def get_pdf(auto_mode: Optional[bool] = True, file_path: Optional[str] = None):
    """Receive a pdf file link and download, save infor in file csv
    param auto_mode: `Default - True` If True get pdf according
                    to setting default
    param file_path: `Default - None` Get pdf according to file
    """

    # start read default
    if auto_mode and file_path is None:
        if automode("get_pdf") is False:
            return None
        else:
            file_path, path_automode = automode("get_pdf")

    data_download = {
        "date_save_pdf": [],  # Date when save pdf
        "pdf_ok": [],  # If the pdf has been saved (True or False)
    }

    web_scraping = pd.read_csv("".join([file_path]), sep=";")
    length = len(web_scraping)

    print(f"Found {length} PDFs")
    print("Download PDF")
    with typer.progressbar(length=length, label="Collecting ") as progress:
        for index in progress:
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

        print(f"\nDownload {length}")

    data_download = pd.DataFrame(data_download)

    # update data in file default
    if auto_mode and path_automode:
        download_of_pdf = [data_download["pdf_ok"].count()]
        update_default(download_of_pdf, search_range, "get_pdf")
        print("Updated dafault data.")

    # Concat data download and data infor links
    path_pdf_to_extract = pd.concat([web_scraping, data_download], axis=1)
    file_path_ = "".join([RAW_PATH, f"{search_range}-path-pdf-to-extract.csv"])
    path_pdf_to_extract.to_csv(file_path_, sep=";", index=False)
    print(f"Data saved in '{file_path_}'")

    return file_path_


def extract_infor(
    auto_mode: Optional[bool] = True, file_path: Optional[str] = None
):
    """Extract infor PDF, save infor in file csv
    param auto_mode: `Default - True` If True extract infor according
                    to setting default
    param file_path: `Default - None` Extract infor according to file
    """

    if auto_mode and file_path is None:
        if automode("extract") is False:
            return None
        else:
            file_path, path_automode = automode("extract")

    path_pdf_to_extract = pd.read_csv("".join([file_path]), sep=";")

    data = {
        "search_range": [],
        "description": [],
        "link_page": [],
        "name": [],
        "birth_date": [],
        "extract_complete": [],
    }

    pages = 0
    length = len(path_pdf_to_extract)

    print(f"Found {length} PDFs for extract")
    print("Extracting (name, birth date)")
    with typer.progressbar(length=length, label="Extracting ") as progress:
        for index in progress:
            name_pdf = path_pdf_to_extract.name_pdf[index]
            file_pdf = "".join([RAW_PATH, f"/pdf/{name_pdf}"])
            exist_file = path_pdf_to_extract.pdf_ok[index]
            description = path_pdf_to_extract.description[index]
            link_page = path_pdf_to_extract.link_page[index]
            search_range = path_pdf_to_extract.search_range[index]

            if exist_file:
                list_name, list_birth_date, number_of_pages = extract_text_pdf(
                    file=file_pdf
                )

                if len(list_name) != len(list_birth_date):
                    print(f"Alert! file: {file_pdf}")

                pages = pages + number_of_pages

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

    print(
        f"\nExtracted: {pages} PDF pages, {data_extract['name'].count()} names"
    )

    # update data in file default
    if auto_mode and path_automode:
        data = [pages, data_extract["name"].count()]
        update_default(data, search_range, "extract")
        print("Updated dafault data.")

    file_path_ = "".join(
        [PROCESSED_PATH, f"{search_range}-extract-pdf-complete.csv"]
    )
    data_extract.to_csv(file_path_, sep=";", index=False)
    print(f"Data saved in '{file_path_}'")

    return file_path_
