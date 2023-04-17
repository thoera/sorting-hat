"""This module defines the commands available after installing the library."""

import click

from sorting_hat.choose_variations import ChooseVariations
from sorting_hat.sorting_hat import SortingHat


@click.group()
def cli() -> None:
    """Finds all the available commands below."""
    pass


@cli.command()
@click.option(
    "-l",
    "--long-quiz",
    is_flag=True,
    default=False,
    help="Use the longer quiz (every variation of each question will be asked).",
)
def sort(long_quiz: bool) -> None:
    """Starts the sorting."""
    chosen_variations = ChooseVariations(
        filename="questions.csv", long_quiz=long_quiz
    ).run()

    SortingHat(
        questions="questions.csv",
        answers="answers.csv",
        weights="weights.csv",
        chosen_variations=chosen_variations,
    ).run()
