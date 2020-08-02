import time
import datetime
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from .sf_aggregate_usage import aggregate_current_month_usage


def start():
    #scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)
    scheduler = BackgroundScheduler()
    #scheduler.add_jobstore(DjangoJobStore(), "default")
    

    #scheduler.add_job(test, 'interval', seconds=10) #, id='job_id', replace_existing=True)
    scheduler.add_job(aggregate_current_month_usage, 'interval', seconds=60) 
    #register_events(scheduler)
    
    scheduler.start()
    print("Scheduler started...")
    #scheduler.remove_job('job_id')

def test():
    #time.sleep(4)
    print('I am testing job at {}'.format(datetime.datetime.now()))

