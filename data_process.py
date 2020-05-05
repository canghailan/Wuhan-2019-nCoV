import pandas as pd
from metadata import get_country_code, get_china_province_code, get_china_city_code, get_china_area_name

data_columns = [
    "date",
    "country",
    "countryCode",
    "province",
    "provinceCode",
    "city",
    "cityCode",
    "confirmed",
    "suspected",
    "cured",
    "dead"
]

data_dtype = {"provinceCode": str, "cityCode": str}

def normalize(df):
    df = df.reindex(columns=data_columns, copy=False)
    df["country"].fillna("", inplace=True)
    df["countryCode"].fillna("", inplace=True)
    df["province"].fillna("", inplace=True)
    df["provinceCode"].fillna("", inplace=True)
    df["city"].fillna("", inplace=True)
    df["cityCode"].fillna("", inplace=True)
    df["confirmed"] = df["confirmed"].fillna(0).astype(int)
    df["suspected"] = df["suspected"].fillna(0).astype(int)
    df["cured"] = df["cured"].fillna(0).astype(int)
    df["dead"] = df["dead"].fillna(0).astype(int)
    # 修正数据
    df["countryCode"] = df.apply(
        lambda x: get_country_code(x.country), axis=1)
    df["provinceCode"] = df.apply(
        lambda x: get_china_province_code(x.province, x.provinceCode), axis=1)
    df["province"] = df.apply(
        lambda x: get_china_area_name(x.provinceCode, x.province), axis=1)
    df["cityCode"] = df.apply(
        lambda x: get_china_city_code(x.provinceCode, x.city, x.cityCode), axis=1)
    df["city"] = df.apply(
        lambda x: get_china_area_name(x.cityCode, x.city), axis=1)
    df.drop_duplicates(
        subset=["date", "country", "province", "city"], keep="last", inplace=True)
    df.sort_values(["date", "countryCode", "provinceCode", "cityCode", "city"], inplace=True)
    return df


def to_json(csv_file, json_file):
    with open(json_file, "w", encoding="utf-8") as fs:
        pd.read_csv(csv_file, dtype=data_dtype).to_json(fs, orient="records", force_ascii=False)


def to_xlsx(csv_file, xlsx_file):
    pd.read_csv(csv_file, dtype=dtype).to_excel(xlsx_file, index=False)


def join_csv(csv_file, csv_file_list):
    with open(csv_file, "w", encoding="utf-8") as w:
        w.write("date,country,countryCode,province,provinceCode,city,cityCode,confirmed,suspected,cured,dead\n")
        for f in csv_file_list:
            with open(f, 'r', encoding="utf-8") as fs:
                header = True
                for line in fs:
                    if header:
                        header = False
                    else:
                        w.write(line)