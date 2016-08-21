#coding:utf-8

import smtplib,sys
from email.mime.text import MIMEText

mail_host="smtp.qq.com"  	#设置服务器
mail_user="linjeffrey@qq.com"    #用户名
mail_pass= "jeff@duoyi314159"   		#密码

def send_mail(to_list,sub,content):
    #to_list：收件人；sub：主题；content：邮件内容;
    me="笑话来了"+"<"+mail_user+">"
    #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content,_subtype='html',_charset='utf-8')    #创建一个邮件消息实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP() 			 #实例化python邮件的smtp类
        s.connect(mail_host)  #连接smtp服务器
        s.login(mail_user,mail_pass)  	 #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

if __name__ == '__main__':
    to_list = ['linjeffrey@qq.com',]
    sub = 'helo'
    content = 'world'
    send_mail(to_list, sub, content)