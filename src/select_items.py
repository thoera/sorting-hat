"""This module will select randomly an item for each question.

An "item" is one of the possible variations for a given question: the question
asked is different but the subject is the same.
The idea is to have more diversity between multiple quizzes and
to make it more difficult to cheat when doing the quiz for a second time.
"""

from copy import copy
from random import randint
from typing import Dict, List

import pandas as pd


class SelectItems:
    """Selects randomly an item for each question."""

    def __init__(self, filename: str) -> None:
        """Initializes the class.

        Args:
            filename: The filename with the referential of questions to ask.
        """
        self.filename = filename

    def run(self) -> List[Dict[str, float]]:
        """Selects randomly an item for each question.

        Returns:
            The item chosen for each question.
        """
        questions = self._load_questions()
        items = get_number_of_items(questions=questions)
        return [self._select_item(question=question) for question in items]

    def _load_questions(self) -> pd.DataFrame:
        """Loads the referential of questions.

        Returns:
            The referential of questions.
        """
        return pd.read_csv(filepath_or_buffer=self.filename)

    @staticmethod
    def _select_item(question: Dict[str, float]) -> Dict[str, float]:
        """Selects randomly an item for a given question.

        Args:
            question: A question with the number of existing items.

        Returns:
            The chosen item for the given question.
        """
        chosen_item = copy(question)
        chosen_item["choice"] = randint(1, chosen_item["item_nb"])
        return chosen_item


def get_number_of_items(questions: pd.DataFrame) -> List[Dict[str, float]]:
    """Gets the number of existing items for each question.

    Args:
        questions: The referential of questions.

    Returns:
        The number of existing items for each question.
    """
    return (
        questions.loc[:, ["question_id", "item_id"]]
        .groupby("question_id")
        .max()
        .rename(columns={"item_id": "item_nb"})
        .reset_index()
        .to_dict(orient="records")
    )
