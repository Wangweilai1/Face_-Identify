# -*- coding: cp936 -*-
import threading
import GetUrl
import urllib.request

g_mutex = threading.Lock()
g_pages = []      #线程下载页面后，将页面内容添加到这个list中
g_dledUrl = []    #所有下载过的url
g_toDlUrl = []    #当前要下载的url
g_failedUrl = []  #下载失败的url
g_totalcount = 0  #下载过的页面数

class WebCrawler:
    def __init__(self,threadNumber, Maxdepth):
        self.threadNumber = threadNumber
        self.threadPool = []
        self.Maxdepth = Maxdepth
        self.logfile = open('#log.txt','w')

    def download(self, url, fileName):
        Cth = CrawlerThread(url, fileName)
        self.threadPool.append(Cth)
        Cth.start()
        
    def downloadAll(self):
        global g_toDlUrl
        global g_totalcount
        i = 0
        TotalUrlCount = len(g_toDlUrl)
        print("The total URL count is：%d\n" %TotalUrlCount)
        while i < TotalUrlCount:
            j = 0
            while j < self.threadNumber and i + j < TotalUrlCount:
                g_totalcount += 1    #进入循环则下载页面数加1
                self.download(g_toDlUrl[i+j],str(g_totalcount)+'.htm')
                print ('Thread started:',i+j,'--File number = ',g_totalcount)
                j += 1
            i += j
            for th in self.threadPool:
                th.join(30)     #等待线程结束，30秒超时
            self.threadPool = []    #清空线程池
        g_toDlUrl = []    #清空列表

    def updateToDl(self):
        global g_toDlUrl
        global g_dledUrl
        newUrlList = []
        for s in g_pages:
            newUrlList += GetUrl.GetUrl(s)   #######GetUrl要具体实现
        g_toDlUrl = list(set(newUrlList) - set(g_dledUrl))    #提示unhashable
                
    def Craw(self,entryUrl):    #这是一个深度搜索，到g_toDlUrl为空时结束
        g_toDlUrl.append(entryUrl)
        self.logfile.write('>>>Entry:\n')                                      ##
        self.logfile.write(entryUrl)                                           ##
        depth = 0
        TotalUrlCount = len(g_toDlUrl)
        while TotalUrlCount != 0 and depth < self.Maxdepth:
            depth += 1
            print ('Searching depth ',depth,'...\n\n')
            self.downloadAll()
            self.updateToDl()
            content = '\n>>>Depth ' + str(depth)+':\n'                         ##
            self.logfile.write(content)                                        ##
            i = 0                                                              ##
            TotalUrlCount = len(g_toDlUrl)
            while i < TotalUrlCount:                                           ##
                content = str(g_totalcount + i + 1) + '->' + g_toDlUrl[i] + '\n'    ##
                self.logfile.write(content)                                    ##
                i += 1
        self.logfile.close()                                                   ## 改动了
         
class CrawlerThread(threading.Thread):
    def __init__(self, url, fileName):
        threading.Thread.__init__(self)
        self.url = url    #本线程下载的url
        self.fileName = fileName

    def run(self):    #线程工作-->下载html页面
        global g_mutex
        global g_failedUrl
        global g_dledUrl
        try:
            f = urllib.request.urlopen(self.url)
            s = f.read()
            fout = open(self.fileName, 'w')
            fout.write(str(s))
            fout.close()
        except:
            g_mutex.acquire()    #线程锁-->锁上
            g_dledUrl.append(self.url)
            g_failedUrl.append(self.url)
            g_mutex.release()    #线程锁-->释放
            print ('Failed downloading and saving',self.url)
            return None    #记着返回!
        
        g_mutex.acquire()    #线程锁-->锁上
        g_pages.append(s)
        g_dledUrl.append(self.url)
        g_mutex.release()    #线程锁-->释放
