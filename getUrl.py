# -*- coding: utf-8 -*-
"""
Created on Thur Dec 7 2017

@author: Oythonhill

@email: hyhyin@163.com

"""

from datetime import datetime
import pandas as pd

beginDate = 20170101
endDate = 20170630
startpage = 1
endpage = 75   #每天最大为75页
txtpath = r"C:\Users\YHY\Desktop\Housing\HouseUrl\houseurl_17-1.txt"

def createDatelist(beginDate, endDate):
    # beginDate, endDate是形如‘20160601’的字符串或datetime格式
    beginDate = str(beginDate)
    endDate = str(endDate)
    datelist = [datetime.strftime(x,'%Y.%m.%d') for x in list(pd.date_range(start=beginDate, end=endDate))]
    return datelist

# print(createDatelist(20150101,20150130))
def createUrl(datelist,txtpath,startpage,endpage):
    neteaseurl = open(txtpath, "a", encoding="utf-8")
    for i in datelist:
        for j in range(startpage, endpage + 1, 1):
            url = "http://data.house.163.com/bj/housing/xx1/ALL/all/" + \
                      str(i) + "-" + str(i) + "/allDistrict/todayflat/desc/all/" + str(j) + ".html?loopline=0#stophere"
            neteaseurl.write(url+"\n")
    neteaseurl.close()

datelist = createDatelist(beginDate,endDate)
createUrl(datelist,txtpath,startpage,endpage)
print("url创建完毕")
