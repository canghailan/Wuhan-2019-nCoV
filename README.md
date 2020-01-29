# 武汉 2019-nCoV 统计数据


2020-01-27后数据从腾讯新闻接口采集而来，每小时57分自动更新。

2020-01-27前数据不全，正在补充中（已完成湖北、全国、北京、天津、山西、河北、辽宁、吉林、黑龙江、上海、江苏、浙江、安徽、福建、内蒙古、江西）。

按天，按国家、省、地级市记录。


## 数据地址
* https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.json
* https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.csv



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


* CSV格式完整数据（数据格式较小，建议使用） Wuhan-2019-nCoV.csv
  * CSV转JSON parseCSV.js
* JSON格式完整数据 Wuhan-2019-nCoV.json
* 卫健委通报数据 ReportData
* 中国行政区划代码 ChinaAreaCode.csv
* 国家地区代码（ISO_3166-1） CountryCode.csv


TODO:

* 2020-01-27前按地区统计数据未更新
* GeoJSON
* 图表
* 与SARS对比



## 疫情通报（原始数据）

* [中华人民共和国国家卫生健康委员会](http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml)
  * [湖北省卫生健康委员会](http://wjw.hubei.gov.cn/bmdt/ztzl/fkxxgzbdgrfyyq/xxfb/)
    * [武汉市卫生健康委员会](http://wjw.wuhan.gov.cn/front/web/list3rd/no/802)
  * [北京市卫生健康委员会](http://wjw.beijing.gov.cn/wjwh/ztzl/xxgzbd/)
  * [天津市卫生健康委员会](http://wsjk.tj.gov.cn/col/col87/index.html)
  * [河北省卫生健康委员会](http://wsjkw.hebei.gov.cn/index.do?cid=326&templet=list)
  * [山西省卫生健康委员会](http://wjw.shanxi.gov.cn/xingfew/index.hrh)
  * [内蒙古自治区卫生健康委员会](http://wjw.nmg.gov.cn/ztlm/2016n/xxgzbdgrdfyyqfk/index.shtml)
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
  * ~~[河南省卫生健康委员会](http://wsjkw.henan.gov.cn/channels/854.shtml)~~
  * ~~[湖南省卫生健康委员会](http://wjw.hunan.gov.cn/wjw/xxgk/gzdt/zyxw_1/index.html)~~
  * [广东省卫生健康委员会](http://wsjkw.gd.gov.cn/xxgzbdfk/yqtb/)
  * [广西壮族自治区卫生健康委员会](http://wsjkw.gxzf.gov.cn/zhuantiqu/ncov/)
  * [海南省卫生健康委员会](http://wst.hainan.gov.cn/swjw/rdzt/yqfk/)
  * [重庆市卫生健康委员会](http://wsjkw.cq.gov.cn/yqxxyqtb/)
  * [四川省卫生健康委员会](http://wsjkw.sc.gov.cn/scwsjkw/gggs/tygl.shtml)
  * [贵州省卫生健康委员会](http://www.gzhfpc.gov.cn/ztzl_500663/xxgzbdgrdfyyqfk/yqdt/)
  * [云南省卫生健康委员会](http://ynswsjkw.yn.gov.cn/wjwWebsite/web/col?id=UU157976428326282067&cn=xxgzbd&pcn=ztlm&pid=UU145102906505319731)
  * 西藏自治区卫生健康委员会
  * [陕西省卫生健康委员会](http://sxwjw.shaanxi.gov.cn/col/col863/index.html)
  * [甘肃省卫生健康委员会](http://wsjk.gansu.gov.cn/channel/10910/index.html)
  * [青海省卫生健康委员会](https://wsjkw.qinghai.gov.cn/zhxw/xwzx/index.html)
  * [宁夏回族自治区卫生健康委员会](http://wsjkw.nx.gov.cn/yqfkdt/yqsd1.htm)
  * [新疆维吾尔自治区卫生健康委员会](http://www.xjhfpc.gov.cn/ztzl/fkxxgzbdfygz/yqtb.htm)
  * ~~[新疆生产建设兵团卫生健康委员会](http://wsj.xjbt.gov.cn/xxgk/tzgg/)~~



## 数据来源

* [腾讯新闻](https://news.qq.com//zt2020/page/feiyan.htm)
  * [日统计](https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_cn_day_counts)
  * [实时全国统计](https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_global_vars)
  * [实时省、市统计](https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_area_counts)
* [丁香医生](https://3g.dxy.cn/newh5/view/pneumonia)



## 数据更新
```shell
export PIPENV_VENV_IN_PROJECT=1 && pipenv install
pipenv run python dataset.py # 手动更新
# pipenv run python cron.py 自动定时更新
```


## 附录
* [国家地区代码](https://zh.wikipedia.org/wiki/ISO_3166-1)
* [2019年中华人民共和国行政区划代码](http://www.mca.gov.cn/article/sj/xzqh/2019/) (中华人民共和国民政部)
