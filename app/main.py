# -*- coding: utf-8 -*-

import falcon.asgi

import log
from app.api.common import base
from app.api.v1.auth import login
from app.api.v1.member import member
from app.api.v1.menu import menu
from app.api.v1.statistics import image
from app.api.v1.twitter import tweet
from app.api.v1.user import users
from app.database import db_session, init_session
from app.errors import AppError
from app.middleware import AuthHandler, JSONTranslator, DatabaseSessionManager, CORSMiddleware, WebsocketHandler

LOG = log.get_logger()


class App(falcon.asgi.App):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        LOG.info("API Server is starting")

        self.add_route("/", base.BaseResource())
        self.add_route("/v1/login", login.Auth())

        self.add_route("/v1/statistics/count/image", image.Count())

        self.add_route("/v1/menu/list", menu.Menu())

        self.add_route("/v1/users", users.Collection())
        self.add_route("/v1/users/{user_id}", users.Item())
        self.add_route("/v1/users/self/login", users.Self())

        self.add_route("/v1/member/list", member.List())
        self.add_route("/v1/member/customes", member.Customes())
        self.add_route("/v1/member/tags", member.Tags())
        self.add_route("/v1/member/tweets", member.Tweets())
        self.add_route("/v1/member/tweet/live", member.TweetLive())
        self.add_route("/v1/member/youtube/channel/list", member.Collection())

        self.add_route("/v1/twitter", tweet.TwitterList())
        self.add_route("/v1/tweet/draws", tweet.Draws())
        self.add_route("/v1/tweet/draws/live", tweet.DrawsLive())

        self.add_route("/v1/tweet/custom/draws", tweet.CustomDraws())
        self.add_route("/v1/tweet/custom/tags", tweet.CustomTags())

        self.add_route("/v1/tweet/renewer/draws", tweet.RenewerDraws())

        self.add_route("/v1/tweet/detail", tweet.TweetInfo())
        self.add_route("/v1/tweet/ids", tweet.TweetIds())

        self.add_route("/v1/tweet/member/{memeber_id}", users.Self())
        self.add_route("/robots.txt", DenyCrawlers())

        self.add_error_handler(AppError, AppError.handle)


class DenyCrawlers(object):
    async def on_get(self, req, resp):
        resp.body = "User-agent: *\nDisallow: /\n"


init_session()
middleware = [CORSMiddleware(), AuthHandler(), JSONTranslator(), DatabaseSessionManager(db_session), WebsocketHandler()]
application = App(middleware=middleware, cors_enable=True)

if __name__ == "__main__":
    # from wsgiref import simple_server
    #
    # httpd = simple_server.make_server("127.0.0.1", 8000, application)
    # httpd.serve_forever()

    import uvicorn

    uvicorn.run(application, host="0.0.0.0", port=8000, log_level="info", ws_ping_interval=10,
                ws_ping_timeout=60 * 60, timeout_keep_alive=60 * 5)
