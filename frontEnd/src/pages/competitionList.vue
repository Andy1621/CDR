<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <h2>竞赛列表</h2>
            <Table stripe border :columns="columns" :data="rows" ref="table" style="width:100%"></Table>
        </div>
        <router-view v-if="isRouterAlive"></router-view>
    </div>
</template>

<script>
    import NavBar from '../components/NavBar.vue'

    export default {
        components: {
            NavBar
        },
        name: 'competitionList',
        inject: ['reload'],
        data() {
            return {
                role: '',
                columns: [
                    {
                        title: '竞赛名称',
                        key: 'competition_name',
                        width: 250
                    },
                    {
                        title: '报名开始时间',
                        key: 'begin_time',
                        width: 150
                    },
                    {
                        title: '报名截止时间',
                        key: 'end_time',
                        width: 150
                    },
                    {
                        title: '参赛作品总数',
                        key: 'count',
                        width: 120,
                    },
                    {
                        title: '竞赛状态',
                        key: 'com_status',
                        width: 130,
                        filters: [
                            {
                                label: '未开始',
                                value: 1
                            },
                            {
                                label: '报名提交',
                                value: 2
                            },
                            {
                                label: '校团委初审',
                                value: 3
                            },
                            {
                                label: '专家初评',
                                value: 4
                            },
                            {
                                label: '现场答辩',
                                value: 5
                            },
                            {
                                label: '最终结果公布',
                                value: 6
                            },
                            {
                                label: '已结束',
                                value: 7
                            }
                        ],
                        filterMultiple: false,
                        filterMethod (value, row) {
                            if (value === 1) {
                                return row.com_status === '未开始';
                            } else if (value === 2) {
                                return row.com_status === '报名提交';
                            } else if (value === 3) {
                                return row.com_status === '校团委初审';
                            } else if (value === 4) {
                                return row.com_status === '专家初评';
                            } else if (value === 5) {
                                return row.com_status === '现场答辩';
                            } else if (value === 6) {
                                return row.com_status === '最终结果公布';
                            } else {
                                return row.com_status === '已结束';
                            }
                        }
                    },
                    {
                        title: '操作',
                        key: 'oper',
                        align: 'center',
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: {
                                        type: 'primary',
                                        size: 'small',
                                        disabled: params.row.com_status == "未开始"
                                    },
                                    style: {
                                        marginRight: '5px',
                                        display: this.role === 'student'? 'none' :'',
                                    },
                                    on: {
                                        click: () => {
                                            this.$router.push({
                                                path: '/stageProList',
                                                query: {
                                                    competitionID: params.row.competition_id,
                                                    // competitionTitle: params.row.competition_name
                                                }
                                            })
                                        }
                                    }
                                }, '竞赛入口'),
                                h('Button', {
                                    props: {
                                        type: 'success',
                                        size: 'small',
                                        disabled: params.row.com_status != "报名提交"
                                    },
                                    style: {
                                        marginRight: '5px',
                                        display: this.role === 'student'? '' :'none',
                                    },
                                    on: {
                                        click: () => {
                                            this.apply_new(params.row.competition_id)
                                        }
                                    }
                                }, '报名竞赛'),
                                h('Button', {
                                    props: {
                                        type: 'primary',
                                        size: 'small',
                                    },
                                    style: {
                                        marginRight: '5px',
                                        display: this.role === 'student'? '' :'none',
                                    },
                                    on: {
                                        click: () => {
                                            this.to_competition(params.row.competition_id)
                                        }
                                    }
                                }, '竞赛详情'),
                                h('Button', {
                                    props: {
                                        type: 'primary',
                                        size: 'small',
                                    },
                                    style: {
                                        marginRight: '5px',
                                        display: (this.role === 'school' && params.row.com_status == "专家初评")? '' :'none',
                                    },
                                    on: {
                                        click: () => {
                                            this.$router.push({
                                                path: '/inviteProfessor',
                                                query: {
                                                    competitionID: params.row.competition_id,
                                                    competitionTitle: params.row.competition_name
                                                }
                                            })
                                        }
                                    }
                                }, '邀请专家'),
                                // h('Button', {
                                //     props: {
                                //         type: 'primary',
                                //         size: 'small',
                                //     },
                                //     style: {
                                //         marginRight: '5px',
                                //         display: (this.role === 'school' && params.row.com_status == "专家初评")? '' :'none',
                                //     },
                                //     on: {
                                //         click: () => {
                                //             let param = {'comp_id': params.row.competition_id};
                                //             this.$http.post(this.$baseURL + "/api/v1/remind_expert",param,{
                                //                 headers:{
                                //                     'Content-Type':"application/json",
                                //                 }
                                //             }).then(function (res) {
                                //                 var detail = res.body.state
                                //                 console.log(detail);
                                //                 if(detail =="fail"){
                                //                     this.$Notice.open({title: "发送失败",duration:0.5});
                                //                 }
                                //                 else{
                                //                     this.$Notice.open({title: "发送成功",duration:0.5});
                                //                 }
                                //             }, function (res) {
                                //                 alert(res);
                                //             });
                                //         }
                                //     }
                                // }, 'gkd'),
                                h('Upload', {
                                    props: {
                                        action: this.$baseURL + '/api/v1/uploadreviewform',
                                        data :{'competition_id': params.row.competition_id},
                                        format: ['xls', 'xlsx']
                                    },
                                    style: {
                                        display: (this.role === 'school' && params.row.com_status == "最终结果公布")? 'inline' :'none',
                                    }
                                }, [
                                    h('Button', {
                                        props: {
                                            type: 'primary',
                                            size: 'small',
                                        },
                                        style: {

                                        }
                                    }, '最终成绩导入')
                                ])
                            ])
                        }
                    }
                ],
                rows: [
                    // {
                    //     competitionName: '冯如杯',
                    //     startTime: '2019-06-29',
                    //     endTime: '2018-07-10',
                    //     groupNumber: 233
                    // }
                ],
                isRouterAlive: true,
            }
        },
        created() {
            this.role = this.$cookie.get('role');
            if (this.role == 'student') {
                this.columns.splice(3, 1)//对于学生不显示作品数
            }
            this.getcomList()
        },
        methods: {
            getcomList() {
                let params = {};
                this.$http.post(this.$baseURL + "/api/v1/contestlist", params, {
                    headers: {
                        'Content-Type': "application/json",
                    }
                }).then(function (res) {
                    var detail = res.body;
                    console.log("请求反回数据 ", detail);
                    if (detail.state == "fail") {
                        this.$Message.info("获取数据失败")
                    } else {
                        for (let item of detail.contests) {
                            switch (item.com_status) {
                                case -1:
                                    item.com_status = "未开始";
                                    break;
                                case 0:
                                    item.com_status = "报名提交";
                                    break;
                                case 1:
                                    item.com_status = "校团委初审";
                                    break;
                                case 2:
                                    item.com_status = "专家初评";
                                    break;
                                case 3:
                                    item.com_status = "现场答辩";
                                    break;
                                case 4:
                                    item.com_status = "最终结果公布";
                                    break;
                                case 5:
                                    item.com_status = "已结束";
                                    break;
                            }
                        }
                        this.rows = detail.contests
                    }
                }, function (res) {
                    alert(res);
                });
            },
            apply_new(competition_id){
                //default
                let params = {
                    'email' : this.$cookie.get('mail'),
                    'name' : this.$cookie.get('username'),
                    'competition_id' : competition_id,
                }
                this.$http.post(this.$baseURL + '/api/v1/add_project',params)
                    .then(function (res) {

                        var detail = res.body
                        console.log(detail)
                        if(detail.state == 'success'){
                            this.$router.push({
                                path: '/apply',
                                query: {
                                    projectID: detail.project_code,
                                }
                            })
                        }
                        else{
                            this.$Message.error('申请失败 ' + detail.reason)
                        }
                    },function (res) {
                        this.$Message.error('Failed')
                    })
            },
            to_competition(competition_id){
                this.$router.push({
                    path : '/messageDetail',
                    query: {
                        type: 'competition',
                        from: 'list',
                        competitionID: competition_id,
                    }
                })
            },
        }
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
        border-left: 5px solid dodgerblue;
        padding: 0 0 0 15px !important;
        font-size: 28px !important;
        margin: 24px 0 !important;
    }
</style>
