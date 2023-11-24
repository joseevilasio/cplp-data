from typing import Optional

import pandas as pd
import typer
from rich import print
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from app.controller import extract_infor, get_pdf, web_scraping, merge_all
from app.utils import PROCESSED_PATH

app = typer.Typer(name="CPLP DATA CLI", add_completion=False)


@app.command()
def merge():
    """Merge all files"""

    merge_all(PROCESSED_PATH)
    

@app.command()
def start_web_scraping(
    date_start: str | None = None,
    date_end: str | None = None,
    auto_mode: bool = False,
):
    """Start web scraping and data collected"""

    print("[bold green]Start Web-Scraping![/bold green] :mag:")

    web_scraping(date_start, date_end, auto_mode)

    print("[bold green]DONE![/bold green] :nerd_face:")


@app.command()
def start_download_pdf(
    path: Annotated[Optional[str], typer.Argument()] = None
):
    """Start download PDF"""

    print("[bold green]Start download![/bold green] :file_folder:")

    get_pdf(file_path=path)

    print("[bold green]DONE![/bold green] :nerd_face:")


@app.command()
def start_extract_pdf(path: Annotated[Optional[str], typer.Argument()] = None):
    """Start extract info in PDF"""

    print("[bold green]Start extract![/bold green] :detective:")

    extract_infor(file_path=path)

    print("[bold green]DONE![/bold green] :nerd_face:")


@app.command()
def start_automode():
    """Start AUTOMODE according to the configured default"""

    print("[bold green]Start AUTOMODE![/bold green] :robot_face:")

    print(
        """[bold navy_blue] -- web scraping -- [/bold navy_blue]
        :robot_face: :mag:"""
    )
    web_scraping(auto_mode=True)

    print(
        """[bold blue1] -- download PDF -- [/bold blue1] :robot_face:
        :file_folder:"""
    )
    get_pdf()

    print(
        """[bold dodger_blue2] -- extract infor -- [/bold dodger_blue2]
        :robot_face: :detective:"""
    )
    extract_infor()

    print("[bold green]DONE![/bold green] :nerd_face:")


@app.command()
def report():
    """Read file default with information about data"""

    table = Table(title="CPLP DATA - Report")
    fields = [
        "Search Range",
        "Items",
        "Downloaded",
        "PDF Pages Extract",
        "Names Extract",
    ]
    for header in fields:
        table.add_column(header, style="magenta")

    default = pd.read_csv("./app/log/default.csv", sep=";")
    default_dict = default.to_dict(orient="records")

    for row in default_dict:
        table.add_row(*[str(value) for value in row.values()])

    x, *total = default.sum().to_list()
    table.add_row("Total", *[str(value) for value in total])

    Console().print(table)


if __name__ == "__main__":
    app()
