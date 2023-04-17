"""This module will play the role of the sorting hat.

By default seven questions will be asked and one of the four houses
will be chosen from the answers.
"""

import csv
import sys
from collections import defaultdict
from importlib import resources
from random import shuffle

import questionary

from sorting_hat.print_house_ascii import print_house_ascii


class SortingHat:
    """Sorts someone into one of the four houses.

    Args:
        questions: The filename with the referential of questions to ask.
        answers: The filename with the referential of answers.
        weights: The filename with the referential of weights for each question.
        chosen_variations: The randomly chosen variation for each question.
    """

    def __init__(
        self,
        questions: str,
        answers: str,
        weights: str,
        chosen_variations: list[dict[str, str]],
    ) -> None:
        """Initializes the class."""
        self.questions_filename = questions
        self.answers_filename = answers
        self.weights_filename = weights
        self.chosen_variations = chosen_variations

    def run(self) -> None:
        """Sorts someone into one of the four houses."""
        questions = self._load(filename=self.questions_filename)
        answers = self._load(filename=self.answers_filename)
        weights = self._load(filename=self.weights_filename)

        # Shuffle the order of the questions to add more randomness.
        shuffle(x=self.chosen_variations)

        print(
            "\n-------------------- "
            "La cérémonie de répartition va débuter !"
            " --------------------\n"
        )

        current_score = defaultdict(float)

        for variation in self.chosen_variations:
            answer = self._ask_question(
                questions=questions, answers=answers, variation=variation
            )
            current_score = self._update_score(
                weights=weights, answer=answer, current_score=current_score
            )

        winning_house = self._get_winning_house(score=current_score)

        print(
            f"\n-------------------- "
            f"Le choix a été fait ! "
            f" --------------------\n"
            f"\n---------- "
            f"La maison {winning_house.capitalize()} te souhaite la bienvenue !"
            f" ----------\n"
        )

        print_house_ascii(house=winning_house)
        self._print_welcome_message(house=winning_house)

    def _ask_question(
        self,
        questions: list[dict[str, str]],
        answers: list[dict[str, str]],
        variation: dict[str, str],
    ) -> dict[str, str]:
        """Asks a question and gets the answer back.

        Args:
            questions: The referential of questions.
            answers: The referential of answers.
            variation: The chosen variation of the question.

        Returns:
            A dictionary with the question_id, the variation_id, and the answer_id.
        """
        for question in questions:
            if (
                question["question_id"] == variation["question_id"]
                and question["variation_id"] == variation["variation_id"]
            ):
                variation_text = question["variation_text"]
                break

        answer_text: list[str] = []

        for answer in answers:
            if (
                answer["question_id"] == variation["question_id"]
                and answer["variation_id"] == variation["variation_id"]
            ):
                answer_text.append(answer["answer_text"])

        try:
            answer_id = str(
                answer_text.index(
                    questionary.select(
                        message=variation_text,
                        choices=answer_text,
                        instruction=" ",
                        qmark="",
                    ).ask()
                )
                + 1  # Add 1 to offset the index and match the referential.
            )
            print("\n")
        except ValueError:
            sys.exit()

        return {
            "question_id": variation["question_id"],
            "variation_id": variation["variation_id"],
            "answer_id": answer_id,
        }

    @staticmethod
    def _load(filename: str) -> list[dict[str, str]]:
        """Loads one of the input files (the questions, the answers or the weights).

        Args:
            filename: The filename to load.

        Returns:
            A list of rows.
        """
        rows = []

        with resources.open_text(
            package="sorting_hat.data", resource=filename, encoding="utf-8"
        ) as f:
            reader = csv.DictReader(f=f)
            for row in reader:
                rows.append(row)

        return rows

    @staticmethod
    def _update_score(
        weights: list[dict[str, str]],
        answer: dict[str, str],
        current_score: defaultdict[str, float],
    ) -> defaultdict[str, float]:
        """Updates the score after a new answer.

        Args:
            weights: The referential of weights.
            answer: The answer given to a specific question.
            current_score: The current state of the score that should be updated.

        Returns:
            The updated score.
        """
        for weight in weights:
            if (
                weight["question_id"] == answer["question_id"]
                and weight["variation_id"] == answer["variation_id"]
                and weight["answer_id"] == answer["answer_id"]
            ):
                current_score[weight["house"]] += float(weight["weight"])

        return current_score

    @staticmethod
    def _get_winning_house(score: dict[str, float]) -> str:
        """Gets the winning house.

        In case of a tie, the winning house is chosen at random between the houses
        with the best score.

        Args:
            score: The results once the questionary is done.

        Returns:
            The winning house.
        """
        # Shuffle the dictionary to add more randomness in case of a tie.
        shuffled_score = list(score.items())

        shuffle(x=shuffled_score)
        shuffled_score = dict(shuffled_score)

        return max(shuffled_score, key=shuffled_score.get)

    @staticmethod
    def _print_welcome_message(house: str) -> None:
        """Prints a different welcome message for each house.

        Args:
            house: The house for which to print the welcome message.
        """
        houses = ("gryffondor", "poufsouffle", "serdaigle", "serpentard")

        if house not in houses:
            raise ValueError(f"The house should be one of {', '.join(houses)}.")

        if house == "gryffondor":
            print(
                "\n---------- "
                "On a vu pire que Gryffondor, tu ne t'en sors pas si mal !"
                " ----------\n"
            )

        if house == "poufsouffle":
            print(
                "\n---------- "
                "Ils sont gentils les Poufsouffle, c'est déjà quelque chose !"
                " ----------\n"
            )

        if house == "serdaigle":
            print(
                "\n---------- "
                "Serdaigle, vraiment ? Et bien... bon courage ?"
                " ----------\n"
            )

        if house == "serpentard":
            print(
                "\n---------- " "Aaah Serpentard ! Welcome my friend !" " ----------\n"
            )
