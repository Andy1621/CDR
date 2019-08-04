# CDR
Competition Declaration and Review

科技竞赛申报与评审系统——997雨我无瓜

**Vue.js+Flask+MongoDB**



### frontend指前端

参考文件夹下README.md进行依赖包安装，vue有大量开源组件，可再github上参考借鉴

***注意/scc/main.js下的Vue.prototype.$baseURL为后端服务地址，在自己服务器上使用时记得修改部署***



### backend指后端

后端需要在服务器上部署nginx服务以及mongodb服务，并创建相应空数据表（不创建也莫得问题，程序会自动创建，但校团委账户需要手动创建），推荐使用Robo 3T进行远程访问MongoDB并随时修改数据库

***注意Config.py为配置文件，HOST为MongoDB服务地址，DOMAIN_NAME为后端服务地址，用以上传文件时强制写入文件访问名（使用flask的static静态文件读取）***



### 数据库约定

----
#### user

- **说明**：

  此表用于存储用户的基本信息，账号信息包括__邮箱地址__(mail)、__姓名__(username)、__登陆密码__(password)、__用户类型__(user_type)、__学号__(ID)、__院系__(department)、**专业**(field)、__入学年份__(admission_year)、__联系电话__(phone)、__专家邮件邀请码__(invitation_code)。

- **其他**：
  - 每个邮箱唯一对应一个用户。
  - 密码为""的有且只有未设置密码的专家（邀请前为专家建立账号，密码为""，专家接收邀请时设定密码）。
    __专业__为一个六位的01字符串：1代表属于这个领域，六位代表：

    ```
    A.机械与控制（包括机械、仪器仪表、自动化控制、工程、交通、建筑等）
    B.信息技术（包括计算机、电信、通讯、电子等）
    C.数理（包括数学、物理、地球与空间科学等）
    D.生命科学(包括生物､农学､药学､医学､健康､卫生､食品等)
    E.能源化工（包括能源、材料、石油、化学、化工、生态、环保等）
    F.哲学社会科学（包括哲学、经济、社会、法律、教育、管理）
    ```

    故，若一个专家的领域为：100001，则代表其领域为A和F。

- **对象字段要求**：

  ```python
  {"mail":string,"username":string,"password":string,"user_type":string('^(admin|user|expert)$'),"ID":string,"department":string,"field":string,"admission_year":int,"phone":string,'invitation_code':string,'realm':string}
  ```

#### project

- **说明**：

  此表用于储存建立的项目的基本信息。项目信息包括__项目名称__(project_name)、__（第一）作者邮箱__(author_email)、__（第一）作者姓名__(author_name)、__项目编码__(project_code)、__项目状态__(project_status)、__参加竞赛的id__(competition_id)和一个__项目报名表对象__(registration_form)、__项目文件__(project_files)、__已接受评审的专家数__(ac_exp_num)。

  用以唯一识别的字段为__项目编码__。

- **对象字段要求**：

  ```python
  {"project_name":string,"author_email":string,"author_ename":string,"project_code":string,"competition_id":string(空串或者competition表中存在的"_id"),"project_status":int,"registration_form":form对象,"project_files":[{"file_type":string('^(photo|video|doc)$'),"file_path":string0}],"ac_exp_num":int}
  ```

- **其他**：

  "project_status"字段编码解释：

  ```
  -2：初审未通过
  -1：编辑中
  0：已提交
  1：通过初审，专家评审中
  2：凉凉
  3：进入现场答辩
  4：优秀奖
  5：三等奖
  6：二等奖
  7：一等奖!!!
  ```

  form对象格式如下：

  ```python
  {
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
  'name':'xxx',
  'stuId':'xxx',
  'education':'xxx',
  'phone':'xxx',
  'email'：'xxx'}]
  16.表2作品名称title
  17.表2作品类型type（A,B,C,D,E,F）
  18.作品总体情况说明description
  19.创新点creation
  20.关键词keyword
  21.作品可展示形式display['display1','display2',...,'display8']
  22.作品调查方式investigation['investigation1','investigation2',...,'investigation15']
  }
  ```

#### expert_project

- **说明**:

  此表用于储存专家和项目的关系信息。由于需要实现多对多关系。项目信息包括__项目编码__(project_code)、__专家邮箱__(expert_mail)、__专家姓名__(username)、__专家评分__(score)、__评审意见__(suggestion)、__专家回应状态__(status)、**发送邀请的时间**(invite_date)。

- __对象字段要求__：

  ```
  {"project_code":string,"expert_mail":string,"username":string,"score":int,"suggestion":string,'invitation_code':string,'status':string('待回应|已接受|已拒绝|已评审')}
  ```

- **其他**：

  "status"字段编码解释：

  ```
  -1：待回应
  0：已接受
  1：已拒绝
  2：已评审
  ```

#### competition

- **说明**：

  此表用于储存学生和项目的关系信息。由于需要实现多对多关系。项目信息包括__竞赛名称__(competition_name)、__开始时间__(begin_time)、__提交截止__(submission_ddl)、__初审截止__(first_review_ddl)、__专家初评截止__(expert_comments_ddl)、__现场赛选拔截止__(live_selection_ddl)、__结束时间__(end_time)、__竞赛状态__(com_status,-1,0,1,2,3,4,5)、__竞赛简介__(introduction，只用于发布公告)。

- __其他__：

  - 用以唯一识别的字段为自动生成的"_id"

  - "project_status"字段编码解释：

    ```
    -1：未开始
    0：报名提交阶段
    1：校团委初审阶段
    2：专家初评阶段
    3：现场答辩阶段
    4：最终结果公布
    5：已结束
    ```

- **对象字段要求**：

  ```python
  {"competition_name":string,"":string}...
  ```

#### news

- **说明**：

  此表用于储存校团委发布公告.项目信息包括__公告编码__(news_code)、__公告题目__(title)、__公告时间__(time)、__公告内容__(content)、__公告附件__(files)

- **其他**：

  - 用以唯一识别的字段为自动生成的"_id"

  - 附件字段为地址列表

