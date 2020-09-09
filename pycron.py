import time
from datetime import datetime
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler


def job_func():
    print('current time: ', time.ctime())

# 实例化一个调度器
scheduler = BlockingScheduler()

# 在2020-08-25 16:00:10时触发一次job_func;
scheduler.add_job(job_func, 'date', run_date='2020-08-25 16:00:10')

# 每隔1分钟执行一次 job_func;
scheduler.add_job(job_func, 'interval', minutes=1)

# 每2小时执行一次
scheduler.add_job(job_func, 'interval', seconds=7200)

# 每天6:00执行一次
scheduler.add_job(job_func, 'cron', hour=6, minute=00)

# 带有起止时间的interval;
scheduler.add_job(job_func, 'interval', minutes=0.1, start_date='2020-08-25 17:02:20', end_date='2020-08-25 18:02:40')

# 截止到2019年12月31日前，每个周一到周四，每分钟的0秒时刻，执行一次job_func;
scheduler.add_job(job_func, 'cron', day_of_week='0-4', hour='8-16', minute='0-59', second='0', end_date='2020-09-04')

# 开始执行调度器
scheduler.start()


"""
APScheduler的触发器分为三种类型：date（日期触发），interval（固定间隔触发），cron（周期触发）。日期触发不用多说，
周期触发相比于固定间隔触发，区别在于：周期触发可以理解成特定时期内的固定间隔触发，换句话说，我们可以为不同时间段设置不同的触发间隔。
date     触发器指在某一指定时间下执行脚本的方法
interval 触发器循环执行脚本任务的触发器
cron     触发器指定时间循环执行脚本的触发器
"""
