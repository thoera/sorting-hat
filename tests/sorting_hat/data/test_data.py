"""This module tests that the data used for the sorting hat are correct."""

import csv
from collections import defaultdict
from importlib import resources


def test_weights_sum_to_one() -> None:
    """Tests that the weights for each question sum to 1."""
    weights_per_answer = defaultdict(float)

    with resources.open_text(
        package="sorting_hat.data", resource="weights.csv", encoding="utf-8"
    ) as f:
        reader = csv.DictReader(f=f)
        for row in reader:
            key = row["question_id"] + row["variation_id"] + row["answer_id"]
            weights_per_answer[key] += float(row["weight"])

    assert set(weights_per_answer.values()) == {1.0}
