import log

LOG = log.get_logger()

def get_youtube_data(db_session):
    pass
    # channelStr = ''
    # if channelList:
    #     for row in channelList.__iter__():
    #         channelStr = channelStr + ',' + ''.join(row)
    # else:
    #     channelStr = 'UCP0BspO_AMEe3aQqqpo89Dg,UC8rcEBzJSleTkf_-agPM20g,UC7fk0CB07ly8oSl0aqKkqFg,UCp6993wxpyDPHUpavwDFqgg'
    #     LOG.info('channelList is empty')
    #
    # url = "https://www.googleapis.com/youtube/v3/subscriptions" \
    #       + "?mine=true" + "&part=id%2C%20snippet" + "&maxResults=100" \
    #       + "&forChannelId=" + "UCP0BspO_AMEe3aQqqpo89Dg" + channelStr
    # # + "&forChannelId=" + "UC7fk0CB07ly8oSl0aqKkqFg%2CUCp6993wxpyDPHUpavwDFqgg"+','+channelStr
    #
    # # test url ( base subscribe list of mine ) : https://content-youtube.googleapis.com/youtube/v3/subscriptions?maxResults=100&part=snippet&mine=true
    #
    # # TODO get send
    # r = requests.get(url=url, headers=headers)
    # # TODO update user_static_youtube
    # # LOG.info(r.json())
    #
    # self.__update_user_static__(r.json())
    # self.__session_close__()
    #
    # print("AnalysisSubscribe thread end spend time : ", (time.perf_counter() - start))
    #
    # def __update_user_static__(self, json):
    #     sub_data = json['items']
    #
    #     if sub_data is not None:
    #         for i in sub_data:
    #
    #             id = i['id']
    #             title = i['snippet']['title']
    #             channelId = i['snippet']['resourceId']['channelId']
    #             publishedAt = i['snippet']['publishedAt']
    #             isAdd = False
    #
    #             try:
    #                 user_static_youtube = self.session.query(UserStaticYoutube).filter(
    #                     UserStaticYoutube.user_id == self.user_id) \
    #                     .filter(UserStaticYoutube.channel_id == channelId).one()
    #             except NoResultFound:
    #                 LOG.info(f'AnalysisSubscribe need to add data - {self.user_id} - {channelId}')
    #             except MultipleResultsFound:
    #                 LOG.info(f'AnalysisSubscribe many data - {self.user_id} - {channelId}')
    #                 return
    #
    #             if user_static_youtube is None:
    #                 isAdd = True
    #                 user_static_youtube = UserStaticYoutube()
    #
    #             user_static_youtube.user_id = self.user_id
    #             user_static_youtube.channel_id = channelId
    #             user_static_youtube.sub_date = parse(publishedAt).date()
    #             user_static_youtube.channel_name = title
    #
    #             if title.find("Ch") > -1:
    #                 user_static_youtube.member_name = title[0: int(title.index("Ch")) - 1]
    #
    #             if title.find("ch") > -1:
    #                 user_static_youtube.member_name = title[0: int(title.index("ch")) - 1]
    #
    #             elif title.find("Channel") > -1:
    #                 user_static_youtube.member_name = title[0: int(title.index("Channel")) - 1]
    #
    #             elif title.find("hololive-") > -1:
    #                 user_static_youtube.member_name = title[0: int(title.index("hololive-")) - 1]
    #
    #             user_static_youtube.member_name = user_static_youtube.member_name.strip()
    #
    #             if isAdd:
    #                 LOG.info('add user_static_youtube {}'.format(user_static_youtube.member_name))
    #                 self.session.add(user_static_youtube)
