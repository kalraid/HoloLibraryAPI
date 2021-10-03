# -*- coding: utf-8 -*-

from sqlalchemy import Column, Table, PrimaryKeyConstraint, DateTime, func, String, Integer
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declarative_base, declared_attr

import log
from app.utils import alchemy

LOG = log.get_logger()


@as_declarative()
class BaseModel(object):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    index = Column(Integer, unique=True, autoincrement=True)
    isUse = Column(String(1), default='Y', nullable=False)
    isDelete = Column(String(1), default='N', nullable=False)
    created = Column(DateTime, default=func.now())
    modified = Column(DateTime, default=func.now(), onupdate=func.now())

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def __table_cls__(cls, *arg, **kw):
        for obj in arg[1:]:
            if (isinstance(obj, Column) and obj.primary_key) or isinstance(
                obj, PrimaryKeyConstraint
            ):
                return Table(*arg, **kw)

        return None

    @classmethod
    def find_one(cls, session, id):
        return session.query(cls).filter(cls.get_id() == id).one()

    @classmethod
    def find_update(cls, session, id, args):
        return (
            session.query(cls)
            .filter(cls.get_id() == id)
            .update(args, synchronize_session=False)
        )

    @classmethod
    def get_id(cls):
        pass

    def to_dict(self):
        intersection = set(self.__table__.columns.keys()) & set(self.FIELDS)
        return dict(
            map(
                lambda key: (
                    key,
                    (lambda value: self.FIELDS[key](value) if value else None)(
                        getattr(self, key)
                    ),
                ),
                intersection,
            )
        )

    FIELDS = {
        "isUse": str,
        "isDelete": str,
        "created": alchemy.datetime_to_timestamp,
        "modified": alchemy.datetime_to_timestamp,

    }

Base = declarative_base(cls=BaseModel)