#coding:utf-8

"""
Created on 2016-08-16
@author: jeff
"""

import urllib2
import urllib
import gzip
import re
import time
import smtplib

from email.mime.text import MIMEText
from StringIO import StringIO
from datetime import datetime

import pdb


g_test = 1

g_url = "http://caipiao.163.com/award/qxc/"
g_save_file = "last.txt"
g_refresh_weekday = (1, 4, 6)

PATTERN_TIME = re.compile('\<span id="time"\>([\S\s]+?)\<\/span\>')
PATTERN_NUMBER = re.compile('\<span class="red_ball"\>(\d)\<\/span\>')

def DownloadParseResult(url):
    req = urllib2.urlopen(url)
    info = req.info()
    encoding = info.getheader('Content-Encoding')
    content = req.read()
    if encoding == 'gzip':
        buf = StringIO(content)
        gf = gzip.GzipFile(fileobj=buf)
        content = gf.read()


    #pdb.set_trace()
    time_index = content.find("开奖时间：")
    slice_len = 100
    time_content = content[time_index : time_index+slice_len]
    time_iters = PATTERN_TIME.finditer(time_content)
    time_str = None
    for _m in time_iters:
        time_str = _m.group(1)
        print time_str
        break

    if not time_str:
        print 'ERROR! TIME NOT FOUND!'
        return

    r_last_time_file = open(g_save_file, mode='r')
    last_time = r_last_time_file.readline()
    r_last_time_file.close()
    if last_time == time_str:
        print 'not refreshed yet'
        return


    number_index = content.find("开奖号码：")
    num_slice_len = 700
    number_content = content[number_index : number_index+num_slice_len]
    number_iters = PATTERN_NUMBER.finditer(number_content)
    count = 7
    result_nums = []
    for _m in number_iters:

        _num = _m.group(1)
        result_nums.append(_num)
        #print _num

        count -= 1
        if count == 0:
            break


    number_str = ','.join(result_nums)
    print "NEW NUMBER : %s" % (number_str)

    breaking_news = "%s\n%s" % (time_str, number_str)
    return breaking_news, time_str



def SendMail(sub, content):
    #sub：主题；content：邮件内容;

    mail_host="smtp.163.com"    #设置服务器
    mail_user="linjiafang33@163.com"    #用户名
    mail_pass= "fang4949449"        #密码
    to_list = ['linjeffrey@qq.com', '13670972282@139.com']#'13580516323@139.com']
    me = mail_user

    #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content, _charset='utf-8')    #创建一个邮件消息实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        print 'connecting'
        s = smtplib.SMTP(mail_host, 25)              #实例化python邮件的smtp类

        if g_test:
            s.set_debuglevel(1)

        print 'connected'
        #s.connect(mail_host)  #连接smtp服务器
        s.login(mail_user,mail_pass)     #登陆服务器
        print 'login'
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        print 'sendmail'
        s.close()
        print 'close'
        return True
    except Exception, e:
        print str(e)
        return False


def IsTime2Update():
    now = datetime.now()
    day_of_week = now.weekday()
    update_hour = 20

    if g_test:
        return True

    if day_of_week in g_refresh_weekday and now.timetuple().tm_hour == update_hour:
        return True

    return False


def SaveTimeStr(time_str):
    w_last_time_file = open(g_save_file, mode='w')
    w_last_time_file.write(time_str)
    w_last_time_file.close()


def DoTask():
    result = DownloadParseResult(g_url)
    if not result:
        return

    news, time_str = result

    print 'BREAKING NEWS: %s' % news

    sub = "七星彩开奖结果"
    if SendMail(sub, news):
        SaveTimeStr(time_str)




def Loop():
    loop_interval = 60
    if g_test:
        loop_interval = 6

    while True:
        if not IsTime2Update():
            print 'not in the update time interval'
            time.sleep(loop_interval)
            continue

        DoTask()
        time.sleep(loop_interval)




if __name__ == '__main__':
    Loop()
    