<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <div v-if="!isMoreNews&&!isDetail">
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
                            <li v-for="(item,index) in latest_news.slice(0,5)" :key="index" @click="show_detail('latest',index)">
<!--                                <a :href="item.url" target="_blank">-->
                                    <Row>
                                        <Col span="18">
                                            <div class="span-title">{{item.title}}</div>
                                        </Col>
                                        <Col span="6">
                                            <span style="float: right; color: #8391a5;">{{item.date}}</span>
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
                            其他消息
                        </p>
                        <a href="#" slot="extra" @click.prevent="more_news('else')">
                            <Icon type="ios-list"></Icon>
                            更多消息
                        </a>
                        <ul>
                            <li v-for="(item,index) in else_news.slice(0,5)" :key="index" @click="show_detail('else',index)">
<!--                                <a :href="item.url" target="_blank">-->
                                    <Row>
                                        <Col span="18">
                                            <div class="span-title">{{item.title}}</div>
                                        </Col>
                                        <Col span="6">
                                            <span style="float: right; color: #8391a5;">{{item.date}}</span>
                                        </Col>
                                    </Row>
<!--                                </a>-->
                            </li>
                        </ul>
                    </Card>
                </Col>
            </Row>
            </div>
            <div v-if="isMoreNews||isDetail">
                <Breadcrumb style="font-size: 16px">
                    <BreadcrumbItem class="breadcrumb-item" @click.native="back_to_index">首页</BreadcrumbItem>
                    <BreadcrumbItem class="breadcrumb-item" @click.native="back_to_list" v-if="isMoreNews">{{newsType}}</BreadcrumbItem>
                    <BreadcrumbItem class="breadcrumb-item" v-if="isDetail">信息详情</BreadcrumbItem>
                </Breadcrumb>
                <Divider/>
                <div v-if="!isDetail">
                    <div class="news-list">
                        <ul style="list-style-type:none">
                            <li v-for="(item,index) in show_news.slice((pageNum-1)*pageSize, pageNum*pageSize)" :key="index" @click="show_detail('default',index)">
                                <div class="paper-detail">
<!--                                    <a :href="item.url" target="_blank">-->
                                        <Row>
                                            <Col span="18">
                                                <div class="span-title">{{item.title}}</div>
                                            </Col>
                                            <Col span="6">
                                                <span style="float: right; color: #8391a5;">{{item.date}}</span>
                                            </Col>
                                        </Row>
<!--                                    </a>-->
                                </div>
                            </li>
                        </ul>
                    </div>
                    <Page :current="pageNum" :total="show_news.length" :page-size="pageSize" @on-change="change_page" simple style="text-align: center; margin-bottom: 20px"/>
                </div>
                <div v-show="isDetail">
                    <div class="news-list">
                        <h3>{{msgDetail.title}}</h3>
                        <h4>{{msgDetail.date}}</h4>
                        <p>{{msgDetail.text}}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import NavBar from '../components/NavBar.vue'
    export default {
        components:{
            NavBar
        },
        name: 'index',
        data () {
            return {
                value2: 0,
                isMoreNews: false,
                isDetail: false,
                newsType: '',
                pageNum: 1,
                pageSize: 20,
                show_news:[],
                latest_news:[],
                else_news:[],
                carousel_pic:[
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
                msgDetail:{
                    'title': '',
                    'date': '',
                    'url': '',
                    'text': '',
                }
            }
        },
        methods:{
            get_news(){
                this.$http.get('https://www.easy-mock.com/mock/5ce254757c25615cbf8ae1ae/example/latest_news',{params: {'user_id':'12138'}})
                .then(function (res) {
                    var detail = res.body
                    console.log(detail)
                    if(detail.state == 'success'){
                        this.latest_news = detail.data.news
                    }
                },function (res) {
                    // var detail = JSON.parse(res.body)
                    console.log("Failed")
                })
                this.$http.get('https://www.easy-mock.com/mock/5ce254757c25615cbf8ae1ae/example/latest_news',{params: {'user_id':'12138'}})
                .then(function (res) {
                    var detail = res.body
                    console.log(detail)
                    if(detail.state == 'success'){
                        this.else_news = detail.data.news
                    }
                },function (res) {
                    // var detail = JSON.parse(res.body)
                    console.log("Failed")
                })
            },
            more_news(type){
                this.$Message.info('moreNews')
                if(type == 'latest'){
                    this.newsType = '最新公告';
                    this.show_news = this.latest_news;
                }
                else if(type == 'else'){
                    this.newsType = '其他消息';
                    this.show_news = this.else_news;
                }
                this.isMoreNews = true
                this.pageNum = 1
            },
            change_page(value){
                this.pageNum = value;
                console.log(this.pageNum);
                document.body.scrollTop = 0;
                document.documentElement.scrollTop = 0;
            },
            back_to_index(){
                this.isMoreNews = false;
                this.isDetail = false;
                this.msgDetail = {};
            },
            back_to_list(){
                this.isDetail = false;
            },
            show_detail(type,index){
                console.log(type + index)
                if(type == 'latest'){
                    this.msgDetail = this.latest_news[index];
                }
                else if(type == 'else'){
                    this.msgDetail = this.else_news[index];
                }
                else{
                    this.msgDetail = this.show_news[index];
                }
                this.isDetail = true

            }
        },
        created() {
            this.get_news();
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .body{
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
    .carousel{
        width: 100%;
        height: 100%;
        background: #8391a5;
        text-align: center;
        font-size: 20px;
        color: white;
    }
    .span-title{
        overflow: hidden;
        text-overflow:ellipsis;
        white-space: nowrap;
    }
    .news-list{
        width: 85%;
        margin-left: 5%;
    }
    .news-list li{
        padding: 15px 0 15px 0;
        border-bottom: #8391a5 dashed 0.5px;
        border-top: #8391a5 dashed 0.5px;
    }
    .news-list li{
        padding: 15px 0 15px 0;
        border-bottom: #8391a5 dashed 0.5px;
        border-top: #8391a5 dashed 0.5px;
    }
    .breadcrumb-item{
        cursor: pointer;
    }
    h1, h2 {
        font-weight: normal;
    }
    ul {
        list-style-type: none;
        padding: 0;
    }
    li{
        padding: 6px 0 6px 0;
        border-bottom: #8391a5 dashed 0.5px;
        border-top: #8391a5 dashed 0.5px;
        cursor: pointer;
    }
    a {
        color: black;
    }
</style>
