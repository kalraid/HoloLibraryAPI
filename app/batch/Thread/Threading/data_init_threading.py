# -*- coding: utf-8 -*-
import threading

from apscheduler.schedulers.background import BackgroundScheduler

import log
from app.database import init_data

LOG = log.get_logger()
sched = BackgroundScheduler()


class DataInitThreading(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        sched.add_job(job, 'cron', second='0', id="test_3")
        print('sched before~')
        sched.start()
        print('sched after~')


@sched.scheduled_job('cron', hour='12', minute='30', id='test_2')
def job():
    init_data()
