#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time

def alarm_email(flag):
    from_addr = '发件邮箱@163.com'
    password = '邮箱系统开启IMAP/SMTP服务后提供的密码'
    to_addr = '收件邮箱@qq.com'
    smtp_server = 'smtp.163.com'
    if flag==1:
        msg = MIMEText('暑期返校开始', 'plain', 'utf-8')
        msg['Subject'] = Header('apple活动已经上线')
    else:
        msg = MIMEText('暑期返校尚未开始', 'plain', 'utf-8')
        msg['Subject'] = Header('apple活动尚未上线')
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    server = smtplib.SMTP_SSL()
    server.connect(smtp_server, 465)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
    print('已发送邮件')

def check():
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    url = 'https://www.apple.com.cn/cn-k12/shop'
    try:
        res = requests.get(url=url, timeout=10)
        if res.status_code != 200:
            return 0
        text = res.text
#        text += "Beats耳机"
        if text.find("耳机") != -1 or text.find("Beats") != -1 or text.find("AirPods") != -1:
            print("活动开始啦!")
            alarm_email(1)
        else:
            print("text length=", len(text))
            localtime = time.localtime(time.time())
            if localtime.tm_hour==0:
                alarm_email(0)
        return 1
    except Exception as e:
        print("error!", e)
        return 0


while 1:
    response = check()
    if response == 1:
        print("checked!")
        break
    time.sleep(10)
