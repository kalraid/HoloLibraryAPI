import twitter

import log
from app.const import CONST
from app.model import HoloMember, HoloMemberTwitterInfo
from app.module.google_api.drive import get_init_datasheet

LOG = log.get_logger()


twitter_api = twitter.Api(consumer_key=CONST.TWITTER_CONSUMER_KEY,
                          consumer_secret=CONST.TWITTER_CONSUMER_SECRET,
                          access_token_key=CONST.TWITTER_ACCESS_TOKEN,
                          access_token_secret=CONST.TWITTER_ACCESS_SECRET)

def get_twitter_data(db_session):
    LOG.debug(' init data - get_twitter_data start ')
    sheet_name = 'twitter'
    df = get_init_datasheet(sheet_name)
    LOG.debug(' init data - get_twitter_data datashhet ok ')

    for index, data_row in df.iterrows():
        holoMemberTwitterInfo = HoloMemberTwitterInfo()

        holoMemberTwitterInfo.twitter_url = data_row[1]
        holoMemberTwitterInfo.twitter_id = data_row[2]
        holoMemberTwitterInfo.twitter_username = data_row[3]
        holoMemberTwitterInfo.twitter_name = data_row[4]
        holoMemberTwitterInfo.twitter_proto = data_row[5]
        holoMemberTwitterInfo.twitter_header_photo = data_row[6]

        twitterInfo = twitter_api.GetUser(user_id = data_row[2])
        LOG.info(twitterInfo)

        item = db_session.query(HoloMemberTwitterInfo).filter(
            holoMemberTwitterInfo.twitter_id == HoloMemberTwitterInfo.twitter_id).first()

        if item is None:
            holoMemberTwitterInfo.member = HoloMember().find_by_id(db_session, data_row[0])
            db_session.add(holoMemberTwitterInfo)

    db_session.commit()
    LOG.debug(' init data - get_twitter_data end ')
