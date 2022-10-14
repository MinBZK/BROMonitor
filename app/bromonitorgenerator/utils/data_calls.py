import json
import requests
import math
import pandas as pd
from bromonitorgenerator.utils.utils import API_BASE


def bronhouder_per_maand():
    response = requests.get(
        API_BASE + "/rapporten/bronhouders-aanleveren-over-tijd")
    data = json.loads(response.content)["data"]

    # create a dictionary of amount of bronhouders per months
    monthly_dic = {}
    highest_amount = 0

    for row in data:
        id = str(row['monthyear'][1]) + '-' + str(row['monthyear'][0]).zfill(2)
        kvk = row['kvk']
        if id not in monthly_dic:
            monthly_dic[id] = {
                "bronhouders": [],
                "aantal": 0
            }
            if kvk not in monthly_dic[id]["bronhouders"]:
                monthly_dic[id]["bronhouders"].append(kvk)
                monthly_dic[id]["aantal"] += 1
        else:
            if kvk not in monthly_dic[id]["bronhouders"]:
                monthly_dic[id]["bronhouders"].append(kvk)
                monthly_dic[id]["aantal"] += 1
                if monthly_dic[id]["aantal"] > highest_amount:
                    highest_amount = monthly_dic[id]["aantal"]

    # round the highest amount up, to have a max for the graph
    max_graph = int(math.ceil(highest_amount / 10.0)) * 10

    # dict from df
    df = pd.DataFrame.from_dict(
        monthly_dic, orient='index', columns=['aantal'])
    df2 = df.sort_index()

    # add months that are not in the frame
    df2.index = pd.to_datetime(df2.index).to_period(freq='M')
    df2 = df2.reindex(pd.period_range(
        df2.index[0], df2.index[-1], freq='M'))
    df2['aantal'] = df2['aantal'].fillna(0)
    df2 = df2.set_index(df2.index.values.astype(str))

    return [df2, max_graph]
