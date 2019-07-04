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
                    <h2 style="text-align: center">{{competitionDetail.title}}</h2>
                    <Divider dashed/>
                    <Row style="color: #8391a5; font-size: 18px">
                        <Col span="10" style="text-align: left">
                            <p>发布者：校团委</p>
                        </Col>
                        <Col offset="4" span="10" style="text-align: right">
                            <p>发布时间：{{competitionDetail.date}}</p>
                        </Col>
                    </Row>
                    <p style="font-size: 16px; margin: 20px;">{{competitionDetail.text}}</p>
                    <Divider style="margin: 10px 0 20px 0;"/>
                    <div v-if="competitionDetail.download!=''">
                        <p style="margin-left: 40px; font-size: 16px">附件下载：</p>
                        <p style="margin-left: 60px">
                            <Icon style="margin-right: 10px" type="ios-cloud-download"></Icon>
                            {{competitionDetail.filename}}
                            <a :download="competitionDetail.filename" :href="competitionDetail.download">
                                <Button ghost shape="circle" style="margin-left: 20px;" type="info">点击下载</Button>
                            </a>
                        </p>
                    </div>
                </div>
            </div>
            <div v-if="isNews">
                <div class="news-list">
                    <h2 style="text-align: center">{{newsDetail.title}}</h2>
                    <Divider dashed/>
                    <Row style="color: #8391a5; font-size: 18px">
                        <Col span="10" style="text-align: left">
                            <p>发布者：校团委</p>
                        </Col>
                        <Col offset="4" span="10" style="text-align: right">
                            <p>发布时间：{{newsDetail.time}}</p>
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
                //this.$http.get(this.$baseURL + '',{params:{'competition_id': query.competitionID}}
            } else {
                console.log(this.$route.query.newsID)
                this.isNews = true
                this.detailType = '公告'
                if (query.from == 'list') {
                    this.listName = '最新公告'
                    this.isFromList = true
                }
                let params = {
                    'news_id': this.$route.query.newsID,
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

    .carousel {
        width: 100%;
        height: 100%;
        background: #8391a5;
        text-align: center;
        font-size: 20px;
        color: white;
    }

    .span-title {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .news-list {
        width: 90%;
        margin-left: 5%;
    }

    .news-list li {
        padding: 15px 0 15px 0;
        border-bottom: #8391a5 dashed 0.5px;
        border-top: #8391a5 dashed 0.5px;
    }

    .news-list li {
        padding: 15px 0 15px 0;
        border-bottom: #8391a5 dashed 0.5px;
        border-top: #8391a5 dashed 0.5px;
    }

    .breadcrumb-item {
        cursor: pointer;
    }

    h1, h2 {
        font-weight: normal;
    }

    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        padding: 6px 0 6px 0;
        border-bottom: #8391a5 dashed 0.5px;
        border-top: #8391a5 dashed 0.5px;
        cursor: pointer;
    }

    p {
        margin: 10px;
    }

    a {
        color: black;
    }
</style>
