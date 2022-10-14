import logging
import locale
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from bromonitorgenerator.utils.colours import colours_dict
from bromonitorgenerator.utils.documentTypes import document_type_dict
from bromonitorgenerator.utils.start_date import get_start_date
from bromonitorgenerator.utils.utils import (
    API_BASE, format_dutch_number, plotly_fig_to_png)
from common.config import date_format, logging_format

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format=logging_format, datefmt=date_format)
log = logging.getLogger(__name__)


def __init_bar_data(object_types, data):
    bar_data = {}
    for t in object_types:
        bar_data[t] = {}
    for d in data:
        bar_data[d['object_type']][d['quality_regime']] = d['count']
    return bar_data


def __single_bar_trace(quality_regime, bar_data, object_types):
    xs = list(map(lambda bd: document_type_dict[bd], bar_data))
    ys = list(map(lambda t: bar_data[t].get(quality_regime, 0), object_types))
    return go.Bar(name=quality_regime,
                  marker_color=colours_dict[quality_regime][:-2],
                  texttemplate="%{value:,f}",
                  x=xs,
                  y=ys)


def __row_trace(table_values, row):
    table_values[0].append(row["TYPE"])
    table_values[1].append(row["IMBRO"])
    table_values[2].append(row["IMBRO/A"])
    table_values[3].append(row["TOTAAL"])


def generate_deltas_figure():
    log.info("Generating stacked barchart for object type deltas")
    # Get the current startdate and update the new one
    start_date = get_start_date()

    # Fetch data and init objects needed for the visualization
    response = requests.get(
        API_BASE + f"/rapporten/document-delta?start_datum={start_date}")
    data = json.loads(response.content)["data"]
    quality_regimes = ["IMBRO/A", "IMBRO"]
    object_types = sorted(document_type_dict.keys(),
                          key=lambda x: document_type_dict[x])
    bar_data = __init_bar_data(object_types, data)

    # Init plot
    fig = go.Figure()

    # Plot the stacked bars
    for q in quality_regimes:
        fig.add_trace(__single_bar_trace(q, bar_data, object_types))

    fig.update_layout(
        separators=',.',
        yaxis_tickformat=',f',
        autosize=True,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        width=900,
        height=500
    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', gridwidth=1, gridcolor='lightgray')

    return plotly_fig_to_png(fig)
