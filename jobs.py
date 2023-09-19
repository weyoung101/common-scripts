import time

import schedule

import csdn.main


# 所有的任务放这里
def jobs():
    csdn.main.wxAppSignIn()


# 设置定时器
# 设置为每天的固定时间点运行代码。
schedule.every().day.at('10:11').do(jobs)  # 这里只需要函数名
# 调用定时任务
while True:
    schedule.run_pending()
    time.sleep(5)
