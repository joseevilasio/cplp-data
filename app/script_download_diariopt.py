import urllib3
from datetime import datetime
import os
import pandas as pd
from time import sleep
from utils import RAW_PATH


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
    print(f"Download Done -> {path_pdf}\n")
    return True


data_download = {
    "date_save_pdf": [],  # Date when save pdf
    "pdf_ok": [],  # If the pdf has been saved (True or False)
}

data_links = pd.read_csv("".join([RAW_PATH, "/data_scraping_raw.csv"]), sep=";")

for index in range(len(data_links)):
    link_pdf = data_links.link_pdf[index]
    name_pdf = data_links.name_pdf[index]
    path_pdf = "".join([RAW_PATH, f"/{name_pdf}"])

    if os.path.exists(path_pdf):
        result = True

    else:
        result = download_pdf(url=link_pdf, path=path_pdf)

    data_download["date_save_pdf"].append(datetime.now().strftime("%d/%m/%Y %H:%M"))
    data_download["pdf_ok"].append(result)


data_download = pd.DataFrame(data_download)

# Concat data download and data infor links
data_complete = pd.concat([data_links, data_download], axis=1)
data_complete.to_csv(
    "".join([RAW_PATH, "/data_scraping_raw_complete.csv"]), sep=";", index=False
)