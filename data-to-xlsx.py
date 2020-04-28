import pandas as pd

csv_file = "Wuhan-2019-nCoV.csv"
xlsx_file = "Wuhan-2019-nCoV.xlsx"
dtype = {"provinceCode": str, "cityCode": str}

df = pd.read_csv(csv_file, dtype=dtype)
df.to_excel(xlsx_file, index=False)