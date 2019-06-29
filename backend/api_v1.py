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
from utils import encode

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


# 自定义异常——出现错误时抛出
class FError(Exception):
    pass


# 上传照片
class UpPhoto(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            img = request.files.get('file')
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = basedir + "/static/photo/"
            project_code = request.form.get('project_code')
            # 取后缀，判断是否在范围中
            ext = os.path.splitext(img.filename)[1]
            if ext[1:] not in ALLOWED_EXTENSIONS_PIC:
                res['content'] = 'File''s type is not allowed'
                raise FError("Error")
            file_name = img.filename
            file_path = path + file_name
            img.save(file_path)
            db_res = db.insert_attachment(project_code,'photo',file_path)
            if db_res.get('state') == 'fail':
                res['content'] = db_res.get('reason')
                raise FError("Error")
            res['state'] = "success"
            res['url'] = Config.DOMAIN_NAME + '/static/photo/' + file_name
        except:
            pass
        finally:
            return jsonify(res)


# 上传视频
class UpVideo(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            video = request.files.get('file')
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = basedir + "/static/video/"
            project_code = request.form.get('project_code')
            ext = os.path.splitext(video.filename)[1]
            if ext[1:] not in ALLOWED_EXTENSIONS_VIDEO:
                res['content'] = 'File''s type is not allowed'
                raise FError("Error")
            file_name = video.filename
            file_path = path + file_name
            video.save(file_path)
            db_res = db.insert_attachment(project_code, 'video', file_path)
            if db_res.get('state') == 'fail':
                res['content'] = db_res.get('reason')
                raise FError("Error")
            res['state'] = "success"
            res['url'] = Config.DOMAIN_NAME + '/static/video/' + file_name
        except:
            pass
        finally:
            return jsonify(res)


# 上传文档
class UpDoc(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            doc = request.files.get('file')
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = basedir + "/static/doc/"
            project_code = request.form.get('project_code')
            ext = os.path.splitext(doc.filename)[1]
            if ext[1:] not in ALLOWED_EXTENSIONS_DOC:
                res['content'] = 'File''s type is not allowed'
                raise FError("Error")
            file_name = doc.filename
            file_path = path + file_name
            doc.save(file_path)
            db_res = db.insert_attachment(project_code, 'video', file_path)
            if db_res.get('state') == 'fail':
                res['content'] = db_res.get('reason')
                raise FError("Error")
            res['state'] = "success"
            res['url'] = Config.DOMAIN_NAME + '/static/doc/' + file_name
        except:
            pass
        finally:
            return jsonify(res)


# 删除附件
class DeleteFile(Resource):
    def get(self):
        res = {"state": "fail"}
        try:
            data = request.form
            file_type = data.get('type')  # video/ doc/ photo
            file_name = data.get('file_name')
            project_code = data.get('project_code')
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = basedir + "/static/" + file_type + "/"
            file_path = path + file_name
            if not os.path.exists(file_path):
                res['content'] = 'The file does not exists'
                raise FError("Error")
            os.remove(file_path)
            db_res = db.delete_attachment(project_code, file_type, file_path)
            if db_res.get('state') == 'fail':
                res['reason'] = db_res.get('reason')
                raise FError("Error")
            res['state'] = 'success'
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
    8.学历education(取值'A','B','C','D', 代码里转换)
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
    17.表2作品类型type(取值'A','B','C','D','E','F', 代码里转换)
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


#######################################################################################################################
"""
登录
"""
class Login(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            password = data.get('password')
            password = encode(password)
            mail = data.get('mail')
            role = data.get('role')
            res = {"state": "fail"}
            res = db.compare_password(password, mail, role)
        except:
            pass
        finally:
            return jsonify(res)


"""
注册学生
"""
class RegisterStudent(Resource):  # 注册请求
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            password = data.get('password')
            password = encode(password)
            mail = data.get('mail')
            username = data.get('username')
            ID = data.get('ID')
            department = data.get('department')
            field = data.get('field')
            admission_year = data.get('admission_year')
            phone = data.get('phone')
            res = db.create_user_student(mail, username, password, ID, department, field, admission_year, phone)
        except:
            pass
        finally:
            return jsonify(res)

"""
注册专家
"""
class RegisterExpert(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            mail = data.get('mail')
            username = data.get('username')
            res = db.create_user_expert(mail, username)
        except:
            pass
        finally:
            return jsonify(res)

##############################################################################################################
'''
初审改变作品状态
    proj_id：项目id（字符串）   result：初审结果（字符串 'True' 'False'）
'''
class FirstTrialChange(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            proj_id = data.get('proj_id')
            result = data.get('result')
            res = db.first_trial_change(proj_id, result)
        except:
            pass
        finally:
            return jsonify(res)

'''
获取提交表数据
    proj_id：项目id（字符串）
'''
class GetTableInfo(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            proj_id = data.get('proj_id')
            res = db.get_table_info(proj_id)
        except:
            pass
        finally:
            return jsonify(res)

################################################################################################################

# 添加api资源
api = Api(app)
api.add_resource(UpPhoto, "/api/v1/up_photo", endpoint="upPhoto")
api.add_resource(UpVideo, "/api/v1/up_video", endpoint="upVideo")
api.add_resource(UpDoc, "/api/v1/up_doc", endpoint="upDoc")
api.add_resource(StoreProject, "/api/v1/store_project", endpoint="storeProject")
api.add_resource(AddProject, "/api/v1/add_project", endpoint="addProject")
api.add_resource(ViewApply, "/api/v1/view_apply", endpoint="viewApply")
api.add_resource(DeleteFile, "/api/v1/delete_file", endpoint="deleteFile")
api.add_resource(FirstTrialChange, "/api/vi/first_trial_change", endpoint="firstTrialChange")
api.add_resource(GetTableInfo, "/api/vi/get_table_info", endpoint="getTableInfo")
api.add_resource(Login, '/api/v1/login', endpoint='login')
api.add_resource(RegisterExpert, '/api/v1/registerexpert', endpoint='registerexpert')
api.add_resource(RegisterStudent, '/api/v1/registerstudent', endpoint='registerstudent')

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
