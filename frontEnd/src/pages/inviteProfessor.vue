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
            <Select v-model="model1" @on-change="selectType($event)"
                    style="width:450px;float: left;margin-top:12px;margin-left: 30px;">
                <Option v-for="item in typeList" :value="item.value" :key="item.value">{{ item.label }}</Option>
            </Select>

        </div>
        <div class="body">
            <h3>作品列表</h3>

            <Table stripe border :columns="columns1" :data="rows1" height="450" ref="project_table" on-select-change=""></Table>
            <div @click="chooseStudent" class="btn-lg btn-info" style="float: right; display: inline; cursor: pointer;margin-top: 10px;">
                选择十个
            </div>
        </div>
        <div class="body" style="width: 40%">
            <h3>邀请专家</h3>
            <Table stripe border :columns="columns2" :data="rows2" height="450" ref="expert_table"></Table>
            <div @click="sendEmail" class="btn-lg btn-success" style="float: right; display: inline; cursor: pointer;margin-top: 10px;">
                一键发送
            </div>
            <div @click="chooseExpert" class="btn-lg btn-info" style="float: right; margin-right:30px;display: inline; cursor: pointer;margin-top: 10px;">
                选择三个
            </div>
        </div>
    </div>
</template>


<script>
    import NavBar from '../components/NavBar.vue'
    import Button from "../../static/css/iview/iview";

    export default {
        name: "inviteProfessor",
        components: {
            Button,
            NavBar
        },
        inject: ['reload'],
        data() {
            return {
                columns1: [
                    {
                        type:'index',
                        width:60,
                        align:'center'
                    },
                    {
                        title: '作品名称',
                        key: 'project_name',
                        width: 340
                    },
                    {
                        title: '已邀请的专家数',
                        key: 'ac_exp_num',
                        width: 150,
                        filters: [
                            {
                              label:'0',
                              value: 0
                            },
                            {
                                label: '1',
                                value: 1
                            },
                            {
                                label: '2',
                                value: 2
                            },
                            {
                                label: '2',
                                value: 3
                            },
                            {
                                label: '3个以上',
                                value: 4
                            },
                        ],
                        filterMultiple: false,
                        filterMethod (value, row) {
                            if (value === 1) {
                                return row.ac_exp_num === 1;
                            } else if (value === 2) {
                                return row.ac_exp_num === 2;
                            } else if (value === 3) {
                                return row.ac_exp_num === 3;
                            } else if (value === 4) {
                                return row.ac_exp_num > 3;
                            } else if (value === 0) {
                                return row.ac_exp_num === 0;
                            }
                        }
                    },
                    {
                        type: 'selection',
                        key: 'project_selection',
                        align: 'center',
                        width: 88.9
                    }
                ],
                columns2: [
                    {
                        type:'index',
                        width:60,
                        align:'center'
                    },
                    {
                        title: '专家姓名',
                        key: 'name',
                        width: 170
                    },
                    {
                        title: '专家邮箱',
                        key: 'email',
                        width: 200
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
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: () => {
                                            this.button_able = true;
                                            let param = {
                                                mails: [this.rows2[params.index].email,],
                                                project_codes: []
                                            };
                                            this.$refs.project_table.getSelection().forEach(v =>{
                                                param.project_codes.push(v.project_code)
                                            });
                                            this.$http.post(this.$baseURL + "/api/v1/multi_invite_mail", param).then(function (res) {
                                                var detail = res.body.state;
                                                if (detail == "fail") {
                                                    this.$Notice.open({title: "发送失败"});
                                                    this.reload();
                                                } else {
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
                    },
                    {
                        type: 'selection',
                        align: 'center',
                        key: 'expert_selection',
                        width: 88
                    }
                ],
                rows1: [],
                rows2: [],
                competition_id:'',
                comp_name: "冯如杯",
                proj_name: "基于",
                project_list : [],
                t_project_list: [],
                expert_list: [],
                t_expert_list:[],
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
        created() {
            this.proj_id = this.$route.query.projectID;
            let url = this.$baseURL + '/api/v1/stageprolist';
            this.competition_id = this.$route.query.competitionID;
            console.log(this.competition_id);
            this.$http.post(url, {'competition_id': this.competition_id}).then(function (res) {
                console.log(res);
                if (res.body.state === 'success'){
                    this.project_list = res.body.B_List;
                    this.rows1 = this.project_list;
                }
                else{
                    this.$Message.error('获取数据失败！');
                }
            },function (res) {
                console.log(res)
            })

            //获取专家
            url = this.$baseURL + '/api/v1/get_expert_list';
            this.$http.post(url).then(function (res) {
                console.log(res);
                if (res.body.state === 'success'){
                    this.expert_list = res.body.list;
                    this.rows2 = this.expert_list;
                }
                else{
                    this.$Message.error('获取数据失败！');
                }
            },function (res) {
                console.log(res)
            })

        },
        methods: {
            selectType(value) {

                this.t_project_list = [];
                this.t_expert_list = [];
                //筛选
                this.project_list.forEach(v=>{
                    if(v.registration_form.type === value){
                        this.t_project_list.push(v);
                    }
                })
                this.rows1 = this.t_project_list;

                //筛选专家
                var pos = value.charCodeAt()-65;
                console.log(this.expert_list);
                this.expert_list.forEach(v=>{
                    if(v.field[pos] === '1'){
                        this.t_expert_list.push(v);
                    }
                })
                this.rows2 = this.t_expert_list;
            },
            chooseStudent(){
                if(this.model1!==''){
                    if(this.rows1.length<=10){
                        this.$refs.project_table.selectAll(true);
                    }
                    else{
                        this.$refs.project_table.selectAll(false);
                        for(var i=0;i<10;i++){
                            this.$refs.project_table.toggleSelect(i);
                        }
                    }
                }else{
                    this.$Message.error('请先选择类别。')
                }
            },
            chooseExpert(){
                if(this.model1!==''){
                    if(this.rows2.length<=3){
                        this.$refs.expert_table.selectAll(true);
                    }
                    else{
                        this.$refs.expert_table.selectAll(false);
                        for(var i=0;i<3;i++){
                            this.$refs.expert_table.toggleSelect(i);
                        }
                    }
                }else{
                    this.$Message.error('请先选择类别。')
                }
            },
            sendEmail(){
                var params = {
                    'mails':[],
                    'project_codes':[]
                };
                if(this.model1!==''){
                    console.log();
                    var proj_list = this.$refs.project_table.getSelection();
                    var lists = this.$refs.expert_table.getSelection();

                    proj_list.forEach(v=>{
                        params.project_codes.push(v.project_code);
                    });

                    lists.forEach(v=>{
                        params.mails.push(v.email);
                    });

                    console.log(params);
                    var url = this.$baseURL + '/api/v1/multi_invite_mail';
                    this.$http.post(url,params).then(function (res) {
                        console.log(res);
                        if(res.body.state !== 'fail'){

                            //启动删除程序
                            for(let y = 0, max1 = proj_list.length; y < max1; y ++){
                                for(let i = 0; i < this.rows1.length; i++){
                                    if(proj_list[y].project_code === this.rows1[i].project_code && proj_list[y].project_name === this.rows1[i].project_name) {
                                        params.project_codes.push(this.rows1[i].project_code);
                                        this.rows1.splice(i, 1);
                                        i--;
                                    }
                                }
                            }
                            this.t_project_list = this.rows1;

                            console.log(lists);
                            for(let y = 0, max1 = lists.length; y < max1; y ++){
                                for(let i = 0, max = this.rows2.length; i < max; i++){
                                    console.log(this.rows2[i]);
                                    if(lists[y].email === this.rows2[i].email && lists[y].name === this.rows2[i].name) {

                                        var tmp = this.rows2[i];
                                        this.rows2.splice(i, 1);
                                        this.rows2.push(tmp);
                                    }
                                }
                            }
                            this.t_expert_list = this.rows2;

                            this.$Message.success('邀请成功！');
                        }else{
                            this.$Message.error('邀请失败！');
                        }
                    },function (res) {
                        this.$Message.error('邀请失败！网络错误。')
                    })


                }else{
                    this.$Message.error('请先选择类别。')
                }
            },
        },
        mounted(){
            this.$Message.config({
                top: 100,
                duration: 1,
            });
        }
    }
</script>

<style scoped>
    .nav {
        left: 280px;
        top: 100px;
        position: relative;
        float: left;
        border: none;
        /*margin: 0px 500px 0px 0px;*/
        padding: 0px 0px 15px 10px;
        width: 80%;
    }

    .body {
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

    .size {
        font-size: 17px;
    }

    h3 {
        border-left: 5px solid purple;
        padding: 0 0 0 15px !important;
        font-size: 24px !important;
        margin: 24px 0 !important;
    }

    h4 {
        border-left: 5px solid purple;
        padding: 0 0 0 15px !important;
        margin: 16px 0 5px 0 !important;
        display: inline;
        float: left;
    }
</style>
