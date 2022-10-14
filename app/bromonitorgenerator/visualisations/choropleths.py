import plotly.express as px
import json
import logging
import os
import pandas as pd
import requests
from bromonitorgenerator.utils.colours import colours_dict_rgb
from bromonitorgenerator.utils.utils import API_BASE, plotly_fig_to_png
from common.config import date_format, logging_format

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format=logging_format, datefmt=date_format
)
log = logging.getLogger(__name__)


def __finalize_layout(fig):
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_traces(marker_line_color="black")
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}, showlegend=False, height=600
    )


def __quality_regime_dataframe(data):
    """Transforms the quality regime data as returned by the API
    into a pandas dataframe to use in the plotting function."""
    d = []
    for data_object in data:
        qrs = list(map(lambda qr: qr.get("key"), data_object["quality_regimes"]))
        if "IMBRO" in qrs:
            d.append((data_object["identifier"], "IMBRO"))
        elif "IMBRO/A" in qrs:
            d.append((data_object["identifier"], "IMBRO/A"))
        else:
            d.append((data_object["identifier"], "Geen"))
    return pd.DataFrame(d, columns=["statcode", "best_regime"])


def __quality_regime_map(geojson, bronhouder):
    """Plots a choropleth map of the 'highest' quality regime
    in which bronhouders have registered document."""
    with open(os.path.dirname(__file__) + f"/../geojson/{geojson}") as f:
        data = json.load(f)
    response = requests.get(
        API_BASE
        + f"/rapporten/kwaliteitsregimes-per-bronhouder?bronhoudertype={bronhouder}"
    )
    df = __quality_regime_dataframe(json.loads(response.content)["data"])
    fig = px.choropleth(
        df,
        geojson=data,
        locations=df["statcode"],
        color=df["best_regime"],
        color_discrete_map=colours_dict_rgb,
        featureidkey="properties.statcode",
        projection="mercator",
    )
    __finalize_layout(fig)
    return plotly_fig_to_png(fig)


def __object_type_counts_dataframe(data):
    """Transforms the object type data as returned by the API
    into a pandas dataframe to use in the plotting function."""
    type_dict = {}
    d = []
    for data_object in data:
        identifier = data_object["key"]["identifier"]
        if identifier not in type_dict.keys():
            type_dict[identifier] = []
        if data_object["count"] > 0:
            type_dict[identifier].append(data_object["key"]["type"])
    for k, v in type_dict.items():
        d.append((k, len(v)))
    return pd.DataFrame(d, columns=["statcode", "typecount"])


def __object_type_dataframe(data_docs):
    """Transforms the object type data as returned by the API
    into a pandas dataframe to use in the plotting function."""
    type_dict = {}
    d = []
    for data_object in data_docs:
        identifier = data_object["key"]["identifier"]
        if identifier not in type_dict.keys():
            type_dict[identifier] = []
        if data_object["count"] > 0:
            type_dict[identifier].append(data_object["key"]["type"])
    for k, v in type_dict.items():
        if "Grondwaterstandonderzoek_aangevuld" in v:
            d.append((k, "GLD"))
        elif "Grondwatermonitoringput" in v or "GeotechnischSondeeronderzoek" in v:
            d.append((k, "CPT+GMW"))
        else:
            d.append((k, "Geen"))
    return pd.DataFrame(d, columns=["statcode", "types"])


def __object_type_map(geojson, bronhouder):
    """Plots a choropleth map of the adoption of the BRO by bronhouders."""
    with open(os.path.dirname(__file__) + f"/../geojson/{geojson}") as f:
        data = json.load(f)
    response_docs = requests.get(
        API_BASE
        + f"/rapporten/brondocumenten-per-bronhouder?bronhoudertype={bronhouder}&gldstatus=ja&only_bronhouders=False"
    )
    df = __object_type_dataframe(json.loads(response_docs.content)["data"])
    fig = px.choropleth(
        df,
        geojson=data,
        locations=df["statcode"],
        color=df["types"],
        color_discrete_map=colours_dict_rgb,
        featureidkey="properties.statcode",
        projection="mercator",
    )
    __finalize_layout(fig)
    return plotly_fig_to_png(fig)


def municipality_object_types():
    """Plots the municipality object type map.
    Returns a png string encoded base64."""
    log.info(f"Generating municipality object type map.")
    return __object_type_map("gemeentegrenzen.json", "Gemeente")


def waterschap_object_types():
    """Plots the waterschap object type map.
    Returns a png string encoded base64."""
    log.info(f"Generating waterschap object type map.")
    return __object_type_map("waterschapsgrenzen.json", "Waterschap")


def province_object_types():
    """Plots the province object type map.
    Returns a png string encoded base64."""
    log.info(f"Generating province object type map.")
    return __object_type_map("provinciegrenzen.json", "Provincie")


def municipality_quality_regimes():
    """Plots the municipality quality regime map.
    Returns a png string encoded base64."""
    log.info(f"Generating municipality quality regime map.")
    return __quality_regime_map("gemeentegrenzen.json", "Gemeente")


def waterschap_quality_regimes():
    """Plots the waterschap quality regime map.
    Returns a png string encoded base64."""
    log.info(f"Generating waterschap quality regime map.")
    return __quality_regime_map("waterschapsgrenzen.json", "Waterschap")


def province_quality_regimes():
    """Plots the province quality regime map.
    Returns a png string encoded base64."""
    log.info(f"Generating province quality regime map.")
    return __quality_regime_map("provinciegrenzen.json", "Provincie")
