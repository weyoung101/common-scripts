import time

import schedule

from csdn.main import csdnWxAppSignIn
from hdlMiniapp.hdlSignin import signInHDL


# 所有的任务放这里
def jobs():
    csdnWxAppSignIn()
    signInHDL()


def testJobs():
    print("testJobs")


if __name__ == '__main__':
    print("任务启动成功------")
    jobs()
    # # 设置为每天的固定时间点运行代码。这里只需要函数名
    # schedule.every().day.at('15:08').do(jobs)
    # # 调用定时任务
    # while True:
    #     schedule.run_pending()
    #     time.sleep(10)
