# -*- coding: utf-8 -*-

import re

import falcon
import requests
from sqlalchemy.orm.exc import NoResultFound

import log
from app.api.common import BaseResource
from app.errors import (
    AppError,
    UserNotExistsError,
    PasswordNotMatch,
)
from app.model import User, UserStaticYoutube
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
    Handle for endpoint: /v1/users/static/youtube
    """

    def on_get(self, req, res):
        session = req.context["session"]
        user_req = req.context["data"]["userInfo"]
        user_dbs = session.query(UserStaticYoutube).filter(UserStaticYoutube.user_id == user_req.user_id).all()
        if user_dbs:
            obj = [user.to_dict() for user in user_dbs]
            self.on_success(res, obj)
        else:
            raise AppError()