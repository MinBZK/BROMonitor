import logging
import os
import numpy as np
import plotly.graph_objects as go
import requests
import json
from bromonitorgenerator.utils.utils import API_BASE, plotly_fig_to_png
from common.config import date_format, logging_format

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format=logging_format, datefmt=date_format)
log = logging.getLogger(__name__)


# Generates a linegraph for objects through time(years)
# Input is a list of count aggregates
def generate_line_graph(object_type):
    log.info(f"Generating line graph for objects over time for {object_type}")
    response = requests.get(
        API_BASE + f"/rapporten/documenten-over-tijd?object_type={object_type}")
    data = json.loads(response.content)["data"]
    years = list(map(lambda x: x["key"], data))
    cumsums = np.cumsum(list(map(lambda x: x["count"], data)))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years,
                             y=cumsums,
                             mode='lines'
                             ))

    # Set the x-axis labels for concrete years only
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=years,
            ticktext=years
        ),
        autosize=True,
        separators=',.',
        yaxis_tickformat=',f',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=20, t=20, b=20),
        width=900,
        height=500
    )

    # Add styling to axes
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(title_text='Aantal registraties', showline=True, linewidth=2, linecolor='black', gridwidth=1, gridcolor='lightgray')

    return plotly_fig_to_png(fig)
