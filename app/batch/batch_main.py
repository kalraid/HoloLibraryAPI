# -*- coding: utf-8 -*-

import falcon.asgi

import log
from app.database import db_session, init_session
from app.errors import AppError
from app.middleware import JSONTranslator, DatabaseSessionManager, CORSMiddleware, WebsocketHandler

LOG = log.get_logger()


class App(falcon.asgi.App):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        LOG.info("Batch Server is starting")

        self.add_error_handler(AppError, AppError.handle)


init_session()
middleware = [CORSMiddleware(), JSONTranslator(), DatabaseSessionManager(db_session), WebsocketHandler()]
application = App(middleware=middleware, cors_enable=True)

if __name__ == "__main__":
    # from wsgiref import simple_server
    #
    # httpd = simple_server.make_server("127.0.0.1", 8000, application)
    # httpd.serve_forever()
    import app.batch.Thread.Threading as BatchThreading

    twitterThreading = BatchThreading.TwitterThreading()
    twitterThreading.start()
    twitterTagthreading = BatchThreading.TwitterTagThreading()
    twitterTagthreading.start()
    twitterCustomTagthreading = BatchThreading.TwitterCustomTagThreading()
    twitterCustomTagthreading.start()

    import uvicorn

    uvicorn.run(application, host="0.0.0.0", port=8000, log_level="info")

if __name__ == '__exit__':
    LOG.info('Threading all stop -- start')

    LOG.info('Threading all stop -- end')
