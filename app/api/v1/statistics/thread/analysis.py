# -*- coding: utf-8 -*-
import threading
import time

import requests
from dateutil.parser import parse
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, MultipleResultsFound

import log
from app.errors import DatabaseError, ERR_DATABASE_ROLLBACK
from app.model.holo_member_ch import HoloMemberCh
from app.model.user_static_youbute import UserStaticYoutube
from app.utils.itertools import partition

LOG = log.get_logger()


class AnalysisSubscribeThread(threading.Thread):
    def __init__(self, access_token, session, user_id):
        super().__init__()
        self.access_token = access_token
        self.session = session
        self.user_id = user_id

    def run(self):
        start = time.perf_counter()
        LOG.info("AnalysisSubscribe thread start ")
        time.sleep(1)

        LOG.error(self.access_token)
        authToken = 'Bearer ' + self.access_token

        headers = {'Authorization': authToken}

        LOG.info(headers)
        channelList = self.session.query(HoloMemberCh.channel_id).all()

        # https://developers.google.com/youtube/v3/docs/subscriptions/list?hl=ko&apix_params=%7B%22part%22%3A%5B%22id%2C%20snippet%22%5D%2C%22forChannelId%22%3A%22UC7fk0CB07ly8oSl0aqKkqFg%2CUCp6993wxpyDPHUpavwDFqgg%2CUCoSrY_IQQVpmIRZ9Xf-y93g%2CUCyl1z3jo3XHR1riLFKG5UAg%2CUCL_qhgtOy0dy1Agp8vkySQg%2CUCHsx4Hqa-1ORjQTh9TYDhww%2CUC8rcEBzJSleTkf_-agPM20g%2CUCsUj0dszADCGbF3gNrQEuSQ%2CUC3n5uGu18FoCy23ggWWp8tA%2CUCmbs8T6MWqUHP1tIQvSgKrg%2CUCO_aKKYxn4tvrqPjcTzZ6EQ%2CUCgmPnx-EEeOrZSg5Tiw7ZRQ%2CUCp6993wxpyDPHUpavwDFqgg%22%2C%22maxResults%22%3A100%2C%22mine%22%3Atrue%7D&apix=true#try-it

        chunks = list(partition(channelList, 45))

        for item in chunks:
            channelStr = ''
            if channelList:
                for row in item.__iter__():
                    channelStr = channelStr + ',' + ''.join(row)
            else:
                channelStr = 'UCP0BspO_AMEe3aQqqpo89Dg,UC8rcEBzJSleTkf_-agPM20g,UC7fk0CB07ly8oSl0aqKkqFg,UCp6993wxpyDPHUpavwDFqgg'
                LOG.info('channelList is empty')

            # test url ( base subscribe list of mine ) : https://content-youtube.googleapis.com/youtube/v3/subscriptions?maxResults=100&part=snippet&mine=true
            url = "https://www.googleapis.com/youtube/v3/subscriptions" \
                  + "?mine=true" + "&part=id%2C%20snippet" + "&maxResults=50" \
                  + "&forChannelId=" + channelStr

            r = requests.get(url=url, headers=headers)

            self.__update_user_static__(r.json())

        self.__session_close__()
        print("AnalysisSubscribe thread end spend time : ", (time.perf_counter() - start))

    def __update_user_static__(self, json):
        sub_data = json['items']

        if sub_data is not None:
            for i in sub_data:

                id = i['id']
                title = i['snippet']['title']
                channelId = i['snippet']['resourceId']['channelId']
                publishedAt = i['snippet']['publishedAt']
                isAdd = False

                try:
                    user_static_youtube = self.session.query(UserStaticYoutube).filter(
                        UserStaticYoutube.user_id == self.user_id) \
                        .filter(UserStaticYoutube.channel_id == channelId).one()
                except NoResultFound:
                    LOG.info(f'AnalysisSubscribe need to add data - {self.user_id} - {channelId}')
                except MultipleResultsFound:
                    LOG.info(f'AnalysisSubscribe many data - {self.user_id} - {channelId}')
                    return

                if user_static_youtube is None:
                    isAdd = True
                    user_static_youtube = UserStaticYoutube()

                user_static_youtube.user_id = self.user_id
                user_static_youtube.channel_id = channelId
                user_static_youtube.sub_date = parse(publishedAt).date()
                user_static_youtube.channel_name = title

                if title.find("Ch") > -1:
                    user_static_youtube.member_name = title[0: int(title.index("Ch")) - 1]

                if title.find("ch") > -1:
                    user_static_youtube.member_name = title[0: int(title.index("ch")) - 1]

                elif title.find("Channel") > -1:
                    user_static_youtube.member_name = title[0: int(title.index("Channel")) - 1]

                elif title.find("hololive-") > -1:
                    user_static_youtube.member_name = title[0: int(title.index("hololive-")) - 1]

                user_static_youtube.member_name = user_static_youtube.member_name.strip()

                if isAdd:
                    LOG.info('add user_static_youtube {}'.format(user_static_youtube.member_name))
                    self.session.add(user_static_youtube)

    def __session_close__(self):
        session = self.session

        try:
            session.commit()
        except SQLAlchemyError as ex:
            session.rollback()
            raise DatabaseError(ERR_DATABASE_ROLLBACK, ex.args, ex.params)

        session.close()
