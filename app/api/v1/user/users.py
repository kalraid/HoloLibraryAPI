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
    "userId": {"type": "string", "required": True, },
    "userEmail": {"type": "string", "required": True, }
}

class Item(BaseResource):
    """
    Handle for endpoint: /v1/users/{user_id}
    """

    def on_get(self, req, res, user_id):
        session = req.context["session"]
        try:
            user_db = User.find_by_id(session, user_id)
            self.on_success(res, user_db.to_dict())
        except NoResultFound:
            raise UserNotExistsError("user id: %s" % user_id)

