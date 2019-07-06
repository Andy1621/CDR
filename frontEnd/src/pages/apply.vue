<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <h1>作品提交内容填写</h1>
            <Steps :current="current" style="margin: 30px" :class="readonly?'steps-readonly':''">
                <Step title="作品基本信息" content="" @click.native="readonly?current=0:current=current"></Step>
                <Step title="申请者信息" content="" @click.native="readonly?current=1:current=current"></Step>
                <Step title="作品详细信息" content="" @click.native="readonly?current=2:current=current"></Step>
                <Step title="附件上传" content="" @click.native="readonly?current=3:current=current"></Step>
            </Steps>
            <Divider/>
            <div class="form" v-show="current == 0">
                <p style="margin: 0 0 20px 20px;color: #8391a5;font-size: 15px">作品编号：{{basicInfo.workCode}}（系统自动生成）</p>
                <Form ref="basicInfo" :model="basicInfo" :rules="ruleBasicInfo" :label-width="80">
                    <FormItem label="作品名称" prop="project">
                        <Input v-model="basicInfo.project" :disabled="readonly" placeholder="请输入作品名称"></Input>
                    </FormItem>
                    <FormItem label="院系名称" prop="college">
                        <Input v-model="basicInfo.college" :disabled="readonly" placeholder="请输入院系名称"></Input>
                    </FormItem>
                    <FormItem label="作品类别" prop="type">
                        <Select v-model="basicInfo.type" :disabled="readonly">
                            <Option value="type1">科技发明制作</Option>
                            <Option value="type2">调查报告和学术论文</Option>
                        </Select>
                    </FormItem>
                </Form>
            </div>
            <div class="form" v-show="current == 1">
                <h4 style="margin-bottom: 20px">第一作者信息</h4>
                <Form ref="authorInfo" :model="authorInfo" :rules="ruleAuthorInfo" :label-width="80">
                    <Row>
                        <Col span="12">
                            <FormItem label="姓名" prop="name">
                                <Input v-model="authorInfo.name" :disabled="readonly" placeholder="请输入姓名"></Input>
                            </FormItem>
                        </Col>
                        <Col span="12">
                            <FormItem label="学号" prop="stu_id">
                                <Input v-model="authorInfo.stu_id" :disabled="readonly" placeholder="请输入学号"></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <FormItem label="出生年月" prop="birth">
                        <DatePicker v-model="authorInfo.birth" type="month" :disabled="readonly" placeholder="请选择出生年月"></DatePicker>
                    </FormItem>
                    <Row>
                        <Col span="12">
                            <FormItem label="现学历" prop="edu_background">
                                <Select v-model="authorInfo.edu_background" :disabled="readonly">
                                    <Option value="A">A.专科</Option>
                                    <Option value="B">B.大学本科</Option>
                                    <Option value="C">C.硕士研究生</Option>
                                    <Option value="D">D.博士研究生</Option>
                                </Select>
                            </FormItem>
                        </Col>
                        <Col span="12">
                            <FormItem label="专业" prop="major">
                                <Input v-model="authorInfo.major" :disabled="readonly" placeholder="请输入专业名称"></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <FormItem label="入学时间" prop="school_date">
                        <Row>
                            <Col span="12">
                                <DatePicker v-model="authorInfo.school_date" type="month" :disabled="readonly" placeholder="请选择入学时间"></DatePicker>
                            </Col>
                        </Row>
                    </FormItem>
                    <FormItem label="作品全称" prop="project">
                        <Input v-model="authorInfo.project" :disabled="readonly" placeholder="请输入作品全称"></Input>
                    </FormItem>
                    <FormItem label="通讯地址" prop="address">
                        <Input v-model="authorInfo.address" :disabled="readonly" placeholder="请输入通讯地址"></Input>
                    </FormItem>
                    <Row>
                        <Col span="12">
                            <FormItem label="联系电话" prop="phone">
                                <Input v-model="authorInfo.phone" :disabled="readonly" placeholder="请输入联系电话"></Input>
                            </FormItem>
                        </Col>
                        <Col span="12">
                            <FormItem label="邮箱" prop="email">
                                <Input v-model="authorInfo.email" :disabled="readonly" placeholder="请输入邮箱"></Input>
                            </FormItem>
                        </Col>
                    </Row>
                    <h4 style="margin-bottom: 20px">合作者信息</h4>
                    <h5 v-show="authorInfo.cooperators.length==0">暂无合作者</h5>
                    <Button :disabled="authorInfo.cooperators.length>=4" v-show="!readonly" @click="add_cooperator">添加合作者</Button>
                    <Button :disabled="authorInfo.cooperators.length==0" v-show="!readonly" @click="del_cooperator">删除合作者</Button>
                    <Row v-for="(item,index) in authorInfo.cooperators" :key="index">
                        <h5>合作者{{index+1}}</h5>
                        <Col span="8">
                            <FormItem label="姓名" :key="index" :prop="'cooperators.'+ index +'.name'" :rules="{required: true, message:'姓名不能为空', trigger: 'blur'}">
                                <Input v-model="item.name" :disabled="readonly" placeholder=""></Input>
                            </FormItem>
                        </Col>
                        <Col span="8">
                            <FormItem label="学号" :key="index" :prop="'cooperators.'+ index +'.stuId'" :rules="{required: true, message:'学号不能为空', trigger: 'blur'}">
                                <Input v-model="item.stuId" :disabled="readonly" placeholder=""></Input>
                            </FormItem>
                        </Col>
                        <Col span="8">
                            <FormItem label="现学历" :key="index" :prop="'cooperators.'+ index +'.education'" :rules="{required: true, message:'请选择现学历', trigger: 'change'}">
                                <Select v-model="item.education" :disabled="readonly">
                                    <Option value="A">A.专科</Option>
                                    <Option value="B">B.大学本科</Option>
                                    <Option value="C">C.硕士研究生</Option>
                                    <Option value="D">D.博士研究生</Option>
                                </Select>
                            </FormItem>
                        </Col>
                        <Col span="12">
                            <FormItem label="联系电话" :key="index" :prop="'cooperators.'+ index +'.phone'" :rules="{required: true, message:'联系电话不能为空', trigger: 'blur'}">
                                <Input v-model="item.phone" :disabled="readonly" placeholder=""></Input>
                            </FormItem>
                        </Col>
                        <Col span="12">
                            <FormItem label="邮箱"  :key="index" :prop="'cooperators.'+ index +'.email'" :rules="{required: true, message:'邮箱为空或格式错误', type: 'email', trigger: 'blur'}">
                                <Input v-model="item.email" :disabled="readonly" placeholder=""></Input>
                            </FormItem>
                        </Col>
                    </Row>
                </Form>
            </div>
            <div class="form" v-show="current == 2">
                <Form ref="projectInfo" :model="projectInfo" :rules="ruleProjectInfo" :label-width="80">
                    <FormItem label="作品全称" prop="project">
                        <Input v-model="projectInfo.project" :disabled="readonly" placeholder="请输入作品全称"></Input>
                    </FormItem>
                    <FormItem label="作品分类" prop="type">
                        <Select v-model="projectInfo.type" :disabled="readonly">
                            <Option value="A">A.机械与控制（包括机械、仪器仪表、自动化控制、工程、交通、建筑等）</Option>
                            <Option value="B">B.信息技术（包括计算机、电信、通讯、电子等）</Option>
                            <Option value="C">C.数理（包括数学、物理、地球与空间科学等）</Option>
                            <Option value="D">D.生命科学（包括生物､农学､药学､医学､健康､卫生､食品等）</Option>
                            <Option value="E">E.能源化工（包括能源、材料、石油、化学、化工、生态、环保等）</Option>
                            <Option value="F">F.哲学社会科学（包括哲学、经济、社会、法律、教育、管理）</Option>
                        </Select>
                    </FormItem>
                    <FormItem label="作品情况" prop="introduction">
                        <Input v-model="projectInfo.introduction" :disabled="readonly" type="textarea" :maxlength="800" :rows="4" :autosize="{minRows: 4,maxRows: 4}" placeholder="请输入作品整体情况说明（不超过800字）"></Input>
                    </FormItem>
                    <FormItem label="创新点" prop="innovation">
                        <Input v-model="projectInfo.innovation" :disabled="readonly" type="textarea" :rows="3" :autosize="{minRows: 3,maxRows: 3}" placeholder="1-5条体现作品主要创意的创新点"></Input>
                    </FormItem>
                    <FormItem label="关键词" prop="keyword">
                        <Input v-model="projectInfo.keyword" :disabled="readonly" type="textarea" :rows="3" :autosize="{minRows: 3,maxRows: 3}" placeholder="4-7个体现作品核心技术和问题的关键词"></Input>
                    </FormItem>
                    <FormItem label="展示形式" v-if="basicInfo.type=='type1'" prop="display">
                        <CheckboxGroup style="row: 3;" v-model="projectInfo.display" :disabled="readonly">
                            <Checkbox label="display1" :disabled="readonly">
                                <span>实物、产品</span>
                            </Checkbox>
                            <Checkbox label="display2" :disabled="readonly">
                                <span>模型</span>
                            </Checkbox>
                            <Checkbox label="display3" :disabled="readonly">
                                <span>图纸</span>
                            </Checkbox>
                            <Checkbox label="display4" :disabled="readonly">
                                <span>磁盘</span>
                            </Checkbox>
                            <Checkbox label="display5" :disabled="readonly">
                                <span>现场演示</span>
                            </Checkbox>
                            <Checkbox label="display6" :disabled="readonly">
                                <span>图片</span>
                            </Checkbox>
                            <Checkbox label="display7" :disabled="readonly">
                                <span>录像</span>
                            </Checkbox>
                            <Checkbox label="display8" :disabled="readonly">
                                <span>样品</span>
                            </Checkbox>
                        </CheckboxGroup>
                    </FormItem>
                    <FormItem label="调查方式" v-if="basicInfo.type=='type2'" prop="investigation">
                        <CheckboxGroup v-model="projectInfo.investigation">
                            <Checkbox label="investigation1" :disabled="readonly">
                                <span>走访</span>
                            </Checkbox>
                            <Checkbox label="investigation2" :disabled="readonly">
                                <span>问卷</span>
                            </Checkbox>
                            <Checkbox label="investigation3" :disabled="readonly">
                                <span>现场采访</span>
                            </Checkbox>
                            <Checkbox label="investigation4" :disabled="readonly">
                                <span>人员介绍</span>
                            </Checkbox>
                            <Checkbox label="investigation5" :disabled="readonly">
                                <span>个别交谈</span>
                            </Checkbox>
                            <Checkbox label="investigation6" :disabled="readonly">
                                <span>亲临实践</span>
                            </Checkbox>
                            <Checkbox label="investigation7" :disabled="readonly">
                                <span>会议</span>
                            </Checkbox>
                            <Checkbox label="investigation8" :disabled="readonly">
                                <span>图片、照片</span>
                            </Checkbox>
                            <Checkbox label="investigation9" :disabled="readonly">
                                <span>书报刊物</span>
                            </Checkbox>
                            <Checkbox label="investigation10" :disabled="readonly">
                                <span>统计报表</span>
                            </Checkbox>
                            <Checkbox label="investigation11" :disabled="readonly">
                                <span>影视资料</span>
                            </Checkbox>
                            <Checkbox label="investigation12" :disabled="readonly">
                                <span>文件</span>
                            </Checkbox>
                            <Checkbox label="investigation13" :disabled="readonly">
                                <span>集体组织</span>
                            </Checkbox>
                            <Checkbox label="investigation14" :disabled="readonly">
                                <span>自发</span>
                            </Checkbox>
                            <Checkbox label="investigation15" :disabled="readonly">
                                <span>其它</span>
                            </Checkbox>
                        </CheckboxGroup>
                    </FormItem>
                </Form>
            </div>
            <div class="form" v-show="current == 3">
                <h4 style="margin-bottom: 20px">相关文档（仅限PDF）</h4>
                <div v-show="readonly" class="show-upload">
                    <ul>
                        <li v-for="item in uploadDocList" @click="docView(item)">
                            <Icon type="md-document"></Icon>{{item.name}}
                        </li>
                    </ul>
                </div>
                <Upload
                    ref="uploadDoc"
                    v-show="!readonly"
                    :show-upload-list="true"
                    :default-file-list="defaultDocList"
                    :on-success="handleSuccessDoc"
                    :on-remove="handleRemoveDoc"
                    :on-preview="docView"
                    :format="['pdf']"
                    :max-size="20480"
                    :on-format-error="handleFormatErrorDoc"
                    :on-exceeded-size="handleMaxSizeDoc"
                    :before-upload="handleBeforeUploadDoc"
                    :action = "up_url"
                    :data = type_doc
                    style="display: inline-block">
                    <Button icon="ios-document" style="width: 100px">文档上传</Button>
                </Upload>
                <Divider/>
                <h4 style="margin-bottom: 20px">作品图片（{{photo_cnt}}/5）</h4>
                <div v-if="false" class="demo-upload-list" v-for="item in uploadPhotoList">
                    <template v-if="item.status === 'finished'">
                        <img :src="item.url">
                        <div class="demo-upload-list-cover">
                            <Icon type="ios-eye-outline" @click.native="handleView(item.url)"></Icon>
                            <Icon type="ios-trash-outline" @click.native="handleRemove(item)" v-show="!readonly"></Icon>
                        </div>
                    </template>
                    <template v-else>
                        <Progress style="margin-top: 20px" v-if="item.showProgress" :percent="item.percentage" hide-info></Progress>
                    </template>
                </div>
                <div v-show="readonly" class="show-upload">
                    <ul>
                        <li v-for="item in uploadPhotoList" @click="photoView(item)">
                            <Icon type="ios-image"></Icon>{{item.name}}
                        </li>
                    </ul>
                </div>
                <Upload
                    ref="uploadPhoto"
                    v-show="!readonly"
                    :show-upload-list="true"
                    :default-file-list="defaultPhotoList"
                    :on-success="handleSuccess"
                    :on-remove="handleRemove"
                    :on-preview="photoView"
                    :format="['jpg','jpeg','png']"
                    :max-size="2048"
                    :on-format-error="handleFormatError"
                    :on-exceeded-size="handleMaxSize"
                    :before-upload="handleBeforeUpload"
                    type="select"
                    :action="up_url"
                    :data = type_photo
                    style="display: inline-block">
<!--                    <div style="width: 96px;height:96px;line-height: 100px;">-->
<!--                        <Icon type="ios-camera" size="30"></Icon>-->
<!--                    </div>-->
                    <Button :disabled="photo_cnt>=5" icon="ios-image" style="width: 100px">图片上传</Button>
                </Upload>
                <Modal title="预览图片" draggable v-model="visible">
                    <img :src="imgUrl" v-if="visible" style="width: 100%">
                </Modal>
                <Divider/>
                <h4 style="margin-bottom: 20px">作品视频（仅限 mp4）</h4>
                <div v-show="readonly" class="show-upload">
                    <ul>
                        <li v-for="item in uploadVideoList" @click="videoView(item)">
                            <Icon type="ios-film"></Icon> {{item.name}}
                        </li>
                    </ul>
                </div>
                <Upload
                    ref="uploadVideo"
                    v-show="!readonly"
                    :show-upload-list="true"
                    :default-file-list="defaultVideoList"
                    :on-success="handleSuccessVideo"
                    :on-remove="handleRemoveVideo"
                    :on-preview="videoView"
                    :format="['mp4']"
                    :max-size="102400"
                    :on-format-error="handleFormatErrorVideo"
                    :on-exceeded-size="handleMaxSizeVideo"
                    :before-upload="handleBeforeUploadVideo"
                    :action="up_url"
                    :data = type_video
                    style="display: inline-block">
                    <Button :disabled="video_cnt>=1" icon="ios-videocam" style="width: 100px">视频上传</Button>
                </Upload>
            </div>
            <Button @click="check_table" style="margin-right: 20px;">预览表格</Button>
            <Button type="primary" :disabled="current == 0" @click="pre_step">上一步</Button>
            <Button type="primary" :disabled="current == 3" @click="next_step">下一步</Button>
            <Button type="primary" v-show="!readonly" @click="save_data" style="margin-left: 20px">保存到草稿箱</Button>
            <Button type="success" v-show="current == 3 && !readonly" @click="submit_project">提交</Button>
        </div>
    </div>
</template>

<script>
    import NavBar from '../components/NavBar.vue'
    export default {
        name: "apply",
        components:{
            NavBar
        },
        data(){
            return{
                current: 3,
                readonly: false,
                project_id: '',
                photo_cnt: 0,
                video_cnt: 0,
                change_btn_click: false,
                up_url: this.$baseURL + '/api/v1/up_file',
                type_doc: {
                    'file_type' : 'doc',
                    'project_code' : '',
                },
                type_video: {
                    'file_type' : 'video',
                    'project_code' : '',
                },
                type_photo: {
                    'file_type' : 'photo',
                    'project_code' : '',
                },
                //basic info
                basicInfo:{
                    workCode: '',
                    project: '',
                    college: '',
                    type: '',
                },
                ruleBasicInfo:{
                    project: [
                        { required: true, message: '作品名称不能为空', trigger: 'blur' }
                    ],
                    college: [
                        { required: true, message: '院系名称不能为空', trigger: 'blur' }
                    ],
                    type: [
                        { required: true, message: '请选择作品类别', trigger: 'change' }
                    ],
                },
                //author info
                authorInfo:{
                    name: '',
                    stu_id: '',
                    birth: '',
                    edu_background: '',
                    major: '',
                    school_date: '',
                    project: '',
                    address: '',
                    phone: '',
                    email: '',
                    cooperators: []
                },
                ruleAuthorInfo:{
                    name: [
                        { required: true, message: '姓名不能为空', trigger: 'blur' }
                    ],
                    stu_id: [
                        { required: true, message: '学号不能为空', trigger: 'blur' }
                    ],
                    birth: [
                        { required: true, type:'date', message: '出生年月不能为空', trigger: 'change' }
                    ],
                    edu_background: [
                        { required: true, message: '现学历不能为空', trigger: 'change' }
                    ],
                    major: [
                        { required: true, message: '专业不能为空', trigger: 'blur' }
                    ],
                    school_date: [
                        { required: true, type:'date', message: '入学时间不能为空', trigger: 'change' }
                    ],
                    project: [
                        { required: true, message: '作品全称不能为空', trigger: 'blur' }
                    ],
                    address: [
                        { required: true, message: '通讯地址不能为空', trigger: 'blur' }
                    ],
                    phone: [
                        { required: true, message: '联系电话不能为空', trigger: 'blur' }
                    ],
                    email: [
                        { required: true, message: '邮箱不能为空', trigger: 'blur' },
                        { type: 'email', message: '邮箱格式错误', trigger: 'blur' }
                    ],
                    cooperators: [
                        { required:true, message: '不能为空', trigger: 'blur' }
                    ]
                },
                // project info
                projectInfo:{
                    project: '',
                    type: '',
                    introduction: '',
                    innovation: '',
                    keyword: '',
                    display: [],
                    investigation: [],
                },
                ruleProjectInfo:{
                    project: [
                        { required: true, message: '作品全称不能为空', trigger: 'blur' }
                    ],
                    type: [
                        { required: true, message: '请选择作品类别', trigger: 'change' }
                    ],
                    introduction: [
                        { required: true, message: '作品情况不能为空', trigger: 'blur' }
                    ],
                    innovation: [
                        { required: true, message: '创新点不能为空', trigger: 'blur' }
                    ],
                    keyword: [
                        { required: true, message: '关键词不能为空', trigger: 'blur' }
                    ],
                    display: [
                        { required:true, type:'array', min: 1, message: '请选择作品展示形式', trigger:'change' }
                    ],
                    investigation: [
                        { required:true, type:'array', min: 1, message: '请选择作品调查方式', trigger:'change' }
                    ]
                },
                // upload
                defaultDocList: [],
                defaultPhotoList: [
                    // {
                    //     'name': 'file3.jpg',
                    //     'url': 'https://o5wwk8baw.qnssl.com/7eb99afb9d5f317c912f08b5212fd69a/avatar'
                    // }
                ],
                defaultVideoList: [],
                imgUrl: '',
                visible: false,
                fileList: [],
                uploadPhotoList: [],
                uploadVideoList: [],
                uploadDocList: [],
            }
        },
        methods:{
            add_cooperator(){
                // console.log(this.authorInfo.cooperators);
                this.authorInfo.cooperators.push({
                    name: '',
                    stuId: '',
                    education: '',
                    phone: '',
                    email: '',
                });
            },
            del_cooperator(){
                this.authorInfo.cooperators.pop();
            },
            next_step(){
                console.log(this.authorInfo.cooperators)
                if(this.readonly){
                    this.current += 1;
                }
                else{
                    var check_name;
                    switch (this.current){
                        case 0:
                            check_name = 'basicInfo';
                            break;
                        case 1:
                            check_name = 'authorInfo';
                            break;
                        case 2:
                            check_name = 'projectInfo';
                            break;
                        case 3:
                            check_name = 'basicInfo';
                            break;
                    }
                    this.$refs[check_name].validate((valid) => {
                        if (valid) {
                            // this.$Message.success('Success!');
                            this.current += 1;
                            this.change_btn_click = true;
                            this.save_data();
                        } else {
                            this.$Message.error('信息有误');
                        }
                    });
                }
            },
            pre_step(){
                if(this.readonly){
                    this.current -= 1;
                }
                else{
                    this.current -= 1;
                    this.change_btn_click = true;
                    this.save_data();
                }
            },
            check_table(){
                // check table
                // this.$Message.info('Check Table')
                this.$http.get(this.$baseURL + '/api/v1/view_apply',{params:{'project_code': this.project_id}})
                    .then(function (res) {
                        var detail = res.body
                        console.log(detail)
                        if(detail.state == 'fail'){
                            this.$Message.error(detail.reason)
                        }
                        else{
                            // this.$Message.success('Yeeeees')
                            // window.location.href = detail.html_url
                            window.open(detail.html_url)
                        }
                    },function (res) {
                        this.$Message.error('Failed')
                    })
            },
            save_data(){
                // save data function
                // this.$Message.info('Save Data')
                console.log(this.authorInfo.birth)
                var birth = this.authorInfo.birth.toString().replace('00:00:00','08:00:00')
                this.authorInfo.birth = new Date(birth)
                var enter = this.authorInfo.school_date.toString().replace('00:00:00','08:00:00')
                this.authorInfo.school_date = new Date(enter)

                if(this.basicInfo.type == 'type1'){
                    this.projectInfo.investigation = [];
                }
                else{
                    this.projectInfo.display = [];
                }

                let params = {
                    'workCode' : this.basicInfo.workCode,
                    'mainTitle' : this.basicInfo.project,
                    'department' : this.basicInfo.college,
                    'mainType' : this.basicInfo.type,

                    'name' : this.authorInfo.name,
                    'stuId' : this.authorInfo.stu_id,
                    'birthday' : this.authorInfo.birth,
                    'education' : this.authorInfo.edu_background,
                    'major' : this.authorInfo.major,
                    'enterTime' : this.authorInfo.school_date,
                    'totalTitle' : this.authorInfo.project,
                    'address' : this.authorInfo.address,
                    'phone' : this.authorInfo.phone,
                    'email' : this.authorInfo.email,
                    'applier' : this.authorInfo.cooperators,

                    'title' : this.projectInfo.project,
                    'type' : this.projectInfo.type,
                    'description' : this.projectInfo.introduction,
                    'creation' : this.projectInfo.innovation,
                    'keyword' : this.projectInfo.keyword,
                    'display' : this.projectInfo.display,
                    'investigation' : this.projectInfo.investigation
                };
                this.$http.post(this.$baseURL + '/api/v1/store_project',params)
                    .then(function (res) {
                        var detail = res.body;
                        console.log(detail)
                        if(detail.state == 'fail'){
                            this.$Message.error('保存失败 ' + detail.reason)
                            return false
                        }
                        else{
                            if(!this.change_btn_click)
                                this.$Message.success('保存成功')
                            this.change_btn_click = false;
                            return true
                        }
                    },function (res) {
                        this.$Message.error('Failed')
                    })
            },
            submit_project(){
                this.uploadPhotoList = this.$refs.uploadPhoto.fileList
                this.uploadVideoList = this.$refs.uploadVideo.fileList
                this.uploadDocList = this.$refs.uploadDoc.fileList
                // console.log(this.uploadPhotoList)
                // console.log(this.uploadVideoList)
                // console.log(this.uploadDocList)
                // console.log(this.$refs.uploadPhoto.fileList)
                // console.log(this.$refs.uploadVideo.fileList)
                // console.log(this.$refs.uploadDoc.fileList)

                var birth = this.authorInfo.birth.toString().replace('00:00:00','08:00:00')
                this.authorInfo.birth = new Date(birth)
                var enter = this.authorInfo.school_date.toString().replace('00:00:00','08:00:00')
                this.authorInfo.school_date = new Date(enter)

                let params = {
                    'workCode' : this.basicInfo.workCode,
                    'mainTitle' : this.basicInfo.project,
                    'department' : this.basicInfo.college,
                    'mainType' : this.basicInfo.type,

                    'name' : this.authorInfo.name,
                    'stuId' : this.authorInfo.stu_id,
                    'birthday' : this.authorInfo.birth,
                    'education' : this.authorInfo.edu_background,
                    'major' : this.authorInfo.major,
                    'enterTime' : this.authorInfo.school_date,
                    'totalTitle' : this.authorInfo.project,
                    'address' : this.authorInfo.address,
                    'phone' : this.authorInfo.phone,
                    'email' : this.authorInfo.email,
                    'applier' : this.authorInfo.cooperators,

                    'title' : this.projectInfo.project,
                    'type' : this.projectInfo.type,
                    'description' : this.projectInfo.introduction,
                    'creation' : this.projectInfo.innovation,
                    'keyword' : this.projectInfo.keyword,
                    'display' : this.projectInfo.display,
                    'investigation' : this.projectInfo.investigation
                };
                this.$http.post(this.$baseURL + '/api/v1/submit_project',params)
                    .then(function (res) {
                        var detail = res.body
                        console.log(detail)
                        if(detail.state == 'fail'){
                            this.$Message.error('提交失败')
                        }
                        else{
                            this.$Message.success('提交成功')
                            this.readonly = true
                        }
                    },function (res) {
                        this.$Message.error('Failed')
                    })
            },
            //upload
            handleView (name) {
                this.imgUrl = name;
                this.visible = true;
            },
            photoView(file){
                console.log(file)
                this.imgUrl = file.url;
                this.visible = true;
            },
            handleRemove (file) {
                console.log(file)
                console.log(file.name)
                console.log(this.project_id)
                const fileList = this.$refs.uploadPhoto.fileList;
                this.$http.get(this.$baseURL + '/api/v1/delete_file',{params:{'type':'photo','file_name':file.name,'project_code':this.project_id}})
                    .then(function (res) {
                        console.log(res.body)
                        if(res.body.state == 'fail'){
                            this.$Message.error('删除失败 '+ res.body.reason)
                            this.$refs.uploadPhoto.fileList.push(file)
                        }
                        else{
                            console.log('Success')
                            this.photo_cnt -= 1
                            // this.$refs.uploadPhoto.fileList.splice(fileList.indexOf(file), 1);
                        }
                    })
                },
            handleSuccess (res, file) {
                console.log(res)
                if(res.state == 'fail'){
                    this.$Message.error('上传失败 ' + res.reason);
                    const fileList = this.$refs.uploadPhoto.fileList;
                    this.$refs.uploadPhoto.fileList.splice(fileList.indexOf(file), 1);
                }
                else{
                    this.$Message.success('成功上传 '+file.name)
                    file.url = res.url;
                    this.photo_cnt += 1
                    var list = this.$refs.uploadPhoto.fileList
                    // console.log(file)
                    // console.log(list)
                    for(var item of list){
                        if(item.name == file.name && list.indexOf(item)!=list.length-1){
                            this.$refs.uploadPhoto.fileList.splice(list.indexOf(item),1)
                            this.photo_cnt -= 1
                            break
                        }
                    }
                    // this.refresh_list()
                    console.log(this.uploadPhotoList)
                }
            },
            handleFormatError (file) {
                this.$Notice.warning({
                    title: '文件格式错误',
                    desc: '文件 ' + file.name + ' 格式错误请选择 jpg 或 png 格式'
                });
            },
            handleMaxSize (file) {
                this.$Notice.warning({
                    title: '文件过大',
                    desc: '文件  ' + file.name + ' 过大，不能超过2M'
                });
            },
            handleBeforeUpload () {
                const check = this.photo_cnt < 5;
                if (!check) {
                    this.$Notice.warning({
                        title: '最多只能上传5张图片'
                    });
                }
                return check;
            },
            //upload video
            videoView(file){
                console.log(file)
                if(file.url)
                    window.open(file.url)
                else
                    window.open(file.response.url)
            },
            handleSuccessVideo (res, file) {
                console.log(res);
                if(res.state == 'fail')
                    this.$Message.error('上传失败 ' + res.reason);
                else{
                    this.$Message.success('成功上传 '+file.name)
                    file.url = res.file_path;
                    this.video_cnt += 1;
                    var list = this.$refs.uploadVideo.fileList
                    // console.log(file)
                    // console.log(list)
                    for(var item of list){
                        if(item.name == file.name && list.indexOf(item)!=list.length-1){
                            this.$refs.uploadVideo.fileList.splice(list.indexOf(item),1)
                            this.video_cnt -= 1
                            break
                        }
                    }
                }
            },
            handleRemoveVideo(file){
                console.log(file)
                this.$http.get(this.$baseURL + '/api/v1/delete_file',{params:{'type':'video','file_name':file.name,'project_code':this.project_id}})
                    .then(function (res) {
                        console.log(res.body)
                        if(res.body.state == 'fail'){
                            this.$Message.error('删除失败 '+ res.body.reason)
                            this.$refs.uploadVideo.fileList.push(file)
                        }
                        else{
                            console.log('Success')
                            this.video_cnt -= 1;
                        }
                    })
            },
            handleFormatErrorVideo (file) {
                this.$Notice.warning({
                    title: '文件格式错误',
                    desc: '文件 ' + file.name + ' 格式错误请选择 mp4 格式'
                });
            },
            handleMaxSizeVideo (file) {
                this.$Notice.warning({
                    title: '文件过大',
                    desc: '文件  ' + file.name + ' 过大，不能超过100M'
                });
            },
            handleBeforeUploadVideo (file) {
                const check = this.video_cnt < 1;
                if (!check) {
                    this.$Notice.warning({
                        title: '最多只能上传1个视频'
                    });
                }
                console.log(file)
                var url = URL.createObjectURL(file);
                 //经测试，发现audio也可获取视频的时长
                var audioElement = new Audio(url);
                var time
                var duration
                var that = this
                // audioElement.addEventListener("loadedmetadata", function (_event) {
                //     time = audioElement.duration;
                //     console.log(time);
                //     duration = time <= 5*60 ? true : false
                //     console.log(duration)
                //     if (!duration) {
                //         that.$Notice.warning({
                //             title: '视频时长不得大于5分钟'
                //         });
                //     }
                //     console.log(check && duration)
                //     return check && duration;
                // });
                var promise = new Promise(function(resolve, reject){
                    audioElement.addEventListener("loadedmetadata", function (_event) {
                        time = audioElement.duration;
                        // console.log(time);
                        duration = time <= 5*60+1 ? true : false
                        // console.log(duration)
                        if (!duration) {
                            that.$Notice.warning({
                                title: '视频时长不得大于5分钟'
                            });
                        }
                        // console.log(check && duration)
                        if(check && duration)
                            resolve()
                        else
                            reject()
                    })
                });
                return promise;
            },
            //upload file
            docView(file){
                console.log(file)
                if(file.url)
                    window.open(file.url)
                else
                    window.open(file.response.url)
            },
            handleSuccessDoc (res, file) {
                console.log(res);
                if(res.state == 'fail')
                    this.$Message.error('上传失败 ' + res.reason);
                else{
                    this.$Message.success('成功上传 '+file.name)
                    file.url = res.file_path;
                    var list = this.$refs.uploadDoc.fileList
                    // console.log(file)
                    // console.log(list)
                    for(var item of list){
                        if(item.name == file.name && list.indexOf(item)!=list.length-1){
                            this.$refs.uploadDoc.fileList.splice(list.indexOf(item),1)
                            break
                        }
                    }
                }
            },
            handleRemoveDoc (file, fileList){
                console.log("this is file")
                console.log(file.name + this.project_id)
                this.$http.get(this.$baseURL + '/api/v1/delete_file',{params:{'type':'doc','file_name':file.name,'project_code':this.project_id}})
                    .then(function (res) {
                        console.log(res.body)
                        if(res.body.state == 'fail'){
                            this.$Message.error('删除失败 '+ res.body.reason)
                            this.$refs.uploadDoc.fileList.push(file)
                        }
                        else{
                            console.log('Success')
                        }
                    })
            },
            handleFormatErrorDoc (file) {
                this.$Notice.warning({
                    title: '文件格式错误',
                    desc: '文件 ' + file.name + ' 格式错误请选择 pdf 格式'
                });
            },
            handleMaxSizeDoc (file) {
                this.$Notice.warning({
                    title: '文件过大',
                    desc: '文件  ' + file.name + ' 过大，不能超过20M'
                });
            },
            handleBeforeUploadDoc () {
                const check = this.uploadDocList.length < 100;
                if (!check) {
                    this.$Notice.warning({
                        title: '最多只能上传100个文件'
                    });
                }
                return check;
            },
            //upload end
            get_project_detail(project_id){
                this.$http.get(this.$baseURL + '/api/v1/get_project_detail',{params:{'project_code': project_id}})
                    .then(function (res) {
                        var detail = res.body;
                        console.log(res.body);
                        if(detail.state == 'fail' && detail.reason == '项目不存在'){
                            console.log()
                        }
                        else{
                            this.readonly = detail.project.project_status !== -1;
                            var form = detail.project.registration_form;
                            console.log(form)
                            this.fileList = detail.project.project_files;
                            for(let item of this.fileList){
                                switch(item.file_type){
                                    case 'doc':
                                        this.defaultDocList.push({
                                            'name' : item.file_name,
                                            'url' : item.file_path,
                                        });
                                        break;
                                    case 'photo':
                                        this.defaultPhotoList.push({
                                            'name' : item.file_name,
                                            'url' : item.file_path,
                                        });
                                        break;
                                    case 'video':
                                        this.defaultVideoList.push({
                                            'name' : item.file_name,
                                            'url' : item.file_path,
                                        });
                                        break;
                                }
                            }

                            this.photo_cnt = this.defaultPhotoList.length
                            this.video_cnt = this.defaultVideoList.length
                            this.project_id = form.workCode;
                            // console.log(form.workCode)
                            this.type_doc = {
                                'file_type' : 'doc',
                                'project_code' : form.workCode,
                            };
                            this.type_video = {
                                'file_type' : 'video',
                                'project_code' : form.workCode,
                            };
                            this.type_photo = {
                                'file_type' : 'photo',
                                'project_code' : form.workCode,
                            };
                            this.basicInfo.workCode = form.workCode;
                            this.basicInfo.project = form.mainTitle;
                            this.basicInfo.college = form.department;
                            this.basicInfo.type = form.mainType;

                            this.authorInfo.name = form.name;
                            this.authorInfo.stu_id = form.stuId;
                            // console.log(form.birthday.length)
                            var nowdate = new Date()
                            // console.log(nowdate)
                            this.authorInfo.birth = form.birthday.length>0 ? form.birthday: nowdate;
                            this.authorInfo.edu_background = form.education;
                            this.authorInfo.major = form.major;
                            this.authorInfo.school_date = form.enterTime.length>0 ? form.enterTime: nowdate;
                            this.authorInfo.project = form.totalTitle;
                            this.authorInfo.address = form.address;
                            this.authorInfo.phone = form.phone;
                            this.authorInfo.email = form.email;
                            this.authorInfo.cooperators = form.applier;

                            this.projectInfo.project = form.title;
                            this.projectInfo.type = form.type;
                            this.projectInfo.introduction = form.description;
                            this.projectInfo.innovation = form.creation;
                            this.projectInfo.keyword = form.keyword;
                            this.projectInfo.display = form.display;
                            this.projectInfo.investigation = form.investigation;
                        }
                    },function (res) {
                        console.log('Failed')
                    })
            },
        },
        mounted () {
            this.uploadDocList = this.defaultDocList;
            // this.uploadDocList = this.$refs.uploadDoc.fileList.length>0 ? this.$refs.uploadDoc.fileList : this.defaultDocList;
            this.uploadPhotoList = this.defaultPhotoList;
            // this.uploadPhotoList = this.$refs.uploadPhoto.fileList.length>0 ? this.$refs.uploadPhoto.fileList : this.defaultPhotoList;
            this.uploadVideoList = this.defaultVideoList;
            // this.uploadVideoList = this.defaultVideoList.length>0 ? this.$refs.uploadVideo.fileList : this.defaultVideoList;
            // this.uploadPhotoList = this.defaultPhotoList;
            // console.log(this.uploadPhotoList)
            //设置Message默认属性
            this.$Message.config({
                top: 100,
                duration: 1,
            });
        },
        created () {
            // console.log(this.defaultPhotoList)
            this.get_project_detail(this.$route.query.projectID?this.$route.query.projectID:'0001')
        },
    }
</script>

<style scoped>
    .body{
        margin-left: 30%;
        margin-bottom: 50px;
        position: relative;
        top: 100px;
        border: 1px dashed black;
        border-radius: 20px;
        /*margin: 100px 0px 50px 30%;*/
        padding: 20px;
        width: 50%;
        text-align: center;
        min-height: 470px;
        min-width: 600px;
        color: black;
    }
    .form{
        text-align: left;
        padding: 10px;
        margin-bottom: 30px;
        font-size: 15px;
    }
    /*upload*/
    .demo-upload-list{
        display: inline-block;
        width: 100px;
        height: 100px;
        text-align: center;
        line-height: 60px;
        border: 1px solid transparent;
        border-radius: 4px;
        overflow: hidden;
        background: #fff;
        position: relative;
        box-shadow: 0 1px 1px rgba(0,0,0,.2);
        margin-right: 4px;
    }
    .demo-upload-list img{
        width: 100%;
        height: 100%;
    }
    .demo-upload-list-cover{
        display: none;
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(0,0,0,.6);
    }
    .demo-upload-list:hover .demo-upload-list-cover{
        display: block;
    }
    .demo-upload-list-cover i{
        color: #fff;
        font-size: 30px;
        cursor: pointer;
        margin: 0 2px;
        padding-top: 35%;
    }
    #sidebar-nav.sidebar{
        padding-top: 0px;
    }
    .show-upload ul{
        list-style-type: none;
    }
    .show-upload li{
        cursor: default;
        padding: 5px 10px 5px 10px;
        margin: 1px;
        width: fit-content;
        border-radius: 5px;
        color: #666666;
    }
    .show-upload li:hover{
        background: #eeeeee;
        color: #2b85e4;
    }
    .steps-readonly{
        cursor: pointer;
    }
    >>>.ivu-input[disabled]{
        color: black;
        background: white;
        cursor: default;
    }
    >>>.ivu-select-disabled .ivu-select-selection{
        color: black;
        background: white;
        cursor: default;
    }
    >>>.ivu-checkbox-input[disabled] {
       cursor: default
    }
    >>>.ivu-checkbox-disabled .ivu-checkbox-inner-input {
        cursor: default
    }
    >>>.ivu-checkbox-disabled + span {
        color: #515a6e;
        cursor: default
    }
    >>>.ivu-checkbox-wrapper-disabled {
        cursor: default;
    }
</style>
