import array
import json

import log
from app.model.holo_member_ch import HoloMemberCh
from app.module.google_api.drive import get_init_datasheet
import requests
from bs4 import BeautifulSoup

LOG = log.get_logger()


def get_channel_data(db_session):
    LOG.debug(' init data - get_channel_data start ')
    sheet_name = 'channel'
    df = get_init_datasheet(sheet_name)
    LOG.debug(' init data - get_channel_data datashhet ok ')

    channelList = []

    for index, data_row in df.iterrows():
        holoMemberCh = HoloMemberCh()

        holoMemberCh.company_name = data_row[0]
        holoMemberCh.member_name = data_row[1]
        holoMemberCh.channel_name = data_row[2]
        holoMemberCh.channel_id = data_row[3]
        holoMemberCh.channel_url = data_row[4]

        item = db_session.query(HoloMemberCh).filter(HoloMemberCh.channel_id == holoMemberCh.channel_id).first()
        if item is None:
            channelList.append(holoMemberCh)

    channelList = __craw_youtube_banner__(channelList)

    for i in channelList:
        db_session.add(i)

    db_session.commit()
    LOG.debug(' init data - get_channel_data end ')


def __craw_youtube_banner__(channelList) -> array:
    result = []
    channelStr = ''

    for i in channelList:
        channelStr = channelStr + ',' + ''.join(i.channel_id)

    url = "https://www.googleapis.com/youtube/v3/channels" \
          + "?id=&part=id&part=snippet&part=brandingSettings" + "&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM" \
          + "&maxResults=100"+ "&id=" + channelStr

    # https://content-youtube.googleapis.com/youtube/v3/channels?id=&part=id&part=snippet&part=brandingSettings&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM

    r = requests.get(url=url)
    LOG.info(r.json())
    # sub_data = json['items']
    #
    # if sub_data is not None:
    #     for i in sub_data:
    #         id = i['id']
    #         title = i['snippet']['title']
    #         channelId = i['snippet']['resourceId']['channelId']
    #         publishedAt = i['snippet']['publishedAt']


    return result
