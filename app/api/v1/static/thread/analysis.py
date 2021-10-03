# -*- coding: utf-8 -*-
import threading
import time
import requests
from six import Iterator

import log

from app.model.user_static_youbute import UserStaticYoutube

LOG = log.get_logger()


class AnalysisSubscribeThread(threading.Thread):
    def __init__(self, user, session):
        super().__init__()
        self.user = user
        self.session = session

    def run(self):
        start = time.perf_counter()
        LOG.info("AnalysisSubscribe thread start ")
        LOG.info(self.session)

        time.sleep(1)

        # TODO header setting used by user.access_token
        authToken = 'Bearer '+self.user.access_token

        headers = { 'Authorization' : authToken}

        LOG.info(headers)
        # TODO select member ch name str list
        channelList = self.session.query(UserStaticYoutube.channel_id).all()


        # https://developers.google.com/youtube/v3/docs/subscriptions/list?hl=ko&apix_params=%7B%22part%22%3A%5B%22id%2C%20snippet%22%5D%2C%22forChannelId%22%3A%22UC7fk0CB07ly8oSl0aqKkqFg%2CUCp6993wxpyDPHUpavwDFqgg%2CUCoSrY_IQQVpmIRZ9Xf-y93g%2CUCyl1z3jo3XHR1riLFKG5UAg%2CUCL_qhgtOy0dy1Agp8vkySQg%2CUCHsx4Hqa-1ORjQTh9TYDhww%2CUC8rcEBzJSleTkf_-agPM20g%2CUCsUj0dszADCGbF3gNrQEuSQ%2CUC3n5uGu18FoCy23ggWWp8tA%2CUCmbs8T6MWqUHP1tIQvSgKrg%2CUCO_aKKYxn4tvrqPjcTzZ6EQ%2CUCgmPnx-EEeOrZSg5Tiw7ZRQ%2CUCp6993wxpyDPHUpavwDFqgg%22%2C%22maxResults%22%3A100%2C%22mine%22%3Atrue%7D&apix=true#try-it


        channelStr = ','.join(Iterator(channelList))

        url = "https://www.googleapis.com/youtube/v3/subscriptions" \
              + "?mine=true" + "&part=id%2C%20snippet" \
              + "&forChannelId=" + "UC7fk0CB07ly8oSl0aqKkqFg%2CUCp6993wxpyDPHUpavwDFqgg"+','+channelStr
              # + "&forChannelId=" + "UC7fk0CB07ly8oSl0aqKkqFg%2CUCp6993wxpyDPHUpavwDFqgg"+','+channelStr

        # TODO post send
        r = requests.get(url=url, headers=headers)
        # TODO update user_static_youtube
        LOG.info(r.json())
        print("AnalysisSubscribe thread end spend time : ", (time.perf_counter() - start))
