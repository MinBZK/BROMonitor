import logging
import os
import json
import requests
import pandas as pd
import numpy as np
from bromonitorgenerator.utils.utils import (
    get_object_type_label,
    get_quality_regime_label,
)
from bromonitorgenerator.utils.utils import add_scope_to_table
from bromonitorgenerator.utils.documentTypes import document_type_dict
from common.config import date_format, logging_format
from bromonitorgenerator.utils.utils import API_BASE, format_dutch_number
from bromonitorgenerator.utils.start_date import get_start_date
from bromonitorgenerator.utils.data_calls import bronhouder_per_maand

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format=logging_format, datefmt=date_format
)
log = logging.getLogger(__name__)


def full_to_short(name: str):
    d = {
        "Grondwatermonitoringnet": "GMN",
        "BodemkundigWandonderzoek": "SFR",
        "GeotechnischBooronderzoek": "BHR-GT",
        "Grondwaterstandonderzoek": "GLD",
        "Grondwatermonitoringput": "GMW",
        "GeotechnischSondeeronderzoek": "CPT",
        "BodemkundigBooronderzoek": "BHR-P",
    }
    if name in d.keys():
        return d[name]
    return name


def generate_barchart_table():
    log.info("Generating acc table for with barchart for object types")
    response = requests.get(API_BASE + "/rapporten/documenttypes")
    data = json.loads(response.content)["data"]

    short_types = []
    for item in data:
        short_types.append(full_to_short(item["key"]))

    df = pd.DataFrame(
        {
            "Type": short_types,
            "Aantal": list(
                map(lambda x: "{:,}".format(x["count"]).replace(",", "."), data)
            ),
        }
    )
    html = df.to_html(index=False, justify="left", classes="tbl_small")
    html = add_scope_to_table(html)
    return html


def generate_line_graph_table(object_type, name_plural):
    log.info(f"Generating acc table for objects over time for {object_type}")
    response = requests.get(
        API_BASE + f"/rapporten/documenten-over-tijd?object_type={object_type}"
    )
    data = json.loads(response.content)["data"]
    cumsums = np.cumsum(list(map(lambda x: x["count"], data)))

    df = pd.DataFrame(
        {
            "Jaar": list(map(lambda x: x["key"], data)),
            "Totaal aantal "
            + name_plural
            + " in BRO": list(
                map(lambda x: "{:,}".format(x).replace(",", "."), cumsums)
            ),
        }
    )
    html = df.to_html(index=False, justify="left", classes="tbl_small")
    html = add_scope_to_table(html)
    return html


def generate_deltas_table():
    log.info("Generating acc table for object type deltas")
    # Get the current startdate
    start_date = get_start_date()

    # Fetch data and init objects needed for the visualization
    response = requests.get(
        API_BASE + f"/rapporten/document-delta?start_datum={start_date}"
    )
    data = json.loads(response.content)["data"]
    quality_regimes = ["IMBRO/A", "IMBRO"]
    document_types_dutch = list(document_type_dict.keys())

    bar_data = {}
    bar_data["Type"] = document_types_dutch
    bar_data["Type"].append("Totaal")
    bar_data["IMBRO"] = [0] * len(document_types_dutch)
    bar_data["IMBRO/A"] = [0] * len(document_types_dutch)
    bar_data["Totaal"] = [0] * len(document_types_dutch)

    for i in data:
        if i["quality_regime"] == "IMBRO":
            position = bar_data["Type"].index(i["object_type"])
            bar_data["IMBRO"][position] += i["count"]
            bar_data["Totaal"][position] += i["count"]
            bar_data["IMBRO"][-1] += i["count"]
            bar_data["Totaal"][-1] += i["count"]
        else:
            position = bar_data["Type"].index(i["object_type"])
            bar_data["IMBRO/A"][position] += i["count"]
            bar_data["Totaal"][position] += i["count"]
            bar_data["IMBRO/A"][-1] += i["count"]
            bar_data["Totaal"][-1] += i["count"]

    bar_data["IMBRO/A"] = [
        "{:,}".format(x).replace(",", ".") for x in bar_data["IMBRO/A"]
    ]
    bar_data["IMBRO"] = ["{:,}".format(x).replace(",", ".") for x in bar_data["IMBRO"]]
    bar_data["Totaal"] = [
        "{:,}".format(x).replace(",", ".") for x in bar_data["Totaal"]
    ]

    pretty = []
    for item in bar_data["Type"]:
        pretty.append(full_to_short(item))
    bar_data["Type"] = pretty

    df = pd.DataFrame.from_dict(bar_data)

    html = df.to_html(index=False, justify="left", classes="tbl_wide")
    html = add_scope_to_table(html)
    return html


def table_quality_regime_map(bronhouder):
    log.info("Generating acc table for " + bronhouder + " quality regime map.")
    response = requests.get(
        API_BASE
        + f"/rapporten/kwaliteitsregimes-per-bronhouder?bronhoudertype={bronhouder}"
    )
    data = json.loads(response.content)["data"]
    table_data = {}

    for i in data:
        if i["bronhouder"] not in table_data.keys():
            values = {"IMBRO": 0, "IMBRO/A": 0}
            for j in i["quality_regimes"]:
                values[j["key"]] = format_dutch_number(j["count"])
            table_data[i["bronhouder"]] = values
        table_data[i["bronhouder"]]["Indicatie"] = get_quality_regime_label(
            table_data[i["bronhouder"]]
        )
    cols = [bronhouder, "Indicatie", "IMBRO", "IMBRO/A"]
    df = (
        pd.DataFrame(table_data)
        .T.reset_index()
        .rename(columns={"index": bronhouder})[cols]
        .sort_values(bronhouder)
    )
    html = df.to_html(index=False, justify="left", classes=["tbl_wide", "tbl_map"])
    html = add_scope_to_table(html)
    return html


def table_object_type_map(bronhouder):
    log.info("Generating acc table for " + bronhouder + " object type map.")
    response = requests.get(
        API_BASE
        + f"/rapporten/brondocumenten-per-bronhouder?bronhoudertype={bronhouder}&gldstatus=ja"
    )
    data = json.loads(response.content)["data"]
    table_data = {}

    for i in data:
        i["key"]["naam"] = i["key"]["naam"].replace(bronhouder + " ", "")
        if bronhouder == "Waterschap" and "Hoogheemraadschap" in i["key"]["naam"]:
            i["key"]["naam"] = i["key"]["naam"].replace("Hoogheemraadschap ", "")
        if i["key"]["naam"] not in table_data.keys():
            values = {
                "Grondwatermonitoringput": 0,
                "GeotechnischSondeeronderzoek": 0,
                "GeotechnischBooronderzoek": 0,
                "Grondwaterstandonderzoek": 0,
                "Grondwaterstandonderzoek_aangevuld": 0,
            }
            values[i["key"]["type"]] = format_dutch_number(i["count"])
            table_data[i["key"]["naam"]] = values
        else:
            table_data[i["key"]["naam"]][i["key"]["type"]] = format_dutch_number(
                i["count"]
            )
    for td in table_data:
        if not "Indicatie" in table_data[td]:
            table_data[td]["Indicatie"] = get_object_type_label(table_data[td])

    cols = [
        bronhouder,
        "Indicatie",
        "Grondwatermonitoringput",
        "GeotechnischSondeeronderzoek",
        "GeotechnischBooronderzoek",
        "Grondwaterstandonderzoek",
        "Grondwaterstandonderzoek_aangevuld",
    ]
    df = (
        pd.DataFrame(table_data)
        .T.reset_index()
        .rename(columns={"index": bronhouder})[cols]
        .sort_values(bronhouder)
        .rename(
            columns={
                "Grondwatermonitoringput": "GMW",
                "GeotechnischSondeeronderzoek": "CPT",
                "GeotechnischBooronderzoek": "BHR-GT",
                "Grondwaterstandonderzoek": "GLD",
                "Grondwaterstandonderzoek_aangevuld": "GLD met meting",
            }
        )
    )
    html = df.to_html(index=False, justify="left", classes=["tbl_wide", "tbl_map"])
    html = add_scope_to_table(html)
    return html


def generate_table_bronhouder_permaand():
    log.info("Generating acc table for bronhouders per maand")
    # Get data as df and improve the df
    df, max_graph = bronhouder_per_maand()
    df.insert(0, "Maand", df.index)
    df["aantal"] = df["aantal"].astype(int)
    df.columns = ["Maand", "Aantal bronhouders"]

    html = df.to_html(index=False, justify="left", classes="tbl_small")
    html = add_scope_to_table(html)

    return html


def generate_data_bronhouder_type(bronhouder: str, doctype: str):
    log.info(f"Generating data for {bronhouder} - {doctype}")
    if doctype == "objecttypen":
        response = requests.get(
            API_BASE
            + f"/rapporten/brondocumenten-per-bronhouder?bronhoudertype={bronhouder}&gldstatus=ja&only_bronhouders=False"
        )
        return json.loads(response.content)["data"]
    else:
        response = requests.get(
            API_BASE
            + f"/rapporten/kwaliteitsregimes-per-bronhouder?bronhoudertype={bronhouder}"
        )
        return json.loads(response.content)["data"]


def get_number_of_bronhouders(data: list):
    bronhouders = []
    for entry in data:
        if entry["count"] > 0:
            bronhouders.append(entry["key"]["kvk"])
    nr_bronhouders = len(set(bronhouders))
    return "{:,}".format(nr_bronhouders).replace(",", ".")
