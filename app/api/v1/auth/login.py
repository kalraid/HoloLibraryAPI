# -*- coding: utf-8 -*-
import falcon
from sqlalchemy.orm.exc import NoResultFound

import log
from app.api.common import BaseResource
from app.errors import (
    InvalidParameterError,
)
from app.model import User
from app.utils.auth import uuid

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict

from app.api.v1.static.thread.analysis import AnalysisSubscribeThread

LOG = log.get_logger()

FIELDS = {
    "accessToken": {"type": "string", "required": True},
    "userId": {"type": "string", "required": True},
    "userEmail": {"type": "string", "required": True},
    "picture": {"type": "String", "required": False},
}


class Auth(BaseResource):
    """
    Handle for endpoint: /v1/login
    """

    def on_post(self, req, res):
        session = req.context["session"]
        user_req = req.context["data"]["userInfo"]
        if user_req:
            user = User()
            user.user_id = user_req["userId"]
            user.username = user_req["userId"]
            user.email = user_req["userEmail"]
            user.access_token = user_req["accessToken"]

            user_db = None
            try:
                user_db = session.query(User).filter(User.email == user.email).one()
            except:
                LOG.info(user.__repr__())

            if not user_db:
                session.add(user)

            else:
                user_db.access_token = user.access_token

                # orm pattern is not need call update
                # session.update(user_db)

            t1 = AnalysisSubscribeThread(user.access_token, session, user.user_id)
            t1.start()

            self.on_success_thread(res, None)
        else:
            raise InvalidParameterError(req.context["data"])


    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.body = self.to_json(self.HELLO_WORLD)
