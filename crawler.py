# -*- coding: utf-8 -*-
"""
Created on Thur Dec 7 2017

@author: Oythonhill

@email: hyhyin@163.com

"""


import requests
from urllib import request
from bs4 import BeautifulSoup
import re

urltxtpath = r"C:\Users\YHY\Desktop\Housing\HouseUrl\houseurl_17-1.txt"
datatxtpath = r"C:\Users\YHY\Desktop\Housing\test_data\housedata_test.txt"
# urltxtpath = r"/data1/chengfan16/neteaseurl_16-17.txt"
# datatxtpath = r"/data1/chengfan16/neteasedata_16-17.txt"

def removeExtraStr(str):
    str = str.strip()
    str = re.sub("\n", "", str)
    str = re.sub("\t", "", str)
    str = re.sub(" ", "", str)
    return str

def getDetails(url):
    details = requests.get(url)
    details.encoding = "utf-8"
    bsobj = BeautifulSoup(details.text, "html.parser")

    # 均价
    price_tag = bsobj.find("li", {"class": "item item_left"})
    price_content = price_tag.find("div", {"class": "tp_item clearfix"}).get_text()
    price_content = removeExtraStr(price_content)
    index = price_content.find("㎡")
    price = price_content[:(index+1)]

    # 区域
    loc_tag = bsobj.find("table", {"class": "qy_main"})
    location = loc_tag.get_text()
    location = removeExtraStr(location)

    # 公交
    bus_raw = bsobj.find("li", {"class": "cont4_item cont4_gj clearfix"}).get_text()
    bus = removeExtraStr(bus_raw)

    # 地铁
    metro_raw = bsobj.find("li", {"class": "cont4_item cont4_dt clearfix"}).get_text()
    metro = removeExtraStr(metro_raw)

    # 医院,超市，学校
    others_tag = bsobj.find("li", {"class": "item item_bottom item_left"})
    alltd = others_tag.find_all("li",{"class":"td1"})
    hospital_text = ""
    shop_text = ""
    school_text = ""
    for i in alltd:
        text = i.get_text()
        hospital_pat = re.compile("医院")
        shop_pat = re.compile("超市")
        school_pat = re.compile("学校")
        if re.search(hospital_pat,text):
            hospital_text = text
            hospital_text = removeExtraStr(hospital_text)
        elif re.search(shop_pat,text):
            shop_text = text
            shop_text = removeExtraStr(shop_text)
        elif re.search(school_pat,text):
            school_text = text
            school_text = removeExtraStr(school_text)
        else:
            pass
        if hospital_pat and shop_text and school_text:
            break
    # 获得的文本放一起
    details = (price + "|" + location + "|" + bus + "|" + metro +
               "|" + hospital_text + "|" + shop_text + "|" + school_text)
    return(details)

def getData(url):

    head = {'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3'}
    response = requests.get(url,headers = head)
    response.encoding = "utf-8"
    bsobj = BeautifulSoup(response.text, "html.parser")

    # 筛选出目标信息所在的标签
    all_tr = bsobj.find_all("tr", {"class": re.compile("mBg[12]")})

    # 循环，爬取信息，写入txt文件
    housedata = []
    count = 0
    for i in all_tr:
        record = ""
        all_td = i.find_all("td", {"class": re.compile("w.")}) # 在i里再找到所有的"td"标签,class属性为"w."
        for j in all_td:
            striped_text = j.get_text().strip().strip("\n")
            record = record + "|" + striped_text
            if striped_text.find("%") != -1:
                url = i.find("td", {"class": "wd2 bOS"}).find("a").attrs["href"]
                try:
                    details = getDetails(url)
                    record = record + "|" + details
                    housedata.append(record)
                    count += 1
                except AttributeError:
                    record = record + "|" +"下载失败"
            else:
                pass
    return housedata

try:
    neteasedata = open(datatxtpath, "a", encoding = "utf-8")
    neteaseurl = open(urltxtpath, "r", encoding = "utf-8")
    while 1:
        url = neteaseurl.readline().strip("\n")
        if url:
            housedata = getData(url)
            for i in housedata:
                neteasedata.write(i+"\n")
        else:
            break
finally:
    neteasedata.close()
# housedata = getData("http://data.house.163.com/bj/housing/xx1/ALL/all/2015.01.01-2015.01.01/allDistrict/todayflat/desc/all/1.html?loopline=0#stophere")
# for i in housedata:
#     print(i)

