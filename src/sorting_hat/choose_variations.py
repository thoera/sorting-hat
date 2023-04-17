"""This module will randomly choose a variation for each question.

A "variation" is an alternative for a given question. The subject of the question
is the same but the wording will be slightly altered.
The idea is to have more diversity between multiple quizzes and
to make it more difficult to cheat when doing the quiz for a second time.

An option is available to use every possible variation of each question to get a longer
(and more robust?) quiz.
"""

import csv
from collections import Counter
from importlib import resources
from random import randint


class ChooseVariations:
    """Chooses randomly a variation for each question.

    Args:
        filename: The filename with the referential of questions to ask.
        long_quiz: A flag to choose to return all variations for each question
            or not. Defaults to False.
    """

    def __init__(self, filename: str, long_quiz: bool = False) -> None:
        """Initializes the class."""
        self.filename = filename
        self.long_quiz = long_quiz

    def run(self) -> list[dict[str, str]]:
        """Chooses randomly a variation for each question.

        Returns:
            The variation chosen for each question.
        """
        questions = self._load_questions()

        if self.long_quiz:
            for question in questions:
                question.pop("variation_text")
            return questions

        number_of_variations = self._get_number_of_variations(questions=questions)
        return self._choose_variation(questions=number_of_variations)

    def _load_questions(self) -> list[dict[str, str]]:
        """Loads the referential of questions.

        Returns:
            The referential of questions.
        """
        questions = []

        with resources.open_text(
            package="sorting_hat.data", resource=self.filename, encoding="utf-8"
        ) as f:
            reader = csv.DictReader(f=f)
            for row in reader:
                questions.append(row)

        return questions

    @staticmethod
    def _choose_variation(questions: list[dict[str, int]]) -> list[dict[str, str]]:
        """Chooses randomly a variation for each question.

        Args:
            questions: A list of questions with the id and the number of variations.

        Returns:
            The chosen variation for the given question.
        """
        return [
            {
                "question_id": question["question_id"],
                "variation_id": str(randint(a=1, b=question["number_of_variations"])),
            }
            for question in questions
        ]

    @staticmethod
    def _get_number_of_variations(
        questions: list[dict[str, str]]
    ) -> list[dict[str, int]]:
        """Gets the number of variations for each question.

        Args:
            questions: The referential of questions.

        Returns:
            The number of existing variations for each question.
        """
        number_of_variations = []

        counter = Counter(question["question_id"] for question in questions)

        for question_id, n_variations in counter.items():
            number_of_variations.append(
                {"question_id": question_id, "number_of_variations": n_variations}
            )

        return number_of_variations
