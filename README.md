# 爬虫脚本集合

日常作业和研究中需要爬取一些网页的数据，这里将一些爬取一组网页的python脚本收集到一起。

### 1 [当当网](http://search.dangdang.com/?key=%B4%F3%CA%FD%BE%DD&act=input)
>以"数据挖掘"、"大数据"、"机器学习"等关键词搜索，爬取了搜索结果中书本的信息和[评论页评论](http://product.dangdang.com/25101651.html)的日期。

### 2 [网易房产](http://data.house.163.com/bj/housing/xx1/ALL/all/1/allDistrict/todayflat/desc/ALL/1.html)
* 爬取了网易房产网页北京地区的数据；

* 时间跨度从2014.01.01到2017.11.30；

* 每天的数据包含约1500个楼盘的观测，维度包含[楼盘列表页](http://data.house.163.com/bj/housing/xx1/ALL/all/1/allDistrict/todayflat/desc/ALL/1.html)和[楼盘名链接页](http://xf.house.163.com/bj/BYOW.html)给出的基本信息如销售金额、均价、地理位置等；
