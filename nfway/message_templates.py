EMITTER_HEADER_TEMPLATE = """
<b>{name}</b>
<i>CNPJ: {cnpj}</i>

<i>{address}</i>
"""

ITEM_TEMPLATE = """
<b>Item:</b> {name}
<b>Quantidade:</b> {quantity} {quantity_unit}
<b>Valor unitário:</b> R$ {unit_value}
<b>Valor do item:</b> R$ {item_value}
"""

NF_INFO_TEMPLATE = """
<b>Número da NF:</b> {number}
<b>Série da NF:</b> {series}
<b>Chave de Acesso da NF:</b> {access_key}
<b>Data de Emissão:</b> {emission_date}
<b>Hora de Emissão:</b> {emission_time}
"""

TOTAL_TEMPLATE = """
<b>Valor Total:</b> R$ {total_value}
<i>Total em Impostos: R$ {total_taxes}</i>
"""

BAD_URL_TEMPLATE = """
<b>Não foi possível ler a Nota Fiscal na URL informada.</b>
Verifique se a URL pertence ao site oficial: https://sat.sef.sc.gov.br/.
"""

BAD_QR_CODE_TEMPLATE = """
<b>Não foi possível identificar o QR code informado.</b>
Por favor, tente novamente com uma imagem mais nítida.
"""

GOOD_QR_CODE_BAD_URL_TEMPLATE = """
<b>O QR code foi lido corretamente, mas nao foi possivel identificar a Nota Fiscal.</b>
Certifique-se de que o QR code pertence a uma Nota Fiscal.
"""
