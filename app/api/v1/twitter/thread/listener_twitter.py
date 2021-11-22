# -*- coding: utf-8 -*-
import threading
import time

import requests
from dateutil.parser import parse
from sqlalchemy.exc import SQLAlchemyError

import log
from app.errors import DatabaseError, ERR_DATABASE_ROLLBACK
from app.model.holo_member_twitter_info import HoloMemberTwitterInfo
from app.model.user_static_youbute import UserStaticYoutube

LOG = log.get_logger()


class TwitterListenerThread(threading.Thread):
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
        # TODO header setting used by user.access_token
        authToken = 'Bearer ' + self.access_token

        headers = {'Authorization': authToken}

        LOG.info(headers)
        # TODO select member ch name str list
        channelList = self.session.query(HoloMemberTwitterInfo.twitter_id).all()

        channelStr = ''
        if channelList:
            for row in channelList.__iter__():
                channelStr = channelStr + ',' + ''.join(row)
        else:
            channelStr = 'UCP0BspO_AMEe3aQqqpo89Dg,UC8rcEBzJSleTkf_-agPM20g,UC7fk0CB07ly8oSl0aqKkqFg,UCp6993wxpyDPHUpavwDFqgg'
            LOG.info('channelList is empty')

        url = "https://www.googleapis.com/youtube/v3/subscriptions" \
              + "?mine=true" + "&part=id%2C%20snippet" + "&maxResults=100" \
              + "&forChannelId=" + "UCP0BspO_AMEe3aQqqpo89Dg" + channelStr
        # + "&forChannelId=" + "UC7fk0CB07ly8oSl0aqKkqFg%2CUCp6993wxpyDPHUpavwDFqgg"+','+channelStr

        # test url ( base subscribe list of mine ) : https://content-youtube.googleapis.com/youtube/v3/subscriptions?maxResults=100&part=snippet&mine=true

        # TODO get send
        r = requests.get(url=url, headers=headers)
        # TODO update user_static_youtube
        # LOG.info(r.json())

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

                user_static_youtube = UserStaticYoutube()
                user_static_youtube.user_id = self.user_id
                user_static_youtube.channel_id = channelId
                user_static_youtube.sub_date = parse(publishedAt).date()
                user_static_youtube.channel_name = title

                if title.find("Ch") > -1:
                    user_static_youtube.member_name = title[0: int(title.index("Ch")) - 1]

                elif title.find("Channel") > -1:
                    user_static_youtube.member_name = title[0: int(title.index("Channel")) - 1]

                elif title.find("hololive-") > -1:
                    user_static_youtube.member_name = title[0: int(title.index("hololive-")) - 1]

                user_static_youtube.member_name = user_static_youtube.member_name.strip()

                user_static_youtube_db = None

                try:
                    user_static_youtube_db = self.session.query(UserStaticYoutube).filter(
                        UserStaticYoutube.user_id == user_static_youtube.user_id) \
                        .filter(UserStaticYoutube.channel_id == user_static_youtube.channel_id).one()
                except:
                    LOG.info('not find data')

                if user_static_youtube_db is None:
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
