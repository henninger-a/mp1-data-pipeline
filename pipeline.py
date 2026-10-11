"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys
from pathlib import Path
from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Check the quality of a CSV file.')

def parse_arguments():
    """Parse command-line arguments."""

    parser.add_argument('--input',
                    '-i',
                    required=True,
                    help='Path to the input file')
    
    parser.add_argument('--config',
                        required=True,
                        help='Path to the yaml cofiguration file')

    parser.add_argument('--output',
                    '-o',
                    required=True,
                    help='Path to the output file')

    parser.add_argument('--verbose',
                        '-v',
                        required=False,
                        action='store_true',
                        help='Enable verbose logging')
    
    return parser.parse_args()

def main():
    """Main pipeline function."""
    parse_arguments()
    setup_logging(parser.parse_args().verbose)
    if validate_input(parser.parse_args().input) == False:
        sys.exit(1)
    if validate_input(parser.parse_args().config) == False:
        sys.exit(1)

    args = parser.parse_args()

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    required_columns = config['validation']['required_columns']
    numeric_columns = config['validation']['numeric_columns']
    original = data.copy()

    try:
        data = validate_dataframe(data, required_columns, numeric_columns)
        logger.info(f'Rows Before Validation: {len(original)} Rows After Validation: {len(data)}')
    except ValueError:
        sys.exit(1)

    try:
        data = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(original, data)
    logger.info(f'Processing Complete: {len(original)} → {len(data)} rows')
    save_data(data, args.output)
    logger.info(f'Saved cleaned data to {args.output}')
    print(f'Cleaning Report: {report}')

if __name__ == "__main__":
    main()
