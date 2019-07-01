<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <h2>作品评审</h2>
            <Table stripe border :columns="columns" :data="rows" ref="table"></Table>
        </div>
    </div>
</template>

<script>
    import NavBar from '../components/NavBar.vue'

    export default {
        name: "projectReview",
        components: {
            NavBar
        },
        data() {
            return {
                columns: [
                    {
                        title: '作品ID',
                        key: 'project_id'
                    },
                    {
                        title: '作品名称',
                        key: 'project_name'
                    },
                    {
                        title: '竞赛名称',
                        key: 'competition_name'
                    },
                    {
                        title: '评审截止',
                        key: 'expert_comments_ddl'
                    },
                    {
                        title: '所处状态',
                        key: 'status'
                    },
                    {
                        title: '操作',
                        key: 'oper',
                        align: 'center',
                        width: 250,
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: {
                                        type: 'warning',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: () => {
                                            if (params.row.status !== '待回应') {
                                                this.$router.push({
                                                    path: '/projectDetail',
                                                    query: {
                                                        project_id: params.row.project_id
                                                    }
                                                })
                                            } else {
                                                this.$http.get(this.$baseURL + '/api/v1/refuse_review', {
                                                    params: {
                                                        project_code: params.row.project_id,
                                                        expert_email: this.$cookie.get('mail')
                                                    }
                                                }).then(function (res) {
                                                    console.log(res)
                                                    alert("成功拒绝该项目的评审")
                                                    this.rows.splice(params.index, 1);
                                                }, function (res) {
                                                    console.log(res)
                                                })
                                            }
                                        }
                                    }
                                }, params.row.status === '待回应' ? '拒绝评审' : '查看作品'),
                                h('Button', {
                                    props: {
                                        type: 'primary',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: () => {
                                            if (params.row.status !== '待回应') {
                                                alert('下载')
                                            } else {
                                                this.$http.get(this.$baseURL + '/api/v1/accept_review', {
                                                    params: {
                                                        project_code: params.row.project_id,
                                                        expert_email: this.$cookie.get('mail')
                                                    }
                                                }).then(function (res) {
                                                    console.log(res)
                                                    if (res.body.state === 'success') {
                                                        params.row.status = '评审中';
                                                        alert("成功接收该项目的评审")
                                                    }
                                                    else {
                                                        alert("操作失败")
                                                    }
                                                }, function (res) {
                                                    console.log(res)
                                                })
                                            }
                                        }
                                    }
                                }, params.row.status === '待回应' ? '接受评审' : '下载作品')
                            ])
                        }
                    },
                ],
                rows: [],
            }
        },
        created() {
            this.getProjectReviewList()
        },
        methods: {
            getProjectReviewList() {
                let url = this.$baseURL + '/api/v1/get_expert_review_list';
                this.$http.post(url, {email: this.$cookie.get('mail')}).then(function (res) {
                    console.log(res)
                    for (let item of res.body.project_lists) {
                        switch (item.status) {
                            case -1:
                                item.status = "待回应";
                                break;
                            case 0:
                                item.status = "评审中";
                                break;
                            case 1:
                                item.status = "已拒绝";
                                break;
                            case 2:
                                item.status = "已评审";
                                break;
                        }
                    }
                    this.rows = res.body.project_lists;
                }, function (res) {
                    console.log(res)
                })
            }
        },
    }
</script>

<style scoped>
    h2 {
        border-left: 5px solid purple;
        padding: 0 0 0 15px !important;
        font-size: 28px !important;
        margin: 24px 0 !important;
    }

    .body {
        margin-left: 280px;
        margin-bottom: 50px;
        position: relative;
        top: 100px;
        border: 1px dashed black;
        border-radius: 20px;
        /*margin: 100px 0px 50px 30%;*/
        padding: 10px;
        width: 77%;
        /*text-align: center;*/
        min-height: 470px;
        min-width: 600px;
        color: black;
    }
</style>
