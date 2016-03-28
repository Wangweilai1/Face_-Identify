# -*- coding: cp936 -*-
import WebCrawler
import time

url = input('设置入口url(例-->www.baidu.com): \n')
thNumber = int(input('设置线程数:'))    #之前类型未转换出bug
Maxdepth = int(input('最大搜索深度：'))

start = time.clock()
url = 'http://' + url
wc = WebCrawler.WebCrawler(thNumber, Maxdepth)
wc.Craw(url)
end = time.clock()

print("The function run time is: %0.02f senconds.\n" %(end - start))
