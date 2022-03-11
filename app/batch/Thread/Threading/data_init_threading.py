# -*- coding: utf-8 -*-
import threading
import schedule

import log

from app.database import init_data

LOG = log.get_logger()


class DataInitThreading(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        s = schedule.every().day.at("01:00").do(job())


def job(self):
    init_data()