#!/usr/bin/env python3
# encoding: utf-8
'''
@author: Kunchnag Li
@contact: 812487273@qq.com
@file: api_v1.py
@time: 2019/6/27 14:16
@desc:
'''
import os

import xlrd
from flask import Flask, render_template, jsonify, request
from flask_restful import Api, Resource
from flask_cors import *
from DBClass import DbOperate
import Config
from utils import encode, make_zip
import time
import threading
import datetime

app = Flask(__name__)
CORS(app, resources=r'/*')
db = DbOperate()

# 合法的后缀集
ALLOWED_EXTENSIONS_PIC = ['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF']
ALLOWED_EXTENSIONS_VIDEO = ['mp4', 'MP4', 'flv', 'FLV']
ALLOWED_EXTENSIONS_DOC = ['pdf', 'PDF']


# 自定义异常——出现错误时抛出
class FError(Exception):
    pass


# 上传附件
class UpFile(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            file = request.files.get('file')
            file_type = request.form.get('file_type')
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = basedir + '/static/' + file_type + '/'
            project_code = request.form.get('project_code')
            # 取后缀，判断是否在范围中
            ext = os.path.splitext(file.filename)[1]
            if file_type == 'photo':
                if ext[1:] not in ALLOWED_EXTENSIONS_PIC:
                    res['reason'] = 'File''s type is not allowed'
                    raise FError("Error")
            elif file_type == 'video':
                if ext[1:] not in ALLOWED_EXTENSIONS_VIDEO:
                    res['reason'] = 'File''s type is not allowed'
                    raise FError("Error")
            elif file_type == 'doc':
                if ext[1:] not in ALLOWED_EXTENSIONS_DOC:
                    res['reason'] = 'File''s type is not allowed'
                    raise FError("Error")
            file_name = project_code + '_' + file.filename
            file_path = path + file_name
            file.save(file_path)
            db_res = db.insert_attachment(project_code, file_type, file_path)
            if db_res.get('state') == 'fail':
                res['reason'] = db_res.get('reason')
                raise FError("Error")
            res['state'] = "success"
            res['url'] = Config.DOMAIN_NAME + '/static/' + file_type + '/' + file_name
            res['file_name'] = file.filename
        except:
            pass
        finally:
            return jsonify(res)


# 删除附件
class DeleteFile(Resource):
    def get(self):
        res = {"state": "fail"}
        try:
            data = request.args
            file_type = data.get('type')  # video/ doc/ photo
            file_name = data.get('file_name')
            project_code = data.get('project_code')
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = basedir + "/static/" + file_type + "/"
            file_path = path + project_code + '_' + file_name
            if not os.path.exists(file_path):
                res['reason'] = 'The file does not exists'
                raise FError("Error")
            os.remove(file_path)
            db_res = db.delete_attachment(project_code, file_path)
            if db_res.get('state') == 'fail':
                res['reason'] = db_res.get('reason')
                raise FError("Error")
            res['state'] = 'success'
        except:
            pass
        finally:
            return jsonify(res)


# 上传公告附件
class UpAnnounceFile(Resource):
    def post(self):
        res = {"state": "fail", 'reason': '网络错误或未知原因'}
        try:
            file = request.files.get('file')
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = basedir + '/static/announce_file/'
            timestamp = int(round(time.time()))
            # 存文件到文件夹
            file_name = str(timestamp) + '_' + file.filename
            file_path = path + file_name
            file.save(file_path)
            res['state'] = "success"
            res['url'] = Config.DOMAIN_NAME + '/static/announce_file/' + file_name
            res['file_name'] = file.filename
        except:
            pass
        finally:
            return jsonify(res)


# 删除附件
class DeleteAnnounceFile(Resource):
    def post(self):
        res = {"state": "fail", 'reason': '网络错误或未知原因'}
        try:
            data = request.get_json()
            file_path = data.get('file_path')
            basedir = os.path.abspath(os.path.dirname(__file__))
            path = basedir + "/static/announce_file/"
            file_path = path + file_path.split('/')[-1]
            if not os.path.exists(file_path):
                res['reason'] = 'The file does not exists'
                raise FError("Error")
            os.remove(file_path)
            res['state'] = 'success'
        except:
            pass
        finally:
            return jsonify(res)


# 打包下载附件
class DownloadFiles(Resource):
    def get(self):
        res = {"state": "fail"}
        try:
            project_code = request.args.get('project_code')
            basedir = os.path.abspath(os.path.dirname(__file__))
            out_filename = basedir + '/static/zip/' + project_code + '.zip'
            db_res = db.require_attachments(project_code)
            if db_res['state'] == 'fail':
                res['reason'] = db_res['reason']
                raise FError
            source_list = db_res['project_files']
            make_zip(source_list,out_filename)
            res['state'] = 'Success'
            res['url'] = Config.DOMAIN_NAME + '/static/zip/' + project_code + '.zip'
        except:
            res['reason'] = '可能是打包错误，查看本地是否有数据库中的数据'
            # this is a test for keyboard. Well, not bad. I must admit that, this is better than mine.
        finally:
            return jsonify(res)


# 获取专家评审项目信息
class GetExpertReviewList(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            expert_email = data.get('email')
            db_res = db.expert_review_list(expert_email)
            res['project_lists'] = db_res['project_lists']
            res['state'] = 'Success'
        except:
            pass
        finally:
            return jsonify(res)
################################################################################################

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
    21.作品可展示形式display
    22.作品调查方式investigation
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
                      'creation': '', 'keyword': '', 'display': list(), 'investigation': list()}
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
            if data.get('display'):
                params['display'] = data.get('display')
            if data.get('investigation'):
                params['investigation'] = data.get('investigation')
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
            db = DbOperate()
            db.update_com_status(competition_id)
            email = data.get('email')
            name = data.get('name')
            res = db.add_project(competition_id, email, name)
        except:
            pass
        finally:
            return jsonify(res)

'''
获取项目信息
参数：
    项目编号project_code
'''
class GetProjectDetail(Resource):
    def get(self):
        res = {"state": "fail"}
        try:
            data = request.args
            project_code = data.get('project_code')
            res = db.get_project_detail(project_code)
        except:
            pass
        finally:
            return jsonify(res)


'''
查看报名表
参数：
    项目编号project_code
'''
class ViewApply(Resource):
    def get(self):
        res = {"state": "fail"}
        try:
            data = request.args
            project_code = data.get('project_code')
            res = db.view_apply(project_code)
        except:
            pass
        finally:
            return jsonify(res)


'''
删除项目报名
参数：
    项目编号project_code
'''
class DeleteProject(Resource):
    def get(self):
        res = {"state": "fail"}
        try:
            data = request.args
            project_code = data.get('project_code')
            res = db.delete_project(project_code)
        except:
            pass
        finally:
            return jsonify(res)


'''
提交项目报名
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
    21.作品可展示形式display
    22.作品调查方式investigation
'''
class SubmitProject(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            params = {'workCode': data.get('workCode'), 'mainTitle': '', 'department': '',
                      'mainType': '', 'name': '', 'stuId': '', 'birthday': '',
                      'education': '', 'major': '', 'enterTime': '',
                      'totalTitle': '', 'address': '', 'phone': '', 'email': '',
                      'applier': list(), 'title': '', 'type': '', 'description': '',
                      'creation': '', 'keyword': '', 'display': list(), 'investigation': list()}
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
            if data.get('display'):
                params['display'] = data.get('display')
            if data.get('investigation'):
                params['investigation'] = data.get('investigation')
            res = db.submit_project(params)
        except:
            pass
        finally:
            return jsonify(res)


'''
获取项目列表
参数：
    学生邮箱author_email
'''
class GetProjectList(Resource):
    def get(self):
        res = {"state": "fail"}
        try:
            data = request.args
            author_email = data.get('author_email')
            res = db.get_project_list(author_email)
        except:
            pass
        finally:
            return jsonify(res)


'''
获取评审意见
参数：
    项目编号project_code
    专家邮箱expert_email
'''
class GetReview(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            project_code = data.get('project_code')
            expert_email = data.get('expert_email')
            res = db.get_review(project_code, expert_email)
        except:
            pass
        finally:
            return jsonify(res)

'''
保存评审意见
参数：
    项目编号project_code
    专家邮箱expert_email
    专家评分score
    评审意见suggestion
'''
class StoreReview(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            project_code = data.get('project_code')
            expert_email = data.get('expert_email')
            score = ''
            if data.get('score'):
                score = data.get('score')
            suggestion = ''
            if data.get('suggestion'):
                suggestion = data.get('suggestion')
            res = db.store_review(project_code, expert_email, score, suggestion)
        except:
            pass
        finally:
            return jsonify(res)

'''
提交评审意见
参数：
    项目编号project_code
    专家邮箱expert_email
    专家评分score
    评审意见suggestion
'''
class SubmitReview(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            project_code = data.get('project_code')
            expert_email = data.get('expert_email')
            score = data.get('score')
            suggestion = data.get('suggestion')
            res = db.submit_review(project_code, expert_email, score, suggestion)
        except:
            pass
        finally:
            return jsonify(res)


'''
接受评审
参数：
    项目编号project_code
    专家邮箱expert_email  
'''
class AcceptReview(Resource):
    def get(self):
        res = {"state": "fail"}
        try:
            data = request.args
            project_code = data.get('project_code')
            expert_email = data.get('expert_email')
            res = db.accept_review(project_code, expert_email)
        except:
            pass
        finally:
            return jsonify(res)


'''
（AOE）接受评审
参数：
    项目编号project_code
    专家邮箱expert_email  
'''
class MultiAcceptReview(Resource):
    def get(self):
        res = {"state": "fail", 'cnt': 0}
        try:
            data = request.args
            project_code = data.get('project_code')
            expert_email = data.get('expert_email')
            project_list = project_code.strip().split("|")
            project_codes = list()
            for pc in project_list:
                if pc == "":
                    continue
                else:
                    project_codes.append(pc)
                res0 = db.multi_accept_review(project_codes, expert_email)
                res['cnt'] += res0['cnt']
            if res['cnt'] > 0:
                res['state'] = 'success'
        except:
            pass
        finally:
            return jsonify(res)


'''
拒绝评审
参数：
    项目编号project_code
    专家邮箱expert_email  
'''
class RefuseReview(Resource):
    def get(self):
        res = {"state": "fail"}
        try:
            data = request.args
            project_code = data.get('project_code')
            expert_email = data.get('expert_email')
            res = db.refuse_review(project_code, expert_email)
        except:
            pass
        finally:
            return jsonify(res)


'''
（AOE）拒绝评审
参数：
    项目编号project_code
    专家邮箱expert_email  
'''
class MultiRefuseReview(Resource):
    def get(self):
        res = {"state": "fail"}
        try:
            data = request.args
            project_code = data.get('project_code')
            expert_email = data.get('expert_email')
            project_list = project_code.strip().split("|")
            project_codes = list()
            for pc in project_list:
                if pc == "":
                    continue
                else:
                    project_codes.append(pc)
                res0 = db.multi_refuse_review(project_codes, expert_email)
                res['cnt'] += res0['cnt']
            if res['cnt'] > 0:
                res['state'] = 'success'
        except:
            pass
        finally:
            return jsonify(res)


'''
新增公告
参数：
    1.题目title
    2.时间time
    3.内容content
    4.附件files
'''
class AddNews(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            title = data.get('title')
            time = data.get('time')
            content = data.get('content')
            files = list()
            if data.get('files'):
                files = data.get('files')
            res = db.add_news(title, time, content, files)
        except:
            pass
        finally:
            return jsonify(res)


'''
获取公告列表
'''
class GetNews(Resource):
    def get(self):
        res = {"state": "fail"}
        try:
            res = db.get_news()
        except:
            pass
        finally:
            return jsonify(res)


'''
获取公告详情
'''
class GetNewsDetail(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            news_id = data.get('news_id')
            res = db.get_news_detail(news_id)
        except:
            pass
        finally:
            return jsonify(res)


'''
删除公告
参数：
    公告ID
'''
class DeleteNews(Resource):
    def get(self):
        res = {"state": "fail"}
        try:
            data = request.args
            news_id = data.get('news_id')
            res = db.delete_news(news_id)
        except:
            pass
        finally:
            return jsonify(res)


'''
检查专家信息表头
参数：
    表头header
'''
class CheckXlsxHeader(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            header = data.get('header')
            res = db.check_xlsx_header(header)
        except:
            pass
        finally:
            return jsonify(res)


'''
导入专家信息
参数：
    专家列表expert_list
'''
class ImportExpert(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            expert_list = data.get('expert_list')
            res = db.import_expert(expert_list)
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

"""
校团委查看竞赛的所有作品信息
"""
class StageProList(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            competition_id = data.get('competition_id')
            db.update_com_status(competition_id)
            res = db.get_contest_projects(competition_id)
        except Exception as e:
            print(str(e))
            pass
        finally:
            return jsonify(res)

"""
校团委查看竞赛列表
"""
class ContestList(Resource):
    def post(self):
        res = {'state': 'fail'}
        try:
            res = db.get_contests()
        except:
            pass
        finally:
            return res

"""
校团委更改竞赛阶段
"""
class ChangeCompStat(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            proj_id = data.get('proj_id')
            op = data.get('op')
            res = db.change_comp_stat(proj_id, op)
        except:
            pass
        finally:
            return jsonify(res)

'''
上传评审excel表
'''
class UploadReviewForm(Resource):
    def post(self):
        res = {'state': 'fail'}
        try:
            competition_id = request.form.get('competition_id')
            file = request.files.get('file')
            f = file.read()
            code_award_list = []
            data = xlrd.open_workbook(file_contents=f)
            table = data.sheets()[0]
            nrows = table.nrows
            print('nrows', nrows)
            for row in range(1, nrows):
                try:
                    code = int(table.cell_value(row, 0))
                except:
                    code = table.cell_value(row, 0)
                award = table.cell_value(row, 3)
                code_award_list.append((code, award))
            res = db.upload_review_form(competition_id, code_award_list)
        except Exception as e:
            print(str(e))
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
            projlst = data.get('projlst')
            res = db.first_trial_change(projlst)
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

'''
获取邀请/未邀请专家列表
    proj_id：项目id（字符串）
'''
class GetExpertInviteList(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            proj_id = data.get('proj_id')
            res = db.get_project_expert_list(proj_id)
        except:
            pass
        finally:
            return jsonify(res)

'''
邀请专家并插入关系
'''
class InviteMail(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            mail = data.get('mail')
            project_code = data.get('project_code')
            if not db.is_expInvitedProj(mail, project_code):
                res = db.invite_mail(mail, project_code)
                if res['state'] == 'success':
                    res = db.add_proj_exp(mail, project_code)
            else:
                return jsonify(res)
        except:
            pass
        finally:
            return jsonify(res)

'''
(AOE)邀请专家并插入关系
'''
class MultiInviteMail(Resource):
    def post(self):
        res = {"state": "fail", 'cnt': 0}
        try:
            data = request.get_json()
            mails = data.get('mails')
            project_codes = data.get('project_codes')
            for mail in mails:
                res1 = db.multi_invite_mail(mail, project_codes)
                if res1['state'] == 'success':
                    db.multi_add_proj_exp(mail, project_codes)
                    res['cnt'] += res1['cnt']
            if res['cnt'] > 0:
                res['state'] = 'success'
        except:
            pass
        finally:
            return jsonify(res)

'''
检查邮箱和邀请码
'''
class CheckCode(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            mail = data.get('mail')
            invitation_code = data.get('invitation_code')
            project_code = data.get('project_code')
            is_accept = data.get('is_accept')
            res = db.check_code(mail, invitation_code, project_code, is_accept)
        except:
            pass
        finally:
            return jsonify(res)

'''
（AOE）检查邮箱和邀请码
'''
class MultiCheckCode(Resource):
    def post(self):
        res = {"state": "fail", "cnt": 0}
        try:
            data = request.get_json()
            mail = data.get('mail')
            invitation_code = data.get('invitation_code')
            project_code = data.get('project_code').strip().split("|")
            project_codes = list()
            is_accept = data.get('is_accept')
            for pc in project_code:
                if pc == "":
                    continue
                project_codes.append(pc)
            res = db.multi_check_code(mail, invitation_code, project_codes, is_accept)
        except:
            pass
        finally:
            return jsonify(res)

'''
专家设置密码
'''
class ExpertSetPassword(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            mail = data.get('mail')
            password = encode(data.get('password'))
            res = db.expert_set_password(mail, password)
        except:
            pass
        finally:
            return jsonify(res)


'''
提醒专家评审
'''
class RemindExpert(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            comp_id = data.get('comp_id')
            res = db.remind_expert_mail(comp_id)
        except:
            pass
        finally:
            return jsonify(res)


'''
作品退回
'''
class RejectProject(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            project_code = data.get('project_code')
            res = db.reject_project(project_code)
        except:
            pass
        finally:
            return jsonify(res)

# 计算当前时间到明日某时间的秒数差
def get_interval_secs():
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y%m%d')
    tomorrow_time = tomorrow + "-09:00:00"
    tomorrow_time_date = datetime.datetime.strptime(tomorrow_time, '%Y%m%d-%H:%M:%S')
    now = datetime.datetime.now()
    interval = tomorrow_time_date - now
    secs = interval.total_seconds()
    return secs

# 定时更新进程
def do_job():
    try:
        global timer
        db.remind_all()
        timer = threading.Timer(86400, do_job)   # 86400秒就是一天
        timer.start()
    except:
        return
    finally:
        return

'''
定时提醒
'''
def begin_job():
    try:
        global timer
        # db.remind_all()
        timer = threading.Timer(get_interval_secs(), do_job)
        timer.start()
    except:
        return False
    finally:
        return True

'''
获取专家列表
'''
class GetExpertList(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            res = db.get_expert_list()
        except:
            pass
        finally:
            return jsonify(res)

################################################################################################################

'''
用户修改密码
'''
class ChangePassword(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            mail = data.get('mail')
            old_password = encode(data.get('old_password'))
            new_password = encode(data.get('new_password'))
            res = db.change_password(mail, old_password, new_password)
            print("asd")
        except:
            pass
        finally:
            return jsonify(res)

'''
用户修改信息
mail，username，string（领域）
'''
class ChangeInfo(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            mail = data.get('mail')
            user_name = data.get('username')
            field = data.get('field')
            res = db.change_info(mail, user_name, field)
        except:
            pass
        finally:
            return jsonify(res)


'''
获取用户信息
'''
class GetUserInfo(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            mail = data.get('mail')
            res = db.get_user_info(mail)
        except:
            pass
        finally:
            return jsonify(res)



'''
录入现场答辩名单
'''
class EnterDefenseList(Resource):
    def post(self):
        res = {"state": "fail"}
        try:
            data = request.get_json()
            lists = data.get('projlst')
            res = db.enter_defense_list(lists)
        except:
            pass
        finally:
            return jsonify(res)

#######################################################################################################################

'''
校团委新建竞赛
'''
class AddCompetition(Resource):
    def post(self):
        res = {"state": "fail", "reason": "网络错误或未知原因"}
        try:
            data = request.get_json()
            competition_name = data.get('competition_name')
            begin_time = data.get('begin_time')
            submission_ddl = data.get('submission_ddl')
            first_review_ddl = data.get('first_review_ddl')
            expert_comments_ddl = data.get('expert_comments_ddl')
            live_selection_ddl = data.get('live_selection_ddl')
            end_time = data.get('end_time')
            introduction = data.get('introduction')
            res = db.add_competition(competition_name, begin_time, submission_ddl, first_review_ddl, expert_comments_ddl, live_selection_ddl, end_time, introduction)
        except:
            pass
        finally:
            return jsonify(res)

'''
获取竞赛详情(包括简介)
'''
class GetCompetitionDetail(Resource):
    def post(self):
        res = {"state": "fail", "reason": "网络错误或未知错误"}
        try:
            data = request.get_json()
            competition_id = data.get('competition_id')
            res = db.get_competition_detail(competition_id)
        except:
            pass
        finally:
            return jsonify(res)

'''
校团委删除专家
'''
class DeleteExpert(Resource):
    def post(self):
        res = {"state": "fail", "reason": "网络错误或未知错误"}
        try:
            data = request.get_json()
            expert_mail = data.get('expert_mail')
            res = db.delete_expert(expert_mail)
        except:
            pass
        finally:
            return jsonify(res)
################################################################################################################

# 添加api资源
api = Api(app)
api.add_resource(UpFile, "/api/v1/up_file", endpoint="upFile")
api.add_resource(StoreProject, "/api/v1/store_project", endpoint="storeProject")
api.add_resource(AddProject, "/api/v1/add_project", endpoint="addProject")
api.add_resource(GetProjectDetail, "/api/v1/get_project_detail", endpoint="getProjectDetail")
api.add_resource(DeleteProject, "/api/v1/delete_project", endpoint="deleteProject")
api.add_resource(ViewApply, "/api/v1/view_apply", endpoint="viewApply")
api.add_resource(DeleteFile, "/api/v1/delete_file", endpoint="deleteFile")
api.add_resource(SubmitProject, "/api/v1/submit_project", endpoint="submitProject")
api.add_resource(GetProjectList, '/api/v1/get_project_list', endpoint='fetProjectList')
api.add_resource(FirstTrialChange, "/api/vi/first_trial_change", endpoint="firstTrialChange")
api.add_resource(GetTableInfo, "/api/vi/get_table_info", endpoint="getTableInfo")
api.add_resource(Login, '/api/v1/login', endpoint='login')
api.add_resource(RegisterExpert, '/api/v1/registerexpert', endpoint='registerexpert')
api.add_resource(RegisterStudent, '/api/v1/registerstudent', endpoint='registerstudent')
api.add_resource(StageProList, '/api/v1/stageprolist', endpoint='stageprolist')
api.add_resource(GetExpertInviteList, '/api/v1/getExpertInviteList', endpoint='getExpertInviteList')
api.add_resource(DownloadFiles, '/api/v1/download_files', endpoint='downloadFiles')
api.add_resource(GetExpertReviewList, '/api/v1/get_expert_review_list', endpoint='expertReviewList')
api.add_resource(SubmitReview, '/api/v1/submit_review', endpoint='submitReview')
api.add_resource(StoreReview, '/api/v1/store_review', endpoint='storeReview')
api.add_resource(AcceptReview, '/api/v1/accept_review', endpoint='acceptReview')
api.add_resource(RefuseReview, '/api/v1/refuse_review', endpoint='refuseReview')
api.add_resource(MultiAcceptReview, '/api/v1/multi_accept_review', endpoint='multiAcceptReview')
api.add_resource(MultiRefuseReview, '/api/v1/multi_refuse_review', endpoint='multiRefuseReview')
api.add_resource(GetReview, '/api/v1/get_review', endpoint='getReview')
api.add_resource(CheckCode, '/api/v1/check_code', endpoint='check_code')
api.add_resource(MultiCheckCode, '/api/v1/multi_check_code', endpoint='multi_check_code')
api.add_resource(ExpertSetPassword, '/api/v1/expert_set_password', endpoint='expert_set_password')
api.add_resource(ChangePassword, '/api/v1/change_password', endpoint='change_password')
api.add_resource(ChangeInfo, '/api/v1/change_info', endpoint='change_info')
api.add_resource(InviteMail, '/api/v1/invite_mail', endpoint='invite_mail')
api.add_resource(MultiInviteMail, '/api/v1/multi_invite_mail', endpoint='multi_invite_mail')
api.add_resource(ContestList, '/api/v1/contestlist', endpoint='contestlist')
api.add_resource(ChangeCompStat, '/api/v1/changeCompStat', endpoint='changeCompStat')
api.add_resource(GetUserInfo, '/api/v1/get_user_info', endpoint='getUserInfo')
api.add_resource(GetNews, '/api/v1/get_news', endpoint='getNews')
api.add_resource(GetNewsDetail, '/api/v1/get_news_detail', endpoint='getNewsDetail')
api.add_resource(DeleteNews, '/api/v1/delete_news', endpoint='seleteNews')
api.add_resource(AddNews, '/api/v1/add_news', endpoint='addNews')
api.add_resource(UpAnnounceFile, '/api/v1/up_announce_file', endpoint='upAnnounceFile')
api.add_resource(DeleteAnnounceFile, "/api/v1/delete_announce_file", endpoint="deleteAnnounceFile")
api.add_resource(EnterDefenseList, '/api/v1/enter_defense_list', endpoint='enterDefenseList')
api.add_resource(AddCompetition, '/api/v1/add_competition', endpoint="addCompetition")
api.add_resource(RemindExpert, '/api/v1/remind_expert', endpoint="remindExpert")
api.add_resource(RejectProject, '/api/v1/reject_project', endpoint="rejectProject")
api.add_resource(UploadReviewForm, '/api/v1/uploadreviewform', endpoint='uploadreviewform')
api.add_resource(GetCompetitionDetail, '/api/v1/get_competition_detail', endpoint="getCompetitionDetail")
api.add_resource(CheckXlsxHeader, '/api/v1/check_xlsx_header', endpoint="checkXlsxHeader")
api.add_resource(GetExpertList, '/api/v1/get_expert_list', endpoint="getExpertList")
api.add_resource(DeleteExpert, '/api/v1/delete_expert', endpoint="deleteExpert")
api.add_resource(ImportExpert, '/api/v1/import_expert', endpoint="importExpert")

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
    begin_job()
