<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <Button primary style="position: fixed; right: 20%; top: 115px" @click="$router.go(-1)">返回</Button>
            <h3 style="margin: 20px 0 30px 47%">作品详情</h3>
            <Steps :current="current" style="margin-left: 12%">
                <Step title="项目基本信息" content="分类、创新、关键词、总体说明" icon="ios-information-circle-outline"
                      @click.native="current = 0"></Step>
                <Step title="项目相关文件" content="文档、视频、图片" icon="ios-camera" @click.native="current = 1"></Step>
                <Step title="评审打分" content="给出评价和分数" icon="ios-chatboxes" @click.native="current = 2"></Step>
            </Steps>
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
                        <Input v-model="basicInfo.description" type="textarea" readonly></Input>
                    </FormItem>
                </Form>
            </div>
            <div v-show="current==1">
                图片视频
            </div>
            <div v-show="current==2">
                <Form ref="reviewInfo" :model="reviewInfo" :label-width="80">
                    <FormItem label="评分">
                        <Input v-model="reviewInfo.marks"></Input>
                    </FormItem>
                    <FormItem label="评价">
                        <Input v-model="reviewInfo.comment" type="textarea"></Input>
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
                current: 0,
                basicInfo: {},
                reviewInfo: {
                    marks: '',
                    comment: ''
                },
                dictionary: {
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
            let url = this.$baseURL + '/api/v1/get_project_detail'
            this.$http.get(url, {params: {project_code: this.$route.query.project_id}}).then(function (res) {
                console.log(res)
                this.basicInfo = res.body.project.registration_form
                this.basicInfo.type = this.dictionary[this.basicInfo.type]
            }, function (res) {
                console.log(res)
            })
        },
        methods: {
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
                        this.$Message.info('保存成功！')
                    }
                }, function (res) {
                    console.log(res)
                })
            },
            upReview() {
                if (this.reviewInfo.marks == '' || this.reviewInfo.comment == '') {
                    alert("请将评审信息填写完整！")
                    return
                } else {
                    this.$Message.info('提交成功')
                    let url = this.$baseURL + '/api/v1/submit_review'
                    this.$http.get(url, {
                        params: {
                            project_code: this.$route.query.project_id,
                            expert_email: this.$cookie.get('mail'),
                            score: this.reviewInfo.marks,
                            suggestion: this.reviewInfo.comment
                        }
                    }).then(function (res) {
                        console.log(res)
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
</style>