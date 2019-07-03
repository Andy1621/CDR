<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <div>
                <Breadcrumb style="font-size: 16px">
                    <BreadcrumbItem class="breadcrumb-item" @click.native="back_to_index">首页</BreadcrumbItem>
                    <BreadcrumbItem class="breadcrumb-item">最新公告</BreadcrumbItem>
                </Breadcrumb>
                <Divider/>
                    <div class="news-list">
                        <ul style="list-style-type:none">
                            <li v-for="(item,index) in latest_news.slice((pageNum-1)*pageSize, pageNum*pageSize)" :key="index" @click="show_detail(item.news_id)">
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
                    <Page :current="pageNum" :total="latest_news.length" :page-size="pageSize" @on-change="change_page" simple style="text-align: center; margin-bottom: 20px"/>
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
        name: 'newsList',
        data () {
            return {
                value2: 0,
                newsType: '',
                pageNum: 1,
                pageSize: 20,
                latest_news: [],
            }
        },
        methods:{
            get_news(){
                this.$http.get(this.$baseURL + '/api/v1/get_news',{params:{}})
                    .then(function (res) {
                        console.log(res)
                        var detail = res.body
                        if(detail.state == 'success'){
                            var list = detail.news_list
                            for(var item of list){
                                item.time = item.time.split(' ')[0]
                            }
                            this.latest_news = list.reverse()//倒置数组 目的是按照时间从新到旧顺序显示
                        }
                        else{
                            this.$Message.error('获取公告列表失败 ' + detail.reason)
                        }
                    })
            },
            change_page(value){
                this.pageNum = value;
                console.log(this.pageNum);
                document.body.scrollTop = 0;
                document.documentElement.scrollTop = 0;
            },
            back_to_index(){
                this.$router.push({
                    path: '/index'
                })
            },
            show_detail(news_id){
                this.$router.push({
                    path: '/messageDetail',
                    query:{
                        'type': 'news',
                        'from': 'list',
                        'newsID': news_id,
                    }
                })
            },
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
        width: 90%;
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
    p{
        margin: 10px;
    }
    a {
        color: black;
    }
</style>
