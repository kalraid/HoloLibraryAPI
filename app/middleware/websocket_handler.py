# -*- coding: utf-8 -*-
from falcon.asgi import Request, WebSocket

import log

LOG = log.get_logger()

class WebsocketHandler(object):
    async def process_request_ws(self, req: Request, ws: WebSocket):
        # This will be called for the HTTP request that initiates the
        #   WebSocket handshake before routing.
        pass

    async def process_resource_ws(self, req: Request, ws: WebSocket, resource, params):
        # This will be called for the HTTP request that initiates the
        #   WebSocket handshake after routing (if a route matches the
        #   request).
        pass