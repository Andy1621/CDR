<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <h1>作品提交内容填写</h1>
            <Steps :current="current" style="margin: 30px">
                <Step title="作品基本信息" content=""></Step>
                <Step title="申请者信息" content=""></Step>
                <Step title="作品详细信息" content=""></Step>
                <Step title="附件上传" content=""></Step>
            </Steps>
            <Divider/>
            <div class="form" v-show="current == 0">
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
                            <FormItem label="学号" :key="index" :prop="'cooperators.'+ index +'.stu_id'" :rules="{required: true, message:'学号不能为空', trigger: 'blur'}">
                                <Input v-model="item.stu_id" :disabled="readonly" placeholder=""></Input>
                            </FormItem>
                        </Col>
                        <Col span="8">
                            <FormItem label="现学历" :key="index" :prop="'cooperators.'+ index +'.edu'" :rules="{required: true, message:'请选择现学历', trigger: 'change'}">
                                <Select v-model="item.edu" :disabled="readonly">
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
                </Form>
            </div>
            <div class="form" v-show="current == 3">
                <h4 style="margin-bottom: 20px">作品图片上传</h4>
                <div class="demo-upload-list" v-for="item in uploadList">
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
                <Upload
                    v-show="!readonly"
                    ref="upload"
                    :show-upload-list="false"
                    :default-file-list="defaultList"
                    :on-success="handleSuccess"
                    :format="['jpg','jpeg','png']"
                    :max-size="2048"
                    :on-format-error="handleFormatError"
                    :on-exceeded-size="handleMaxSize"
                    :before-upload="handleBeforeUpload"
                    multiple
                    type="drag"
                    action="http://127.0.0.1:5000/api/v1/up_photo"
                    style="display: inline-block;width:96px;">
                    <div style="width: 96px;height:96px;line-height: 100px;">
                        <Icon type="ios-camera" size="30"></Icon>
                    </div>
                </Upload>
                <Modal title="预览图片" v-model="visible">
                    <img :src="imgUrl" v-if="visible" style="width: 100%">
                </Modal>
                <Divider/>
                <h4 style="margin-bottom: 20px">作品视频上传</h4>
                <Upload
                    ref="uploadVideo"
                    :show-upload-list="true"
                    :on-success="handleSuccessVideo"
                    :format="['mp4','flv']"
                    :max-size="102400"
                    :on-format-error="handleFormatErrorVideo"
                    :on-exceeded-size="handleMaxSizeVideo"
                    :before-upload="handleBeforeUploadVideo"
                    action="http://127.0.0.1:5000/api/v1/up_video"
                    style="display: inline-block">
                    <Button :disabled="uploadVideoList.length>=1" v-show="!readonly" icon="ios-videocam" style="width: 100px">上传</Button>
                </Upload>
            </div>
            <Button type="" v-show="current == 3" @click="check_table">预览表格</Button>
            <Button type="primary" :disabled="current == 0" @click="pre_step">上一步</Button>
            <Button type="primary" :disabled="current == 3" @click="next_step">下一步</Button>
            <Button type="primary" v-show="!readonly" @click="save_data" style="margin-left: 20px">保存到草稿箱</Button>
            <Button type="success" v-show="current == 3 && !readonly">提交</Button>
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
                //basic info
                basicInfo:{
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
                    ]
                },
                // upload
                defaultList: [
                    // {
                    //     'name': 'file1',
                    //     'url': 'http://127.0.0.1:5000/static/photo/1561694068_32.3-2.png'
                    // },
                    // {
                    //     'name': 'file2',
                    //     'url': 'http://127.0.0.1:5000/static/photo/Test123.png'
                    // },
                    {
                        'name': 'file3',
                        'url': 'https://o5wwk8baw.qnssl.com/7eb99afb9d5f317c912f08b5212fd69a/avatar'
                    }
                ],
                imgUrl: '',
                visible: false,
                uploadList: [],
                uploadVideoList: [],
            }
        },
        methods:{
            add_cooperator(){
                console.log(this.authorInfo.cooperators);
                this.authorInfo.cooperators.push({
                    name: '',
                    stu_id: '',
                    edu: '',
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
                        } else {
                            this.$Message.error('信息有误');
                        }
                    });
                    this.save_data();
                }
            },
            pre_step(){
                if(this.readonly){
                    this.current -= 1;
                }
                else{
                    this.current -= 1;
                    this.save_data();
                }
            },
            check_table(){
                // check table
                this.$Message.info('Check Table')
            },
            save_data(){
                // save data function
                this.$Message.info('Save Data')
            },
            //upload
            handleView (name) {
                this.imgUrl = name;
                this.visible = true;
            },
            handleRemove (file) {
                const fileList = this.$refs.upload.fileList;
                this.$refs.upload.fileList.splice(fileList.indexOf(file), 1);
            },
            handleSuccess (res, file) {
                // file.url = URL.createObjectURL(file.raw);
                console.log(res)
                if(res.state == 'fail')
                    this.$Message.error('上传失败');
                console.log(file)
                file.url = 'https://o5wwk8baw.qnssl.com/7eb99afb9d5f317c912f08b5212fd69a/avatar';
                file.name = 'defaultfile';
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
                const check = this.uploadList.length < 5;
                if (!check) {
                    this.$Notice.warning({
                        title: '最多只能上传5张图片'
                    });
                }
                return check;
            },
            //upload video
            handleSuccessVideo (res, file) {
                // file.url = URL.createObjectURL(file.raw);
                console.log(res);
                if(res.state == 'fail')
                    this.$Message.error('上传失败');
                console.log(file)
                file.url = 'file/url';
                // file.name = 'filename.flv';
            },
            handleFormatErrorVideo (file) {
                this.$Notice.warning({
                    title: '文件格式错误',
                    desc: '文件 ' + file.name + ' 格式错误请选择 mp4 或 flv 格式'
                });
            },
            handleMaxSizeVideo (file) {
                this.$Notice.warning({
                    title: '文件过大',
                    desc: '文件  ' + file.name + ' 过大，不能超过100M'
                });
            },
            handleBeforeUploadVideo () {
                const check = this.uploadVideoList.length < 1;
                if (!check) {
                    this.$Notice.warning({
                        title: '最多只能上传1个视频'
                    });
                }
                return check;
            },
            //upload end
        },
        mounted () {
            this.uploadList = this.$refs.upload.fileList;
            this.uploadVideoList = this.$refs.uploadVideo.fileList;
            //设置Message默认属性
            this.$Message.config({
                top: 100,
                duration: 1,
            });
        }
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
    /*upload end*/
</style>
