import subprocess
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from dingtalkchatbot.chatbot import DingtalkChatbot

"""
    定时检测局域网内的公网IP，每次记录public_ip.txt文件中比对，如果公网IP有变动则发送告警信息至钉钉群组
    使用了aspchduler定时任务模块和dingtalkchatbot钉钉消息模块
    pip3 install dingtalkchatbot
    pip3 install apscheduler
    我的脚本使用systemd管理启停，脚本路径放在/etc/public_ip/ip.py
    注意：curl ip.cip.cc 获取Ip，有可能访问超时，则会误报推送信息。可以替换访问速度快的网站： ip.42.pl/raw
    我使用了一个while循环，如果获取不到ip，则一直循环
"""

# 实例化一个调度器
scheduler = BlockingScheduler()

def job_ip(): 
    subp = subprocess.Popen('curl ip.42.pl/raw',shell=True,stdout=subprocess.PIPE)
    while len(subp) == 0:
        subp = subprocess.Popen('curl ip.42.pl/raw',shell=True,stdout=subprocess.PIPE)
        
    subp2 = subprocess.Popen('cat /etc/public_ip/public_ip.txt',shell=True,stdout=subprocess.PIPE)
    new_ip=subp.stdout.readline().decode().strip()
    old_ip=subp2.stdout.readline().decode().strip()
    
    if new_ip == old_ip :
        f = open("/etc/public_ip/public_ip.txt","w")
        print(old_ip,file=f)
    else:
        webhook = 'https://oapi.dingtalk.com/robot/send?access_token=d8e39e1882ce3cc441f6a74c761e488ab3e0d0ba883444dd8aef6079a37ca29a'
        secret = 'SEC5c6455acea1d51a5187d682cfd93bbc6d7d32d704ae717b31ea2c4b72e51db8f'
        xiaoding = DingtalkChatbot(webhook, secret=secret)
        at_mobiles = [18566744982]
        xiaoding.send_text(msg= '公网IP已经变动，请添加白名单，公网IP：%s '%(new_ip), at_mobiles=at_mobiles)  
        f = open("/etc/public_ip/public_ip.txt","w")
        print(new_ip,file=f)

# 每分钟执行一次
scheduler.add_job(job_ip, 'interval', minutes=1)

# 开始执行调度器
scheduler.start()
