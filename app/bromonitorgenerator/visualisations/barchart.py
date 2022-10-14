import logging
import os
import plotly.graph_objects as go
import requests
import json
from plotly.graph_objects import Layout
from bromonitorgenerator.utils.documentTypes import document_type_dict
from bromonitorgenerator.utils.utils import API_BASE, plotly_fig_to_png
from common.config import date_format, logging_format

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format=logging_format, datefmt=date_format)
log = logging.getLogger(__name__)


# Generates a barchart png image to use in the static bromonitor
# Input is a list of count aggregates
def generate_barchart():
    log.info("Generating barchart for object types")
    response = requests.get(API_BASE + "/rapporten/documenttypes")
    data = json.loads(response.content)["data"]

    fig = go.Figure([go.Bar(x=list(
        map(lambda x: document_type_dict[x["key"]], data)),
        y=list(
        map(lambda x: x["count"], data)),
        texttemplate="%{value:,f}",
        textposition='auto'
    )])
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
