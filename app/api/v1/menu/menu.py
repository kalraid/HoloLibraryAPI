# -*- coding: utf-8 -*-
import falcon

import log
from app.api.common import BaseResource

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict

from app.api.v1.static.thread.analysis import AnalysisSubscribeThread

LOG = log.get_logger()

FIELDS = {
}


class Menu(BaseResource):
    """
    Handle for endpoint: /v1/menu
    """
    ## this list is menu name list
    def on_get(self, req, res):
        data = [
            {
                'menu_name': '테이블',
                'menu_id': 'M1109',
                'role': 'admin'
            },
            {
                'menu_name': '테이블2',
                'menu_id': 'M1108',
                'role': 'admin'
            },
            {
                'menu_name': '테이블3',
                'menu_id': 'M1107',
                'role': 'admin'
            },
            {
                'menu_name': 'Data-Table',
                'menu_id': 'M1110',
                'role': 'admin'
            },
            {
                'menu_name': 'Ag-Grid',
                'menu_id': 'M1111',
                'role': 'admin'
            },
            {
                'menu_name': '폼',
                'menu_id': 'M1112',
                'role': 'admin'
            },
            {
                'menu_name': 'CloudPc',
                'menu_id': 'M1113',
                'role': 'admin'
            },
            {
                'menu_name': 'CloudPc',
                'menu_id': 'M1114',
                'role': 'admin'
            },
            {
                'menu_name': 'CloudPc',
                'menu_id': 'M1115',
                'role': 'admin'
            },
            {
                'menu_name': 'CloudPc',
                'menu_id': 'M1101',
                'role': 'admin'
            },
            {
                'menu_name': 'CloudPc',
                'menu_id': 'M1101',
                'role': 'user'
            },
            {
                'menu_name': '홀로라이브 정보 모아보기',
                'menu_id': 'M20100',
                'role': 'user'
            },
            {
                'menu_name': '멤버 목록',
                'menu_id': 'M20101',
                'role': 'user'
            },
            {
                'menu_name': '멤버 유투브 커뮤니티',
                'menu_id': 'M20102',
                'role': 'user'
            },
            {
                'menu_name': '멤버 트위터',
                'menu_id': 'M20103',
                'role': 'user'
            },
            {
                'menu_name': '라이브러리',
                'menu_id': 'M20200',
                'role': 'user'
            },
            {
                'menu_name': '영상 히스토리',
                'menu_id': 'M20201',
                'role': 'user'
            },
            {
                'menu_name': '밈 정리소',
                'menu_id': 'M20202',
                'role': 'user'
            },
            {
                'menu_name': '트위터 보관소',
                'menu_id': 'M20203',
                'role': 'user'
            },
            {
                'menu_name': '키리누키 명함판',
                'menu_id': 'M20204',
                'role': 'user'
            },

        ]

        response = {'data': data}
        res.status = falcon.HTTP_200
        res.body = self.to_json(response)
