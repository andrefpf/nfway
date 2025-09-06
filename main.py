from nfway.scrapper import read_url
from nfway.cli import cli_parser
from nfway.csv_writer import write_to_csv

from pprint import pprint


def main():
    parser = cli_parser()
    args = parser.parse_args()

    result_value = None
    if args.url is not None:
        try:
            result_value = read_url(args.url)
        except Exception as e:
            print(f"Ocorreu um erro durante a leitura da NF")
            exit(1)

    elif args.qr_code is not None:
        raise NotImplementedError("QR code reading not implemented yet.")

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
