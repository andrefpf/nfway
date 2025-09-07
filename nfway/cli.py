from argparse import ArgumentParser, HelpFormatter
from pathlib import Path


def cli_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="NF-Way CLI Tool.",
        formatter_class=lambda prog: HelpFormatter(
            prog, max_help_position=40, width=100
        ),
    )

    parser.add_argument(
        "--url",
        metavar="<url>",
        type=str,
        help="URL of the NF-e page to scrape",
    )

    parser.add_argument(
        "--qr-code",
        metavar="<path>",
        type=Path,
        help="Path to read the QR code image containing the NF-e URL",
        default=None,
    )

    parser.add_argument(
        "--output",
        type=Path,
        metavar="<path>",
        help="Output CSV file to save the NF-e data",
        default=None,
    )

    parser.add_argument(
        "--telegram-bot",
        metavar="<token>",
        type=str,
        help="Start the Telegram bot server",
    )

    return parser
