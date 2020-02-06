import os
import re
import pandas as pd
import yaml
from metadata import get_country_code, get_china_province_code, get_china_city_code, get_china_area_name


def read_report(fp):
    with open(fp, "r") as f:
        return yaml.load(f, Loader=yaml.Loader)


def parse_int(text):
    if text:
        result = re.search("\\d+", text)
        if result:
            return result.group()


def parse_list(text, keys):
    if text:
        result = []
        for i in re.finditer("([\u4e00-\u9fa5]+)(\\d+)", text):
            result.append({
                keys[0]: i.group(1),
                keys[1]: i.group(2)
            })
        return result


def parse_report(report):
    date = str(report["时间"])
    province = report.get("省", "")
    confirmed = parse_int(report.get("确诊"))
    suspected = parse_int(report.get("疑似"))
    cured = parse_int(report.get("治愈"))
    dead = parse_int(report.get("死亡"))
    area_key = "city" if province else "province"
    confirmed_list = parse_list(report.get("确诊详情"), [area_key, "confirmed"])
    suspected_list = parse_list(report.get("疑似详情"), [area_key, "suspected"])
    cured_list = parse_list(report.get("治愈详情"), [area_key, "cured"])
    dead_list = parse_list(report.get("死亡详情"), [area_key, "dead"])
    foreign_confirmed_list = parse_list(report.get("国外确诊详情"), ["country", "confirmed"])
    foreign_cured_list = parse_list(report.get("国外治愈详情"), ["country", "cured"])

    provinceCode = get_china_province_code(province) if province else ""
    province = get_china_area_name(provinceCode, province) if provinceCode else ""

    data = {
        "provinceCode": provinceCode,
        "province": province,
        "confirmed": confirmed,
        "suspected": suspected,
        "cured": cured,
        "dead": dead
    }

    for data_list in [confirmed_list, suspected_list, cured_list, dead_list]:
        if data_list:
            for x in data_list:
                if province:
                    x["provinceCode"] = provinceCode
                    x["province"] = province
                    x["cityCode"] = get_china_city_code(provinceCode, x["city"])
                    x["city"] = get_china_area_name(x["cityCode"], x["city"])
                else:
                    x["provinceCode"] = get_china_province_code(x["province"])
                    x["province"] = get_china_area_name(x["provinceCode"], x["province"])

    df_list = [pd.DataFrame(x) for x in [confirmed_list, suspected_list, cured_list, dead_list] if x]
    df = None
    for index, x in enumerate(df_list):
        if df is None:
            df = x
        else:
            df = pd.merge(df, x, on=area_key, how="outer", suffixes=["", f"""_{index}"""], sort=False, copy=False)

    columns = [
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
    if df is None:
        df = pd.DataFrame([data], columns=columns)
    else:
        df = pd.DataFrame(df, columns=columns)
        df = df.append([data])
    df["country"] = "中国"
    df["countryCode"] = "CN"
    df["province"].fillna(province, inplace=True)
    df["provinceCode"].fillna(provinceCode, inplace=True)
    df["city"].fillna("", inplace=True)
    df["cityCode"].fillna("", inplace=True)
    df["provinceCode"] = df["province"].map(get_china_province_code)
    df["cityCode"] = df.apply(
        lambda x: get_china_city_code(x.provinceCode, x.city), axis=1)

    for data_list in [foreign_confirmed_list, foreign_cured_list]:
        if data_list:
            for x in data_list:
                x["countryCode"] = get_country_code(x["country"])

    foreign_df = None
    foreign_df_list = [pd.DataFrame(x) for x in [foreign_confirmed_list, foreign_cured_list] if x]
    for index, x in enumerate(foreign_df_list):
        if foreign_df is None:
            foreign_df = x
        else:
            foreign_df = pd.merge(foreign_df, x, on="country", how="outer", suffixes=["", f"""_{index}"""], sort=False, copy=False)
    if foreign_df is not None:
        df = pd.concat([df, pd.DataFrame(foreign_df, columns=columns)], sort=False)

    df["date"] = date
    df.sort_values(["date", "countryCode", "provinceCode", "cityCode", "city"], inplace=True)
    return df


parse_date = "2020-01-31"
for r in os.listdir("Report"):
    try:
        report = read_report(os.path.join("Report", r))
        if str(report["时间"]) >= parse_date:
            report_data = parse_report(report)
            report_data.to_csv(f"""ReportData/{report.get("时间")}{report.get("省", "")}.csv""", index=False)
    except Exception as e:
        print(r)
        raise e

# 合并通报数据
csv_file = "Wuhan-2019-nCoV.csv"
json_file = "Wuhan-2019-nCoV.json"
xlsx_file = "Wuhan-2019-nCoV.xlsx"
dtype = {"provinceCode": str, "cityCode": str}
df = pd.read_csv(csv_file, dtype=dtype)
report_df_list = [pd.read_csv(os.path.join("ReportData", x), dtype=dtype) for x in sorted(os.listdir("ReportData"))]
df = pd.concat([df] + report_df_list, sort=False)
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
df.drop_duplicates(
    subset=["date", "country", "province", "city"], keep="last", inplace=True)
df.sort_values(["date", "countryCode", "provinceCode", "cityCode", "city"], inplace=True)
df.to_csv(csv_file, index=False, encoding='utf-8')
df.to_json(json_file, orient="records", force_ascii=False)
df.to_excel(xlsx_file, index=False)
