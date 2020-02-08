import json
import re
from datetime import datetime
import requests
import pandas as pd
from metadata import get_country_code, get_china_province_code, get_china_city_code, get_china_area_name

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

# 读取头条数据
use_toutiao_date = "2020-02-07"
toutiao_forum = requests.get("https://i.snssdk.com/forum/home/v1/info/?forum_id=1656784762444839").json()
toutiao_data = json.loads(toutiao_forum["forum"]["extra"]["ncov_string_list"])

data_list = []
data_date = datetime.fromtimestamp(toutiao_data["updateTime"]).strftime('%Y-%m-%d')
for province in toutiao_data["provinces"]:
    data_list.append({
        "date": data_date,
        "countryCode": "CN",
        "country": "中国",
        "provinceCode": province["id"].ljust(6, '0'),
        "province": province["name"],
        "cityCode": "",
        "city": "",
        "confirmed": province["confirmedNum"],
        "suspected": 0,
        "cured": province["curesNum"],
        "dead": province["deathsNum"]
    })
    for city in province["cities"]:
        data_list.append({
            "date": data_date,
            "countryCode": "CN",
            "country": "中国",
            "provinceCode": province["id"].ljust(6, '0'),
            "province": province["name"],
            "cityCode": city["id"].ljust(6, '0'),
            "city": city["name"],
            "confirmed": city["confirmedNum"],
            "suspected": 0,
            "cured": city["curesNum"],
            "dead": city["deathsNum"]
        })
    for province_history in province["series"]:
        if province_history["date"] >= use_toutiao_date:
            data_list.append({
                "date": province_history["date"],
                "countryCode": "CN",
                "country": "中国",
                "provinceCode": province["id"].ljust(6, '0'),
                "province": province["name"],
                "cityCode": "",
                "city": "",
                "confirmed": province_history["confirmedNum"],
                "suspected": 0,
                "cured": province_history["curesNum"],
                "dead": province_history["deathsNum"]
            })
        # else:
        #     print(f"""忽略{province_history["date"]}{province["name"]}数据""")

data_list.append({
    "date": data_date,
    "countryCode": "CN",
    "country": "中国",
    "provinceCode": "",
    "province": "",
    "cityCode": "",
    "city": "",
    "confirmed": toutiao_data["nationTotal"]["confirmedTotal"],
    "suspected": toutiao_data["nationTotal"]["suspectedTotal"],
    "cured": toutiao_data["nationTotal"]["curesTotal"],
    "dead": toutiao_data["nationTotal"]["deathsTotal"]
})

for cn_history in toutiao_data["nationwide"]:
    if cn_history["date"] >= use_toutiao_date:
        data_list.append({
            "date": cn_history["date"],
            "countryCode": "CN",
            "country": "中国",
            "provinceCode": "",
            "province": "",
            "cityCode": "",
            "city": "",
            "confirmed": cn_history["confirmedNum"],
            "suspected": cn_history["suspectedNum"],
            "cured": cn_history["curesNum"],
            "dead": cn_history["deathsNum"]
        })
    # else:
    #     print(f"""忽略{cn_history["date"]}全国数据""")

for country in toutiao_data["world"]:
    data_list.append({
        "date": data_date,
        "country": country["country"],
        "confirmed": country["confirmedNum"],
        "suspected": country["suspectedNum"],
        "cured": country["curesNum"],
        "dead": country["deathsNum"]
    })

# 更新数据
csv_file = "Wuhan-2019-nCoV.csv"
json_file = "Wuhan-2019-nCoV.json"
xlsx_file = "Wuhan-2019-nCoV.xlsx"

df = pd.read_csv(csv_file)
df["date"] = df["date"].map(
    lambda x: "-".join([i.zfill(2) for i in re.split("\\D+", x)]))
df = pd.concat([df, pd.DataFrame(data_list)], sort=False)
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
df["countryCode"] = df["country"].map(get_country_code)
df["provinceCode"] = df["province"].map(get_china_province_code)
df["province"] = df.apply(
    lambda x: get_china_area_name(x.provinceCode, x.province), axis=1)
df["cityCode"] = df.apply(
    lambda x: get_china_city_code(x.provinceCode, x.city), axis=1)
df["city"] = df.apply(
    lambda x: get_china_area_name(x.cityCode, x.city), axis=1)
df.drop_duplicates(
    subset=["date", "country", "province", "city"], keep="last", inplace=True)
df.sort_values(["date", "countryCode", "provinceCode", "cityCode", "city"], inplace=True)
df.to_csv(csv_file, index=False, encoding='utf-8')
df.to_json(json_file, orient="records", force_ascii=False)
df.to_excel(xlsx_file, index=False)

print(f"""{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}数据更新成功""")
