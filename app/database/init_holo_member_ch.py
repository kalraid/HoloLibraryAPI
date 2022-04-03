import array

import requests

import log
from app.model.holo_member_ch import HoloMemberCh
from app.module.google_api.drive import get_init_datasheet

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
        else:
            channelList.append(item)

    for i in channelList:
        db_session.add(i)

    db_session.commit()
    LOG.debug(' init data - get_channel_data end ')