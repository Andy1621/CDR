<template>
    <div>
        <NavBar></NavBar>
        <div class="nav">
            <Breadcrumb style="text-align: left">
                <BreadcrumbItem to="/competitionList">竞赛列表</BreadcrumbItem>
                <BreadcrumbItem> "{{this.$route.query.competitionTitle}}"</BreadcrumbItem>
            </Breadcrumb>
        </div>
        <div class="body" style="width: 80%;">
            <h4>选择类别</h4>
            <Select v-model="model1" style="width:200px;float: left;margin-top:12px;margin-left: 30px;">
                <Option v-for="item in typeList" :value="item.value" :key="item.value">{{ item.label }}</Option>
            </Select>
        </div>
        <div class="body">
            <h3>作品列表</h3>

            <Table stripe border :columns="columns1" :data="rows1" height="450" ref="table"></Table>
        </div>
        <div class="body" style="width: 40%">
            <h3>邀请专家</h3>
            <Table stripe border :columns="columns2" :data="rows2" height="450" ref="table"></Table>
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
    import ISelect from "../../static/css/iview/iview";
    export default {
        name: "inviteProfessor",
        components:{
            NavBar
        },
        inject: ['reload'],
        data(){
            return{
                columns1: [
                    {
                        title: '专家名称',
                        key: 'username',
                        width: 100
                    },
                    {
                        title: '专家邮箱',
                        key: 'expert_mail'
                    },
                    {
                        title: '评审状态',
                        key: 'status',
                        width: 85
                    },
                    {
                        title: '操作',
                        key: 'oper',
                        width: 100,
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
                                            this.score = this.rows1[params.index].score;
                                            this.suggestion = this.rows1[params.index].suggestion;
                                        }
                                    }
                                }, params.row.status=="已评审" ? '查看详情' : '')
                            ] : '不可操作')
                        }
                    }
                ],
                columns2: [
                    {
                        title: '专家名称',
                        key: 'username',
                        width: 100
                    },
                    {
                        title: '专家邮箱',
                        key: 'mail'
                    },
                    {
                        title: '研究领域',
                        key: 'field',
                        width: 140
                    },
                    {
                        title: '操作',
                        key: 'oper',
                        width: 120,
                        align: 'center',
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: {
                                        type: 'primary',
                                        size: 'small',
                                        disabled: this.button_able
                                    },
                                    style: {
                                        marginRight:'5px'
                                    },
                                    on: {
                                        click: () => {
                                            this.button_able = true;
                                            let param = {mail:this.rows2[params.index].mail, project_code:this.proj_id};
                                            this.$http.post(this.$baseURL + "/api/v1/invite_mail",param).then(function (res) {
                                                var detail = res.body.state;
                                                if(detail == "fail"){
                                                    this.$Notice.open({title: "发送失败"});
                                                    this.reload();
                                                }
                                                else{
                                                    this.$Notice.open({title: "已发送邮件"});
                                                    this.reload();
                                                }
                                            }, function (res) {
                                                alert(res);
                                            });
                                        }
                                    }
                                }, '发送评审邀请')
                            ])
                        }
                    }
                ],
                rows1: [],
                rows2: [],
                detail: false,
                proj_id: '0001',
                score: 1,
                suggestion: "",
                isRouterAlive: true,
                button_able: false,
                comp_name: "冯如杯",
                proj_name: "基于",
                typeList: [
                    {
                        value: 'A',
                        label: 'A.机械与控制（包括机械、仪器仪表、自动化控制、工程、交通、建筑等）'
                    },
                    {
                        value: 'B',
                        label: 'B.信息技术（包括计算机、电信、通讯、电子等）'
                    },
                    {
                        value: 'C',
                        label: 'C.数理（包括数学、物理、地球与空间科学等）'
                    },
                    {
                        value: 'D',
                        label: 'D.生命科学（包括生物､农学､药学､医学､健康､卫生､食品等）'
                    },
                    {
                        value: 'E',
                        label: 'E.能源化工（包括能源、材料、石油、化学、化工、生态、环保等）'
                    },
                    {
                        value: 'F',
                        label: 'F.哲学社会科学（包括哲学、经济、社会、法律、教育、管理）'
                    }
                ],
                model1: ''
            }
        },
        created(){
            this.proj_id = this.$route.query.projectID;
            this.getTwoList();
        },
        methods:{
            getTwoList(){
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
                        this.rows1 = res.body.list_invited;
                        this.rows2 = res.body.list_uninvited;
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
        border: 1px dashed black;
        border-radius: 5px;
        /*margin: 0px 500px 0px 0px;*/
        padding: 0px 20px 10px 20px;
        width: 40%;
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
    h4{
        border-left: 5px solid purple;
        padding: 0 0 0 15px!important;
        margin: 16px 0 5px 0!important;
        display: inline;
        float:left;
    }
</style>
