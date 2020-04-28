import os
import pandas as pd

data_dir = "Data"
csv_file = "Wuhan-2019-nCoV.csv"
dtype = {"provinceCode": str, "cityCode": str}

df = pd.read_csv(csv_file, dtype=dtype)

for d in df["date"].unique():
    df_date = df[df["date"] == d]
    df_date.to_csv(os.path.join(data_dir, f"{d}.csv"), index=False, encoding="utf-8")
    with open(os.path.join(data_dir, f"{d}.json"), "w", encoding="utf-8") as file:
        df_date.to_json(file, orient="records", force_ascii=False)
