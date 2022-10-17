# -*- coding: utf-8 -*-
import falcon
import sqlalchemy.orm.scoping as scoping
from sqlalchemy.exc import SQLAlchemyError

import log
from app import config
from app.errors import DatabaseError, ERR_DATABASE_ROLLBACK

LOG = log.get_logger()


class DatabaseSessionManager(object):
    def __init__(self, db_session):
        self._session_factory = db_session
        self._scoped = isinstance(db_session, scoping.ScopedSession)

    async def process_request(self, req, res, resource=None):
        """
        Handle post-processing of the response (after routing).
        """
        ## TODO 현재부분에서 __init__에 scopefunc에 값이 안들어가기때문에 비동기 처리가 되지 않음
        ## https://www.hides.kr/m/1081
        ## Session = scoped_session(sessionmaker(), scopefunc=get_current_tornado_request)
        req.context["session"] = self._session_factory

    async def process_response(self, req, res, resource=None, req_succeeded=None):
        """
        Handle post-processing of the response (after routing).
        """
        if req.method != "OPTIONS":
            session = req.context["session"]
            try:
                if config.DB_AUTOCOMMIT:
                    try:
                        session.commit()
                    except SQLAlchemyError as ex:
                        if res.status is not falcon.HTTP_202:
                            session.rollback()
                        raise DatabaseError(ERR_DATABASE_ROLLBACK, ex.args, ex.params)

                if res.status is not falcon.HTTP_202:
                    if self._scoped:
                        # remove any database-loaded state from all current objects
                        # so that the next access of any attribute, or any query execution will retrieve new state
                        session.remove()
                    else:
                        session.close()
            except KeyError as ex:
                LOG.error('not in session ')
