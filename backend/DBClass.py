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
from . import Config


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

    '''
    保存申报信息
    '''
    def storeInfomation(self):
        pass


    '''
    检查邮箱是否已注册
    '''
    def check_mail(self, mail):
        user_list = self.getCol("user")
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            test = user_list.find_one({'mail': mail})
            # 邮箱已被注册
            if test:
                res['reason'] = '邮箱已被注册'
            else:
                res['reason'] = ""
                res['state'] = 'success'
            return res
        except:
            return res

    '''
    注册学生用户
    '''
    def create_user_student(self, mail, username, password, ID, department, field, admission_year, phone):
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            check = self.check_mail(mail)
            if check['state'] == 'false':
                res['reason'] = check['reason']
                return res
            new_student = {'username': username,
                           'mail': mail,
                           'password': password,
                           'user_type': 'user',
                           'ID': ID,
                           'department': department,
                           'field': field,
                           'admission_year': admission_year,
                           'phone': phone
                           }
            user_list = self.getCol("user")
            user_list.insert_one(new_student)
            res['state'] = 'success'
            return res
        except:
            return res

    '''
    注册专家用户
    '''
    def create_user_expert(self, mail, username):
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            check = self.check_mail(mail)
            if check['state'] == 'false':
                res['reason'] = check['reason']
                return res
            new_expert = {'username': username,
                           'mail': mail,
                           'password': "",
                           'user_type': 'expert',
                           }
            user_list = self.getCol("user")
            user_list.insert_one(new_expert)
            res['state'] = 'success'
            return res
        except:
            return res

    '''
    用户登录
    '''
    def compare_password(self, password, mail):
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            find_user = self.getCol('user').find_one({'mail': mail})
            # 搜索到唯一用户
            if find_user:
                real_psw = find_user['password']
                if real_psw == "" and find_user['user_type'] == 'expert':
                    res['reason'] = '该专家尚未设置密码!'
                elif real_psw == password:
                    res['state'] = 'success'
                else:
                    res['reason'] = '密码错误'
            # 用户不存在
            else:
                res['reason'] = '用户不存在'
            return res
        except:
            return res

    '''
    用户登录
    '''
    def compare_password(self, password, mail):
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            find_user = self.getCol('user').find_one({'mail': mail})
            # 搜索到唯一用户
            if find_user:
                real_psw = find_user['password']
                if real_psw == "" and find_user['user_type'] == 'expert':
                    res['reason'] = '该专家尚未设置密码!'
                elif real_psw == password:
                    res['state'] = 'success'
                else:
                    res['reason'] = '密码错误'
            # 用户不存在
            else:
                res['reason'] = '用户不存在'
            return res
        except:
            return res