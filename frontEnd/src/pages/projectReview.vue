<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <h2>作品评审</h2>
            <div style="margin-bottom: 10px; text-align: center">
                作品ID：
                <Input style="width: 15%;margin-right: 5%" placeholder="输入作品ID搜索" v-model="searchContent1"
                       @on-change="handleChange"/>
                作品名称：
                <Input style="width: 15%;margin-right: 5%" placeholder="输入作品名称搜索" v-model="searchContent2"
                       @on-change="handleChange"/>
                竞赛名称：
                <Input style="width: 15%;margin-right: 5%" placeholder="输入竞赛名称搜索" v-model="searchContent3"
                       @on-change="handleChange"/>
                <!--评审截止时间：
                <DatePicker confirm split-panels type="daterange" placeholder="选择订单日期范围"
                            style="width: 20%"></DatePicker>-->
            </div>
            <Table stripe border :columns="columns" :data="rows" ref="table"
                   @on-selection-change="setSelectedData"></Table>
            <div style="margin-top: 10px;text-align: center">
                <Button type="primary" @click="exportData(1)">
                    <Icon type="ios-download-outline"></Icon>
                    下载全部作品文档
                </Button>
                <Button type="success" @click="exportData(2)">
                    <Icon type="ios-download-outline"></Icon>
                    下载选择作品文档
                </Button>
            </div>
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
                        type: 'selection',
                        width: 60,
                        align: 'center'
                    },
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
                                                    console.log(res);
                                                    if (res.body.state === 'fail') {
                                                        this.$Message.error(res.body.reason);
                                                        return;
                                                    }
                                                    this.$Message.success("成功拒绝该项目的评审");
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
                                                this.$http.get(this.$baseURL + '/api/v1/download_files', {
                                                    params: {
                                                        project_code: params.row.project_id
                                                    }
                                                }).then(function (res) {
                                                    console.log(res);
                                                    if (res.body.state === 'Success') {
                                                        window.location.href = res.body.url;
                                                    } else {
                                                        this.$Message.error("下载失败" + res.body.reason)
                                                    }
                                                }, function (res) {
                                                    console.log(res)
                                                })
                                            } else {
                                                this.$http.get(this.$baseURL + '/api/v1/accept_review', {
                                                    params: {
                                                        project_code: params.row.project_id,
                                                        expert_email: this.$cookie.get('mail')
                                                    }
                                                }).then(function (res) {
                                                    console.log(res);
                                                    if (res.body.state === 'success') {
                                                        params.row.status = '评审中';
                                                        this.$Message.success("成功接收该项目的评审")
                                                    } else {
                                                        this.$Message.error("操作失败，请稍后再试")
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
                selectedData: [],
                initRows: [],
                searchContent1: '',
                searchContent2: '',
                searchContent3: '',
            }
        },
        created() {
            this.getProjectReviewList()
        },
        methods: {
            getProjectReviewList() {
                let url = this.$baseURL + '/api/v1/get_expert_review_list';
                this.$http.post(url, {email: this.$cookie.get('mail')}).then(function (res) {
                    console.log(res);
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
                        if (item.status !== '评审中' && item.status !== '已评审') {
                            item._disabled = true;
                        }
                    }
                    this.rows = res.body.project_lists;
                    this.initRows = this.rows;
                }, function (res) {
                    console.log(res)
                })
            },
            setSelectedData(selection) {
                this.selectedData = selection
            },
            compareObject(obj1, obj2) {
                let attrs1 = Object.keys(obj1);
                let attrs2 = Object.keys(obj2);
                if (attrs1.length !== attrs2.length) {
                    return false
                }
                for (let j = 0; j < attrs1.length; j++) {
                    let attrNames = attrs1[j];
                    if (obj1[attrNames] !== obj2[attrNames]) {
                        return false
                    }
                }
                return true
            },
            exportData(type) {
                for (let item of this.rows) {
                    if (item.status === '已评审' || item.status === '评审中') {
                        let flag = false;
                        if (type === 2) {
                            console.log('in')
                            for (let selected of this.selectedData) {
                                if (this.compareObject(selected, item))
                                    flag = true;
                            }
                        } else flag = true;
                        if (flag) {
                            this.$http.get(this.$baseURL + '/api/v1/download_files', {
                                params: {
                                    project_code: item.project_id
                                }
                            }).then(function (res) {
                                if (res.body.state === 'Success') {
                                    window.location.href = res.body.url;
                                } else {
                                    this.$Message.error("下载" + item.project_id + "号作品失败，" + res.body.reason)
                                }
                            }, function (res) {
                                console.log(res)
                            })
                        }
                    }
                }
            },
            handleChange() {
                this.rows = this.initRows;
                this.rows = this.search(this.rows, {
                    'project_id': this.searchContent1,
                    'project_name': this.searchContent2,
                    'competition_name': this.searchContent3,
                })
            },
            search(data, argumentObj) {
                let res = data;
                let dataClone = data;
                for (let argu in argumentObj) {
                    if (argumentObj[argu].length > 0) {
                        res = dataClone.filter(d => {
                            return d[argu].indexOf(argumentObj[argu]) > -1
                        });
                        dataClone = res
                    }
                }
                return res
            },
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
