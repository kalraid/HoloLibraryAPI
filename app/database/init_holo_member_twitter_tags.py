import log
from app.model import HoloMember, HoloMemberHashtag
from app.module.google_api.drive import get_init_datasheet

LOG = log.get_logger()


def get_twitter_tags_data(db_session):
    LOG.debug(' init data - get_twitter_tags_data start ')
    sheet_name = 'base_tag'
    df = get_init_datasheet(sheet_name)
    LOG.debug(' init data - get_twitter_tags_data datashhet ok ')

    names = df[:0].columns  # tag type array
    for _, data_row in df[0:].iterrows():
        holo_member_name_kor = data_row[0]
        member = db_session.query(HoloMember).filter(HoloMember.member_name_kor == holo_member_name_kor).first()
        for index, value in enumerate(data_row[1:]):
            if value != "-" and value == value:  # "-" and  NaN  values not start
                if ',' in value:
                    for hashtag_str in value.split(','):
                        hashtag = hashtag_str.strip()
                        if hashtag[0] != '#':
                            hashtag = '#' + hashtag

                        holoMemberHashtag = db_session.query(HoloMemberHashtag).filter(
                            HoloMemberHashtag.member_id == member.index) \
                            .filter(HoloMemberHashtag.hashtag == hashtag).first()

                        if holoMemberHashtag is None:
                            holoMemberHashtag = HoloMemberHashtag()

                        holoMemberHashtag.hashtag = hashtag;
                        holoMemberHashtag.datatype = "init";
                        holoMemberHashtag.tagtype = names[index + 1];
                        holoMemberHashtag.member = member

                else:
                    holoMemberHashtag = db_session.query(HoloMemberHashtag).filter(
                        HoloMemberHashtag.member_id == member.index) \
                        .filter(HoloMemberHashtag.hashtag == value).first()

                    if holoMemberHashtag is None:
                        holoMemberHashtag = HoloMemberHashtag()

                    holoMemberHashtag.hashtag = value;
                    holoMemberHashtag.datatype = "init";
                    holoMemberHashtag.tagtype = names[index + 1];
                    holoMemberHashtag.member = member

    db_session.commit()
    LOG.debug(' init data - get_twitter_data end ')
