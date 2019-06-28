#!/usr/bin/env python
# encoding: utf-8
'''
@author: Kunchnag Li
@contact: 812487273@qq.com
@file: DBClass.py
@time: 2019/6/28 14:45
@desc:
'''

from pymongo import MongoClient
from elasticsearch import Elasticsearch
import Config


class DbOperate:
    '''
    连接数据库和ES
    '''
    def __init__(self):
        self.host = Config.HOST
        self.port = Config.PORT_DB
        self.client = MongoClient(self.host, self.port)
        self.es = Elasticsearch([{u'host': Config.HOST, u'port': Config.PORT_ES}], timeout=3600)

    '''
    取得Business数据库的指定表
    '''
    def getCol(self, name):
        db = self.client[Config.DATABASE]
        col = db[name]
        return col
