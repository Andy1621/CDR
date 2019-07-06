<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <Breadcrumb style="font-size: 16px">
                <BreadcrumbItem @click.native="back_to_index" class="breadcrumb-item">首页</BreadcrumbItem>
                <BreadcrumbItem @click.native="back_to_list" class="breadcrumb-item" v-if="isFromList">{{listName}}
                </BreadcrumbItem>
                <BreadcrumbItem class="breadcrumb-item" v-if="isCompetition||isNews">{{detailType}}详情
                </BreadcrumbItem>
            </Breadcrumb>
            <Divider/>
            <div v-if="isCompetition">
                <div class="news-list">
                    <h2 style="text-align: center">{{competitionDetail.competition_name}}</h2>
                    <Divider dashed/>
                    <Row style="color: #8c8c8c; font-size: 18px; font-family: '华文楷体'">
                        <Col offset="14" span="10" style="text-align: right">
                            <span>发布者：校团委</span>
                        </Col>
                    </Row>
                    <Row class="info-detail">
                        <Col span="4"><span class="info-title">竞赛名称：</span></Col>
                        <Col span="19"><p class="info-competition">{{competitionDetail.competition_name}}</p></Col>
                    </Row>
                    <Row class="info-detail">
                        <Col span="4"><span class="info-title">报名开始时间：</span></Col>
                        <Col span="19"><p class="info-competition">{{competitionDetail.begin_time}}</p></Col>
                    </Row>
                    <Row class="info-detail">
                        <Col span="4"><span class="info-title">报名截止时间：</span></Col>
                        <Col span="19"><p class="info-competition">{{competitionDetail.submission_ddl}}</p></Col>
                    </Row>
                    <Row class="info-detail">
                        <Col span="4"><span class="info-title">竞赛结束时间：</span></Col>
                        <Col span="19"><p class="info-competition">{{competitionDetail.end_time}}</p></Col>
                    </Row>
                    <Row class="info-detail">
                        <Col span="4"><span class="info-title">竞赛简介：</span></Col>
                        <Col span="19"><p class="info-competition" v-html="competitionDetail.introduction"></p></Col>
                    </Row>
                    <Divider style="margin: 10px 0 20px 0;"/>
                </div>
            </div>
            <div v-if="isNews">
                <div class="news-list">
                    <h2 style="text-align: center">{{newsDetail.title}}</h2>
                    <Divider dashed/>
                    <Row style="color: #8c8c8c; font-size: 18px; font-family: '华文楷体'">
                        <Col span="10" style="text-align: left">
                            <span style="margin: 5px 10px 5px 10px">发布者：校团委</span>
                        </Col>
                        <Col offset="4" span="10" style="text-align: right">
                            <span style="margin: 5px 10px 5px 10px">发布时间：{{newsDetail.time}}</span>
                        </Col>
                    </Row>
                    <p style="font-size: 16px; margin: 20px;" v-html="newsDetail.content"></p>
                    <Divider style="margin: 10px 0 20px 0;"/>
                    <div v-if="newsDetail.files!=''">
                        <p style="margin-left: 40px; font-size: 16px">附件下载：</p>
                        <div v-for="item in newsDetail.files">
                            <p style="margin-left: 60px">
                                <Icon style="margin-right: 10px" type="ios-cloud-download"></Icon>
                                {{item.name}}
                                <Button @click="download(item.url)" ghost shape="circle"
                                        style="margin-left: 20px;" type="info">点击下载
                                </Button>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import NavBar from '../components/NavBar.vue'

    export default {
        components: {
            NavBar
        },
        name: 'messageDetail',
        data() {
            return {
                value2: 0,
                isFromList: false,
                isCompetition: false,
                isNews: false,
                listName: '',
                detailType: '',
                competitionDetail: {},
                newsDetail: {},
            }
        },
        methods: {
            back_to_index() {
                this.isFromList = false;
                this.isCompetition = false;
                this.isNews = false;
                this.$router.push({
                    path: '/index',
                })
            },
            back_to_list() {
                if (this.listName == '竞赛列表') {
                    this.$router.push({
                        path: '/competitionList'
                    })
                }
                else{
                    this.$router.push({
                        path: '/newsList',
                    })
                }
            },
            download(url) {
                window.open(url)
            },
        },
        created() {
            let query = this.$route.query
            if (query.type == 'competition') {
                console.log(this.$route.query.competitionID)
                this.isCompetition = true
                this.detailType = '竞赛'
                if (query.from == 'list') {
                    this.listName = '竞赛列表'
                    this.isFromList = true
                }
                let params = {
                    'competition_id': this.$route.query.competitionID
                }
                this.$http.post(this.$baseURL + '/api/v1/get_competition_detail', params)
                    .then(function (res) {
                        console.log(res)
                        var detail = res.body
                        if(detail.state == 'success'){
                            var temp_detail = detail.competition
                            // temp_detail['begin_time'] = temp_detail['begin_time'].split(' ')[0]
                            if (temp_detail['introduction'].length == 0)
                                temp_detail['introduction'] = '暂无竞赛简介'
                            this.competitionDetail = temp_detail
                        }
                        else{
                            this.$Message.error('获取竞赛详情失败 ' + detail.reason)
                        }
                    },function (res) {
                        this.$Message.error('Failed')
                    })
            }
            else {
                console.log(this.$route.query.newsID)
                this.isNews = true
                this.detailType = '公告'
                if (query.from == 'list') {
                    this.listName = '最新公告'
                    this.isFromList = true
                }
                let params = {
                    'news_code': this.$route.query.newsID,
                }
                this.$http.post(this.$baseURL + '/api/v1/get_news_detail', params)
                    .then(function (res) {
                        console.log(res)
                        var detail = res.body
                        if (detail.state == 'success') {
                            this.newsDetail = detail.news_detail
                            console.log(this.newsDetail)
                        } else {
                            this.$Message.error('获取公告详情失败 ' + detail.reason)
                        }
                    }, function (res) {
                        this.$Message.error('Failed')
                    })
            }
        },
        mounted() {
            this.$Message.config({
                top: 100,
                duration: 1,
            });
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .body {
        margin-left: 280px;
        margin-bottom: 50px;
        position: relative;
        top: 100px;
        padding: 10px;
        width: 77%;
        /*text-align: center;*/
        min-height: 470px;
        min-width: 600px;
        color: black;
    }

    .info-detail{
        margin: 20px 50px 20px 50px;
        font-family: 微软雅黑;
        /*border-bottom: 1px dodgerblue dashed;*/
    }

    .info-title{
        border-left: 4px solid green;
        padding: 2px 0 2px 5px;
        font-family: 华文中宋;
        font-size: 18px;
        line-height: 30px;
    }

    .info-competition{
        padding: 5px 10px 5px 10px;
        line-height: 30px;
        border: 1px solid dodgerblue;
        border-radius: 5px;
    }

    h1, h2 {
        font-weight: normal;
    }

    p {
        line-height: 30px;
        padding: 5px 10px 5px 10px;
    }

</style>
