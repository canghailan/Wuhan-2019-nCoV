import json
import os
import re
from datetime import datetime, timedelta
import requests
import pandas as pd
import data_process


# 读取头条数据
use_toutiao_date = "2020-02-09"
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


df = pd.DataFrame(data_list)
df = data_process.normalize(df)


csv_date = os.path.join("Data", f"{data_date}.csv")
json_date = os.path.join("Data", f"{data_date}.json")
df_date = df[df["date"] == data_date]
df_date.to_csv(csv_date, index=False, encoding='utf-8')
with open(json_date, "w", encoding="utf-8") as f:
    df_date.to_json(f, orient="records", force_ascii=False)


yesterday = datetime.strftime(datetime.strptime(data_date, "%Y-%m-%d") - timedelta(days=1), "%Y-%m-%d")
csv_yesterday = os.path.join("Data", f"{yesterday}.csv")
json_yesterday = os.path.join("Data", f"{yesterday}.json")
df_yesterday = pd.read_csv(csv_yesterday, dtype=data_process.data_dtype)
df_yesterday = pd.concat([df_yesterday, pd.DataFrame(df[df["date"] == csv_yesterday])], sort=False)
df_yesterday = data_process.normalize(df_yesterday)
df_yesterday.to_csv(csv_yesterday, index=False, encoding='utf-8')
with open(json_yesterday, "w", encoding="utf-8") as f:
    df_yesterday.to_json(f, orient="records", force_ascii=False)

print(f"""{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}数据更新成功""")
