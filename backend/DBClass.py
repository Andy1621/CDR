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
from utils import replace_apply_html, html2pdf
import Config


class DbOperate:
    '''
    连接数据库和ES
    '''
    def __init__(self):
        self.host = Config.HOST
        self.port = Config.PORT_DB
        self.client = MongoClient(self.host, self.port)

    '''
    取得Business数据库的指定表
    66666:Good looking laptop. Good feeling. Good touching.
    '''
    def getCol(self, name):
        db = self.client[Config.DATABASE]
        col = db[name]
        return col

    '''
    保存申报信息
    '''
    def store_project(self, params):
        res = {'state': 'fail', 'reason': "信息字段出错"}
        try:
            project_code = params['workCode']
            apply = self.getCol('project').find_one({'project_code': project_code})
            if apply:
                apply['form'] = params
                self.getCol('project').update_one({'project_code': 'project_code'}, {'$set': apply})
                res['state'] = 'success'
            else:
                res['reason'] = "申请编号不存在"
        except:
            pass
        finally:
            return res

    '''
    新增项目报名
    '''
    def add_project(self, competition_id, email):
        res = {'state': 'fail', 'reason': "未知错误"}
        try:
            competition = self.getCol('competition').find_one({'_id': competition_id})
            if competition:
                result = self.getCol('project').insert({'email': email,
                                                        'competition_id': competition_id,
                                                        'status': 'editing'})
                res['state'] = 'success'
                res['project_id'] = str(result.inserted_id)
            else:
                res['reason'] = "竞赛不存在"
        except:
            pass
        finally:
            return res

    '''
    查看申请表
    '''
    def view_apply(self, project_id):
        res = {'state': 'fail', 'reason': "未知错误"}
        try:
            form = self.getCol('project').find_one({'_id': project_id})
            if form:
                html = replace_apply_html(form)
                filename = form['workCode'] + ".pdf"
                html2pdf(html, filename)
                pdf_url = Config.DOMAIN_NAME + "/static/export_pdf/" + filename
                res['state'] = 'success'
                res['pdf_url'] = pdf_url
            else:
                res['reason'] = "竞赛不存在"
        except:
            pass
        finally:
            return res


if __name__ == '__main__':
    pass
