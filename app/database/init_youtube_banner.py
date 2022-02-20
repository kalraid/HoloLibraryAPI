import array

import requests

import log
from app.model.holo_member_ch import HoloMemberCh
from app.utils.itertools import partition

LOG = log.get_logger()



def get_youtube_banner(db_session):
    channelList = []

    data = db_session.query(HoloMemberCh).all()
    for i in data:
        channelList.append(i)

    channelList = __craw_youtube_banner__(channelList)

    for i in channelList:
        LOG.info(i)

    db_session.commit()

def __craw_youtube_banner__(channelList) -> array:
    result = []
    channelStr = ''

    chunks = list(partition(channelList, 45))

    for item in chunks:
        for idx, i, in enumerate(item):
            if idx == 0:
                channelStr = i.channel_id
            else:
                channelStr = channelStr + '%2C' + i.channel_id

        # https://content-youtube.googleapis.com/youtube/v3/channels?id=&part=id&part=snippet&part=brandingSettings&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM
        # + "&id=UC7fk0CB07ly8oSl0aqKkqFg%2CUCp6993wxpyDPHUpavwDFqgg%2CUCoSrY_IQQVpmIRZ9Xf-y93g%2CUCyl1z3jo3XHR1riLFKG5UAg%2CUCL_qhgtOy0dy1Agp8vkySQg%2CUCHsx4Hqa-1ORjQTh9TYDhww%2CUC8rcEBzJSleTkf_-agPM20g%2CUCsUj0dszADCGbF3gNrQEuSQ%2CUC3n5uGu18FoCy23ggWWp8tA%2CUCmbs8T6MWqUHP1tIQvSgKrg%2CUCO_aKKYxn4tvrqPjcTzZ6EQ%2CUCgmPnx-EEeOrZSg5Tiw7ZRQ%2CUCp6993wxpyDPHUpavwDFqgg" \
        headers = {'x-referer': 'https://explorer.apis.google.com'}
        url = "https://content-youtube.googleapis.com/youtube/v3/channels?" \
              + "part=id%2C%20snippet%2C%20brandingSettings" \
              + "&id=" + channelStr \
              + "&key=AIzaSyBsllwXmQhh-sX-dCUyJgZYanUx9XppLgs"
        r = requests.get(url=url, headers=headers)
        __update_user_static__(r.json(), item)

    return result


def __update_user_static__(json, item) -> []:
    result = []
    sub_data = json['items']

    if sub_data is not None:
        for i in sub_data:
            id = i['id']
            try:
                thumbnail = i['snippet']['thumbnails']['high']['url']
            except:
                thumbnail = None
            try:
                image = i['brandingSettings']['image']['bannerExternalUrl']
            except:
                image = None

            holoMemberCh = item[[x.channel_id == id for x in item].index(True)]
            holoMemberCh.channel_profile_img_url = thumbnail
            holoMemberCh.channel_banner_img_url = image

    return item