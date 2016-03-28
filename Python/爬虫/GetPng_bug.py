#coding=utf-8
import urllib.request
import re

def cbk(a, b, c):  
    '''回调函数 
    @a: 已经下载的数据块 
    @b: 数据块的大小 
    @c: 远程文件的大小 
    '''  
    per = 100.0 * a * b / c  
    if per > 100:  
        per = 100  
    print ('%.2f%%' % pe)
    
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html

def getImg(html):
    imgre = re.compile(r'src="(.+?\.jpg)" pic_ext')
    imglist = imgre.findall(str(html))
    x = 0
    for imgurl in imglist:
        print("wangweilai1:%s\n")
        urllib.request.urlcleanup()
        filename = urllib.request.urlretrieve(imgurl)#, str(x) + '.jpg')
        print(filename)
        print("wangweilai2\n")
        x+=1


html = getHtml("http://tieba.baidu.com/p/2460150866")
getImg(html)
#print (str(getImg(html)))
