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
        16.
'''
class Store(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
        except:
            pass




















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

# 添加api资源
api = Api(app)
api.add_resource(UpPhoto, "/api/v1/up_photo", endpoint="upPhoto")
api.add_resource(UpVideo, "/api/v1/up_video", endpoint="upVideo")
api.add_resource(UpDoc, "/api/v1/up_doc", endpoint="upDoc")
api.add_resource(Store, "/api/v1/store", endpoint="store")

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
