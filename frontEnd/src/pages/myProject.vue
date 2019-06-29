<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <h2>我的项目</h2>
            <Table stripe border :columns="columns" :data="rows" ref="table" ></Table>
        </div>
    </div>
</template>

<script>
    import NavBar from '../components/NavBar.vue'
    export default {
        name: "myProject",
        components:{
            NavBar
        },
        data(){
            return{
                columns: [
                    {
                        title: '项目id',
                        key: 'projectID'
                    },
                    {
                        title: '项目名称',
                        key: 'projectName'
                    },
                    {
                        title: '竞赛名称',
                        key: 'competition'
                    },
                    {
                        title: '作品状态',
                        key: 'status'
                    },
                    {
                        title: '操作',
                        key: 'oper',
                        width: 200,
                        align: 'center',
                        render: (h, params) => {
                            return h('div', [
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
                                            this.$router.push({
                                                path: '/apply',
                                            })
                                        }
                                    }
                                }, params.row.status=='已提交'?'查看作品':'编辑作品'),
                                h('Button', {
                                    props: {
                                        type: params.row.status=='已提交'?'success':'error',
                                        size: 'small',
                                    },
                                    on: {
                                        click: () => {
                                            let p = params;
                                            let url = '';
                                            if (params.row.status=='已提交')
                                            {
                                                url = '';
                                                /*this.$http.get(url, {params:{projectID:p.row.projectID}).then(function (res) {
                                                    location.href(res.body.url)
                                                },function (res) {
                                                    console.log(res)
                                                })
                                                return;*/
                                            }
                                            else
                                            {
                                                var that = this;
                                                this.$Modal.confirm({
                                                    onOk(){
                                                        that.remove(params.index);
                                                        url = '';
                                                        /*this.$http.post(url, {projectID:p.row.projectID},{emulateJSON: true}).then(function (res) {
                                                            console.log(res)
                                                        },function (res) {
                                                            console.log(res)
                                                        })*/
                                                    }
                                                })
                                            }
                                        }
                                    }
                                }, params.row.status=='已提交'?'导出作品':'删除作品')
                            ])
                        }
                    }
                ],
                rows: []
            }
        },
        created(){
            let url='https://www.easy-mock.com/mock/5c833375e0e0f75c246237e4/example/mock'
            this.$http.get(url).then(function (res) {
                this.rows=res.body.rows;
            },function (res) {
                console.log(res)
            })
        },
        methods:{
            remove (index) {
                this.rows.splice(index, 1);
            }
        },
    }
</script>

<style scoped>
    .body{
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
    h2{
        border-left: 5px solid purple;
        padding: 0 0 0 15px!important;
        font-size: 28px!important;
        margin: 24px 0!important;
    }
</style>