# -*- coding: utf-8 -*-
from uuid import uuid4

import falcon
from sqlalchemy.exc import SQLAlchemyError

import log
from app import config
from app.database import get_engine, get_scoped_session
from app.errors import DatabaseError, ERR_DATABASE_ROLLBACK

LOG = log.get_logger()


class DatabaseSessionManager(object):
    def __init__(self):
        self._session_factory = {}
        self._scoped_keys = []

    async def process_request(self, req, res, resource=None):

        # request Id 발급
        requestId = uuid4().hex

        def get_request_id():
            return requestId

        print(f'req : {req}, requestId : {requestId}')

        req.context["requestId"] = requestId
        self._scoped_keys.append(requestId)

        scoped_session = get_scoped_session(get_request_id)
        req.context["session"] = scoped_session
        self._session_factory[requestId] = scoped_session

        print(f'req.contest : {req.context}')

    async def process_response(self, req, res, resource=None, req_succeeded=None):
        """
        Handle post-processing of the response (after routing).
        """
        if req.method != "OPTIONS":
            scoped_session = req.context["session"]
            try:
                if config.DB_AUTOCOMMIT:
                    try:
                        scoped_session.commit()
                    except SQLAlchemyError as ex:
                        if res.status is not falcon.HTTP_202:
                            scoped_session.rollback()
                        raise DatabaseError(ERR_DATABASE_ROLLBACK, ex.args, ex.params)

                if res.status is not falcon.HTTP_202:
                    if req.context["requestId"] in self._scoped_keys:
                        # keys 목록에서 index찾아서 제거
                        self._scoped_keys.remove(self._scoped_keys.index(req.context["request_id"]))
                        # session 딕셔너리에서 제외
                        scoped_session.remove()
                        self._session_factory[req.context["request_id"]] = None
                    else:
                        scoped_session.close()
            except KeyError as ex:
                LOG.error('not in session ')
