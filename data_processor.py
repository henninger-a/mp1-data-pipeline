# data_processor.py
import logging
import pandas as pd
import yaml

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
    before = df
    if method == 'iqr':
        for column in columns:
            if column not in df.columns:
                logger.warning(f'column {column} not in data')
                continue
            if pd.api.types.is_numeric_dtype(column) is False:
                logger.warning(f'column {column} is not numeric')
                continue
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - threshold * iqr
        upper = q3 + threshold * iqr
        df = df[(df["Score"] >= lower) & (df["Score"] <= upper)]
    if method == 'zscore':
        for column in columns:
            if column not in df.columns:
                logger.warning(f'column {column} not in data')
                continue
            if pd.api.types.is_numeric_dtype(column) is False:
                logger.warning(f'column {column} is not numeric')
                continue
            mean = df[column].mean()
            std = df[column].std()
            z_scores = []
            for num in column:
                df['z_scores'] ((num - mean) / std)
        df = df[[abs(x) for x in z_scores] <= 3]
    logger.debug(f'Method: {method}, Threshold: {threshold}, Rows removed: {len(before) - len(df)}')
    return df


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    with open(config, "r") as f:
        config = yaml.safe_load(f)
    if config['processing']['remove_duplicates'] == 'true':
        df = remove_duplicates(df)
    elif config['processing']['enabled'] == 'true':
        df = handle_missing(df, config['processing']['axis'])
    elif config['outliers']['enabled'] == 'true':
        df = remove_outliers(df, config['outliers']['columns'], config['outliers']['method'], config['outliers']['threshold'])
    return df


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    return {'rows_before': df_before.shape[0], 'rows_after': df_after.shape[0], 'rows_removed': df_before.shape[0] - df_after.shape[0], 
            'columns_before': df_before.shape[1], 'columns_after': df_after.shape[1], 'columns_removed': df_before.shape[1] - df_after.shape[1]}
