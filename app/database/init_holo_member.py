import log
from app.model.holo_member import HoloMember
from app.module.google_api.drive import get_init_datasheet

LOG = log.get_logger()


def get_member_data(db_session):
    LOG.debug(' init data - get_member_data start ')

    sheet_name = 'member'
    df = get_init_datasheet(sheet_name)
    LOG.debug(' init data - get_member_data datashhet ok ')

    LOG.info(656565)

    for index, data_row in df.iterrows():
        holoMember = HoloMember()

        holoMember.company_name_alias = data_row[0]
        holoMember.member_classification = data_row[1]
        holoMember.member_generation = data_row[2]
        holoMember.member_name_kor = data_row[3]
        holoMember.member_name_eng = data_row[4]
        holoMember.member_name_jp = data_row[5]

        LOG.info(holoMember.__repr__())

        # if this line error ['InstanceState' object has no attribute '_post_inspect']
        # you check to queery in name ( that is not alias but modelname)
        item = db_session.query(HoloMember).filter(HoloMember.member_name_kor == holoMember.member_name_kor).first()

        if item is None:
            db_session.add(holoMember)

    db_session.commit()
    LOG.debug(' init data - get_member_data end ')
