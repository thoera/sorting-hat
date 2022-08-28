"""This module will play the role of the sorting hat.

Seven questions will be asked and one of the four houses will be chosen
from the answers.
"""

import sys
from random import choice, shuffle
from typing import Dict, List

import pandas as pd
import questionary

from src.print_house_ascii import print_house_ascii


class SortingHat:
    """Sorts someone into one of the four houses."""

    def __init__(
        self,
        questions: str,
        answers: str,
        weights: str,
        selected_items: List[Dict[str, float]],
    ) -> None:
        """Initializes the class.

        Args:
            questions: The filename with the referential of questions to ask.
            answers: The filename with the referential of answers.
            weights: The filename with the referential of weights for each question.
            selected_items: The randomly selected item for each question.
        """
        self.questions_filename = questions
        self.answers_filename = answers
        self.weights_filename = weights
        self.selected_items = selected_items

    def run(self) -> None:
        """Sorts someone into one of the four houses."""
        questions = self._load_questions()
        answers = self._load_answers()
        weights = self._load_weights()

        houses = set(weights["house"])
        current_score = pd.DataFrame(
            data={"house": list(houses), "weight": [0] * len(houses)}
        ).set_index("house")

        # Shuffle the order of the questions to add more randomness.
        shuffle(self.selected_items)

        print(
            "\n-------------------- "
            "La cérémonie de répartition va débuter !"
            " --------------------\n"
        )

        for item in self.selected_items:
            answer = self._ask_question(
                questions=questions, answers=answers, item=item
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
            f"La maison {winning_house.capitalize()} vous souhaite la bienvenue !"
            f" ----------\n"
        )

        print_house_ascii(house=winning_house)
        self._print_welcome_message(house=winning_house)

    def _load_questions(self) -> pd.DataFrame:
        """Loads the referential of questions.

        Returns:
            The referential of questions.
        """
        return pd.read_csv(filepath_or_buffer=self.questions_filename)

    def _load_answers(self) -> pd.DataFrame:
        """Loads the referential of answers.

        Returns:
            The referential of answers.
        """
        return pd.read_csv(filepath_or_buffer=self.answers_filename)

    def _load_weights(self) -> pd.DataFrame:
        """Loads the referential of weights.

        Returns:
            The referential of weights.
        """
        return pd.read_csv(filepath_or_buffer=self.weights_filename)

    def _ask_question(
        self,
        questions: pd.DataFrame,
        answers: pd.DataFrame,
        item: Dict[str, float],
    ) -> Dict[str, float]:
        """Asks a question and gets the answer back.

        Returns:
            A dictionary with the question_id, the item_id, and the answer_id.
        """
        item_text = questions.loc[
            (questions["question_id"] == item["question_id"])
            & (questions["item_id"] == item["choice"]),
            :,
        ]["item_text"].iloc[0]

        answer_text = answers.loc[
            (answers["question_id"] == item["question_id"])
            & (answers["item_id"] == item["choice"]),
            :,
        ]["answer_text"].to_list()

        try:
            answer_id = (
                answer_text.index(
                    questionary.select(
                        message=item_text,
                        choices=answer_text,
                        instruction=" ",
                        qmark="",
                    ).ask()
                )
                + 1  # Add 1 to offset the index and match the referential.
            )
            print("")
        except ValueError:
            sys.exit()

        return {
            "question_id": item["question_id"],
            "item_id": item["choice"],
            "answer_id": answer_id,
        }

    @staticmethod
    def _update_score(
        weights: pd.DataFrame,
        answer: Dict[str, float],
        current_score: pd.DataFrame,
    ) -> pd.DataFrame:
        """Updates the score after a new answer.

        Args:
            weights: The referential of weights.
            answer: The answer given to a specific question.
            scores: The current score.

        Returns:
            The updated score.
        """
        score = weights.loc[
            (weights["question_id"] == answer["question_id"])
            & (weights["item_id"] == answer["item_id"])
            & (weights["answer_id"] == answer["answer_id"]),
            :,
        ]
        score = score[["house", "weight"]].set_index("house")

        return current_score.add(score)

    @staticmethod
    def _get_winning_house(score: pd.DataFrame) -> str:
        """Gets the winning house.

        In case of a tie, the winning house is chosen at random between the houses
        with the best score.

        Args:
            score: The results once the questionary is done.

        Returns:
            The winning house.
        """
        winning_house = score[
            score["weight"].values == score["weight"].values.max()
        ].index.to_list()

        if len(winning_house) > 1:
            return choice(winning_house)
        return winning_house[0]

    @staticmethod
    def _print_welcome_message(house: str) -> None:
        """Prints a different welcome message for each house.

        Args:
            house: The house for which to print the welcome message.
        """
        assert house in (
            "gryffondor",
            "poufsouffle",
            "serdaigle",
            "serpentard",
        )

        if house == "gryffondor":
            print(
                "\n---------- "
                "On a vu pire que Gryffondor, tu ne t'en sors pas si mal !"
                " ----------\n"
            )

        if house == "poufsouffle":
            print(
                "\n---------- "
                "Ils sont gentils les Poufsouffle, c'est déjà quelque chose j'imagine !"
                " ----------\n"
            )

        if house == "serdaigle":
            print(
                "\n---------- "
                "Serdaigle vraiment ? Et bien... bon courage ?"
                " ----------\n"
            )

        if house == "serpentard":
            print(
                "\n---------- "
                "Aaah Serpentard ! Le monde t'appartient désormais !"
                " ----------\n"
            )
