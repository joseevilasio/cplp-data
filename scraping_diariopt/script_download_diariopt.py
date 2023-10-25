from urllib import request
from datetime import datetime
import os
import pandas as pd
from time import sleep


# Path
here = os.path.dirname(os.path.abspath(__file__))
raw_path = "".join([here, "/assets/raw_pdf"])

data = {        
    "date_save_pdf": [], # Date when save pdf
    "pdf_ok": [], # If the pdf has been saved (True or False)
}

spreedsheet = pd.read_csv("".join([raw_path, "/data_scraping_raw.csv"]), sep=";")

for index in range(len(spreedsheet)):

    link_pdf = spreedsheet.link_pdf[index]
    name_pdf = spreedsheet.name_pdf[index]

    if os.path.exists("".join([raw_path, f"/{name_pdf}"])):
        result = True
    else:
        print(f"Download - {link_pdf} -- Arquivo - {name_pdf}")    
        response = True # request.urlretrieve(link_pdf, "".join([raw_path, f"/{name_pdf}"]))
        # result = True if response else result = False

    sleep(2)    

    data["date_save_pdf"] = datetime.now()
    data["pdf_ok"] = result

print(data)

#TODO: Mesclar dados com a planilha
