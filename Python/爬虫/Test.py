# -*- coding: cp936 -*-
import WebCrawler
import time

url = input('�������url(��-->www.baidu.com): \n')
thNumber = int(input('�����߳���:'))    #֮ǰ����δת����bug
Maxdepth = int(input('���������ȣ�'))

start = time.clock()
url = 'http://' + url
wc = WebCrawler.WebCrawler(thNumber, Maxdepth)
wc.Craw(url)
end = time.clock()

print("The function run time is: %0.02f senconds.\n" %(end - start))
