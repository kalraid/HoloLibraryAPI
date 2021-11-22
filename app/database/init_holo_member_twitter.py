import log
from app.model import HoloMember, HoloMemberTwitterInfo
from app.module.google_api.drive import get_init_datasheet

LOG = log.get_logger()


def get_twitter_data(db_session):
    LOG.debug(' init data - get_twitter_data start ')
    sheet_name = 'twitter'
    df = get_init_datasheet(sheet_name)
    LOG.debug(' init data - get_twitter_data datashhet ok ')

    for index, data_row in df.iterrows():
        holoMemberTwitterInfo = HoloMemberTwitterInfo()
        holoMemberTwitterInfo.member = HoloMember().find_by_id(db_session, data_row[0])

        holoMemberTwitterInfo.twitter_url = data_row[1]
        holoMemberTwitterInfo.twitter_id = data_row[2]
        holoMemberTwitterInfo.twitter_username = data_row[3]
        holoMemberTwitterInfo.twitter_name = data_row[4]



        item = db_session.query(HoloMemberTwitterInfo).filter(
            holoMemberTwitterInfo.twitter_id == HoloMemberTwitterInfo.twitter_id).first()
        if item is None:
            db_session.add(holoMemberTwitterInfo)

    db_session.commit()
    LOG.debug(' init data - get_twitter_data end ')
