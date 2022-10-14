import json
import os
import pandas as pd
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime
from bromonitorgenerator.utils.utils import add_scope_to_table
from bromonitorgenerator.utils.utils import (
    API_BASE,
    pretty_print_type_date,
    format_dutch_number,
)
from bromonitorgenerator.utils.documentTypes import (
    document_type_dict,
    short_to_dutch_fullname,
)
from bromonitorgenerator.utils.start_date import get_start_date
from common.config import date_format, logging_format

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format=logging_format, datefmt=date_format
)
log = logging.getLogger(__name__)


def document_type_table_data():
    response = requests.get(API_BASE + "/bromonitor/bromonitor-timestamp")
    data = json.loads(response.content)["types"]
    table_data = list(
        map(
            lambda x: {
                "fullname": short_to_dutch_fullname[x["type"]],
                "abbreviation": "BHR-P" if x["type"] == "BHR" else x["type"],
                "date": pretty_print_type_date(x["updated"]),
            },
            data,
        )
    )
    return table_data


logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format=logging_format, datefmt=date_format
)
log = logging.getLogger(__name__)


def generate_top20_as_html(type=None):
    endpoint = API_BASE + "/rapporten/top20"
    if type:
        log.info(f"Generating top-20 for {type}")
        endpoint = f"{endpoint}?type={type}"
    else:
        log.info("Generating top-20 for all object types")

    response = requests.get(endpoint)
    data = json.loads(response.content)["data"]
    first_col = []
    keys = list(map(lambda x: x["key"], data))
    for i in range(0, len(data)):
        first_col.append(f"{i+1}. {keys[i]}")
    df = pd.DataFrame(
        {
            "Bronhouder": first_col,
            "Aantal": list(
                map(lambda x: "{:,}".format(x["count"]).replace(",", "."), data)
            ),
        }
    )
    html = df.to_html(index=False, justify="left", classes=["tbl_wide", "top-20"])
    # Add aria label to the # tableheader
    soup = BeautifulSoup(html, "lxml")
    ths = soup.find_all("th")
    for th in ths:
        th["scope"] = "col"
        if th.text == "#":
            th["aria-label"] = "Positie in top 20"
            th["style"] = "text-align: center;"
    html = str(soup)
    return html


def generate_top20_since_date_as_html():
    start_date = get_start_date()
    endpoint = API_BASE + f"/rapporten/top20-sinds-datum?start_datum={start_date}"
    log.info(f"Generating top-20 since date {start_date}")
    response = requests.get(endpoint)
    data = json.loads(response.content)["data"]
    df = pd.DataFrame(
        {
            "Bronhouder": [x["bronhouder"] for x in data],
            "Type": [document_type_dict[x["object_type"]].upper() for x in data],
            "IMBRO": ["{:,}".format(x["imbro_count"]).replace(",", ".") for x in data],
            "IMBRO/A": [
                "{:,}".format(x["imbroa_count"]).replace(",", ".") for x in data
            ],
        }
    )
    html = df.to_html(index=False, justify="left")
    html = add_scope_to_table(html)
    return html


def generate_gld_since_date_as_html():
    start_date = get_start_date()
    endpoint = API_BASE + f"/rapporten/nieuwe-glds?date={start_date}"
    log.info(f"Generating GLDs since date {start_date}")
    response = requests.get(endpoint)
    data = json.loads(response.content)["data"]
    if len(data) == 0:
        return "<p style='font-style:italic'>Er zijn geen nieuwe grondwatermetingen aangeleverd afgelopen week.</p>"
    df = pd.DataFrame(
        {
            "Bronhouder": [x["key"]["naam"] for x in data],
            "Aantal peilbuizen met metingen": [
                "{:,}".format(x["count"]).replace(",", ".") for x in data
            ],
        }
    )
    html = df.to_html(index=False, justify="left", classes="tbl_small")
    html = add_scope_to_table(html)
    return html


def registrations_per_year(year_count: int = 3):
    log.info("Generating table of object counts through years")
    object_types = sorted(document_type_dict.keys())
    current_year = datetime.now().year
    years = [current_year - x for x in reversed(range(year_count))]
    table_rows = []

    # Add individual rows for types
    for object_type in object_types:
        short_name = document_type_dict[object_type]
        full_name = short_to_dutch_fullname[short_name]

        response = requests.get(
            API_BASE + f"/rapporten/documenten-over-tijd?object_type={object_type}"
        )
        data = json.loads(response.content)["data"]

        counts = []
        for year in years:
            if str(year) in list(map(lambda x: x["key"], data)):
                counts.append(next((x["count"] for x in data if x["key"] == str(year))))
            else:
                counts.append(0)
        total = sum(map(lambda x: x["count"], data))

        table_rows.append({"type": full_name, "counts": counts, "total": total})
    # Add totals
    table_rows.append(
        {
            "type": "Totaal",
            "counts": [sum(x) for x in zip(*(map(lambda x: x["counts"], table_rows)))],
            "total": sum(map(lambda x: x["total"], table_rows)),
        }
    )

    return {"years": years, "rows": table_rows}


def gld_registrations_and_supplements():
    endpoint = API_BASE + f"/rapporten/status-glds"
    log.info(
        f"Showing top 20 of all GLDs and difference between registration and supplement"
    )
    response = requests.get(endpoint)
    data = json.loads(response.content)["data"]

    if len(data) == 0:
        return "<p style='font-style:italic'>Er staan nog geen GLDs in de database.</p>"

    glds = {}
    for x in data:
        if x["key"]["naam"] in glds:
            if x["key"]["status"] == "aangevuld":
                glds[x["key"]["naam"]][2] = x["count"]
                glds[x["key"]["naam"]][1] += x["count"]
            else:
                glds[x["key"]["naam"]][1] += x["count"]
        else:
            glds[x["key"]["naam"]] = [x["key"]["naam"], 0, 0]
            if x["key"]["status"] == "aangevuld":
                glds[x["key"]["naam"]][2] = x["count"]
                glds[x["key"]["naam"]][1] = x["count"]
            else:
                glds[x["key"]["naam"]][1] = x["count"]

    # df, sort, cut off > 20
    df = pd.DataFrame.from_dict(
        glds, orient="index", columns=["Bronhouder", "GLD", "Aanvulling"]
    )
    df = df.sort_values(["Aanvulling", "GLD"], ascending=[False, False])[:20]

    # format
    df.loc[:, "Actieve peilbuizen"] = ""
    df.loc[:, "Waarvan met grondwatermeting"] = ""

    for index, row in df.iterrows():
        df.at[index, "Actieve peilbuizen"] = format_dutch_number(row["GLD"])
        df.at[index, "Waarvan met grondwatermeting"] = format_dutch_number(
            row["Aanvulling"]
        )

    df.drop("GLD", inplace=True, axis=1)
    df.drop("Aanvulling", inplace=True, axis=1)

    html = df.to_html(index=False, justify="left", classes="tbl_wide")
    html = add_scope_to_table(html)

    return html
