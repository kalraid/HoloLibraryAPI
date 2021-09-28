# -*- coding: utf-8 -*-

import re
import falcon
import requests

from sqlalchemy.orm.exc import NoResultFound
from cerberus import Validator

import log
from app.api.common import BaseResource
from app.utils.hooks import auth_required
from app.utils.auth import encrypt_token, hash_password, verify_password, uuid
from app.model import User
from app.errors import (
    AppError,
    InvalidParameterError,
    UserNotExistsError,
    PasswordNotMatch,
)

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
        user_dbs = session.query(User).all()
        if user_dbs:
            obj = [user.to_dict() for user in user_dbs]
            self.on_success(res, obj)
        else:
            raise AppError()


class Item(BaseResource):
    """
    Handle for endpoint: /v1/users/static/youtube/{user_id}
    """

    #@falcon.before(auth_required)
    def on_get(self, req, res, user_id):

        ## DB 구상 목록
        # 1. 홀로 채널 TABLE : 채널 명, 채널 ID, 버튜버 key
        # 2. 홀로 멤버 TABLE : 이름, 애칭(json)

        ## 홀로애들 채널 목록 DB ( 채널 명, 채널 ID, 버튜버 key, )
        # https://developers.google.com/youtube/v3/docs/subscriptions/list?hl=ko&apix_params=%7B%22part%22%3A%5B%22id%2C%20snippet%22%5D%2C%22forChannelId%22%3A%22UC7fk0CB07ly8oSl0aqKkqFg%2CUCp6993wxpyDPHUpavwDFqgg%2CUCoSrY_IQQVpmIRZ9Xf-y93g%2CUCyl1z3jo3XHR1riLFKG5UAg%2CUCL_qhgtOy0dy1Agp8vkySQg%2CUCHsx4Hqa-1ORjQTh9TYDhww%2CUC8rcEBzJSleTkf_-agPM20g%2CUCsUj0dszADCGbF3gNrQEuSQ%2CUC3n5uGu18FoCy23ggWWp8tA%2CUCmbs8T6MWqUHP1tIQvSgKrg%2CUCO_aKKYxn4tvrqPjcTzZ6EQ%2CUCgmPnx-EEeOrZSg5Tiw7ZRQ%2CUCp6993wxpyDPHUpavwDFqgg%22%2C%22maxResults%22%3A100%2C%22mine%22%3Atrue%7D&apix=true#try-it

        url = "https://www.googleapis.com/youtube/v3/subscriptions" \
              + "mine=true"+"&"+"forChannelId="+"UC7fk0CB07ly8oSl0aqKkqFg%2CUCp6993wxpyDPHUpavwDFqgg"+"&part=id%2C%20snippet"+"&"+"key="+"AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"
        requests.post('https://www.googleapis.com/youtube/v3/subscriptions', )
        user_id
        # try:
        #     user_db = User.find_one(session, user_id)
        #     self.on_success(res, user_db.to_dict())
        # except NoResultFound:
        #     raise UserNotExistsError("user id: %s" % user_id)


class Self(BaseResource):
    """
    Handle for endpoint: /v1/users/self
    """

    LOGIN = "login"
    RESETPW = "resetpw"

    def on_get(self, req, res):
        cmd = re.split("\\W+", req.path)[-1:][0]
        if cmd == Self.LOGIN:
            self.process_login(req, res)
        elif cmd == Self.RESETPW:
            self.process_resetpw(req, res)

    def process_login(self, req, res):
        data = req.context["data"]
        email = data["email"]
        password = data["password"]
        session = req.context["session"]
        try:
            user_db = User.find_by_email(session, email)
            if verify_password(password, user_db.password.encode("utf-8")):
                self.on_success(res, user_db.to_dict())
            else:
                raise PasswordNotMatch()
        except NoResultFound:
            raise UserNotExistsError("User email: %s" % email)

    @falcon.before(auth_required)
    def process_resetpw(self, req, res):
        pass