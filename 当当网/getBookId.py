"""
Created on Thu Nov 28 09:19:45 2017

@author: Oythonhill

@email: hyhyin@163.com
"""

import requests
import re
from urllib import parse

bookid = open("C:\\Users\\YHY\\Desktop\\bookid.txt", "w", encoding="utf-8")

def getBooksListNum(KeyWords):
    bookid = []
    SearchUrl = []
    header1 = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    for i in KeyWords:
        keywords = parse.quote(i) # 将输入的关键词转化为urlcode
        searchUrl = r"http://search.dangdang.com/?key="+keywords+"&act=input" # 根据keywords的urlcode构造url地址
        SearchUrl.append(searchUrl)
        # 总共获取每个关键词的前24页的url地址
        for j in range(2,25):
            bookUrlpages = r"http://search.dangdang.com/?key="+str(keywords)+"&act=input"+"&page_index="+str(j)
            SearchUrl.append(bookUrlpages)
    # 从每个url地址里获取里面书本的id
    for k in SearchUrl:
        response = requests.get(k, headers = header1)
        repattern = re.compile("\[\\d{8}\]")
        bookIdList = re.findall(repattern, response.text)
        for i in bookIdList:
            bookid.append(i[1:9])
    return bookid

chineseKeyWords = ["大数据","机器学习","人工智能","数据挖掘","统计学习","数据科学"]
data = getBooksListNum(chineseKeyWords)
try:
    for i in data:
        bookid.write(i+"\n")
finally:
    bookid.close()
