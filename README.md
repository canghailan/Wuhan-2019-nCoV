# 2019-nCoV 全量每日统计数据（支持接口读取）

本项目记录了2019-12-01日至今，每日精确到国家、省、市的确诊、疑似、治愈、死亡人数。

2019-12-01至2020-01-02数据来自[asycns](https://github.com/asycns)提供的[实验室确诊数据](https://github.com/canghailan/Wuhan-2019-nCoV/issues/1)([实验室论文原文](https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)30183-5/fulltext))。

2020-01-02至2020-01-10数据无变化。

2020-01-10至2020-02-06数据来自国家、各省、武汉市卫健委疫情通告。

2020-02-07后数据从[今日头条](https://i.snssdk.com/ugc/hotboard_fe/hot_list/template/hot_list/forum_tab.html)[接口](https://i.snssdk.com/forum/home/v1/info/?forum_id=1656784762444839)采集，每小时57分自动更新。国家、省级历史数据会根据卫健委数据更新，市级历史数据与卫健委数据有差异（略小于）。

数据以CSV格式存储在版本库中，同时提供JSON及EXCEL格式数据。

建议读取CSV格式数据（体积较小），通过[脚本](https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/parseCSV.js)转换为JSON格式。

目前接口只提供全量数据，需自行在客户端进行预处理，过滤出所需数据。

数据各字段已标准化，国家、国家代码遵循ISO-3166标准，省、市遵循中华人民共和国民政部2019年中华人民共和国行政区划代码。


## 数据接口
* https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.csv
* https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.json

### CSV转JSON
* https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/parseCSV.js

### 省市区、国家代码
* https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/ChinaAreaCode.csv
* https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/CountryCode.csv


## 数据使用示例
```javascript
let data_list = parseCSV(
`date,country,countryCode,province,provinceCode,city,cityCode,confirmed,suspected,cured,dead
2020-01-16,中国,CN,,,,,45,0,15,2
2020-01-16,中国,CN,湖北省,420000,,,45,0,15,2
2020-01-16,中国,CN,湖北省,420000,武汉市,420100,45,0,15,2
2020-01-16,日本,JP,,,,,1,0,0,0
2020-01-16,泰国,TH,,,,,1,0,0,0
2020-01-17,中国,CN,,,,,62,0,19,2
2020-01-17,中国,CN,湖北省,420000,,,62,0,19,2
2020-01-17,中国,CN,湖北省,420000,武汉市,420100,62,0,19,2
2020-01-18,中国,CN,,,,,198,0,24,3
2020-01-18,中国,CN,湖北省,420000,,,121,0,24,3
2020-01-18,中国,CN,湖北省,420000,武汉市,420100,121,0,24,3
2020-01-19,中国,CN,,,,,275,0,25,4
2020-01-19,中国,CN,湖北省,420000,,,198,0,25,3
2020-01-19,中国,CN,湖北省,420000,武汉市,420100,198,0,25,3
2020-01-19,中国,CN,广东省,440000,,,1,0,0,0
2020-01-19,中国,CN,广东省,440000,深圳市,440300,1,0,0,0`, 
{ confirmed: Number, suspected: Number, cured: Number, dead: Number });
// 2020-01-16所有数据
let date_list = data_list.filter(e => e.date == '2020-01-16');
// 2020-01-16所有国家级数据
let date_country_list = data_list.filter(e => e.date == '2020-01-16' && !e.province);
// 2020-01-19所有省级数据
let date_province_list = data_list.filter(e => e.date == '2020-01-19' && e.province && !e.city);
// 2020-01-19湖北省所有市级数据
let date_province_city_list = data_list.filter(e => e.date == '2020-01-19' && e.province == '湖北省' && e.city);
// 2020-01-19湖北省武汉市数据
let date_city = data_list.filter(e => e.date == '2020-01-19' && e.province == '湖北省' && e.city == '武汉市');
// 中国所有时间数据
let country_list = data_list.filter(e => e.country == '中国' && !e.province);
// 湖北省所有时间数据
let province_list = data_list.filter(e => e.province == '湖北省' && !e.city);
// 湖北省武汉市所有时间数据
let city_list = data_list.filter(e => e.province == '湖北省' && e.city == '武汉市'); 
```


## 数据说明

| 字段           | 说明    |
| ------------ | ----- |
| date         | 时间（天） |
| country      | 国家    |
| countryCode  | 国家代码  |
| province     | 省     |
| provinceCode | 省代码   |
| city         | 市     |
| cityCode     | 市代码   |
| confirmed    | 确诊人数  |
| suspected    | 疑似人数  |
| cured        | 治愈人数  |
| dead         | 死亡人数  |


```shell
Report # 卫健委通报数据
ReportData # 卫健委通报整理后数据
PIIS0140673620301835.pdf # 2019-12-01至2019-01-02实验室数据
Wuhan-2019-nCoV.csv # CSV格式完整数据（数据格式较小，建议使用）
Wuhan-2019-nCoV.json # JSON格式完整数据
Wuhan-2019-nCoV.xlsx # EXCEL格式完整数据，供阅读、手工处理
parseCSV.js # CSV转JSON
ChinaAreaCode.csv # 中国行政区划代码，来自中华人民共和国民政部
CountryCode.csv # 国家地区代码（ISO_3166-1）
```


TODO:

* GeoJSON
* 图表
* 与SARS对比



## 疫情通报（原始数据）

* [中华人民共和国国家卫生健康委员会](http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml)
  * [湖北省卫生健康委员会](http://wjw.hubei.gov.cn/bmdt/ztzl/fkxxgzbdgrfyyq/xxfb/)
    * [武汉市卫生健康委员会](http://wjw.wuhan.gov.cn/front/web/list3rd/no/802)
  * [北京市卫生健康委员会](http://wjw.beijing.gov.cn/wjwh/ztzl/xxgzbd/gzbdyqtb/)
  * [天津市卫生健康委员会](http://wsjk.tj.gov.cn/col/col87/index.html)
  * [河北省卫生健康委员会](http://wsjkw.hebei.gov.cn/index.do?cid=326&templet=list)
  * [山西省卫生健康委员会](http://wjw.shanxi.gov.cn/xingfew/index.hrh)
  * [内蒙古自治区卫生健康委员会](http://wjw.nmg.gov.cn/ztlm/2016n/xxgzbdgrdfyyqfk/yqtb/index.shtml)
  * [辽宁省卫生健康委员会](http://wsjk.ln.gov.cn/wst_zdzt/xxgzbd/yqtb/)
  * [吉林省卫生健康委员会](http://www.jl.gov.cn/szfzt/jlzxd/yqtb/)
  * [黑龙江省卫生健康委员会](http://wsjkw.hlj.gov.cn/index.php/Home/Zwgk/all/typeid/42)
  * [上海市卫生健康委员会](http://wsjkw.sh.gov.cn/xwfb/index.html)
  * [江苏省卫生健康委员会](http://wjw.jiangsu.gov.cn/col/col7290/index.html)
  * [浙江省卫生健康委员会](http://www.zjwjw.gov.cn/col/col1202101/index.html)
  * [安徽省卫生健康委员会](http://wjw.ah.gov.cn/news_list_477_1.html)
  * [福建省卫生健康委员会](http://wjw.fujian.gov.cn/xxgk/gzdt/wsjsyw/)
  * [江西省卫生健康委员会](http://hc.jiangxi.gov.cn/xwzx/wjxw/index.shtml)
  * [山东省卫生健康委员会](http://wsjkw.shandong.gov.cn/wzxxgk/zwgg/)
  * [河南省卫生健康委员会](http://wsjkw.henan.gov.cn/channels/854.shtml)
  * [湖南省卫生健康委员会](http://wjw.hunan.gov.cn/wjw/xxgk/gzdt/zyxw_1/index.html)
  * [广东省卫生健康委员会](http://wsjkw.gd.gov.cn/xxgzbdfk/yqtb/)
  * [广西壮族自治区卫生健康委员会](http://wsjkw.gxzf.gov.cn/zhuantiqu/ncov/ncovyqtb/)
  * [海南省卫生健康委员会](http://wst.hainan.gov.cn/swjw/rdzt/yqfk/)
  * [重庆市卫生健康委员会](http://wsjkw.cq.gov.cn/yqxxyqtb/)
  * [四川省卫生健康委员会](http://wsjkw.sc.gov.cn/scwsjkw/gggs/tygl.shtml)
  * [贵州省卫生健康委员会](http://www.gzhfpc.gov.cn/ztzl_500663/xxgzbdgrdfyyqfk/yqdt/)
  * [云南省卫生健康委员会](http://ynswsjkw.yn.gov.cn/wjwWebsite/web/col?id=UU157976428326282067&cn=xxgzbd&pcn=ztlm&pid=UU145102906505319731)
  * [西藏自治区卫生健康委员会](http://wjw.xizang.gov.cn/xwzx/wsjkdt/) [疫情](http://wjw.xizang.gov.cn/xwzx/wsjkdt/202001/t20200129_131159.html)
  * [陕西省卫生健康委员会](http://sxwjw.shaanxi.gov.cn/col/col863/index.html)
  * [甘肃省卫生健康委员会](http://wsjk.gansu.gov.cn/channel/10910/index.html)
  * [青海省卫生健康委员会](https://wsjkw.qinghai.gov.cn/zhxw/xwzx/index.html)
  * [宁夏回族自治区卫生健康委员会](http://wsjkw.nx.gov.cn/yqfkdt/yqsd1.htm)
  * [新疆维吾尔自治区卫生健康委员会](http://www.xjhfpc.gov.cn/ztzl/fkxxgzbdfygz/yqtb.htm)
  * ~~[新疆生产建设兵团卫生健康委员会](http://wsj.xjbt.gov.cn/xxgk/tzgg/)~~ 数据合并至新疆维吾尔自治区卫生健康委员会

* [Clinical features of patients infected with 2019 novel coronavirus in Wuhan, China](https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)30183-5/fulltext)
* [Early Transmission Dynamics in Wuhan, China, of Novel Coronavirus–Infected Pneumonia](https://www.nejm.org/doi/full/10.1056/NEJMoa2001316)


## 数据来源

* [今日头条](https://i.snssdk.com/ugc/hotboard_fe/hot_list/template/hot_list/forum_tab.html)
  * [数据接口](https://i.snssdk.com/forum/home/v1/info/?forum_id=1656784762444839)
* [丁香医生](https://3g.dxy.cn/newh5/view/pneumonia)
* ~~[腾讯新闻](https://news.qq.com//zt2020/page/feiyan.htm)~~
  * ~~[日统计](https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_cn_day_counts)~~
  * ~~[实时全国统计](https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_global_vars)~~
  * ~~[实时省、市统计](https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_area_counts)~~



## 数据更新
```shell
export PIPENV_VENV_IN_PROJECT=1 && pipenv install
pipenv run python dataset.py # 手动更新
# pipenv run python cron.py 自动定时更新
# pipenv run python python.py 解析卫健委通报，并更新数据
```


## 附录
* [国家地区代码](https://zh.wikipedia.org/wiki/ISO_3166-1)
* [2019年中华人民共和国行政区划代码](http://www.mca.gov.cn/article/sj/xzqh/2019/) (中华人民共和国民政部)
* [WHO SARS 统计数据](https://www.who.int/csr/sars/country/en/)