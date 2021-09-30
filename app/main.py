# -*- coding: utf-8 -*-

import falcon

import log
from app.api.common import base
from app.api.v1.auth import login
from app.api.v1.static import youtube
from app.api.v1.user import users
from app.database import db_session, init_session
from app.errors import AppError
from app.middleware import AuthHandler, JSONTranslator, DatabaseSessionManager, CORSMiddleware

LOG = log.get_logger()


class App(falcon.App):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        LOG.info("API Server is starting")

        self.add_route("/", base.BaseResource())
        self.add_route("/v1/login", login.Auth())

        self.add_route("/v1/users", users.Collection())
        self.add_route("/v1/users/{user_id}", users.Item())
        self.add_route("/v1/users/self/login", users.Self())

        self.add_route("/v1/users/static/static/{user_id}", youtube.Item())
        self.add_route("/v1/users/static/static", youtube.Collection())

        self.add_error_handler(AppError, AppError.handle)


init_session()
middleware = [CORSMiddleware(), AuthHandler(), JSONTranslator(), DatabaseSessionManager(db_session)]
application = App(middleware=middleware, cors_enable=True)

if __name__ == "__main__":
    from wsgiref import simple_server

    httpd = simple_server.make_server("127.0.0.1", 8000, application)
    httpd.serve_forever()
