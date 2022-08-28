import click

from src.select_items import SelectItems
from src.sorting_hat import SortingHat


@click.group()
def cli() -> None:
    "Creates a group of cli commands."
    pass


@cli.command()
def sort() -> None:
    """Starts the sorting."""
    select_items = SelectItems(filename="data/questions.csv")
    selected_items = select_items.run()

    sorting_hat = SortingHat(
        questions="data/questions.csv",
        answers="data/answers.csv",
        weights="data/weights.csv",
        selected_items=selected_items,
    )
    sorting_hat.run()
