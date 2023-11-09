import pandas as pd
import typer
from rich.console import Console
from rich.table import Table

main = typer.Typer(name="CPLP DATA CLI", add_completion=False)


@main.command()
def start_web_scraping():
    pass


@main.command()
def start_download_pdf():
    pass


@main.command()
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
