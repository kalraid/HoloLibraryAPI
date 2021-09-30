# -*- coding: utf-8 -*-
import threading
import time

import log

LOG = log.get_logger()


class AnalysisSubscribeThread(threading.Thread):
    def __init__(self, user, session):
        super().__init__()
        self.user = user
        self.session = session

    def run(self):
        start = time.perf_counter()
        print("AnalysisSubscribe thread start ")

        time.sleep(1)

        # TODO header setting used by user.access_token

        # TODO select member ch name str list

        # TODO post send

        # TODO update user_static_youtube

        print("AnalysisSubscribe thread end spend time : ", (time.perf_counter() - start))
