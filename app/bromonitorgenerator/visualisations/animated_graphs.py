import os
import logging
import pandas as pd
import base64
from PIL import Image
from common.config import date_format, logging_format
from io import BytesIO
import plotly.express as px


from bromonitorgenerator.utils.utils import API_BASE
from bromonitorgenerator.utils.data_calls import bronhouder_per_maand


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format=logging_format, datefmt=date_format)
log = logging.getLogger(__name__)


# Generates a linechart gif image to use in the static bromonitor
def generate_linechart_bronhouder_permaand():
    log.info("Generating animated chart for bronhouders")

    df, max_graph = bronhouder_per_maand()

    # create images to put in the gif
    frames = []

    for i in range(2, len(df.index)):
        # get a part of the df so the line can grow
        df2 = df[:i]

        # make the fig
        fig = px.line(
            df2, x=df2.index, y=df2["aantal"]
        )
        fig.update_layout(
            xaxis_tickformat='%Y-%m',
            xaxis_title='Periode',
            yaxis_range=[0, max_graph],
            yaxis_title='Aantal',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            width=900,
            height=500
        )

        fig.update_xaxes(showline=True, linewidth=2, linecolor='black', gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='black', gridwidth=1, gridcolor='lightgray')


        # make the fig into png and import the png to pillow image
        img_bytes = fig.to_image(format="png")
        image = Image.open(BytesIO(img_bytes))

        # make the png into a gif
        frame = Image.composite(image, Image.new(
            'RGB', image.size, 'white'), image)

        # save the gif to improve graphics and add to frame list
        fobj = BytesIO()
        frame.save(fobj, 'gif')
        frame = Image.open(fobj)
        frames.append(frame)

    # settings for the gif
    durations = [10] * (len(frames) + 1)
    durations[-1] = 1000

    # save gif for testing
    # frames[0].save('out.gif', save_all=True,
    #               append_images=frames, duration=durations)

    # save the gif
    animated_gif = BytesIO()
    frames[0].save(animated_gif, save_all=True, append_images=frames,
                   format="GIF", duration=durations)

    # encode and decode gif
    base64_bytes = base64.b64encode(animated_gif.getvalue())
    return base64_bytes.decode()
