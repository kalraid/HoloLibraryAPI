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
        LOG.info(req.context)
        session = req.context["session"]
        data = req.context["data"]
        if data:
            user = User()
            user_req = data['userInfo']

            if user_req:

                user.user_id = uuid
                user.email = user_req["userEmail"]
                user.user_name = user_req["userId"]
                user.access_token = user_req["accessToken"]

                LOG.info(user.__repr__())
                try:
                    user_db = session.query(User).filter(User.email == user.email).one()
                    LOG.info(user_db.__repr__)
                except NoResultFound:
                    user_db = None

                LOG.info(session.__repr__)
                if not user_db:
                    session.add(user)

                else:
                    user_db.access_token = user.access_token
                    session.update(user_db)

                t1 = AnalysisSubscribeThread(user, session)
                t1.start()

                self.on_success(res, None)
            else:
                raise InvalidParameterError(req.context["data"]['userInfo'])
        else:
            raise InvalidParameterError(req.context["data"])

    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.body = self.to_json(self.HELLO_WORLD)
