"""This module tests that the data used for the sorting hat are correct."""

import numpy as np
import pandas as pd


def test_data_lng() -> None:
    """Tests that the file with the weights for each question is correct."""
    data = pd.read_csv("data/weights.csv")
    computed = (
        data.groupby(["question_id", "variation_id", "choice_id"])
        .sum()
        .to_numpy()
    )
    assert np.all(computed == 1)
