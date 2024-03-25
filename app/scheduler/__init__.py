from apscheduler.schedulers.background import BackgroundScheduler

from app.lib.function import get_now_time

scheduler = BackgroundScheduler(timezone='Asia/Seoul')

@scheduler.scheduled_job('cron', second='*/5', id='test')
def scheduler_test():
    str = f"[{get_now_time()}] scheduler test"
    print(str)
