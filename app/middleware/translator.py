# -*- coding: utf-8 -*-

import json

import falcon

import log
from app.errors import InvalidParameterError

LOG = log.get_logger()


class JSONTranslator(object):
    async def process_request(self, req, res):
        if req.content_type is not None and "json" in req.content_type:
            try:
                data = await req.stream.read()
            except Exception:
                message = 'Read Error'
                raise falcon('Bad request', message)
            try:
                req.context['data'] = json.loads(data)
            except ValueError:
                raise InvalidParameterError('No JSON object could be decoded or Malformed JSON')
            except UnicodeDecodeError:
                raise InvalidParameterError('Cannot be decoded by utf-8')

