from nfway.scrapper import read_url
from nfway.cli import cli_parser

from pprint import pprint


def main():
    parser = cli_parser()
    args = parser.parse_args()

    result_value = None
    if args.url is not None:
        result_value = read_url(args.url)

    elif args.qr_code is not None:
        raise NotImplementedError("QR code reading not implemented yet.")

    else:
        print("No input provided.")
        parser.print_help()
        exit()

    if args.output is not None:
        raise NotImplementedError("Output to file not implemented yet.")

    else:
        pprint(result_value)


if __name__ == "__main__":
    main()
