import os
import re
import pandas as pd
import yaml
from metadata import get_china_province_code, get_china_city_code, get_china_area_name


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
    area_key = "province"
    province = report.get("省")
    confirmed = parse_int(report.get("确诊"))
    suspected = parse_int(report.get("疑似"))
    cured = parse_int(report.get("治愈"))
    dead = parse_int(report.get("死亡"))
    area_key = "city" if province else "province"
    confirmed_list = parse_list(report.get("确诊详情"), [area_key, "confirmed"])
    suspected_list = parse_list(report.get("疑似详情"), [area_key, "suspected"])
    cured_list = parse_list(report.get("治愈详情"), [area_key, "cured"])
    dead_list = parse_list(report.get("死亡详情"), [area_key, "dead"])

    data = None
    if confirmed or suspected or cured or dead:
        data = {
            "confirmed": confirmed,
            "suspected": suspected,
            "cured": cured,
            "dead": dead
        }
        if province:
            data["provinceCode"] = get_china_province_code(province)
            data["province"] = get_china_area_name(data["provinceCode"], province)

    for data_list in [confirmed_list, suspected_list, cured_list, dead_list]:
        if data_list:
            for x in data_list:
                if province:
                    x["provinceCode"] = get_china_province_code(province)
                    x["province"] = get_china_area_name(x["provinceCode"], province)
                    x["cityCode"] = get_china_city_code(x["provinceCode"], x["city"])
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
    df["date"] = date
    df["country"] = "中国"
    df["countryCode"] = "CN"
    df["province"].fillna("", inplace=True)
    df["provinceCode"].fillna("", inplace=True)
    df["city"].fillna("", inplace=True)
    df["cityCode"].fillna("", inplace=True)
    df.sort_values(["date", "countryCode", "provinceCode", "cityCode"], inplace=True)
    return df


for r in os.listdir("report"):
    report = read_report(os.path.join("report", r))
    report_data = parse_report(report)
    report_data.to_csv(f"""report_data/{report.get("时间")}{report.get("省", "")}.csv""", index=False)
