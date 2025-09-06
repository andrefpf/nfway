from nfway.scrapper import read_url
from pprint import pprint
from argparse import ArgumentParser
from pathlib import Path


def cli_parser() -> ArgumentParser:
    parser = ArgumentParser(description="NF-Way CLI Tool.")

    parser.add_argument(
        "-u",
        "--url",
        type=str,
        help="URL of the NF-e page to scrape",
    )

    parser.add_argument(
        "-q",
        "--qr-code",
        type=Path,
        help="Path to read the QR code image containing the NF-e URL",
        default=None,
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output CSV file to save the NF-e data",
        default=None,
    )

    return parser
