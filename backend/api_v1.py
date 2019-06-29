#!/usr/bin/env python
# encoding: utf-8
'''
@author: Kunchnag Li
@contact: 812487273@qq.com
@file: api_v1.py
@time: 2019/6/27 14:16
@desc:
'''
import os
from flask import Flask, render_template, jsonify, request
from flask_restful import Api, Resource
from flask_cors import *
from DBClass import DbOperate
import Config

app = Flask(__name__)
CORS(app, resources=r'/*')
db = DbOperate()

# 合法的后缀集
ALLOWED_EXTENSIONS_PIC = ['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF']
ALLOWED_EXTENSIONS_VIDEO = ['mp4', 'MP4', 'flv', 'FLV']
ALLOWED_EXTENSIONS_DOC = ['pdf', 'PDF']


@app.route('/apply')
def apply():
    return render_template('apply.html')

@app.route('/apply.pdf')
def apply_pdf():
    html = render_template('apply.html')
    return render_pdf(HTML(string=html))


class FError(Exception):
    pass


class UpPhoto(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            img = request.files.get('img')
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = basedir + "/static/photo/"
            #取后缀，判断是否在范围中
            ext = os.path.splitext(img.filename)[1]
            if ext[1:] not in ALLOWED_EXTENSIONS_PIC:
                raise FError("Error")
            file_name = request.form.get('name')
            file_path = path + file_name
            img.save(file_path)
            res['state'] = "success"
            res['url'] = Config.DOMAIN_NAME + '/static/photo/' + file_name
        except:
            pass
        finally:
            return jsonify(res)


class UpVideo(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            video = request.files.get('video')
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = basedir + "/static/video/"
            ext = os.path.splitext(video.filename)[1]
            if ext[1:] not in ALLOWED_EXTENSIONS_VIDEO:
                raise FError("Error")
            file_name = request.form.get('name')
            file_path = path + file_name
            print(file_path)
            video.save(file_path)
            res['state'] = "success"
            res['url'] = Config.DOMAIN_NAME + '/static/video/' + file_name
        except:
            pass
        finally:
            return jsonify(res)


class UpDoc(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            doc = request.files.get('doc')
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = basedir + "/static/doc/"
            ext = os.path.splitext(doc.filename)[1]
            if ext[1:] not in ALLOWED_EXTENSIONS_DOC:
                raise FError("Error")
            file_name = request.form.get('name')
            file_path = path + file_name
            print(file_path)
            doc.save(file_path)
            res['state'] = "success"
            res['url'] = Config.DOMAIN_NAME + '/static/doc/' + file_name
        except:
            pass
        finally:
            return jsonify(res)


'''
保存项目报名
参数：
    1.作品编码workCode
    2.封面作品名称mainTitle
    3.院系名称department
    4.类别用于封面打钩mainType(取值'type1','type2')
    5.姓名name
    6.学号stuId
    7.出生年月birthday
    8.学历education(取值'A','B','C','D',后续生成pdf再转换)
    9.专业major
    10.入学时间enterTime
    11.作品全称totalTitle
    12.通讯地址address
    13.联系电话phone
    14.邮箱email
    15.申报者情况applier[{
                    'name': 'xxx',
                    'stuId': 'xxx',
                    'education': 'xxx',
                    'phone': 'xxx',
                    'email'： 'xxx'}]
    16.表2作品名称title
    17.表2作品类型type
    18.作品总体情况说明description
    19.创新点creation
    20.关键词keyword
'''
class StoreProject(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            params = {'workCode': data.get('workCode'), 'mainTitle': '', 'department': '',
                      'mainType': '', 'name': '', 'stuId': '', 'birthday': '',
                      'education': '', 'major': '', 'enterTime': '',
                      'totalTitle': '', 'address': '', 'phone': '', 'email': '',
                      'applier': list(), 'title': '', 'type': '', 'description': '',
                      'creation': '', 'keyword': ''}
            if data.get('mainTitle'):
                params['mainTitle'] = data.get('mainTitle')
            if data.get('department'):
                params['department'] = data.get('department')
            if data.get('mainType'):
                params['mainType'] = data.get('mainType')
            if data.get('name'):
                params['name'] = data.get('name')
            if data.get('stuId'):
                params['stuId'] = data.get('stuId')
            if data.get('birthday'):
                params['birthday'] = data.get('birthday')
            if data.get('education'):
                params['education'] = data.get('education')
            if data.get('major'):
                params['major'] = data.get('major')
            if data.get('enterTime'):
                params['enterTime'] = data.get('enterTime')
            if data.get('totalTitle'):
                params['totalTitle'] = data.get('totalTitle')
            if data.get('address'):
                params['address'] = data.get('address')
            if data.get('phone'):
                params['phone'] = data.get('phone')
            if data.get('email'):
                params['email'] = data.get('email')
            if data.get('applier'):
                params['applier'] = data.get('applier')
            if data.get('title'):
                params['title'] = data.get('title')
            if data.get('type'):
                params['type'] = data.get('type')
            if data.get('description'):
                params['description'] = data.get('description')
            if data.get('creation'):
                params['creation'] = data.get('creation')
            if data.get('keyword'):
                params['keyword'] = data.get('keyword')
            res = db.store_project(params)
        except:
            pass
        finally:
            return jsonify(res)


'''
新增项目报名
参数：
    1.竞赛编号competition_id
    2.学号stu_id 
'''
class AddProject(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            competition_id = data.get('competition_id')
            email = data.get('email')
            res = db.add_project(competition_id, email)
        except:
            pass
        finally:
            return jsonify(res)

'''
查看报名表
参数：
    项目编号project_id
'''
class ViewApply(Resource):
    def get(self):
        res = {"state": "fail"}
        try:
            data = request.args
            project_id = data.get('project_id')
            res = db.view_apply(project_id)
        except:
            pass
        finally:
            return jsonify(res)


# 添加api资源
api = Api(app)
api.add_resource(UpPhoto, "/api/v1/up_photo", endpoint="upPhoto")
api.add_resource(UpVideo, "/api/v1/up_video", endpoint="upVideo")
api.add_resource(UpDoc, "/api/v1/up_doc", endpoint="upDoc")
api.add_resource(StoreProject, "/api/v1/store_project", endpoint="storeProject")
api.add_resource(AddProject, "/api/v1/add_project", endpoint="addProject")
api.add_resource(ViewApply, "/api/v1/view_apply", endpoint="viewApply")

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
