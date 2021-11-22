# -*- coding: utf-8 -*-

import re

import falcon
import requests
from sqlalchemy.orm.exc import NoResultFound
from collections import defaultdict

import log, json
from app.api.common import BaseResource
from app.errors import (
    AppError,
    UserNotExistsError,
    PasswordNotMatch,
)
from app.model import User, UserStaticYoutube, HoloMemberCh, HoloMember
from app.utils.auth import verify_password
from app.utils.hooks import auth_required

LOG = log.get_logger()

FIELDS = {
    "username": {"type": "string", "required": True, "minlength": 4, "maxlength": 20},
    "email": {
        "type": "string",
        "regex": "[a-zA-Z0-9._-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}",
        "required": True,
        "maxlength": 320,
    },
    "password": {
        "type": "string",
        "regex": "[0-9a-zA-Z]\w{3,14}",
        "required": True,
        "minlength": 8,
        "maxlength": 64,
    },
    "info": {"type": "dict", "required": False},
}


class Collection(BaseResource):
    """
    Handle for endpoint: /v1/member/youtube/collection
    """

    def on_get(self, req, res):
        session = req.context["session"]

        queryString = dict()
        for key, value in req.params.items():
            queryString[key] = value;
            # LOG.info(f'key  : {key} , value : {value}, req.params : {req.params}, queryString : {queryString}')

        if queryString.get('user_id'):
            member_ch_dbs = session.query(HoloMemberCh, UserStaticYoutube.sub_date, HoloMember.member_classification,
                                          HoloMember.member_generation) \
                .join(UserStaticYoutube, UserStaticYoutube.channel_id == HoloMemberCh.channel_id) \
                .join(HoloMember, HoloMember.member_name_kor == HoloMemberCh.member_name).all()
            member_ch_list = []
            for i in member_ch_dbs:
                # LOG.info(f" type(i) : {type(i)}, i : {i[0]} , i[1] : {i[1]}")
                temp = i[0].to_dict()
                temp['sub_date'] = i[1].strftime('%Y-%m-%d')
                temp['class'] = i[2]
                temp['genera'] = i[3]
                member_ch_list.append(temp)


        else:
            member_ch_dbs = session.query(HoloMemberCh, HoloMember.member_classification, HoloMember.member_generation) \
                .join(HoloMember, HoloMember.member_name_kor == HoloMemberCh.member_name).all()
            member_ch_list = []
            for i in member_ch_dbs:
                temp = i[0].to_dict()
                temp['class'] = i[1]
                temp['genera'] = i[2]
                member_ch_list.append(temp)

        data = member_ch_list
        obj = {'data': data}
        self.on_success(res, obj)
