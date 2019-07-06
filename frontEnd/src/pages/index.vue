<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <div v-if="!isMoreNews">
                <h3>雨我无瓜科技竞赛</h3>
                <Divider style="margin: 3px"/>
                <Carousel autoplay :autoplay-speed="3000" :height="250" v-model="value2" loop>
                    <CarouselItem v-for="(item,index) in carousel_pic" :key="index">
                        <img :src="item.url" class="carousel">
                    </CarouselItem>
                </Carousel>
                <Row style="margin-top: 20px;">
                    <Col span="12">
                        <Card :dis-hover="false">
                            <p slot="title">
                                <Icon type="ios-mail"></Icon>
                                最新公告
                            </p>
                            <a href="#" slot="extra" @click.prevent="more_news('latest')">
                                <Icon type="ios-list"></Icon>
                                更多消息
                            </a>
                            <ul>
                                <li v-for="(item,index) in latest_news.slice(0,5)" :key="index"
                                    @click="show_detail(item.news_code)">
                                    <!--                                <a :href="item.url" target="_blank">-->
                                    <Row>
                                        <Col span="18">
                                            <div class="span-title">{{item.title}}</div>
                                        </Col>
                                        <Col span="6">
                                            <span style="float: right; color: #8391a5;">{{item.time}}</span>
                                        </Col>
                                    </Row>
                                    <!--                                </a>-->
                                </li>
                            </ul>
                        </Card>
                    </Col>
                    <Col span="11" offset="1">
                        <Card :dis-hover="false">
                            <p slot="title">
                                <Icon type="ios-chatboxes"></Icon>
                                竞赛列表
                            </p>
                            <router-link :to="{path:'/competitionList'}" slot="extra">
                                <Icon type="ios-list"></Icon>
                                更多竞赛
                            </router-link>
                            <ul>
                                <li v-for="(item,index) in contest_list.slice(0,5)" :key="index"
                                    @click="to_competition(item.competition_id)">
                                    <!--                                <a :href="item.url" target="_blank">-->
                                    <Row>
                                        <Col span="18">
                                            <div class="span-title">{{item.competition_name}}</div>
                                        </Col>
                                        <Col span="6">
                                            <span style="float: right; color: #8391a5;">{{item.com_status}}</span>
                                        </Col>
                                    </Row>
                                    <!--                                </a>-->
                                </li>
                            </ul>
                        </Card>
                    </Col>
                </Row>
            </div>
            <div v-if="isMoreNews">
                <Breadcrumb style="font-size: 16px">
                    <BreadcrumbItem class="breadcrumb-item" @click.native="back_to_index">首页</BreadcrumbItem>
                    <BreadcrumbItem class="breadcrumb-item" @click.native="back_to_list" v-if="isMoreNews">
                        {{newsType}}
                    </BreadcrumbItem>
                </Breadcrumb>
                <Divider/>
                <div class="news-list">
                    <ul style="list-style-type:none">
                        <li v-for="(item,index) in show_news.slice((pageNum-1)*pageSize, pageNum*pageSize)" :key="index"
                            @click="show_detail(item.news_code)">
                            <div class="paper-detail">
                                <!--                                    <a :href="item.url" target="_blank">-->
                                <Row>
                                    <Col span="18">
                                        <div class="span-title">{{item.title}}</div>
                                    </Col>
                                    <Col span="6">
                                        <span style="float: right; color: #8391a5;">{{item.time}}</span>
                                    </Col>
                                </Row>
                                <!--                                    </a>-->
                            </div>
                        </li>
                    </ul>
                </div>
                <Page :current="pageNum" :total="show_news.length" :page-size="pageSize" @on-change="change_page" simple
                      style="text-align: center; margin-bottom: 20px"/>
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
        name: 'index',
        data() {
            return {
                value2: 0,
                isMoreNews: false,
                newsType: '',
                pageNum: 1,
                pageSize: 20,
                show_news: [],
                latest_news: [],
                contest_list: [],
                competition_news: [],
                carousel_pic: [
                    {
                        'name': 'pic1',
                        'url': '../../static/picture/test1.jpg'
                    },
                    {
                        'name': 'pic2',
                        'url': '../../static/picture/test2.jpg'
                    },
                    {
                        'name': 'pic3',
                        'url': '../../static/picture/test3.jpg'
                    },
                    {
                        'name': 'pic4',
                        'url': '../../static/picture/test4.jpg'
                    },
                    {
                        'name': 'pic5',
                        'url': '../../static/picture/test5.jpg'
                    }
                ],
                msgDetail: {
                    'title': '',
                    'date': '',
                    'url': '',
                    'text': '',
                    'download': '',
                    'filename': '',
                }
            }
        },
        methods: {
            get_news() {
                this.$http.get(this.$baseURL + '/api/v1/get_news', {params: {}})
                    .then(function (res) {
                        console.log(res);
                        var detail = res.body;
                        if (detail.state === 'success') {
                            var list = detail.news_list;
                            for (var item of list) {
                                item.time = item.time.split(' ')[0]
                            }
                            this.latest_news = list.reverse()//倒置数组 目的是按照时间从新到旧顺序显示
                        } else {
                            this.$Message.error('获取公告列表失败 ' + detail.reason)
                        }
                    });

                let params = {};
                this.$http.post(this.$baseURL + '/api/v1/contestlist', params)
                    .then(function (res) {
                        console.log(res);
                        var detail = res.body;
                        if (detail.state === 'success') {
                            this.contest_list = detail.contests.reverse();
                            // console.log(this.contest_list)
                            for (let item of this.contest_list) {
                                switch (item.com_status) {
                                    case -1:
                                        item.com_status = '未开始';
                                        break;
                                    case 0:
                                        item.com_status = '报名中';
                                        break;
                                    case 1:
                                        item.com_status = '校团委初审';
                                        break;
                                    case 2:
                                        item.com_status = '专家评审中';
                                        break;
                                    case 3:
                                        item.com_status = '进行现场赛';
                                        break;
                                    case 4:
                                        item.com_status = '结果公布中';
                                        break;
                                    case 5:
                                        item.com_status = '已结束';
                                        break;
                                }
                            }
                        } else {
                            this.$Message.error('获取竞赛列表失败 ' + detail.reason)
                        }
                    }, function (res) {
                        this.$Message.error('Failed')
                    })
            },
            more_news(type) {
                // this.$Message.info('moreNews')
                if (type == 'latest') {
                    this.newsType = '最新公告';
                    this.show_news = this.latest_news;
                } else if (type == 'competition') {
                    this.newsType = '竞赛列表';
                    this.show_news = this.competition_news;
                }
                this.isMoreNews = true
                this.pageNum = 1
                this.$router.push({
                    path: '/newsList',
                })
            },
            change_page(value) {
                this.pageNum = value;
                console.log(this.pageNum);
                document.body.scrollTop = 0;
                document.documentElement.scrollTop = 0;
            },
            back_to_index() {
                this.isMoreNews = false;
            },
            show_detail(news_code) {
                this.$router.push({
                    path: '/messageDetail',
                    query: {
                        'type': 'news',
                        'from': this.isMoreNews ? 'list' : 'index',
                        'newsID': news_code,
                    }
                })
            },
            to_competition(competition_id) {
                let role = this.$cookie.get('role');
                this.$router.push({
                    path: '/messageDetail',
                    query: {
                        type: 'competition',
                        from: 'index',
                        competitionID: competition_id,
                        who: role,
                    }
                })
            }
        },
        created() {
            this.get_news();
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
        /*border: 1px dashed black;*/
        /*border-radius: 20px;*/
        /*margin: 100px 0px 50px 30%;*/
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
