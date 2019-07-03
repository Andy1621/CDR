<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <Button primary style="position: absolute; right: 10px; top: 10px" @click="$router.go(-1)">返回</Button>
            <h1 style="margin: 20px 0 30px 40%">作品详情</h1>
            <Steps :current="current" style="margin-left: 12%">
                <Step title="项目基本信息" content="分类、创新、关键词、总体说明" icon="ios-information-circle-outline"
                      @click.native="current = 0"></Step>
                <Step title="项目相关文件" content="文档、视频、图片" icon="ios-camera" @click.native="current = 1"></Step>
                <Step title="评审打分" content="给出评价和分数" icon="ios-chatboxes" @click.native="current = 2"></Step>
            </Steps>
            <Divider/>
            <div class="form" v-show="current == 0">
                <Form ref="basicInfo" :model="basicInfo" :label-width="80">
                    <FormItem label="作品全称">
                        <Input v-model="basicInfo.title" readonly></Input>
                    </FormItem>
                    <FormItem label="作品分类">
                        <Input v-model="basicInfo.type" readonly></Input>
                    </FormItem>
                    <FormItem label="创新点">
                        <Input v-model="basicInfo.creation" readonly></Input>
                    </FormItem>
                    <FormItem label="关键词">
                        <Input v-model="basicInfo.keyword" readonly></Input>
                    </FormItem>
                    <FormItem label="项目介绍">
                        <Input v-model="basicInfo.description" type="textarea" :rows="4" readonly></Input>
                    </FormItem>
                </Form>
            </div>
            <div v-show="current==1" style="margin: 10px">
                <h4 style="margin: 10px">项目图片：</h4>
                <div class="demo-upload-list" v-for="item in photoList">
                    <template v-if="item.file_type === 'photo'">
                        <img :src="item.file_path">
                        <div class="demo-upload-list-cover">
                            <Icon type="ios-eye-outline" @click.native="handleView(item.file_path)"></Icon>
                        </div>
                    </template>
                </div>
                <Divider/>
                <h4 style="margin: 10px">项目视频：</h4>
                <video-player class="video-player vjs-custom-skin"
                              ref="videoPlayer"
                              :playsinline="true"
                              :options="playerOptions"></video-player>
                <Divider/>
                <h4 style="margin: 10px">项目文档：</h4>
                <div>
                    <ul>
                        <li v-for="item in docList" style="" @click="viewDoc(item.file_path)">
                            <Icon type="md-document"></Icon>
                            {{item.file_name}}
                        </li>
                    </ul>
                </div>
                <Modal title="View Image" v-model="visible">
                    <img :src="photoViewUrl" v-if="visible" style="width: 100%">
                </Modal>
            </div>
            <div v-show="current==2">
                <Form ref="reviewInfo" :model="reviewInfo" :label-width="80">
                    <FormItem label="评分">
                        <Input v-model="reviewInfo.marks" :disabled="disable" placeholder="请输入评分，0-100"></Input>
                    </FormItem>
                    <FormItem label="评价">
                        <Input v-model="reviewInfo.comment" :disabled="disable" type="textarea"
                               placeholder="请在此输入您的评价"></Input>
                    </FormItem>
                </Form>
            </div>
            <Button type="primary" shape="circle" :disabled="current == 0" @click="current-=current>0?1:0"
                    icon="ios-arrow-back" style="margin-right: 30%;margin-left: 30%"></Button>
            <Button type="primary" shape="circle" :disabled="current == 2" @click="current+=current<2?1:0"
                    icon="ios-arrow-forward"></Button>
            <div style="margin: 15px 0 0 40%" v-show="current == 2">
                <Button type="primary" style="margin-right:6%" @click="saveReview">保存</Button>
                <Button type="error" @click="upReview">提交</Button>
            </div>
        </div>
    </div>
</template>

<script>
    import NavBar from '../components/NavBar.vue'
    import LInput from '../components/InputWithLabel.vue'

    export default {
        name: "projectDetail",
        components: {
            NavBar,
            LInput
        },
        data() {
            return {
                disable: false,
                current: 1,
                basicInfo: {},
                reviewInfo: {
                    marks: '',
                    comment: ''
                },
                photoList: [],
                docList: [],
                videoList: [],
                photoViewUrl: '',
                visible: false,
                playerOptions: {
                    playbackRates: [0.7, 1.0, 1.5, 2.0], //播放速度
                    autoplay: false, //如果true,浏览器准备好时开始回放。
                    muted: false, // 默认情况下将会消除任何音频。
                    loop: false, // 导致视频一结束就重新开始。
                    preload: 'auto', // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
                    language: 'zh-CN',
                    aspectRatio: '16:9', // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
                    fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
                    sources: [{
                        src: '',  // 路径
                        type: 'video/mp4'  // 类型
                    }],
                    //poster: "../../static/images/test.jpg", //你的封面地址
                    // width: document.documentElement.clientWidth,
                    notSupportedMessage: '此视频暂无法播放，请稍后再试', //允许覆盖Video.js无法播放媒体源时显示的默认信息。
                    controlBar: {
                        timeDivider: true,
                        durationDisplay: true,
                        remainingTimeDisplay: false,
                        fullscreenToggle: true  //全屏按钮
                    }
                },
                dictionary: {
                    dictionary: [
                        "请您先接受该项目的评审",
                        "",
                        "您已经拒绝该项目的评审",
                        "您已经评审过该做品"
                    ],
                    A: '机械与控制（包括机械、仪器仪表、自动化控制、工程、交通、建筑等）',
                    B: '信息技术（包括计算机、电信、通讯、电子等）',
                    C: '数理（包括数学、物理、地球与空间科学等）',
                    D: '生命科学(包括生物､农学､药学､医学､健康､卫生､食品等)',
                    E: '能源化工（包括能源、材料、石油、化学、化工、生态、环保等）',
                    F: '哲学社会科学（包括哲学、经济、社会、法律、教育、管理）'
                }
            }
        },
        created() {
            let url = this.$baseURL + '/api/v1/get_project_detail';
            this.$http.get(url, {params: {project_code: this.$route.query.project_id}}).then(function (res) {
                console.log(res);
                this.basicInfo = res.body.project.registration_form;
                this.basicInfo.type = this.dictionary[this.basicInfo.type];
                let files = res.body.project.project_files;
                for (let i of files) {
                    if (i.file_type === 'photo')
                        this.photoList.push(i);
                    else if (i.file_type === 'doc')
                        this.docList.push(i);
                    else {
                        this.videoList.push(i);
                        this.playerOptions.sources[0].src = i.file_path;
                    }
                }
                console.log(this.photoList, files)
            }, function (res) {
                console.log(res)
            });
            this.$http.post(this.$baseURL + '/api/v1/get_review', {
                expert_email: this.$cookie.get('mail'),
                project_code: this.$route.query.project_id
            }).then(function (res) {
                console.log(res);
                if (res.body.state === 'fail') {
                    this.disable = true;
                    alert("异常，请稍后再试！");
                    this.$router.go(-1);
                    return;
                }
                let temp = res.body.review;
                this.reviewInfo.marks = temp.score;
                this.reviewInfo.comment = temp.suggestion;
                this.status = temp.status;
                if (temp.status !== 0) {
                    this.disable = true;
                    alert(this.dictionary.dictionary[temp.status + 1])
                }
            }, function (res) {
                console.log(res)
            })
        },
        methods: {
            viewDoc(url) {
                window.open(url);
            },
            handleView(url) {
                this.photoViewUrl = url;
                this.visible = true;
            },
            saveReview() {
                let url = this.$baseURL + '/api/v1/store_review';
                let data = {
                    project_code: this.$route.query.project_id,
                    expert_email: this.$cookie.get('mail'),
                    score: this.reviewInfo.marks,
                    suggestion: this.reviewInfo.comment
                };
                this.$http.post(url, data).then(function (res) {
                    console.log(res);
                    if (res.body.state === 'fail') {
                        alert(res.body.reason)
                    } else {
                        alert('保存成功！');
                    }
                }, function (res) {
                    console.log(res)
                })
            },
            upReview() {
                if (this.reviewInfo.marks === '' || this.reviewInfo.comment === '') {
                    alert("请将评审信息填写完整！");
                    return;
                } else if (Number(this.reviewInfo.marks) < 0 || Number(this.reviewInfo.marks) > 100) {
                    alert("分数在0-100内，请填写正确的评分！")
                } else {
                    let url = this.$baseURL + '/api/v1/submit_review';
                    this.$http.post(url, {
                            project_code: this.$route.query.project_id,
                            expert_email: this.$cookie.get('mail'),
                            score: this.reviewInfo.marks,
                            suggestion: this.reviewInfo.comment
                        }
                    ).then(function (res) {
                        console.log(res);
                        this.disable = true;
                        let alertContent = res.body.state === 'fail' ? res.body.reason : '提交成功';
                        alert(alertContent);
                    }, function (res) {
                        console.log(res)
                    })
                }
            },
        },
    }
</script>

<style scoped>
    .body {
        margin: 0 100px 50px 480px;
        position: relative;
        top: 100px;
        border: 1px dashed black;
        border-radius: 20px;
        /*margin: 100px 0px 50px 30%;*/
        padding: 10px;
        width: 50%;
        /*text-align: center;*/
        min-height: 470px;
        min-width: 600px;
        color: black;
    }

    .form {
        text-align: left;
        padding: 3px;
        margin-bottom: 5px;
        font-size: 15px;
    }

    .demo-upload-list {
        display: inline-block;
        width: 60px;
        height: 60px;
        text-align: center;
        line-height: 60px;
        border: 1px solid transparent;
        border-radius: 4px;
        overflow: hidden;
        background: #fff;
        position: relative;
        box-shadow: 0 1px 1px rgba(0, 0, 0, .2);
        margin-left: 10px;
    }

    .demo-upload-list img {
        width: 100%;
        height: 100%;
    }

    .demo-upload-list-cover {
        display: none;
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(0, 0, 0, .6);
    }

    .demo-upload-list:hover .demo-upload-list-cover {
        display: block;
    }

    .demo-upload-list-cover i {
        color: #fff;
        font-size: 20px;
        cursor: pointer;
        margin: 0 2px;
    }

    ul {
        list-style-type: none;
    }

    li {
        cursor: default;
        padding: 5px 10px 5px 10px;
        margin: 1px;
        width: fit-content;
        border-radius: 5px;
        color: #666666;
    }

    li:hover {
        background: #eeeeee;
        color: #2b85e4;
    }
    >>> .video-js .vjs-big-play-button{
        position: absolute;
        top: 43%;
        left: 44%;
    }
</style>
