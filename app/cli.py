import typer
from rich.console import Console
from rich.table import Table


main = typer.Typer(name="CPLP DATA CLI", add_completion=False)


@main.command()
def start_web_scraping():
    """Lists all users"""
    table = Table(title="dundie users")
    fields = ["name", "username", "dept", "email", "currency"]
    for header in fields:
        table.add_column(header, style="magenta")

    with Session(engine) as session:
        users = session.exec(select(User))
        for user in users:
            table.add_row(*[getattr(user, field) for field in fields])

    Console().print(table)


@main.command()
def start_download_pdf(
    name: str,
    email: str,
    password: str,
    dept: str,
    username: str | None = None,
    currency: str = "USD",
):
    """Create user"""
    with Session(engine) as session:
        user = User(
            name=name,
            email=email,
            password=password,  # pyright: ignore
            dept=dept,
            username=username or generate_username(name),
            currency=currency,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        typer.echo(f"created {user.username} user")
        return user


@main.command()
def report():
    """Lists all users"""
    # table = Table(title="dundie users")
    # fields = ["name", "username", "dept", "email", "currency"]
    # for header in fields:
    #     table.add_column(header, style="magenta")

    # with Session(engine) as session:
    #     users = session.exec(select(User))
    #     for user in users:
    #         table.add_row(*[getattr(user, field) for field in fields])

    # Console().print(table)
