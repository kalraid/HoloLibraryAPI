# -*- coding: utf-8 -*-

import re

import falcon
from sqlalchemy.orm.exc import NoResultFound

import log
from app.api.common import BaseResource
from app.api.v1.static.thread.analysis import AnalysisSubscribeThread
from app.errors import (
    AppError,
    InvalidParameterError,
    UserNotExistsError,
    PasswordNotMatch,
)
from app.model import User
from app.utils.auth import verify_password
from app.utils.hooks import auth_required

LOG = log.get_logger()

FIELDS = {
    "accessToken": {"type": "string", "required": True},
    "userId": {"type": "string", "required": True, },
    "userEmail": {"type": "string", "required": True, },
    "picture": {"type": "String", "required": False},
}

class Collection(BaseResource):
    """
    Handle for endpoint: /v1/users
    """
    def on_post(self, req, res):
        session = req.context["session"]
        user_req = req.context["data"]
        if user_req:
            user = User()
            user.user_id = user_req["user_id"]
            user.user_name = user_req["user_name"]
            user.email = user_req["email"]
            user.access_token = user_req["access_token"]

            user_db = session.query(User).filter(User.email == user.email).one()

            if not user_db:
                session.add(user)

            else:
                user_db.access_token = user.access_token
                session.update(user_db)

            t1 = AnalysisSubscribeThread(user, session)
            t1.start()

            self.on_success(res, None)
        else:
            raise InvalidParameterError(req.context["data"])

    @falcon.before(auth_required)
    def on_get(self, req, res):
        session = req.context["session"]
        user_dbs = session.query(User).all()
        if user_dbs:
            obj = [user.to_dict() for user in user_dbs]
            self.on_success(res, obj)
        else:
            raise AppError()

    @falcon.before(auth_required)
    def on_put(self, req, res):
        pass


class Item(BaseResource):
    """
    Handle for endpoint: /v1/users/{user_id}
    """

    @falcon.before(auth_required)
    def on_get(self, req, res, user_id):
        session = req.context["session"]
        try:
            user_db = User.find_one(session, user_id)
            self.on_success(res, user_db.to_dict())
        except NoResultFound:
            raise UserNotExistsError("user id: %s" % user_id)


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
