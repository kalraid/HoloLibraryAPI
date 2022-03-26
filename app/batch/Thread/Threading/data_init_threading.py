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
        sched.add_job(job, 'cron', hour='4,12', minute='30', id='test_2')
        print('sched before~')
        sched.start()
        print('sched after~')


def job():
    init_data()
