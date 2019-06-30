<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <h2>作品评审</h2>
            <Table stripe border :columns="columns" :data="rows" ref="table" ></Table>
        </div>
    </div>
</template>

<script>
    import NavBar from '../components/NavBar.vue'
    export default {
        name: "projectReview",
        components:{
            NavBar
        },
        data(){
            return {
                columns:[
                    {
                        title: '作品ID',
                        key: 'projectID'
                    },
                    {
                        title: '作品名称',
                        key: 'projectName'
                    },
                    {
                        title: '竞赛名称',
                        key: 'competition'
                    },
                    {
                        title: '评审截止',
                        key: 'endTime'
                    },
                    {
                        title: '操作',
                        key: 'oper',
                        align: 'center',
                        width: 250,
                        render:(h, params) => {
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
                                            alert('查看')
                                            this.$router.push({
                                                path: '/projectDetail',
                                                query: {
                                                    projectID: params.row.projectID
                                                }
                                            })
                                        }
                                    }
                                }, '查看作品'),
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
                                            alert('下载')
                                        }
                                    }
                                }, '下载作品')
                            ])
                        }
                    },
                ],
                rows: [],
            }
        },
        created(){
            this.getProjectReviewList()
        },
        methods:{
            getProjectReviewList(){
                let url = 'https://www.easy-mock.com/mock/5c833375e0e0f75c246237e4/example/mock';
                this.$http.get(url, {params:{professerID: 'aaa'}}).then(function (res) {
                    this.rows=res.body.rowsProject;
                },function (res) {
                    console.log(res)
                })
            }
        },
    }
</script>

<style scoped>
    h2{
        border-left: 5px solid purple;
        padding: 0 0 0 15px!important;
        font-size: 28px!important;
        margin: 24px 0!important;
    }
    .body{
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