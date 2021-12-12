import json

import pandas as pd
import git
import os

from mapping.stations import map_stations
from utils.sql_utils import insert_on_conflict_do_update

df_charging = pd.DataFrame()

#station_data = "data/Ladesaeulenregister.xlsx"

#github_ocm_data = "https://raw.githubusercontent.com/openchargemap/ocm-export/main/data/AD/OCM-163394.json"

exists = os.path.exists("./ocm-export")
if exists == False:
    git.Git("/data").clone("https://github.com/openchargemap/ocm-export")
else:
    rootdir = "./ocm-export/data"

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            # Opening JSON file
            f = open(os.path.join(subdir, file))

            # returns JSON object as a dictionary
            data = json.load(f)
            pandas_raw = pd.json_normalize(data)
            df_charging = df_charging.append(pandas_raw)
            df_charging = df_charging.reset_index(drop=True)
    df_mappped = map_stations(df_charging)
    insert_on_conflict_do_update(df_mappped, "stations", check_cols=['ID'])

