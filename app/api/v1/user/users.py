# -*- coding: utf-8 -*-

import re

import falcon
from sqlalchemy.orm.exc import NoResultFound

import log
from app.api.common import BaseResource
from app.errors import (
    AppError,
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

    @falcon.before(auth_required)
    async def on_get(self, req, res):
        session = req.context["session"]
        user_dbs = session.query(User).all()
        if user_dbs:
            obj = [user.to_dict() for user in user_dbs]
            self.on_success(res, obj)
        else:
            raise AppError()

    @falcon.before(auth_required)
    async def on_put(self, req, res):
        pass


class Item(BaseResource):
    """
    Handle for endpoint: /v1/users/{user_id}
    """

    # @falcon.before(auth_required)
    async def on_get(self, req, res, user_id):
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

    async def on_get(self, req, res):
        cmd = re.split("\\W+", req.path)[-1:][0]
        if cmd == Self.LOGIN:
            self.process_login(req, res)
        elif cmd == Self.RESETPW:
            self.process_resetpw(req, res)

    async def process_login(self, req, res):
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
    async def process_resetpw(self, req, res):
        pass
