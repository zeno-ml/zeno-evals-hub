import os

import pandas as pd
from zeno import DistillReturn, distill

# read file from same directory as this file
area_df = pd.read_csv(os.path.dirname(__file__) + "/country-areas.csv")
# set index to country
area_df.set_index("country", inplace=True)
# given a string like 23,180 (8,950) extract the first number

area_df = area_df[area_df["land"] != "not determined"]
area_df["area"] = area_df["land"].apply(
    lambda x: x if isinstance(x, float) else float(x.split(" ")[0].replace(",", ""))
)


@distill
def area(df, ops):
    areas = []
    for output in df[ops.label_column]:
        if output in area_df.index:
            areas.append(area_df.loc[output]["area"])
        else:
            areas.append(-1)
    return DistillReturn(distill_output=areas)
