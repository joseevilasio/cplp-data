from script_web_scraping import extract_data_from_search_page
from typing import Optional



def web_scraping(date_start:  Optional[str] = None, date_end:  Optional[str] = None, mode: Optional[bool] = False):
    """Extract data from search page of the site diariodeportugal.pt
    for file.csv according to date information.
    Args: 
    date_start -> None, filter search today
    date_end -> None, filter search today
    mode -> Default False, if True filter search according to file logdatesearch.csv
    """

    #TODO: Implementar decisões

    # function extract, return file csv
    extract_data_from_search_page(date_start, date_end)    


def download_pdf():
    pass


def extract_infor():
    pass
