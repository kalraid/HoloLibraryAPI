# -*- coding: utf-8 -*-
import threading
import time

import requests
from dateutil.parser import parse
from sqlalchemy.exc import SQLAlchemyError

import log
from app.errors import DatabaseError, ERR_DATABASE_ROLLBACK
from app.model.holo_member_ch import HoloMemberCh
from app.model.user_static_youbute import UserStaticYoutube

from app.batch.Thread.Run.twitter_tag_run import twitter_tag_run

LOG = log.get_logger()


class TwitterTagThreading(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        twitter_tag_run()