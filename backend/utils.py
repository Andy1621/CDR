#!/usr/bin/env python
# encoding: utf-8
'''
@author: Kunchnag Li
@contact: 812487273@qq.com
@file: utils.py
@time: 2019/6/27 16:11
@desc:
'''

from bs4 import BeautifulSoup
import hashlib
import os
import zipfile

SPECIAL_STR = "cxk"                     # MD5加密特殊字符串
MD5_LEN = 10                            # 加密组合长度

'''
form内容:
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
def replace_apply_html(form, filename):
    workType = {
        'A': "机械与控制（包括机械、仪器仪表、自动化控制、工程、交通、建筑等）",
        'B': "信息技术（包括计算机、电信、通讯、电子等）",
        'C': "数理（包括数学、物理、地球与空间科学等）",
        'D': "生命科学(包括生物､农学､药学､医学､健康､卫生､食品等)",
        'E': "能源化工（包括能源、材料、石油、化学、化工、生态、环保等）",
        'F': "哲学社会科学（包括哲学、经济、社会、法律、教育、管理）"
    }
    educationType = {
        'A': "大专",
        'B': "大学本科",
        'C': "硕士研究生",
        'D': "博士研究生"
    }
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_path = basedir + "/templates/apply.html"
    with open(file_path, 'rb') as f1:
        data = f1.read()
        html = BeautifulSoup(data, 'lxml')
        for key in form.keys():
            if key == 'applier':
                for i, applier in enumerate(form[key]):
                    for c_key in applier.keys():
                        temp_component = html.select('#' + c_key + str(i + 1))
                        temp_component[0].string = applier[c_key]
            elif key == 'type':
                if form[key] in workType.keys():
                    temp_component = html.select('#' + key)
                    temp_component[0].string = workType[form[key]]
            elif key == 'mainType':
                temp_component = html.select('#' + form[key])
                temp_component[0]['class'] = "glyphicon glyphicon-check"
            elif key == 'education':
                if form[key] in educationType.keys():
                    temp_component = html.select('#' + key)
                    temp_component[0].string = educationType[form[key]]
            else:
                temp_component = html.select('#' + key)
                temp_component[0].string = form[key]
        with open(basedir + "/static/export_html/" + filename, 'wb') as f2:
            f2.write(html.prettify().encode())

def encode(password):
    hl = hashlib.md5()
    hl.update(password.encode(encoding='utf-8'))
    final_password = hl.hexdigest()
    hl.update(SPECIAL_STR.encode(encoding='utf-8'))
    special = hl.hexdigest()
    final_password = final_password[: -MD5_LEN] + special[-MD5_LEN:]
    return final_password


# 打包文件
def make_zip(source_dir_list, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    for f in source_dir_list:
        pathfile = f['file_path']
        arcname = pathfile.split('/')[-1]
        zipf.write(pathfile,arcname)
    zipf.close()


if __name__ == '__main__':
    form = {'workCode': '201906291001',
            'mainTitle': '基于LSTM的QQ说说情感分析',
            'department': '软件学院',
            'mainType': 'type1',
            'name': '李狗蛋',
            'stuId': '16211000',
            'birthday': '19980228',
            'education': 'A',
            'major': '软件工程',
            'enterTime': '2016.9.1',
            'totalTitle': '基于LSTM的QQ说说情感分析',
            'address': '北京市海淀区大运村1公寓707D',
            'phone': '15666666666',
            'email': '1234567@qq.com',
            'applier': [{'name': '李一', 'stuId': '16211000', 'education': '本科', 'phone': '15666666666',
                         'email': '1234567@qq.com'},
                        {'name': '李二', 'stuId': '16211000', 'education': '本科', 'phone': '15666666666',
                         'email': '1234567@qq.com'},
                        {'name': '李三', 'stuId': '16211000', 'education': '本科', 'phone': '15666666666',
                         'email': '1234567@qq.com'},
                        {'name': '李四', 'stuId': '16211000', 'education': '本科', 'phone': '15666666666',
                         'email': '1234567@qq.com'}],
            'title': '基于LSTM的QQ说说情感分析',
            'type': 'A',
            'description': "word2vec是通过学习文本来用词向量的方式表征词的语义信息，即通过一个嵌入空间使得语义上相似的单词在该空间内距离很近。Embedding其实就是一个映射，将单词从原先所属的空间映射到新的多维空间中，也就是把原先词所在空间嵌入到一个新的空间中去。它的基本思路是，为每一个词汇设置一个初始向量（在这里我设置成了200维），然后根据每个词对应的词向量去预测该词的周边词汇，通过反向传播修改词向量，使词向量的预测结果越来越接近目标词汇。因为语义相似的词汇有着相似的语境，在直观上会表现为词向量在高维空间内距离越来越近。常用的训练模型有两种：Skip-gram模型和cbow模型。CBOW模型是多个周边词对一词的预测，Skip-gram模型是由一个词汇对多个周边词的预测。在训练时，可以直接使用python的gensim工具包。训练语料可以采用中文维基数据或者搜狗实验室的语料。",
            'creation': '就是非常牛逼',
            'keyword': 'lstm'}
    filename = form["workCode"] + ".html"
    replace_apply_html(form, filename)
    print("ok")
