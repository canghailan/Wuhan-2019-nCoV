import pandas as pd

csv_file = "Wuhan-2019-nCoV.csv"
json_file = "Wuhan-2019-nCoV.json"
dtype = {"provinceCode": str, "cityCode": str}

df = pd.read_csv(csv_file, dtype=dtype)
with open(json_file, "w", encoding="utf-8") as file:
    df.to_json(file, orient="records", force_ascii=False)