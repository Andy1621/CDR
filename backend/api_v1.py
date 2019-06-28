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
import Config

app = Flask(__name__)
CORS(app, resources=r'/*')

#合法的后缀集
ALLOWED_EXTENSIONS_PIC = ['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF']
ALLOWED_EXTENSIONS_VIDEO = ['mp4', 'MP4','flv','FLV']
ALLOWED_EXTENSIONS_DOC = ['pdf','PDF']


@app.route('/apply')
def homework1():
    return render_template('apply.html')

# @app.route('/upload',methods=['post','get'])
# def up_photo():
#


class FError(Exception):
    pass


class User(Resource):
    def get(self):
        s = ['User', 'Andy']
        t = dict()
        t['data'] = s
        return jsonify(t)


class Greeting(Resource):  # 路由带参数
    def get(self, hello_name=None, goodbye_name=None):
        res = {"state": "fail"}
        try:
            if hello_name:
                res['state'] = 'success'
                res['content'] = 'Hello! ' + hello_name
            elif goodbye_name:
                res['state'] = 'success'
                res['content'] = 'Goodbye! ' + goodbye_name
        except:
            res['content'] = "It seems that you didn't input right parameter"
        finally:
            return jsonify(res)


class Up_photo(Resource):
    def post(self):
        res = {"state" : "fail"}
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
            return dumps(res,ensure_ascii=False)
        except:
            return dumps(res,ensure_ascii=False)


class Up_video(Resource):
    def post(self):
        res = {"state" : "fail"}
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
            return dumps(res,ensure_ascii=False)
        except:
            return dumps(res,ensure_ascii=False)


class Up_doc(Resource):
    def post(self):
        res = {"state" : "fail"}
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
            return dumps(res,ensure_ascii=False)
        except:
            return dumps(res,ensure_ascii=False)


# 添加api资源
api = Api(app)
api.add_resource(User, "/api/v1/user", endpoint="user")
api.add_resource(Greeting, "/api/v1/hello/<string:hello_name>", endpoint="hello")
api.add_resource(Greeting, "/api/v1/goodbye/<string:goodbye_name>", endpoint="goodbye")
api.add_resource(Up_photo,"/api/v1/up_photo",endpoint="up_photo")
api.add_resource(Up_video,"/api/v1/up_video",endpoint="up_video")
api.add_resource(Up_doc,"/api/v1/up_doc",endpoint="up_doc")

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)