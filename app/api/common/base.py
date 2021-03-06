# -*- coding: utf-8 -*-

import json

import falcon
from sqlalchemy import func, or_, text
from sqlalchemy.orm import aliased

from app.model import DrawStatisticsMenual

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict

import log
from app.utils.alchemy import new_alchemy_encoder
from app.config import BRAND_NAME, MYSQL
from app.database import engine
from app.errors import NotSupportedError

LOG = log.get_logger()


class BaseResource(object):
    HELLO_WORLD = {
        "server": "%s" % BRAND_NAME,
        "database": "%s (%s)" % (engine.name, MYSQL["host"]),
    }

    def to_json(self, body_dict):
        return json.dumps(body_dict)

    def from_db_to_json(self, db):
        return json.dumps(db, cls=new_alchemy_encoder())

    def on_error(self, res, error=None):
        res.status = error["status"]
        meta = OrderedDict()
        meta["code"] = error["code"]
        meta["message"] = error["message"]

        obj = OrderedDict()
        obj["meta"] = meta
        res.body = self.to_json(obj)

    def on_success(self, res, data=None):
        res.status = falcon.HTTP_200
        meta = OrderedDict()
        meta["code"] = 200
        meta["message"] = "OK"

        obj = OrderedDict()
        obj["meta"] = meta
        obj["data"] = data
        res.body = self.to_json(obj)

    def on_success_thread(self, res, data=None):
        res.status = falcon.HTTP_202
        meta = OrderedDict()
        meta["code"] = 202
        meta["message"] = "OK - thread is running"

        obj = OrderedDict()
        obj["meta"] = meta
        obj["data"] = data
        res.body = self.to_json(obj)

    async def on_get(self, req, res):
        if req.path == "/":
            res.status = falcon.HTTP_200
            res.body = self.to_json(self.HELLO_WORLD)
        else:
            raise NotSupportedError(method="GET", url=req.path)

    async def on_post(self, req, res):
        if req.path == "/":
            res.status = falcon.HTTP_200
            res.body = self.to_json(self.HELLO_WORLD)
        else:
            raise NotSupportedError(method="POST", url=req.path)

    async def on_put(self, req, res):
        raise NotSupportedError(method="PUT", url=req.path)

    async def on_delete(self, req, res):
        raise NotSupportedError(method="DELETE", url=req.path)


class SessionCommonAlias:
    def ban_images(self, session):
        not_show_draw = session.query(DrawStatisticsMenual.holo_twitter_draw_id,
                                      DrawStatisticsMenual.holo_twitter_custom_draw_id,
                                      func.sum(DrawStatisticsMenual.like).label('like'),
                                      func.sum(DrawStatisticsMenual.dislike).label('dislike'),
                                      func.sum(DrawStatisticsMenual.adult).label('adult'),
                                      func.sum(DrawStatisticsMenual.ban).label('ban')
                                      ).group_by(DrawStatisticsMenual.holo_twitter_draw_id,
                                                 DrawStatisticsMenual.holo_twitter_custom_draw_id). \
            filter(or_(text("adult > 0"), text("ban > 0"), text("dislike > 8"))).subquery()
        alias = aliased(DrawStatisticsMenual, not_show_draw)
        return alias
