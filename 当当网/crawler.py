"""
Created on Thu Nov 28 09:19:45 2017

@author: Oythonhill

@email: hyhyin@163.com
"""

from bs4 import BeautifulSoup
from urllib import request
import requests
import re
from urllib import parse
import urllib


def getBookDeatils(url):
    try:
        headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3'}
        u1 = request.Request(url, headers=headers)

        # 使用urlopen函数获取网页的response
        response = request.urlopen(u1)

        # 将response转换成beautifulsoup对象
        bsobj = BeautifulSoup(response, "html.parser")

        # 从bsobj中找到书本信息所在的标签，并获取标签内容
        salesboxObj = bsobj.find("div", {"class": "sale_box clearfix"})
        details1 = salesboxObj.find("h1").get_text().strip("\n").strip()

        wrapperObj = bsobj.find("div", {"class": "product_wrapper"})
        details2 = wrapperObj.find("div", {"class": "pro_content"}).get_text().strip("\n").strip()

        # 在获取的标签内容中寻找日期数据
        repattern = re.compile("\\d+年\d+月\d+日")

        # 匹配日期数据，并对可能找不到日期数据进行处理
        try:
            details2 = re.findall(repattern, details2)[0]
        except IndexError:
            details2 = " "
        text = details1 + "|" + details2

    # 如果出现AttributeError将该次text赋值为空格
    except AttributeError:
        text = " "
    return text

def getComments(url):

    #构造requests需要用到的header
    header1 = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "product.dangdang.com",
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

    #使用requests.get获取url返回
    response = requests.get(url, headers=header1)

    #使用正则匹配日期数据
    repattern = re.compile("\\d{4}-\\d{2}-\\d{2}.{9}")
    comments = re.findall(repattern, response.text)

    #返回结果，comments是一个列表
    return comments

idfile = open("C:\\Users\\YHY\\Desktop\\bookid.txt","r",encoding="utf-8")
datafile = open("C:\\Users\\YHY\\Desktop\\bookdata_30-100.txt","a",encoding="utf-8")


# 下面是从文件中读取书本id，并构造获取details的url和comments的url
# 通过上面定义的两个函数，获取数据后写入Txt文件，最后关闭文件
count = 0
try:
    while count < 70:
        bookid = idfile.readline()
        count +=1
        if bookid:
            bookid = bookid.strip("\n")
            bookurl = "http://product.dangdang.com/" + str(bookid) + "." + "html"
            bookdetails = getBookDeatils(bookurl)
            print(bookdetails)
            if bookdetails == " ":
                continue
            datafile.write(bookdetails+"|")
            for j in range(1,200):
                commentsurl = "http://product.dangdang.com/index.php?r=comment%2Flist&productId="+str(bookid)+"&categoryPath=01.54.05.08.00.00&mainProductId="+str(bookid)+"&mediumId=0&pageIndex="+str(j)+"&sortType=1&filterType=1&isSystem=1&tagId=0&tagFilterCount=0"
                comments = getComments(commentsurl)
                for k in comments:
                    datafile.write(k+",")
            datafile.write("\n")
        else:
            break
finally:
    idfile.close()
    datafile.close()

# End
