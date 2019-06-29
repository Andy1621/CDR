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
from weasyprint import HTML

def export2pdf(filename):
    HTML('templates/apply.html').write_pdf('static/export_pdf/'+filename)


html = '''
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <table border="1">
        <tr>
            <td>姓名</td>
            <td id="name">达哥</td>
            <td>学号</td>
            <td id="stuId">16211020</td>
        </tr>
        <tr>
            <td>学历</td>
            <td id="eduBackground">本科</td>
            <td>出生年月</td>
            <td id="birthdate">1999.7</td>
        </tr>
    </table>
</body>
</html>
'''

soup = BeautifulSoup(html, 'lxml')
name = soup.select('#name')
name[0].string = '许志达'
print(soup.prettify())
