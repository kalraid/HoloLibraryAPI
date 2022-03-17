import twitter

import log
from app.const import CONST
from app.database import get_session, init_session
from app.model import HoloMember, HoloMemberTwitterInfo
from app.module.google_api.drive import get_init_datasheet

LOG = log.get_logger()
init_session()
db_session = get_session()
twitter_api = twitter.Api(consumer_key=CONST.TWITTER_CONSUMER_KEY,
                          consumer_secret=CONST.TWITTER_CONSUMER_SECRET,
                          access_token_key=CONST.TWITTER_ACCESS_TOKEN,
                          access_token_secret=CONST.TWITTER_ACCESS_SECRET)


def get_twitter_data(): # TODO automation
    LOG.debug(' init data - get_twitter_data start ')
    sheet_name = 'twitter'
    df = get_init_datasheet(sheet_name)
    LOG.debug(' init data - get_twitter_data datashhet ok ')

    for index, data_row in df.iterrows():
        isAdd = False
        holoMemberTwitterInfo = HoloMemberTwitterInfo.find_by_twitter_info_id(db_session, data_row[2])

        if holoMemberTwitterInfo is None:
            holoMemberTwitterInfo = HoloMemberTwitterInfo()
            isAdd = True

        holoMemberTwitterInfo.twitter_url = data_row[1]
        holoMemberTwitterInfo.twitter_id = data_row[2]
        holoMemberTwitterInfo.twitter_username = data_row[3]
        holoMemberTwitterInfo.twitter_name = data_row[4]

        twitterInfo = twitter_api.GetUser(user_id=data_row[2])
        holoMemberTwitterInfo.twitter_header_photo = twitterInfo.profile_banner_url

        proto = twitterInfo.profile_image_url_https
        proto = proto.replace('_normal.jpg','_400x400.jpg')
        holoMemberTwitterInfo.twitter_proto = proto

        holoMemberTwitterInfo.member = HoloMember().find_by_id(db_session, data_row[0])

        if isAdd:
            db_session.add(holoMemberTwitterInfo)

    db_session.commit()
    LOG.debug(' init data - get_twitter_data end ')


get_twitter_data()
