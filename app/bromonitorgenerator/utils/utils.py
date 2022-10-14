from datetime import datetime
from dateutil import parser
import base64
import locale
import os
import requests
import json
from bs4 import BeautifulSoup

API_BASE = os.environ.get("backendApi", "http://localhost:8000/api")
locale.setlocale(locale.LC_ALL, "nl_NL.UTF8")


def today():
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def pretty_print_type_date(date_str):
    locale.setlocale(locale.LC_ALL, "nl_NL.UTF-8")
    date_object = datetime.fromisoformat(date_str)
    return date_object.strftime("%d %B").lstrip("0").replace(" 0", " ")


def pretty_print_datetime(date_str):
    locale.setlocale(locale.LC_ALL, "nl_NL.UTF-8")
    date_object = datetime.fromisoformat(str(date_str))
    return date_object.strftime("%A %d %B %Y %H:%M")


def pretty_print_today():
    locale.setlocale(locale.LC_ALL, "nl_NL.UTF-8")
    return today().strftime("%A %d %B %Y").capitalize()


def get_bromonitor_sources():
    response = requests.get(API_BASE + "/bromonitor/bromonitor-timestamp")
    data = json.loads(response.content)
    timestamp = f"Bron: {data['name'].upper()}"
    return timestamp


def get_bromonitor_timestamp():
    response = requests.get(API_BASE + "/bromonitor/bromonitor-timestamp")
    data = json.loads(response.content)
    timestamp = f"Bron: {data['name'].upper()}"
    for type in data["types"]:
        date = parser.parse(type["updated"]).date().strftime("%d-%m-%Y")
        timestamp = f"{timestamp}, {type['type'].upper()}:{date} "
    return timestamp


def plotly_fig_to_png(fig):
    img_bytes = fig.to_image(format="png")
    base64_bytes = base64.b64encode(img_bytes)
    return base64_bytes.decode()


def format_dutch_number(number):
    return locale.format_string("%d", number, grouping=True)


def add_scope_to_table(table):
    try:
        soup = BeautifulSoup(str(table), "lxml")
        for th in soup.find_all("th"):
            th["scope"] = "col"
    except:
        return table
    finally:
        return str(soup)


def get_quality_regime_label(row):
    if row["IMBRO"]:
        return "Heeft één of meerdere objecten in kwaliteitsregime IMBRO geregistreerd"
    elif row["IMBRO/A"]:
        return "Heeft enkel objecten in kwaliteitsregime IMBRO/A geregistreerd"
    return "Heeft geen gegevens geregistreerd"


def get_object_type_label(row):
    if row["Grondwaterstandonderzoek_aangevuld"]:
        # For accessability purposes, the string below contains unicode characters
        # for soft-hyphenation to break the string like this: grondwater-stand-metingen.
        # The unicode character may not be visible in your editor, but it is there.
        return "Heeft één of meerdere grondwater­stand­metingen geregistreerd."
    elif any(val not in [0, "0"] for val in row.values()):
        return "Heeft één of meerdere gegevens geregistreerd"
    return "Heeft geen gegevens geregistreerd"
