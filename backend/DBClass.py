#!/usr/bin/env python
# encoding: utf-8
'''
@author: Kunchnag Li
@contact: 812487273@qq.com
@file: DBClass.py
@time: 2019/6/28 14:45
@desc:
'''
import copy

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

################################################################################################
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
                res['reason'] = ''
            else:
                res['reason'] = "项目编号不存在"
        except:
            pass
        finally:
            return res

    '''
    新增项目报名
    '''
    def add_project(self, competition_id, email, name):
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
                    'author_name': name,
                    'project_code': code,
                    'competition_id': competition_id,
                    'project_status': -1,
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
                res['reason'] = ''
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
                        'file_name': temp[-1].split('_')[-1],
                        'file_path': Config.DOMAIN_NAME + '/' + '/'.join(temp[-3:]),
                        'file_type': file['file_type']
                        })
                project['project_files'] = temp_files
                res['project'] = project
                res['reason'] = ''
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
                res['reason'] = ''
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
                    res['reason'] = ''
            else:
                res['reason'] = "项目不存在"
        except:
            pass
        finally:
            return res

    '''
    提交项目报名
    '''
    def submit_project(self, params):
        res = {'state': 'fail', 'reason': "未知错误"}
        try:
            project_code = params['workCode']
            project = self.getCol('project').find_one({'project_code': project_code})
            if project:
                if 'mainTitle' in params.keys():
                    project['project_name'] = params['mainTitle']
                project['registration_form'] = params
                project['project_status'] = 0
                self.getCol('project').update_one({'project_code': project_code}, {'$set': project})
                filename = project_code + ".html"
                replace_apply_html(params, filename)
                res['state'] = 'success'
                res['reason'] = ''
        except:
            pass
        finally:
            return res

    '''
    获取项目列表
    '''
    def get_project_list(self, author_email):
        res = {'state': 'fail', 'reason': "未知错误"}
        try:
            temp_list = self.getCol('project').find({'author_email': author_email},
                                                    {'project_code': 1,
                                                     'project_name': 1,
                                                     'competition_id': 1,
                                                     'project_status': 1})
            project_list = list()
            for p in temp_list:
                print(p['competition_id'])
                competition_name = self.getCol('competition').find_one({'_id': ObjectId(p['competition_id'])},
                                                                       {'competition_name': 1})
                project_list.append({
                    'project_code': p['project_code'],
                    'project_name': p['project_name'],
                    'competition_id': p['competition_id'],
                    'project_status': p['project_status'],
                    'competition_name': competition_name['competition_name']
                })
            res['state'] = 'success'
            res['reason'] = ''
            res['project_list'] = project_list
        except:
            pass
        finally:
            return res

    '''
    保存评审意见
    '''
    def store_review(self, project_code, expert_email, score, suggestion):
        res = {'state': 'fail', 'reason': "未知错误"}
        try:
            review = self.getCol('expert_project').find_one({'project_code': project_code,
                                                             'expert_email': expert_email})
            if review and review['status'] == 0:
                review['score'] = score
                review['suggestion'] = suggestion
                self.getCol('expert_project').update_one({'project_code': project_code,
                                                          'expert_email': expert_email}, {'$set': review})
                res['status'] = review['status']
                res['state'] = 'success'
                res['reason'] = ''
            else:
                res['reason'] = "项目不存在或专家没有权利评审该项目"
        except:
            pass
        finally:
            return res


    '''
    提交评审意见
    '''
    def submit_review(self, project_code, expert_email, score, suggestion):
        res = {'state': 'fail', 'reason': "未知错误"}
        try:
            review = self.getCol('expert_project').find_one({'project_code': project_code,
                                                             'expert_email': expert_email})
            if review and review['status'] == 0:
                review['score'] = score
                review['suggestion'] = suggestion
                review['status'] = 2
                self.getCol('expert_project').update_one({'project_code': project_code,
                                                          'expert_email': expert_email}, {'$set': review})
                res['state'] = 'success'
                res['status'] = review['status']
                res['reason'] = ''
            else:
                res['reason'] = "项目不存在或专家没有权利评审该项目"
        except:
            pass
        finally:
            return res

    '''
    获取评审意见
    '''
    def get_review(self, project_code, expert_email):
        res = {'state': 'fail', 'reason': "未知错误"}
        try:
            review = self.getCol('expert_project').find_one({'project_code': project_code,
                                                             'expert_mail': expert_email})
            if review and (review['status'] == 0 or review['status'] == 2):
                review.pop('_id')
                res['state'] = 'success'
                res['reason'] = '' 
                res['review'] = review
            else:
                res['reason'] = "项目不存在或专家没有权利评审该项目"
        except:
            pass
        finally:
            return res

    '''
    接受评审
    '''
    def accept_review(self, project_code, expert_email):
        res = {'state': 'fail', 'reason': "未知错误"}
        try:
            review = self.getCol('expert_project').find_one({'project_code': project_code,
                                                             'expert_email': expert_email})
            if review and review['status'] == -1:
                review['status'] = 0
                self.getCol('expert_project').update_one({'project_code': project_code,
                                                          'expert_email': expert_email}, {'$set': review})
                res['state'] = 'success'
                res['status'] = review['status']
                res['reason'] = ''
            else:
                res['reason'] = "项目不存在或专家没有权利处理是否评审"
        except:
            pass
        finally:
            return res

    '''
    拒绝评审
    '''
    def refuse_review(self, project_code, expert_email):
        res = {'state': 'fail', 'reason': "未知错误"}
        try:
            review = self.getCol('expert_project').find_one({'project_code': project_code,
                                                             'expert_email': expert_email})
            if review and review['status'] == -1:
                review['status'] = 1
                self.getCol('expert_project').update_one({'project_code': project_code,
                                                          'expert_email': expert_email}, {'$set': review})
                res['state'] = 'success'
                res['status'] = review['status']
                res['reason'] = ''
            else:
                res['reason'] = "项目不存在或专家没有权利处理是否评审"
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
    hash
    '''
    def hash_code(self, name):
        code = str(name.__hash__())
        return code

    '''
    注册专家用户
    '''
    def create_user_expert(self, mail, username, field):
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            check = self.check_mail(mail)
            if check['state'] == 'fail':
                res['reason'] = check['reason']
                return res
            invitation_code = self.hash_code(mail)
            new_expert = {'username': username,
                          'mail': mail,
                          'password': "",
                          'user_type': 'expert',
                          'field': field,
                          'invitation_code': invitation_code}
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
    专家设置密码
    '''
    def expert_set_password(self, mail, password):
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            user = self.getCol('user')
            expert = user.find_one({'user_type': 'expert', 'mail': mail})
            print(expert)
            if expert is None:
                res['reason'] = "未找到专家"
                return res
            if expert['password'] != "":
                res['reason'] = "已设置密码"
                return res
            user.update_one({'user_type': 'expert', 'mail': mail}, {"$set": {'password': password}})
            res['state'] = 'success'
        except:
            return res
        return res

    '''
    判断某专家是否已被邀请参评某作品
    '''
    def is_expInvitedProj(self, mail, proj_id):
        try:
            test = self.getCol("expert_project").find_one({'expert_mail': mail, 'project_code': proj_id})
            # 专家已被邀请过参评该作品
            if test:
                return True
            # 专家未被邀请过参评该作品
            else:
                return False
        except:
            return False

    '''
    校团委发送邮件
    '''
    def send_mail(self, mail, header, message):
        try:
            msg = MIMEText(message, 'html', 'utf-8')
            msg['Subject'] = Header(header, 'utf-8')
            msg['From'] = '校团委 <team_997ywwg@163.com>'
            msg['To'] = '<' + mail + u'>'
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
    添加项目-专家关系
    '''
    def add_proj_exp(self, expert_email, project_code):
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            user_list = self.getCol("user")
            test = user_list.find_one({'mail': expert_email})
            # 专家账号存在
            if test:
                name = test['username']
                new_relation = {"project_code": project_code, "expert_mail": expert_email, "username": name,
                                "score": 0, "suggestion": "", "status": -1}
                exp_proj = self.getCol("expert_project")
                exp_proj.insert_one(new_relation)
                res['state'] = 'success'
            # 专家账号不存在
            else:
                res['reason'] = "专家账号不存在"
            return res
        except:
            return res

    '''
    向专家发送邀请邮件
    '''
    def invite_mail(self, mail, project_code):
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            user = self.getCol('user')
            expert = user.find_one({'user_type': 'expert', 'mail': mail})
            if expert is None:
                res['reason'] = "未找到专家"
                return res
            expert_name = expert["username"]
            invitation_code = expert['invitation_code']
            project = self.getCol('project')
            pro = project.find_one({'project_code': project_code})
            if pro is None:
                res['reason'] = "未找到项目"
                return res
            project_name = pro["project_name"]
            comp_code = pro["competition_id"]
            competition = self.getCol('competition')
            comp = competition.find_one({'_id': ObjectId(comp_code)})
            if comp is None:
                res['reason'] = "未找到竞赛"
                return res
            comp_name = comp["competition_name"]
            header = comp_name + "项目评审邀请"
            accept_addr = "http://localhost:8080/#/?token=" + invitation_code + \
                          "&email=" + mail + \
                          "&project_code=" + project_code + "&is_accept=" + "true"
            # accept_addr = "<a href=\"" + accept_addr + "\">" + accept_addr + "</a>"
            accept_addr = "<a href=\"" + accept_addr + "\">" + "接受评审" + "</a>"
            refuse_addr = "http://localhost:8080/#/?token=" + invitation_code + \
                          "&email=" + mail + \
                          "&project_code=" + project_code + "&is_accept=" + "false"
            # refuse_addr = "<a href=\"" + refuse_addr + "\">" + refuse_addr + "</a>"
            refuse_addr = "<a href=\"" + refuse_addr + "\">" + "拒绝评审" + "</a>"
            message = "<p>尊敬的 " + expert_name + " 先生/女士您好，\n</p>" + \
                      "<p>" + comp_name + "组委会诚邀您参与参赛项目：\"" + project_name + "\"的评审工作。\n</p>" + \
                      "<p>如果您接受此邀请，请点击链接: " + accept_addr + " 进入竞赛系统。\n</p>" + \
                      "<p>如果您希望拒绝此邀请，请点击链接: " + refuse_addr + "确认拒绝。\n</p>" + \
                      "<p>衷心感谢您的付出和支持。\n</p>" + \
                      "<p>----" + comp_name + "组委会\n</p>"
            if self.send_mail(mail, header, message) is False:
                res['reason'] = "邮件发送失败"
                return res
            res['state'] = 'success'
        except:
            return res
        return res

    '''
    检查邮箱和邀请码
    '''
    def check_code(self, mail, invitation_code, project_code, is_accept):
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            user = self.getCol('user')
            expert = user.find_one({'user_type': 'expert', 'mail': mail})
            if expert is None:
                res['reason'] = "未找到专家"
                return res
            if expert['invitation_code'] != invitation_code:
                res['reason'] = "验证码错误"
                return res
            expert_project = self.getCol('expert_project')
            e_p = expert_project.find_one({'expert_mail': mail, 'project_code': project_code})
            if e_p is None:
                res['reason'] = "未找到关系"
                return res
            status = e_p['status']
            if expert["password"] == "":
                res['registered'] = False
            else:
                res['registered'] = True
            res['old_status'] = status
            if status == -1:
                if is_accept:
                    new_status = 0
                else:
                    new_status = 1
                expert_project.update_many({'expert_mail': mail, 'project_code': project_code}, {"$set": {'status': new_status}})
                # res['operation_ok'] = True
            else:
                1  # res['operation_ok'] = False
            res['state'] = 'success'
        except:
            return res
        return res

    '''
    对于某个项目，返回邀请过和未邀请的专家列表
    '''
    def get_project_expert_list(self, project_code):
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            expert_project = self.getCol('expert_project')
            user = self.getCol('user')
            list_invited = expert_project.find({'project_code': project_code}, {"_id": 0,
                                                                                "expert_mail": 1,
                                                                                "username": 1,
                                                                                'status': 1,
                                                                                'score': 1,
                                                                                'suggestion': 1})
            invited = []
            res_invited = []
            for item0 in list_invited:
                res_invited.append(item0)
                invited.append(item0['expert_mail'])
            list_all = user.find({'user_type': 'expert'}, {"_id": 0, "mail": 1, "username": 1, 'field': 1})
            list_uninvited = []
            for item1 in list_all:
                if item1['mail'] not in invited:
                    list_uninvited.append(item1)
            res['list_invited'] = res_invited
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

    '''
    获取专家评审项目信息
    '''
    def expert_review_list(self, email):
        res = {'state': 'fail', 'reason': '网络错误或其他问题!'}
        try:
            find_project = self.getCol(
                'expert_project').find({'expert_mail': email, 'status': {'$ne': 1}})
            # 搜索到专家对应的列表
            if find_project:
                project_lists = list()
                for fp in find_project:
                    proj_id = fp['project_code']
                    status = fp['status']
                    proj = self.getCol('project').find_one({'project_code': proj_id},
                                                           {'project_name': 1, 'competition_id': 1})
                    proj_name = proj['project_name']
                    comp = self.getCol('competition').find_one({'_id': ObjectId(proj['competition_id'])},
                                                               {'competition_name': 1, 'expert_comments_ddl': 1})
                    comp_name = comp['competition_name']
                    exp_com_ddl = comp['expert_comments_ddl']
                    project_list = {
                        'project_id': proj_id,
                        'project_name': proj_name,
                        'competition_name': comp_name,
                        'expert_comments_ddl': exp_com_ddl,
                        'status': status
                    }
                    project_lists.append(project_list)
                res['state'] = 'Success'
                res['reason'] = 'None'
                res['project_lists'] = project_lists
            # 专家不存在
            else:
                res['state'] = 'Success'
                res['reason'] = '专家没有评审的项目'
        except:
            pass
        finally:
            return res


    '''
    查询竞赛所有作品信息
    '''
    def num2status(self,num):
        num_map = {
            -1: '编辑中',
            0: '已提交',
            1: '通过初审',
            2: '凉凉',
            3: '进入现场答辩',
            4: '优秀奖',
            5: '三等奖',
            6: '二等奖',
            7: '一等奖',
        }
        return num_map[num]

    '''
    任意阶段看A或B，A或B的显示规则
    '''
    def rule_A(self, A_List):
        temp = A_List.copy()
        for index, project in enumerate(temp):
            if project['project_status'] >= 1:
                temp[index]['project_status'] = 1
            temp[index]['project_status'] = self.num2status(temp[index]['project_status'])
        return temp

    '''
    C阶段看C，C的显示规则
    '''
    def rule_CC(self, C_List):
        for index, project in enumerate(C_List):
            if project['project_status'] >= 3:
                C_List[index]['project_status'] = 3
            C_List[index]['project_status'] = self.num2status(C_List[index]['project_status'])
        return C_List

    '''
    D阶段看C，C的显示规则
    '''
    def rule_DC(self, C_List):
        for index, project in enumerate(C_List):
            if project['project_status'] >= 3:
                C_List[index]['project_status'] = 3
            elif project['project_status'] <= 2:
                C_List[index]['project_status'] = 2
            C_List[index]['project_status'] = self.num2status(C_List[index]['project_status'])
        return C_List

    '''
    D阶段看D，D的显示规则
    '''
    def rule_D(self, D_List):
        for index, project in enumerate(D_List):
            D_List[index]['project_status'] = self.num2status(D_List[index]['project_status'])
        return D_List

    def get_contest_projects(self, competition_id):
        res = {
            'state': 'fail',
            'reason': '网络出错或BUG出现！',
            'A_List': [],
            'B_List': [],
            'C_List': [],
            'D_List': [],
            'com_status': '',
            'competition_name': '',
        }
        project_collection = self.getCol('project')
        com_collection = self.getCol('competition')
        try:
            projects = []
            for item in project_collection.find({'competition_id': competition_id}, {'_id': 0}):
                projects.append(item)
            com_status = com_collection.find_one({'_id': ObjectId(competition_id)})['com_status']
            competition_name = com_collection.find_one({'_id': ObjectId(competition_id)})['competition_name']
            res['com_status'] = com_status
            res['competition_name'] = competition_name
            if len(projects) > 0:
                res['state'] = 'success'
                res['reason'] = '成功获取竞赛作品列表'
                # 当前状态是初审
                if com_status == 1:
                    res['A_List'] = self.rule_A(copy.deepcopy(projects))
                # 当前状态是初评
                elif com_status == 2:
                    res['A_List'] = self.rule_A(copy.deepcopy(projects))
                    res['B_List'] = self.rule_A(list(filter(lambda x: x['project_status'] >= 1, copy.deepcopy(projects))))
                # 当前状态是筛选并现场答辩
                elif com_status == 3:
                    res['A_List'] = self.rule_A(copy.deepcopy(projects))
                    res['B_List'] = self.rule_A(list(filter(lambda x: x['project_status'] >= 1, copy.deepcopy(projects))))
                    res['C_List'] = self.rule_CC(list(filter(lambda x: x['project_status'] >= 1, copy.deepcopy(projects))))
                # 当前状态是录入并公布最终结果
                elif com_status == 4:
                    res['A_List'] = self.rule_A(copy.deepcopy(projects))
                    res['B_List'] = self.rule_A(list(filter(lambda x: x['project_status'] >= 1, copy.deepcopy(projects))))
                    res['C_List'] = self.rule_DC(list(filter(lambda x: x['project_status'] >= 1, copy.deepcopy(projects))))
                    res['D_List'] = self.rule_D(list(filter(lambda x: x['project_status'] >= 3, copy.deepcopy(projects))))
            elif len(projects) == 0:
                res['state'] = 'success'
                res['reason'] = '竞赛作品列表为空'
        except:
            pass
        finally:
            return res

    """
    查看竞赛列表
    """
    def get_contests(self):
        res = {'state': 'fail', 'reason': '网络出错或BUG出现！', 'contests': [], }
        com_collection = self.getCol('competition')
        project_collection = self.getCol('project')
        try:
            if com_collection.count()<1:
                res['reason'] = '竞赛列表为空'
            else:
                res['state'] = 'success'
                res['reason'] = '查询成功'
                for com in com_collection.find():
                    com['count'] = project_collection.find({'competition_id': str(com['_id'])}).count()
                    com['competition_id'] = str(com['_id'])
                    com.pop('_id')
                    res['contests'].append(com)
        except:
            pass
        finally:
            return res

###############################################################################################

    '''
    初审改变作品状态
    proj_id:项目id（字符串）   result:初审结果（字符串 'True' 'False'）
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
    获取提交表数据以及该作品所属竞赛当前所处阶段
    '''
    def get_table_info(self, proj_id):
        res = {'state': 'fail', 'reason': '网络出错或BUG出现！'}
        try:
            proj = self.getCol('project').find_one({'project_code': proj_id}, {'registration_form': 1,
                                                                               'competition_id': 1})
            if proj:
                # 查找对应竞赛
                competition = self.getCol('competition').find_one({'_id': ObjectId(proj['competition_id'])},
                                                                  {'com_status': 1})
                if competition:
                    # 先处理作品表数据
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
                    # 设置结果值
                    form['com_status'] = competition['com_status']
                    res['state'] = 'success'
                    res['msg'] = form
                else:
                    res['reason'] = '作品所属竞赛不存在'
            else:
                res['reason'] = '该作品不存在'
            return res
        except:
            return res
