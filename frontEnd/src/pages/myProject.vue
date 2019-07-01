<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <h2>我的项目</h2>
            <Button style="margin: 10px" icon="md-add-circle" @click="apply_new">申请项目</Button>
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
                project_list: [],
                columns: [
                    {
                        title: '项目id',
                        key: 'project_code'
                    },
                    {
                        title: '项目名称',
                        key: 'project_name'
                    },
                    {
                        title: '竞赛名称',
                        key: 'competition_name'
                    },
                    {
                        title: '作品状态',
                        key: 'project_status'
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
                                                query: {
                                                    projectID: params.row.project_code
                                                }
                                            })
                                        }
                                    }
                                }, params.row.project_status!=='未提交'?'查看作品':'编辑作品'),
                                h('Button', {
                                    props: {
                                        type: params.row.project_status!=='未提交'?'success':'error',
                                        size: 'small',
                                    },
                                    on: {
                                        click: () => {
                                            let p = params;
                                            let url = '';
                                            if (params.row.project_status!=='未提交')
                                            {
                                                //查看并导出
                                                url = '';
                                                this.$http.get(this.$baseURL + '/api/v1/view_apply',{params:{'project_code': p.row.project_code}})
                                                    .then(function (res) {
                                                        var detail = res.body
                                                        console.log(detail)
                                                        if(detail.state == 'fail'){
                                                            this.$Message.error(detail.reason)
                                                        }
                                                        else{
                                                            // this.$Message.success('Yeeeees')
                                                            // window.location.href = detail.html_url
                                                            window.open(detail.html_url)
                                                        }
                                                    },function (res) {
                                                        this.$Message.error('Failed')
                                                    })
                                            }
                                            else
                                            {
                                                //删除项目
                                                var that = this;
                                                this.$Modal.confirm({
                                                    title:'是否确认删除',
                                                    onOk(){
                                                        that.remove(params.index);
                                                        url = '';
                                                        this.$http.get(this.$baseURL + '/api/v1/delete_project', {params:{'project_code' : p.row.project_code}},{emulateJSON: true})
                                                            .then(function (res) {
                                                                console.log(res.body)
                                                                if(res.body.state == 'success'){
                                                                    this.$Message.success('成功删除')
                                                                }
                                                                else{
                                                                    this.$Message.error('删除失败 '+res.body.reason)
                                                                }
                                                            },function (res) {
                                                                console.log(res)
                                                            })
                                                    }
                                                })
                                            }
                                        }
                                    }
                                }, params.row.project_status!=='未提交'?'导出作品':'删除作品')
                            ])
                        }
                    }
                ],
                rows: []
            }
        },
        created(){
            // let url='https://www.easy-mock.com/mock/5c833375e0e0f75c246237e4/example/mock'
            // this.$http.get(url).then(function (res) {
            //     this.rows=res.body.rows;
            //     console.log(this.rows)
            // },function (res) {
            //     console.log(res)
            // })
            this.$Message.config({
                top: 100,
                duration: 1,
            });
            this.$http.get(this.$baseURL + '/api/v1/get_project_list',{params:{'author_email':this.$cookie.get('username')}})
                .then(function (res) {
                    var detail = res.body
                    console.log(detail)
                    if(detail.state == 'success'){
                        var tmp_list = detail.project_list;
                        var length = tmp_list.length;
                        for(var i=0; i<length; i++){
                            switch(tmp_list[i].project_status){
                                case -1:
                                    tmp_list[i].project_status = '未提交';
                                    break;
                                case 0:
                                    tmp_list[i].project_status = '待初审';
                                    break;
                                case 1:
                                    tmp_list[i].project_status = '专家审核中';
                                    break;
                                case 2:
                                    tmp_list[i].project_status = '未进入现场赛';
                                    break;
                                case 3:
                                    tmp_list[i].project_status = '进入现场赛';
                                    break;
                                case 4:
                                    tmp_list[i].project_status = '优秀奖';
                                    break;
                                case 5:
                                    tmp_list[i].project_status = '三等奖';
                                    break;
                                case 6:
                                    tmp_list[i].project_status = '二等奖';
                                    break;
                                case 7:
                                    tmp_list[i].project_status = '一等奖';
                                    break;
                            }
                            if(tmp_list[i].project_name==''){
                                tmp_list[i].project_name = '暂未填写';
                            }
                        }
                        this.project_list = tmp_list;
                        this.rows=this.project_list;
                    }
                    else{
                        this.$Message.error('获取列表失败 ' + detail.reason)
                    }
                    console.log(this.rows)
                },function (res) {
                    this.$Message.error('Failed')
                })
        },
        methods:{
            remove (index) {
                this.rows.splice(index, 1);
            },
            apply_new(){
                //default
                let params = {
                    'email' : this.$cookie.get('mail'),
                    'name' : this.$cookie.get('username'),
                    'competition_id' : '5d170bd90a21e6053e45f3eb',
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