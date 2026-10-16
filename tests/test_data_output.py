#tests/test_data_output.py

import pandas as pd

from src import save_data


def test_save_data_creates_csv(sample_df, tmp_path):
    output_path = tmp_path / "clean.csv"

    # TODO: Call save_data() and store its return value.
    output = save_data(sample_df, output_path)
    # TODO: Assert that the returned path is correct.
    assert output == output_path
    # TODO: Read the saved CSV with pandas.
    output_df = pd.read_csv(output)
    # TODO: Assert that its row count and column names match sample_df.
    assert len(output_df) == len(sample_df) and output_df.columns.tolist() == sample_df.columns.tolist()