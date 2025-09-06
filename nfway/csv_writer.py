from nfway.nf_info import NFInfo
from pathlib import Path
import csv


def write_to_csv(nf_info: NFInfo, file_path: Path):
    items_table = create_items_table(nf_info)
    general_info_table = create_general_info_table(nf_info)
    combined_table = combine_tables_side_by_side(items_table, general_info_table)

    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(combined_table)


def create_items_table(nf_info: NFInfo):
    items_data = [
        ["Itens da NF"],
        ["Nome", "Código", "Quantidade", "Unidade", "Valor Unitário", "Valor Total"],
    ]

    for item in nf_info.items:
        row = [
            item.name,
            item.code,
            item.quantity,
            item.quantity_unit,
            item.unit_value,
            item.item_value,
        ]
        items_data.append(row)

    items_data = make_columns_equal_length(items_data)
    return items_data


def create_general_info_table(nf_info: NFInfo):
    general_header = [
        ["Emissor", nf_info.emiter_name],
        ["CNPJ do Emissor", nf_info.emiter_cnpj],
        ["Endereço do Emissor", nf_info.emiter_address],
        ["Coordenadas do Emissor", nf_info.emiter_coords],
        [],
        ["Número da NF", nf_info.number],
        ["Série da NF", nf_info.series],
        ["Chave de Acesso da NF", nf_info.access_key],
        [],
        ["Data de Emissão", nf_info.emission_date],
        ["Hora de Emissão", nf_info.emission_time],
        [],
        ["Valor Total", nf_info.total_value],
        ["Total de Impostos", nf_info.total_taxes],
        [],
        [],
    ]
    return general_header


def combine_tables_side_by_side(table1, table2):
    table1 = make_columns_equal_length(table1)
    table2 = make_columns_equal_length(table2)

    left_padding = [""] * len(table1[0])
    right_padding = [""] * len(table2[0])

    while len(table1) < len(table2):
        table1.append(left_padding)

    while len(table1) > len(table2):
        table2.append(right_padding)

    spacing = [""] * 2

    combined_table = []
    for row1, row2 in zip(table1, table2):
        combined_table.append(row1 + spacing + row2)
    return combined_table


def make_columns_equal_length(data: list[list]) -> list[list]:
    max_length = max(len(row) for row in data)
    for row in data:
        diff = max_length - len(row)
        if diff == 0:
            continue
        row += [""] * diff
    return data
