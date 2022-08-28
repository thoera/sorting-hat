"""This module tests that the data used for the sorting hat are correct."""

import numpy as np
import pandas as pd


def test_weights() -> None:
    """Tests that the weights for each question are correct."""
    data = pd.read_csv("data/weights.csv")
    computed = (
        data.groupby(["question_id", "item_id", "answer_id"]).sum().to_numpy()
    )
    assert np.all(computed == 1)
