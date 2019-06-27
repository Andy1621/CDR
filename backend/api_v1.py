#!/usr/bin/env python
# encoding: utf-8
'''
@author: Kunchnag Li
@contact: 812487273@qq.com
@file: api_v1.py
@time: 2019/6/27 14:16
@desc:
'''

from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_cors import *

app = Flask(__name__)
CORS(app, resources=r'/*')


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


# 添加api资源
api = Api(app)
api.add_resource(User, "/api/v1/user", endpoint="user")
api.add_resource(Greeting, "/api/v1/hello/<string:hello_name>", endpoint="hello")
api.add_resource(Greeting, "/api/v1/goodbye/<string:goodbye_name>", endpoint="goodbye")

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
