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
import shutil
import time

from flask import Flask, render_template, jsonify, request
from flask_restful import Api, Resource
from flask_cors import *
from json import dumps
from backend.encrypt import encode
from backend import Config
from backend.DBClass import DbOperate

app = Flask(__name__)
CORS(app, resources=r'/*')
db = DbOperate()
# 合法的后缀集
ALLOWED_EXTENSIONS_PIC = ['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF']
ALLOWED_EXTENSIONS_VIDEO = ['mp4', 'MP4', 'flv', 'FLV']
ALLOWED_EXTENSIONS_DOC = ['pdf', 'PDF']


@app.route('/apply')
def homework1():
    return render_template('apply.html')


class FError(Exception):
    pass


class UpPhoto(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            img = request.files.get('img')
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = basedir + "/static/photo/"
            # 取后缀，判断是否在范围中
            ext = os.path.splitext(img.filename)[1]
            if ext[1:] not in ALLOWED_EXTENSIONS_PIC:
                res['content'] = 'File''s type is not allowed'
                raise FError("Error")
            file_name = img.filename
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
            video = request.files.get('file')
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = basedir + "/static/video/"
            ext = os.path.splitext(video.filename)[1]
            if ext[1:] not in ALLOWED_EXTENSIONS_VIDEO:
                res['content'] = 'File''s type is not allowed'
                raise FError("Error")
            file_name = video.filename
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
            doc = request.files.get('file')
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = basedir + "/static/doc/"
            ext = os.path.splitext(doc.filename)[1]
            if ext[1:] not in ALLOWED_EXTENSIONS_DOC:
                res['content'] = 'File''s type is not allowed'
                raise FError("Error")
            file_name = doc.filename
            file_path = path + file_name
            print(file_path)
            doc.save(file_path)
            res['state'] = "success"
            res['url'] = Config.DOMAIN_NAME + '/static/doc/' + file_name
        except:
            pass
        finally:
            return jsonify(res)


class DeleteFile(Resource):
    def get(self):
        res = {"state": "fail"}
        try:
            data = request.form
            file_type = data.get('type')  # video/ doc/ photo
            file_name = data.get('file_name')
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = basedir + "/static/" + file_type + "/"
            file_path = path + file_name
            if not os.path.exists(file_path):
                res['content'] = 'The file does not exists'
                raise FError("Error")
            os.remove(file_path)
            res['state'] = 'success'
        except:
            pass
        finally:
            return jsonify(res)


'''
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
class Store(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            workCOde = data.get('workCode')
            mainTitle = ''
            if data.get('mainTitle'):
                mainTitle = data.get('mainTitle')
            department = ''
            if data.get('department'):
                department = data.get('department')
            mainType = ''
            if data.get('mainType'):
                mainType = data.get('mainType')
            name = ''
            if data.get('name'):
                name = data.get('name')
            stuId = ''
            if data.get('stuId'):
                stuId = data.get('stuId')
            birthday = ''
            if data.get('birthday'):
                birthday = data.get('birthday')
            education = ''
            if data.get('education'):
                education = data.get('education')
            major = ''
            if data.get('major'):
                major = data.get('major')
            enterTime = ''
            if data.get('enterTime'):
                enterTime = data.get('enterTime')
            totalTitle = ''
            if data.get('totalTitle'):
                totalTitle = data.get('totalTitle')
            address = ''
            if data.get('address'):
                address = data.get('address')
            phone = ''
            if data.get('phone'):
                phone = data.get('phone')
            email = ''
            if data.get('email'):
                email = data.get('email')
            applier = list()
            if data.get('applier'):
                applier = data.get('applier')
            title = ''
            if data.get('title'):
                title = data.get('title')
            type = ''
            if data.get('type'):
                type = data.get('type')
            description = ''
            if data.get('description'):
                description = data.get('description')
            creation = ''
            if data.get('creation'):
                creation = data.get('creation')
            keyword = ''
            if data.get('keyword'):
                keyword = data.get('keyword')
        except:
            pass
        finally:
            return jsonify(res)


#######################################################################################################################
"""
登录
"""
class Login(Resource):
    def post(self):
        data = request.get_json()
        password = data.get('password')
        password = encode(password)
        username = data.get('username')
        res = {"state": "fail"}
        try:
            res = db.compare_password(password, username)
            return dumps(res, ensure_ascii=False)
        except:
            return dumps(res, ensure_ascii=False)



"""
注册
"""
class Register(Resource):  # 注册请求
    def post(self):
        data = request.get_json()
        password = data.get('password')
        password = encode(password)
        email = data.get('email')
        username = data.get('username')
        email_code = data.get('email_code')
        res = db.create_user(password, email, username, email_code)
        return dumps(res, ensure_ascii=False)

##############################################################################################################3

# 添加api资源
api = Api(app)
api.add_resource(UpPhoto, "/api/v1/up_photo", endpoint="upPhoto")
api.add_resource(UpVideo, "/api/v1/up_video", endpoint="upVideo")
api.add_resource(UpDoc, "/api/v1/up_doc", endpoint="upDoc")
api.add_resource(Store, "/api/v1/store", endpoint="store")
api.add_resource(DeleteFile, "/api/v1/delete_file", endpoint="deleteFile")


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
