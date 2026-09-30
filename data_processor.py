# data_processor.py
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    """Remove duplicate rows."""
    no_duplicates_df = df.drop_duplicates()
    logger.debug(f'Removed {len(df)-len(no_duplicates_df)} duplicate row(s)')
    return no_duplicates_df


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == 'rows':
        rows_dropped_df = df.dropna()
        logger.debug(f'Dropped {len(df) - len(rows_dropped_df)} row(s) with missing values')
        return rows_dropped_df
    elif axis == 'columns':
        columns_dropped_df = df.dropna()
        logger.debug(f'Dropped {len(df) - len(columns_dropped_df)} columns(s) with missing values')
        return columns_dropped_df
    else:
        logger.error(f'Unsupported value for axis: {axis}')
        raise ValueError


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    pass


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    pass


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    pass
