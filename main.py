from pprint import pprint

from nfway.cli import cli_parser
from nfway.csv_writer import write_to_csv
from nfway.qrcode_reader import read_qrcode
from nfway.scrapper import read_url


def main():
    parser = cli_parser()
    args = parser.parse_args()

    if args.telegram_bot is not None:
        from nfway.telegram_bot import initialize

        return initialize(args.telegram_bot)

    result_value = None
    if args.url is not None:
        try:
            result_value = read_url(args.url)
        except Exception:
            print("Ocorreu um erro durante a leitura da NF")
            return

    elif args.qr_code is not None:
        try:
            url = read_qrcode(args.qr_code)
        except Exception:
            print("Ocorreu um erro durante a leitura do QR code")
            return

        if url is None:
            print("Ocorreu um erro durante a leitura do QR code")
            return

        try:
            result_value = read_url(url)
        except Exception:
            print("Ocorreu um erro durante a leitura da NF")
            return

    else:
        print("Nenhum argumento fornecido.")
        parser.print_help()
        exit()

    if result_value is None:
        print("Nenhum dado foi encontrado na NF.")
        exit()

    elif args.output is not None:
        write_to_csv(result_value, args.output)

    else:
        pprint(result_value)


if __name__ == "__main__":
    main()
