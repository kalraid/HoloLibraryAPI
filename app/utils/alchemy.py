# -*- coding: utf-8 -*-

import datetime
import json
import time

from sqlalchemy.ext.declarative import DeclarativeMeta


def new_alchemy_encoder():
    # http://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                for field in [
                    x for x in dir(obj) if not x.startswith("_") and x != "metadata"
                ]:
                    fields[field] = obj.__getattribute__(field)
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder


def passby(data):
    return data


def datetime_to_timestamp(date):
    if isinstance(date, datetime.date):
        return int(time.mktime(date.timetuple()))
    else:
        return None

def db_result_to_dict_list(data):
    list = []
    if type(data) == type(list):
        for i in data:  # convert list[objects] to list[dict]
            temp = i.to_dict()
            list.append(temp)
    else:
        if data is not None:
            list.append(data.to_dict())

    return list