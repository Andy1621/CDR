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
from utils import replace_apply_html
from bson.objectid import ObjectId
import Config
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import random
import os



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
            project = self.getCol('project').find_one({'project_code': project_code})
            if project:
                if 'mainTitle' in params.keys():
                    project['project_name'] = params['mainTitle']
                project['registration_form'] = params
                self.getCol('project').update_one({'project_code': project_code}, {'$set': project})
                filename = project_code + ".html"
                replace_apply_html(params, filename)
                res['state'] = 'success'
            else:
                res['reason'] = "项目编号不存在"
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
            competition = self.getCol('competition').find_one({'_id': ObjectId(competition_id)})
            if competition:
                # 生成项目编码
                project_list = self.getCol('project')
                num = random.randint(0, 99999)
                code = str(num)
                pro = project_list.find_one({'project_code': code})
                cnt = 0
                while pro is not None:
                    num = (num + 1) % 100000
                    code = str(num)
                    pro = project_list.find_one({'project_code': code})
                    cnt += 1
                    if cnt > 100000:
                        res['reason'] = '项目数量超限'
                        return res
                code.zfill(5)
                t_project = {
                    'project_name': '',
                    'author_email': email,
                    'project_code': code,
                    'competition_id': competition_id,
                    'project_status': 'editing',
                    'registration_form': {'workCode': code, 'mainTitle': '',
                                          'department': '', 'mainType': '',
                                          'name': '', 'stuId': '', 'birthday': '',
                                          'education': '', 'major': '',
                                          'enterTime': '', 'totalTitle': '',
                                          'address': '', 'phone': '', 'email': '',
                                          'applier': list(), 'title': '',
                                          'type': '', 'description': '',
                                          'creation': '', 'keyword': ''},
                    'project_files': list()
                }
                self.getCol('project').insert_one(t_project)
                res['state'] = 'success'
                res['project_code'] = code
                # filename = code + ".html"
                # replace_apply_html(t_project['registration_form'], filename)
            else:
                res['reason'] = "竞赛不存在"
        except:
            pass
        finally:
            return res

    '''
    获取项目信息
    '''
    def get_project_detail(self, project_code):
        res = {'state': 'fail', 'reason': "未知错误"}
        try:
            project = self.getCol('project').find_one({'project_code': project_code})
            if project:
                res['state'] = 'success'
                project.pop('_id')
                temp_files = list()
                project_files = project['project_files']
                for file in project_files:
                    temp = file['file_path'].split('/')
                    temp_files.append({
                        'file_name': temp[-1],
                        'file_path': Config.DOMAIN_NAME + '/' + '/'.join(temp[-3:])})
                project['project_files'] = temp_files
                res['project'] = project
            else:
                res['reason'] = "项目不存在"
        except:
            pass
        finally:
            return res

    '''
    查看申请表
    '''
    def view_apply(self, project_code):
        res = {'state': 'fail', 'reason': "未知错误"}
        try:
            project = self.getCol('project').find_one({'project_code': project_code})
            if project:
                filename = project_code + ".html"
                replace_apply_html(project['registration_form'], filename)
                html_url = Config.DOMAIN_NAME + "/static/export_html/" + filename
                res['state'] = 'success'
                res['html_url'] = html_url
            else:
                res['reason'] = "项目不存在"
        except:
            pass
        finally:
            return res


    '''
    删除项目报名
    '''
    def delete_project(self, project_code):
        res = {'state': 'fail', 'reason': "未知错误"}
        try:
            project = self.getCol('project').find_one({'project_code': project_code})
            if project:
                files = self.getCol('project').find_one({'project_code': project_code},  {'project_files': 1})
                project_files = files['project_files']
                flag = True
                basedir = os.path.abspath(os.path.dirname(__file__))
                for pf in project_files:
                    file_path = basedir + "/static/" + pf['file_type'] + "/" + pf["file_path"]
                    if not os.path.exists(file_path):
                        res['reason'] = '附件不存在，请联系管理员'
                        flag = False
                        break
                    os.remove(file_path)
                if flag:
                    html_path = basedir + "/static/export_html/" + project_code + '.html'
                    os.remove(html_path)
                    self.getCol('project').remove({'project_code': project_code})
                    res['state'] = 'success'
            else:
                res['reason'] = "项目不存在"
        except:
            pass
        finally:
            return res
##############################################################################################
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
            if check['state'] == 'fail':
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
            if check['state'] == 'fail':
                res['reason'] = check['reason']
                return res
            new_expert = {'username': username,
                          'mail': mail,
                          'password': "",
                           'user_type': 'expert',
                          'invitation_code': ''
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
    def compare_password(self, password, mail, user_type):
        res = {'username': '', 'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            find_user = self.getCol('user').find_one({'mail': mail})
            # 搜索到唯一用户
            if find_user:
                res['username'] = find_user['username']
                real_psw = find_user['password']
                if real_psw == "" and find_user['user_type'] == 'expert':
                    res['reason'] = '该专家尚未设置密码!'
                elif real_psw == password:
                    dictionary = {'student': 'user', 'professor': 'expert', 'school': 'admin'}
                    if dictionary[user_type] != find_user['user_type']:
                        res['reason'] = '用户类型不匹配'
                        return res
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
    校团委发送邮件
    '''
    def send_mail(self, mail, header, message):
        try:
            msg = MIMEText(message, 'plain', 'utf-8')
            msg['Subject'] = Header(header, 'utf-8')
            msg['From'] = '校团委 <team_997ywwg@163.com>'
            msg['To'] = '<' + mail + '>'
            # 输入Email地址和口令:
            from_addr = 'team_997ywwg@163.com'
            password = 'nxdmdyzxcxk233'
            # 输入SMTP服务器地址:
            smtp_server = 'smtp.163.com'
            # 输入收件人地址:
            to_addr = mail
            server = smtplib.SMTP(smtp_server)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())
            server.quit()
        except:
            return False
        return True
 
    '''
    对于某个项目，返回邀请过和未邀请得专家列表
    '''
    def get_project_expert_list(self, project_code):
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            expert_project = self.getCol('expert_project')
            user = self.getCol('user')
            list_invited = expert_project.find({'project_code': project_code}, {"expert_mail": 1,
                                                                                "username": 1,
                                                                                'status': 1,
                                                                                'score': 1,
                                                                                'suggestion': 1})
            invited = []
            for item0 in list_invited:
                invited.append(item0['expert_mail'])
            list_all = user.find({'user_type': 'expert'}, {"mail": 1, "username": 1, 'invitation_code': 1})
            list_uninvited = []
            for item1 in list_all:
                if item1['mail'] not in invited:
                    list_uninvited.append(item1)
            res['list_invited'] = list_invited
            res['list_uninvited'] = list_uninvited
            res['state'] = 'success'
        except:
            return res
        return res

##############################################################################################
    '''
    插入附件信息
    '''
    def insert_attachment(self, project_code, file_type, file_path):
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            find_project = self.getCol('project').find_one({'project_code': project_code}, {'project_files': 1})
            # 搜索到唯一项目
            if find_project:
                project_files = find_project.get('project_files')
                if not project_files:
                    project_files = []
                project_file = {
                    'file_type': file_type,
                    'file_path': file_path
                }
                flag = True
                for pf in project_files:
                    if file_path == pf.get('file_path'):
                        res['reason'] = '附件已存在'
                        flag = False
                        break
                if flag:
                    project_files.append(project_file)
                    self.getCol('project').update_one({'project_code': project_code},
                                                  {"$set": {"project_files": project_files}})
                    res['state'] = 'success'
                    res['reason'] = 'None'
            # 项目不存在
            else:
                res['reason'] = '项目不存在'
        except:
            pass
        finally:
            return res

    '''
    删除附件
    '''
    def delete_attachment(self, project_code, file_path):
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            find_project = self.getCol('project').find_one({'project_code': project_code}, {'project_files': 1})
            # 搜索到唯一项目
            if find_project:
                project_files = find_project.get('project_files')
                flag = True
                for pf in project_files:
                    if file_path == pf.get('file_path'):
                        project_files.remove(pf)
                        flag = False
                        break
                if not flag:
                    self.getCol('project').update_one({'project_code': project_code},
                                                  {"$set": {"project_files": project_files}})
                    res['state'] = 'Success'
                    res['reason'] = 'None'
                else:
                    res['state'] = '附件不存在'
            # 项目不存在
            else:
                res['reason'] = '项目不存在'
        except:
            pass
        finally:
            return res


    '''
    获取附件列表
    '''
    def require_attachments(self, project_code):
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            find_project = self.getCol('project').find_one({'project_code': project_code}, {'project_files': 1})
            # 搜索到唯一项目
            if find_project:
                project_files = find_project.get('project_files')
                if len(project_files) > 0:
                    res['project_files'] = project_files
                    res['state'] = 'Success'
                    res['reason'] = 'None'
                else:
                    res['state'] = '该项目无附件'
            # 项目不存在
            else:
                res['reason'] = '项目不存在'
        except:
            pass
        finally:
            return res
###############################################################################################

    '''
    初审改变作品状态
    proj_id：项目id（字符串）   result：初审结果（字符串 'True' 'False'）
    '''
    def first_trial_change(self, proj_id, result):
        res = {'state': 'fail', 'reason': '网络出错或BUG出现！'}
        try:
            proj_list = self.getCol('project')
            find_proj = proj_list.find_one({'project_code': proj_id}, {'_id': 1})
            # 成功搜索到该项目
            if find_proj:
                if result == 'True':
                    now_stat = 1
                else:
                    now_stat = -1
                proj_list.update_one({"project_code": proj_id},
                                     {"$set": {"project_status": now_stat}})
                res['state'] = 'success'
            # 未搜索到该项目
            else:
                res['reason'] = '该项目不存在'
            return res
        except:
            return res

    '''
    获取提交表数据
    '''
    def get_table_info(self, proj_id):
        res = {'state': 'fail', 'reason': '网络出错或BUG出现！'}
        try:
            proj = self.getCol('project').find_one({'project_code': proj_id}, {'registration_form': 1})
            if proj:
                form = proj['registration_form']
                form.pop('workCode')
                # 将类别选项改为汉字值
                if form['mainType'] == 'type1':
                    form['mainType'] = '科技发明制作'
                else:
                    form['mainType'] = '调查报告和学术论文'
                # 将学历选项改为汉字值
                if form['education'] == 'A':
                    form['education'] = '大专'
                elif form['education'] == 'B':
                    form['education'] = '大学本科'
                elif form['education'] == 'C':
                    form['education'] = '硕士研究生'
                else:
                    form['education'] = '博士研究生'
                res['state'] = 'success'
                res['msg'] = form
            else:
                res['reason'] = '该项目不存在'
            return res
        except:
            return res
