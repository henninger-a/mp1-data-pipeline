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


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%H:%M:%S'
    )

    logger = logging.getLogger(__name__)

    if verbose is True:
        logger.setLevel(logging.DEBUG)
        logger.debug(f'Arguments parsed: input={parser.parse_args().input}, output={parser.parse_args().output}, format={parser.parse_args().format}')

parser = argparse.ArgumentParser(description='Check the quality of a CSV file.')

def parse_arguments():
    """Parse command-line arguments."""

    parser.add_argument('--input',
                    '-i',
                    required=True,
                    help='Path to the input file')

    parser.add_argument('--output',
                    '-o',
                    required=True,
                    help='Path to the output file')

    parser.add_argument('--format',
                        required=False,
                        choices=['csv', 'json'],
                        default='csv',
                        help='Output format: csv or json; default is csv')

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

if __name__ == "__main__":
    main()
