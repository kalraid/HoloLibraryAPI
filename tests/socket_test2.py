#!/usr/bin/env python

import asyncio
import time

import websockets
from websockets.exceptions import ConnectionClosed

import log, json

LOG = log.get_logger()


async def hello():
    # async with websockets.connect("ws://localhost:8000/v1/member/tweet/live", subprotocols=["live_tweet"],
    #                               ping_interval=10, ping_timeout=60 * 60) as websocket:
    #     LOG.info("websocket start ")
    #     for i in range(0, 2000):
    #         data = {"message": "Hello world!"}
    #         data = json.dumps(data)
    #         sending = await websocket.send(data)
    #         LOG.info(f' sending : {sending} ')
    #         message = await websocket.recv()
    #         LOG.info(f' message : {message} ')
    #         time.sleep(5)

    while True:
        try:
            async with websockets.connect("ws://localhost:8000/v1/member/tweet/live", subprotocols=["live_tweet"],
                                          ping_interval=10, ping_timeout=60 * 60) as ws:
                LOG.info("twitter_custom_tag_run websocket standing ")
                time.sleep(30)
                while True:
                    # try:
                    for i in range(0, 2000):
                        data = {"message": "Hello world!"}
                        data = json.dumps(data)
                        sending = await ws.send(data)
                        LOG.info(f' sending : {sending} ')
                        message = await ws.recv()
                        LOG.info(f' message : {message} ')
                    # if len(sending_list) > 0:
                    #     LOG.info(f'sending_list : {sending_list}')
                    #     i = sending_list.pop()
                    #     LOG.info(f'websocket sending i : {i}')
                    #     result = await ws.send(json.dumps(i))
                    #     LOG.info(f'websocket result : {result}')

        except ConnectionClosed:
            # log something else
            LOG.info("----| ConnectionClosed |----")
            continue

asyncio.run(hello())
