import re
from datetime import date, time
from decimal import Decimal

import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

from nfway.nf_info import NFInfo, NFItem

ITEM_ID_REGEX = re.compile(r"Item \+ \d+")
CODE_REGEX = re.compile(r"\d+")
CNPJ_REGEX = re.compile(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}")
DATE_REGEX = re.compile(r"\d{2}/\d{2}/\d{4}")
TIME_REGEX = re.compile(r"\d{2}:\d{2}:\d{2}")
TEXT_SPACES_REGEX = re.compile(r"([^\W\d]|[\s])+")
NUMBER_REGEX = re.compile(r"\d+")
CEP_REGEX = re.compile(r"\d{5}-\d{3}")


def read_url(url) -> NFInfo:
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve page content: {response.status_code}")

    soup = BeautifulSoup(response.content, "html.parser")

    emiter_name_element = soup.find("div", id="u20")
    emiter_cnpj_element = emiter_name_element.find_next_sibling("div", class_="text")
    emiter_address_element = emiter_cnpj_element.find_next_sibling("div", class_="text")

    item_elements = soup.find_all("tr", id=ITEM_ID_REGEX)

    total_value_element = soup.find("span", class_="totalNumb txtMax")
    tax_value_element = soup.find("span", class_="totalNumb txtObs")
    general_info_element = soup.find("li")
    access_key_element = soup.find("span", class_="chave")

    name = fix_spacement(emiter_name_element.text)
    address = fix_spacement(emiter_address_element.text)
    global_coords = find_global_coords(address)

    cnpj = ""
    if result := CNPJ_REGEX.search(emiter_cnpj_element.text):
        cnpj = result.group(0)

    items = list()
    for item_element in item_elements:
        item = parse_item(item_element)
        items.append(item)

    total_value = as_money(total_value_element.text)
    total_taxes = as_money(tax_value_element.text)

    nf_number = general_info_element.contents[4].get_text(strip=True)
    nf_series = general_info_element.contents[6].get_text(strip=True)
    access_key = access_key_element.get_text(strip=True)

    emission_date = None
    if result := DATE_REGEX.search(general_info_element.contents[8].text):
        day, month, year = result.group(0).split("/")
        day, month, year = int(day), int(month), int(year)
        emission_date = date(year, month, day)

    emission_time = None
    if result := TIME_REGEX.search(general_info_element.contents[8].text):
        hour, minute, second = result.group(0).split(":")
        hour, minute, second = int(hour), int(minute), int(second)
        emission_time = time(hour, minute, second)

    return NFInfo(
        items=tuple(items),
        total_value=total_value,
        total_taxes=total_taxes,
        #
        emission_date=emission_date,
        emission_time=emission_time,
        #
        emiter_name=name,
        emiter_cnpj=cnpj,
        emiter_address=address,
        emiter_coords=global_coords,
        #
        number=nf_number,
        series=nf_series,
        access_key=access_key,
    )


def parse_item(item_element: BeautifulSoup) -> NFItem:
    name_element = item_element.find("span", class_="txtTit")
    code_element = item_element.find("span", class_="RCod")
    quantity_element = item_element.find("span", class_="Rqtd")
    quantity_unit_element = item_element.find("span", class_="RUN")
    unit_value_element = item_element.find("span", class_="RvlUnit")
    item_value_element = item_element.find("span", class_="valor")

    code = ""
    if result := CODE_REGEX.search(code_element.text):
        code = result.group(0)

    return NFItem(
        name=fix_spacement(name_element.text),
        quantity=as_quantity(quantity_element.contents[1]),
        quantity_unit=quantity_unit_element.contents[1].strip(),
        unit_value=as_money(unit_value_element.contents[1]),
        item_value=as_money(item_value_element.text.strip()),
        code=code,
    )


def fix_spacement(text: str) -> str:
    return " ".join(text.split())


def as_money(text: str) -> Decimal:
    return Decimal(text.replace(",", "."))


def as_quantity(text: str) -> float | int:
    quantity = float(text.replace(",", "."))
    if quantity.is_integer():
        return int(quantity)
    return quantity


def find_global_coords(address: str) -> tuple[float, float] | None:
    filtered_address_parts = list()
    for part in address.split(","):
        part = part.strip()
        if any(
            [
                TEXT_SPACES_REGEX.fullmatch(part),
                NUMBER_REGEX.fullmatch(part),
                CEP_REGEX.fullmatch(part),
            ]
        ):
            filtered_address_parts.append(part)

    address = ", ".join(filtered_address_parts)
    geolocator = Nominatim(user_agent="nfway_app")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    return None
