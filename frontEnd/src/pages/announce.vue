<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <h2>发布公告</h2>
            <div class="form">
                <Form ref="announce" :model="announceInfo" :rules="ruleAnnounceInfo" :label-width="80">
                    <FormItem label="题目" prop="title">
                        <Input v-model="announceInfo.title" placeholder="请输入公告题目"></Input>
                    </FormItem>
                    <FormItem label="内容" prop="content">
                        <Input v-model="announceInfo.content" type="textarea" :maxlength="800" :rows="6"
                               :autosize="{minRows: 6,maxRows: 6}" placeholder="请输入公告内容（不超过800字）"></Input>
                    </FormItem>
                </Form>
            </div>
            <Divider/>
            <div style="margin-left: 50px">
                <h5 style="margin-bottom: 20px">附件上传</h5>
                <div v-if="readonly" class="show-upload">
                    <ul>
                        <li v-for="item in uploadDocList" @click="docView(item)">
                            <Icon type="md-document"></Icon>
                            {{item.name}}
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
                        :max-size="20480"
                        :on-format-error="handleFormatErrorDoc"
                        :on-exceeded-size="handleMaxSizeDoc"
                        :before-upload="handleBeforeUploadDoc"
                        :action="up_url"
                        :data=data
                        style="display: inline-block">
                    <Button icon="ios-document" style="width: 100px">上传</Button>
                </Upload>
            </div>
            <Button type="primary" @click="announce" style="margin-left: 45%;">发布公告</Button>
        </div>
    </div>
</template>

<script>
    import NavBar from '../components/NavBar.vue'

    export default {
        components: {
            NavBar
        },
        name: 'announce',
        data() {
            return {
                readonly: false,
                data: {},
                news_code: '',
                announceInfo: {
                    title: '',
                    content: '',
                    fileList: [],
                },
                ruleAnnounceInfo: {
                    title: [
                        {required: true, message: '题目不能为空', trigger: 'blur'}
                    ],
                    content: [
                        {required: true, message: '内容不能为空', trigger: 'blur'}
                    ],
                    fileList: [],
                },
                up_url: this.$baseURL + '/api/v1/up_announce_file',
                defaultDocList: [],
                uploadDocList: [],
            }
        },
        methods: {
            announce() {
                this.$refs['announce'].validate((valid) => {
                    if (valid) {
                        this.announceInfo.fileList = this.$refs.uploadDoc.fileList;

                        var nowdate = new Date()
                        var time = nowdate.getFullYear() + '/' + (nowdate.getMonth() + 1) + '/' + nowdate.getDate() + ' '
                        time = time + (nowdate.getHours().toString().length >= 1 ? nowdate.getHours() : '0' + nowdate.getHours()) + ':' + (nowdate.getMinutes().toString().length > 1 ? nowdate.getMinutes() : '0' + nowdate.getMinutes())
                        console.log(time)

                        let params = {
                            'news_code': this.news_code,
                            'title': this.announceInfo.title,
                            'time': time,
                            'content': this.announceInfo.content,
                            'files': this.announceInfo.fileList,
                        }
                        this.$http.post(this.$baseURL + '/api/v1/add_news', params)
                            .then(function (res) {
                                console.log(res)
                                var detail = res.body
                                if (detail.state == 'success') {
                                    this.$Message.success('发布成功')
                                    this.$router.push({
                                        path: '/index'
                                    })
                                } else {
                                    this.$Message.error('发布失败，请稍后再试')
                                }
                            }, function (res) {
                                this.$Message.error('Failed')
                            })
                    } else {
                        this.$Message.error('信息有误');
                    }
                });
            },
            //upload
            docView(file) {
                console.log(file)
                window.open(file.url)
            },
            handleSuccessDoc(res, file) {
                console.log(res);
                if (res.state == 'fail') {
                    this.$Message.error('上传失败 ' + res.reason);
                    var list = this.$refs.uploadDoc.fileList
                    this.$refs.uploadDoc.fileList.splice(list.indexOf(file), 1)
                } else {
                    // this.$Message.success('成功上传')
                    file.url = res.url;
                }
            },
            handleRemoveDoc(file, fileList) {
                let params = {'file_path': file.url}
                this.$http.post(this.$baseURL + '/api/v1/delete_announce_file', params)
                    .then(function (res) {
                        console.log(res.body)
                        if (res.body.state == 'fail') {
                            this.$Message.error('删除失败 ' + res.body.reason)
                            this.$refs.uploadDoc.fileList.push(file)
                        } else {
                            console.log('Success')
                        }
                    })
            },
            handleFormatErrorDoc(file) {
                this.$Notice.warning({
                    title: '文件格式错误',
                    desc: '文件 ' + file.name + ' 格式错误请选择 pdf 格式'
                });
            },
            handleMaxSizeDoc(file) {
                this.$Notice.warning({
                    title: '文件过大',
                    desc: '文件  ' + file.name + ' 过大，不能超过20M'
                });
            },
            handleBeforeUploadDoc() {
                const check = this.uploadDocList.length < 100;
                if (!check) {
                    this.$Notice.warning({
                        title: '最多只能上传100个文件'
                    });
                }
                return check;
            },
        },
        mounted() {
            this.uploadDocList = this.$refs.uploadDoc.fileList.length > 0 ? this.$refs.uploadDoc.fileList : this.defaultDocList;
            this.$Message.config({
                top: 100,
                duration: 1,
            });
        },
        created() {
            this.$http.get(this.$baseURL + '/api/v1/random_news')
                .then(function(res){
                    console.log(res)
                    var detail = res.body;
                    if(detail.state == 'success'){
                        this.news_code = detail.news_code
                        this.data = {
                            'news_code': detail.news_codes
                        }
                    }
                    else{
                        this.$Message.error(detail.reason)
                    }
                },function(res){
                    this.$Message.error("Failed")
                })
        },
    }
</script>

<style scoped>
    .body {
        left: 280px;
        bottom: 50px;
        position: relative;
        top: 100px;
        border: 1px dashed black;
        border-radius: 20px;
        /*margin: 100px 0px 50px 30%;*/
        padding: 20px;
        width: 75%;
        /*text-align: center;*/
        min-height: 470px;
        min-width: 600px;
        color: black;
    }

    h2 {
        border-left: 5px solid orange;
        padding: 0 0 0 15px !important;
        font-size: 28px !important;
        margin: 24px 0 !important;
    }
</style>