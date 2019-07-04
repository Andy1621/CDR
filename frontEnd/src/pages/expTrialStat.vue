<template>
    <div>
        <NavBar></NavBar>
        <div class="nav">
            <Breadcrumb style="text-align: left">
                <BreadcrumbItem to="/competitionList">竞赛列表</BreadcrumbItem>
                <BreadcrumbItem :to="{path:'/stageProList',query: {competitionID:this.$route.query.competition_id,}}">
                    {{this.$route.query.competition_title}}</BreadcrumbItem>
                <BreadcrumbItem> "{{this.$route.query.projectName}}"</BreadcrumbItem>
            </Breadcrumb>
        </div>
        <div class="body">
            <h3>专家评审状况</h3>
            <Table stripe border :columns="columns" :data="rows" height="450" ref="table"></Table>
            <Modal
                v-model="detail"
                title="评审结果详情"
                width="500">
                <p class="size"><b>专家评分：</b>{{score}}</p><br /><br />
                <p class="size"><b>评审意见：</b>{{suggestion}}</p>
            </Modal>
        </div>
        <router-view v-if="isRouterAlive"></router-view>
    </div>
</template>


<script>
    import NavBar from '../components/NavBar.vue'
    export default {
        name: "expTrialStat",
        components:{
            NavBar
        },
        inject: ['reload'],
        data(){
            return{
                com_stat: {title: '评审状态', key: 'status', width: 120, align: 'center'},
                com_score: {title: '专家评分', key: 'score', width: 90, align: 'center'},
                com_detail: {title: '专家评审意见', key: 'suggestion', width: 550},
                columns: [
                    {
                        title: '专家名称',
                        key: 'username',
                        width: 130
                    },
                    {
                        title: '专家邮箱',
                        key: 'expert_mail',
                        width: 230
                    },
                    {
                        title: '操作',
                        key: 'oper',
                        width: 110,
                        align: 'center',
                        render: (h, params) => {
                            return h('div', params.row.status=="已评审" ? [
                                h('Button', {
                                    props: {
                                        type: 'primary',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight:'5px'
                                    },
                                    on: {
                                        click: () => {
                                            this.detail = true;
                                            console.log(this.detail);
                                            this.score = this.rows[params.index].score;
                                            this.suggestion = this.rows[params.index].suggestion;
                                        }
                                    }
                                }, params.row.status=="已评审" ? '查看详情' : '')
                            ] : '不可操作')
                        }
                    }
                ],
                rows: [],
                detail: false,
                proj_id: '0001',
                score: 1,
                suggestion: "",
                isRouterAlive: true,
                comp_name: "冯如杯",
                proj_name: "基于",
                from_2_3: 2,
            }
        },
        created(){
            this.proj_id = this.$route.query.projectID;
            this.from_2_3 = this.$route.query.fromState;
            this.getList();
        },
        methods:{
            getList(){
                if(this.from_2_3 == 2){
                    this.columns.splice(2, 0, this.com_stat);
                }
                else{
                    this.columns.splice(2, 0, this.com_score, this.com_detail);
                }
                let params = {'proj_id': this.proj_id};
                this.$http.post(this.$baseURL + "/api/v1/getExpertInviteList",params,{
                    headers:{
                        'Content-Type':"application/json",
                    }
                }).then(function (res) {
                    if(res.body.state=="fail"){
                        this.$Notice.open({title: "获取数据失败"});
                    }
                    else{
                        for (let item of res.body.list_invited) {
                            switch (item.status) {
                                case -1:
                                    item.status = "待回应";
                                    break;
                                case 0:
                                    item.status = "已接受";
                                    break;
                                case 1:
                                    item.status = "已拒绝";
                                    break;
                                case 2:
                                    item.status = "已评审";
                                    break;
                            }
                        }
                        if(this.from_2_3 == 3){
                            let new_list = [];
                            for (let item of res.body.list_invited) {
                                if(item.status == "已评审"){
                                    new_list.push(item);
                                }
                            }
                            this.rows = new_list;
                        }
                        else{
                            this.rows = res.body.list_invited;
                        }
                    }
                }, function (res) {
                    alert(res);
                });
            }
        },
    }
</script>

<style scoped>
    .nav{
        left: 280px;
        top: 100px;
        position: relative;
        float: left;
        border: none;
        /*margin: 0px 500px 0px 0px;*/
        padding: 0px 0px 15px 10px;
        width: 80%;
    }
    .body{
        left: 280px;
        top: 100px;
        position: relative;
        float: left;
        /*border: 1px dashed black;*/
        /*border-radius: 5px;*/
        /*margin: 0px 500px 0px 0px;*/
        padding: 0px 20px 10px 20px;
        /*width: 75%;*/
        text-align: left;
        color: black;
    }
    .size{
        font-size: 17px;
    }
    h3{
        border-left: 5px solid purple;
        padding: 0 0 0 15px!important;
        font-size: 24px!important;
        margin: 24px 0!important;
    }
</style>
