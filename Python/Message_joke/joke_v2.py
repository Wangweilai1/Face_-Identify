# -*- coding: utf-8 -*-
'''
Created on 2016年2月18日
@author: 王维来
'''
import urllib2, json,sys,smtplib
from email.mime.text import MIMEText

reload(sys)
sys.setdefaultencoding('utf-8')#避免中文编码问题

mail_host="smtp.qq.com"     #设置服务器
mail_user="************"    #用户名
mail_pass="*********"       #口令 
mailto_list=['*******']     #邮件接受者

def send_mail(to_list,part1,sub,content):                
    #to_list：收件人；sub：主题；content：邮件内容;
    me=part1+"<"+mail_user+">"  #hello
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')#创建一个实例，这里设置为纯文字格式邮件编码utf8
    msg['Subject'] = sub    #设置主题
    msg['From'] = me        #设置发件人
    msg['To'] = ";".join(to_list)  
    try:  
        s = smtplib.SMTP()             #实例化       
        s.connect(mail_host)           #连接smtp服务器
        s.login(mail_user,mail_pass)   #登陆服务器
        s.sendmail(me, to_list, msg.as_string()) #发送邮件
        s.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False
if __name__ == '__main__': 
    appkey = "e2376cfbe3b27dff923ed61698839a67"
    url = 'http://apis.baidu.com/showapi_open_bus/showapi_joke/joke_text?page=1'
    req = urllib2.Request(url)
    req.add_header("apikey", appkey)
    resp = urllib2.urlopen(req)
    content = resp.read()
    if(content):
        json_result = json.loads(content)
        content_list = json_result['showapi_res_body']['contentlist']
        minlen = 10000
        for item in content_list:
            if len(item['text'])<minlen:
                first_title = item['title']
                first_text = item['text']
                minlen = len(item['text'])
        print 'title：'+first_title
        print 'content：'+first_text
        length = len(first_text)
        part1 = first_text[0:10]
        part2 = first_text[10:22]
        part3 = first_text[22:length]
        print part1,"+",part2,"+",part3
        if send_mail(mailto_list,part1,part2,part3):  
            print "send msg succeed"
        else:  
            print "send msg failed"  
    else:
        print "get joke error"


Vi /etc/crontab   #Linux
