# -*- coding: utf-8 -*-

import json

from falcon.asgi import Request, WebSocket
from falcon.errors import WebSocketDisconnected

import log
from app.api.common import BaseResource
from app.database import get_session
from app.model import DrawStatistics, HoloTwitterDraw, HoloTwitterCustomDraw

LOG = log.get_logger()
db_session = get_session()


class Count(BaseResource):
    """
    Handle for endpoint: /v1/statistics/count/image
    """

    async def on_websocket(self, req: Request, socket: WebSocket):
        statistics_connection_clients = []
        LOG.info("----- /v1/statistics/count/image statistic websocket init start ---------")
        LOG.info(req)

        if 'statistics' not in socket.subprotocols:
            return

        try:
            await socket.accept(subprotocol='statistics')
            statistics_connection_clients.append(socket)
            LOG.info(statistics_connection_clients)
        except WebSocketDisconnected:
            LOG.error("statistic websocket WebSocketDisconnected - not accepted")
            if socket in statistics_connection_clients:
                statistics_connection_clients.remove(socket)
                LOG.info(statistics_connection_clients)
            return

        while True:
            try:
                statistics_object = await socket.receive_media()
                LOG.info(statistics_object)

                drawStatistics = DrawStatistics()
                drawStatistics.event = statistics_object['message']
                if not statistics_object['data'] or 'index' not in statistics_object['data']:
                    return

                if drawStatistics.event == 'disable':
                    if 'base' in statistics_object['type']:
                        holoTwitterDraw = HoloTwitterDraw().get_by_id(db_session, statistics_object['data']['index'])
                        holoTwitterDraw.isUse = 'N'
                    elif 'custom' in statistics_object['type'] :
                        holoTwitterCustomDraw = HoloTwitterCustomDraw().get_by_id(db_session, statistics_object['data']['index'])
                        holoTwitterCustomDraw.isUse = 'N'

                drawStatistics.user_uuid = statistics_object['user']
                if statistics_object['type'] == 'base':
                    drawStatistics.holo_twitter_draw_id = statistics_object['data']['index']
                elif statistics_object['type'] == 'custom':
                    drawStatistics.holo_twitter_custom_draw_id = statistics_object['data']['index']

                db_session.add(drawStatistics)
                db_session.commit()

            except WebSocketDisconnected:
                LOG.error("statistic websocket WebSocketDisconnected")
                if socket in statistics_connection_clients:
                    statistics_connection_clients.remove(socket)
                    LOG.info(statistics_connection_clients)
                return
            except TypeError:
                LOG.error("statistic websocket TypeError")

                pass
            except json.JSONDecodeError:
                LOG.error("statistic websocket JSONDecodeError")
                pass
