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
