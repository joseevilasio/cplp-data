import pandas as pd
import typer
from rich import print
from rich.console import Console
from rich.table import Table

from app.controller import web_scraping

app = typer.Typer(name="CPLP DATA CLI", add_completion=False)


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
def start_download_pdf():
    """Start download PDF"""
    pass


@app.command()
def start_extract_pdf():
    """Start extract info in PDF"""
    pass


@app.command()
def start_automode():
    """Start AUTOMODE according to the configured default"""
    pass


@app.command()
def report():
    """Read file default with information about data"""

    table = Table(title="CPLP DATA - Report")
    fields = [
        "Search Range",
        "Pages",
        "Downloaded",
        "Pages Extract",
        "Names Extract",
    ]
    for header in fields:
        table.add_column(header, style="magenta")

    default = pd.read_csv("./app/log/default.csv", sep=";")
    default_dict = default.to_dict(orient="records")

    for row in default_dict:
        table.add_row(*[str(value) for value in row.values()])

    Console().print(table)


if __name__ == "__main__":
    app()
