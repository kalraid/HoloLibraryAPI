import copy

import log
from app.model.holo_member import HoloMember
from app.model.holo_member_image import HoloMemberImage
from app.module.google_api.drive import get_init_datasheet

LOG = log.get_logger()


def get_member_img_data(db_session):
    LOG.debug(' init data - get_member_img_data start ')

    sheet_name = 'member_img'
    df = get_init_datasheet(sheet_name)
    LOG.debug(' init data - get_member_img_data datashhet ok ')

    for index, data_row in df.iterrows():
        holoMember = HoloMember().find_by_id(db_session, data_row[0])

        holoMemberImg = HoloMemberImage()
        holoMemberImg.member = holoMember
        small_img = data_row[1]
        holoMemberImg.img_url = small_img
        holoMemberImg.img_type = 'small'
        db_session.add(holoMemberImg)

        holoMemberImg = HoloMemberImage()
        holoMemberImg.member = holoMember
        circle_img = data_row[2]
        if circle_img != '-':
            holoMemberImg.img_url = circle_img
        else:
            holoMemberImg.img_url = small_img
        holoMemberImg.img_type = 'circle'
        db_session.add(holoMemberImg)

        large_img = data_row[3]

        if "," in large_img:
            for i in large_img.split(","):
                holoMemberImg = HoloMemberImage()
                holoMemberImg.member = holoMember
                holoMemberImg.img_url = i
                holoMemberImg.img_type = 'large'
                db_session.add(holoMemberImg)
        else:
            holoMemberImg = HoloMemberImage()
            holoMemberImg.member = holoMember
            holoMemberImg.img_url = large_img
            holoMemberImg.img_type = 'large'
            db_session.add(holoMemberImg)

    db_session.commit()
    LOG.debug(' init data - get_member_data end ')
