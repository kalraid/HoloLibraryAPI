# -*- coding: utf-8 -*-
import falcon

import log
from app.api.common import BaseResource
from app.errors import (
    InvalidParameterError,
)
from app.model import User, UserStaticYoutube

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict

from app.api.v1.statistics.thread.analysis import AnalysisSubscribeThread

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

    async def on_post(self, req, res):
        session = req.context["session"]
        user_req = req.context["data"]["userInfo"]
        if user_req:
            user = User()
            user.user_id = user_req["userId"]
            user.username = user_req["userName"]
            user.email = user_req["userEmail"]
            user.access_token = user_req["accessToken"]

            user_db = None
            age = UserStaticYoutube()
            try:
                user_db = session.query(User).filter(User.email == user.email).one()
            except:
                LOG.info(user.__repr__())

            if not user_db:
                session.add(user)
                age = session.query(UserStaticYoutube).filter(UserStaticYoutube.user_id == user.user_id) \
                    .order_by(UserStaticYoutube.sub_date.desc()).first()
            else:
                user_db.access_token = user.access_token

                # orm pattern is not need call update
                # session.update(user_db)

            t1 = AnalysisSubscribeThread(user.access_token, session, user.user_id)
            t1.start()

            user.user_id = user_req["userId"]
            user.username = user_req["userName"]
            user.email = user_req["userEmail"]
            user.access_token = user_req["accessToken"]

            response = {'user_id': user.user_id, 'username': user.username, 'email': user.email, 'access_token': user.access_token, 'age': age.sub_date}

            self.on_success_thread(res, response)
        else:
            raise InvalidParameterError(req.context["data"])

    async def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.body = self.to_json(self.HELLO_WORLD)
