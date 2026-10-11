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
from data_loaders import load_data
from data_processor import process_data, create_cleaning_report

logger = logging.getLogger(__name__)

def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    logging.basicConfig(
        level=logging.DEBUG if parser.parse_args().verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt='%H:%M:%S'
    )

    logger.debug(f'Arguments parsed: input={parser.parse_args().input}, output={parser.parse_args().output}')

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


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if Path(filepath).is_file() is True:
        logger.info(f"Input file validated: '{filepath}'")
        return True
    else:
        logger.error(f"Input file not fould: '{filepath}'")
        return False

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

    original = data.copy()

    try:
        data = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(original, data)
    logger.info(f'Processing Complete: {len(original)} → {len(data)} rows')
    data.to_csv(args.output, index = False)
    logger.info(f'Saved cleaned data to {args.output}')
    print(report)

if __name__ == "__main__":
    main()
