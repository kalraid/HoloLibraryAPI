# -*- coding: utf-8 -*-

import log
from app.errors import UnauthorizedError
from app.utils.auth import decrypt_token

LOG = log.get_logger()


class AuthHandler(object):
    async def process_request(self, req, res, resource=None):
        LOG.debug("Authorization: %s", req.auth)
        if req.auth is not None:
            token = decrypt_token(req.auth)
            if token is None:
                raise UnauthorizedError("Invalid auth token: %s" % req.auth)
            else:
                req.context["auth_user"] = token.decode("utf-8")
        else:
            req.context["auth_user"] = None