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

# 读取腾讯新闻实时统计数据
# cn_global_api = "https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_global_vars"
# cn_global_data = requests.get(cn_global_api).json()
# cn_global = json.loads(cn_global_data["data"])
# cn_global_df = pd.DataFrame(cn_global)
# cn_global_df.rename(columns={
#     "area": "province",
#     "confirmCount": "confirmed",
#     "suspectCount": "suspected",
#     "cure": "cured",
#     "deadCount": "dead"
# }, inplace=True)
# cn_global_df["date"] = datetime.today().strftime('%Y-%m-%d')
# cn_global_df["country"] = "中国"
# cn_global_df = pd.DataFrame(cn_global_df, columns=columns)


# 读取腾讯新闻实时分地区数据
cn_area_api = "https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_area_counts"
cn_area_data = requests.get(cn_area_api).json()
cn_area = json.loads(cn_area_data["data"])
cn_area_df = pd.DataFrame(cn_area)
cn_area_df.rename(columns={
    "area": "province",
    "confirm": "confirmed",
    "suspect": "suspected",
    "heal": "cured"
}, inplace=True)
cn_area_df["date"] = datetime.today().strftime('%Y-%m-%d')


# 读取腾讯新闻日统计数据
cn_day_api = "https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_cn_day_counts"
cn_day_data = requests.get(cn_day_api).json()
cn_day = json.loads(cn_day_data["data"])
cn_day_df = pd.DataFrame(cn_day)
cn_day_df.rename(columns={
    "confirm": "confirmed",
    "suspect": "suspected",
    "heal": "cured"
}, inplace=True)
cn_day_df["date"] = cn_day_df["date"].map(
    lambda x: "2020-" + x.replace(".", "-"))
cn_day_df["country"] = "中国"
cn_day_df = cn_day_df[cn_day_df.date >= "2020-01-20"]


# 更新数据
csv_file = "Wuhan-2019-nCoV.csv"
json_file = "Wuhan-2019-nCoV.json"

df = pd.read_csv(csv_file)
# report_df_list = [pd.read_csv(os.path.join("ReportData", x)) for x in sorted(os.listdir("ReportData"))]
df["date"] = df["date"].map(
    lambda x: "-".join([i.zfill(2) for i in re.split("\\D+", x)]))
# df = pd.concat([df, cn_area_df, cn_global_df, cn_day_df] + report_df_list, sort=False)
df = pd.concat([df, cn_area_df, cn_day_df], sort=False)
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

print(f"""{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}数据更新成功""")
