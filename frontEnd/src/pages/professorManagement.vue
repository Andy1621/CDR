<template>
    <div>
        <NavBar></NavBar>
        <div class="body" v-if="table1">
            <h2>{{this.title}}</h2>
            <v-table
                is-vertical-resize
                is-horizontal-resize
                style="width:100%"
                :min-height='300'
                :height='320'
                :columns="columns"
                :table-data="tableData"
                row-hover-color="#eee"
                row-click-color="#edf7ff"
                @on-custom-comp="customCompFunc"
            ></v-table>
            <Button type="primary" @click="import_expert = true" style="font-size:16px; margin-left: 45%; margin-top: 20px">导入专家</Button>          
        </div>
        <Modal
            v-model="import_expert"
            title="导入专家">
            <h4 style="color: #EA2027">务必按照附件模板格式导入</h4>
            <h5 style="margin-left: 5px; color: #0652DD">注意专家领域仅能在六种领域选择，不同领域之间逗号隔开</h5>
            <ul style="margin-left: 20px">
                <li style="color: #0652DD">机械与控制（包括机械、仪器仪表、自动化控制、工程、交通、建筑等）</li>
                <li style="color: #0652DD">信息技术（包括计算机、电信、通讯、电子等）</li>
                <li style="color: #0652DD">数理（包括数学、物理、地球与空间科学等）</li>
                <li style="color: #0652DD">生命科学（包括生物､农学､药学､医学､健康､卫生､食品等）</li>
                <li style="color: #0652DD">能源化工（包括能源、材料、石油、化学、化工、生态、环保等）</li>
                <li style="color: #0652DD">哲学社会科学（包括哲学、经济、社会、法律、教育、管理）</li>
            </ul>
            <p>
                <Icon style="margin-right: 10px" type="ios-cloud-download"></Icon>
                专家导入模板.xlsx
                <Button @click="download(attachment_url)" ghost shape="circle"
                        style="margin-left: 20px;" type="info">点击下载
                </Button>
            </p>
            <div slot="footer">
                <vue-xlsx-table @on-select-file="handleSelectedFile">导入</vue-xlsx-table>
            </div>
        </Modal>
        <Modal
            v-model="edit1"
            title="修改专家信息"
            @on-ok="sumbit_edit1"
            @on-cancel="cancel_edit1"
            width="600">
            <Row type="flex" justify="center" align="middle" class="code-row-bg">
                <Col span="3" ><B style="font-size: 16px">用户名</B></Col>
                <Col span="21"><Input v-model="name" placeholder="请输入您的用户名" size="large"></Input></Col>
            </Row>
            <br>
            <Row type="flex" justify="center" align="middle" class="code-row-bg">
                <Col span="3" ><B style="font-size: 16px">领域</B></Col>
                <Col span="21">
                    <CheckboxGroup v-model="field" >
                        <Checkbox label="A" size="large">机械与控制（包括机械、仪器仪表、自动化控
制、工程、交通、建筑等）</Checkbox><br>
                        <Checkbox label="B" size="large">信息技术（包括计算机、电信、通讯、电子等）</Checkbox><br>
                        <Checkbox label="C" size="large">数理（包括数学、物理、地球与空间科学等）</Checkbox><br>
                        <Checkbox label="D" size="large">生命科学（包括生物､农学､药学､医学､健
康､卫生､食品等）</Checkbox><br>
                        <Checkbox label="E" size="large">能源化工（包括能源、材料、石油、化学、化
工、生态、环保等）</Checkbox><br>
                        <Checkbox label="F" size="large">哲学社会科学（包括哲学、经济、社会、法律、教育、管理）</Checkbox><br>
                    </CheckboxGroup>
                </Col>
            </Row>
        </Modal>
        <Modal
            v-model="delete_expert"
            title="修改专家信息"
            @on-ok="submit_delete"
            @on-cancel="cancel_delete"
            width="600">
            <B>确认删除专家【{{name}}】吗？</B>
        </Modal>
        <div class="body" v-if="table2">
            <h2>{{this.title}}</h2>
            <v-table
                is-vertical-resize
                is-horizontal-resize
                style="width:100%"
                :min-height='300'
                :height='320'
                :columns="columns"
                :table-data="tableData"
                row-hover-color="#eee"
                row-click-color="#edf7ff"
                @on-custom-comp="customCompFunc"
            ></v-table>
            <Row>
                <Col span="4" offset="6">
                    <Button type="success" @click="sumbit_import" style="font-size:16px; margin-left: 40%; margin-top: 20px">确认</Button>
                </Col>
                <Col span="4">
                    <Button type="error" @click="cancel_import" style="font-size:16px; margin-left: 60%; margin-top: 20px">取消</Button>
                </Col>
            </Row>
        </div>
        <Modal
            v-model="edit2"
            title="修改专家信息"
            @on-ok="sumbit_edit2"
            @on-cancel="cancel_edit2"
            width="600">
            <Row type="flex" justify="center" align="middle" class="code-row-bg">
                <Col span="3" ><B style="font-size: 16px">用户名</B></Col>
                <Col span="21"><Input v-model="name" placeholder="请输入您的用户名" size="large"></Input></Col>
            </Row>
            <br>
            <Row type="flex" justify="center" align="middle" class="code-row-bg">
                <Col span="3" ><B style="font-size: 16px">领域</B></Col>
                <Col span="21">
                    <CheckboxGroup v-model="field" >
                        <Checkbox label="A" size="large">机械与控制（包括机械、仪器仪表、自动化控
制、工程、交通、建筑等）</Checkbox><br>
                        <Checkbox label="B" size="large">信息技术（包括计算机、电信、通讯、电子等）</Checkbox><br>
                        <Checkbox label="C" size="large">数理（包括数学、物理、地球与空间科学等）</Checkbox><br>
                        <Checkbox label="D" size="large">生命科学（包括生物､农学､药学､医学､健
康､卫生､食品等）</Checkbox><br>
                        <Checkbox label="E" size="large">能源化工（包括能源、材料、石油、化学、化
工、生态、环保等）</Checkbox><br>
                        <Checkbox label="F" size="large">哲学社会科学（包括哲学、经济、社会、法律、教育、管理）</Checkbox><br>
                    </CheckboxGroup>
                </Col>
            </Row>
        </Modal>
    </div>
</template>

<script>
    import NavBar from '../components/NavBar.vue'
    import Vue from 'vue'
import { connect } from 'net';
import { constants } from 'fs';

    export default {
        components:{
            NavBar
        },
        name: 'professorManagement',
        data () {
            return {
                    tableData: [],
                    columns: [
                        //  {
                        //     field: 'custome', title:'序号', width: 50, titleAlign: 'center', columnAlign: 'center',
                        //     formatter: function (rowData,rowIndex,pagingIndex,field) {
                        //         return rowIndex + 1
                        //     }, isFrozen: true,isResize:true
                        // },
                        {field: 'name', title: '姓名', width: 100, titleAlign: 'center', columnAlign: 'center',isResize:true},
                        {field: 'email', title: '邮箱', width: 200, titleAlign: 'center', columnAlign: 'center',isResize:true},
                        {field: 'field', title: '领域', width: 300, titleAlign: 'center', columnAlign: 'center',
                            formatter: function (rowData,rowIndex,pagingIndex,field) {
                                return `<span class='cell-edit-color'>${rowData[field]}</span>`;
                            }, isResize:true},
                        {field: 'custome-adv', title: '操作',width: 80, titleAlign: 'center',columnAlign:'center',componentName:'table-operation',isResize:true}
                    ],
                    import_expert: false,
                    attachment_url: this.$baseURL + "/static/doc/20190704_专家导入模板.xlsx",
                    table1: true,
                    table2: false,
                    edit1: false,
                    edit2: false,

                    title: "专家列表",

                    // 表格编辑修改信息
                    name: '',
                    email :'',
                    field: [],
                    index: '',

                    // 删除专家信息
                    delete_expert: false
            }
        },
        methods:{
            customCompFunc(params){
                if (params.type === 'delete'){
                    this.delete_expert = true;
                    console.log(params)
                    this.name = params.rowData['name'];
                    this.email = params.rowData['email'];
                    this.index = params.index;
                }
                else if (params.type === 'edit'){
                    // alert(`行号：${params.index} 姓名：${params.rowData['name']}`)
                    if(this.table1){
                        this.edit1 = true;
                        this.edit2 = false;
                        this.index = params.index;
                        this.name = params.rowData['name'];
                        this.email = params.rowData['email'];
                        var field = this.field2string(params.rowData['field']);
                        this.field = [];
                        for(var i = 0;i<6; i++){
                            if (field[i] === '1'){
                                this.field.push(String.fromCharCode(65+i));
                            }
                        }
                    }
                    if(this.table2){
                        this.edit1 = false;
                        this.edit2 = true;
                        this.index = params.index;
                        this.name = params.rowData['name'];
                        this.email = params.rowData['email'];
                        var field = this.field2string(params.rowData['field']);
                        this.field = [];
                        for(var i = 0;i<6; i++){
                            if (field[i] === '1'){
                                this.field.push(String.fromCharCode(65+i));
                            }
                        }
                    }
                }

            },

            download(url) {
                window.open(url);
            },

            handleSelectedFile (convertedData) {
                // console.log(convertedData)
                let params = {
                    'header': convertedData.header
                }
                this.$http.post(this.$baseURL + '/api/v1/check_xlsx_header', params)
                    .then(function (res) {
                        var detail = res.body
                        if(detail.state == 'success'){
                            this.tableData = convertedData.body
                            this.import_expert = false
                            this.title = "导入专家"
                            this.table1 = false
                            this.table2 = true
                            this.$Message.success('导入成功')
                        }
                        else{
                            alert('导入专家信息表失败：' + detail.reason)
                        }
                    },function (res) {
                        this.$Message.error('Failed')
                    })
            },
            
            string2field(onehot) {
                var res = "";
                var field = [];
                if(onehot[0] == '1'){
                    field.push("机械与控制");
                }
                if(onehot[1] == '1'){
                    field.push("信息技术");
                }
                if(onehot[2] == '1'){
                    field.push("数理");
                }
                if(onehot[3] == '1'){
                    field.push("生命科学");
                }
                if(onehot[4] == '1'){
                    field.push("能源化工");
                }
                if(onehot[5] == '1'){
                    field.push("哲学社会科学");
                }
                res = field.join('，');
                return res;
            },

            field2string(str) {
                var res = "";
                var field = str.split('，');
                if(field.indexOf("机械与控制") != -1){
                    res += "1";
                }
                else{
                    res += "0";
                }
                if(field.indexOf("信息技术") != -1){
                    res += "1";
                }
                else{
                    res += "0";
                }
                if(field.indexOf("数理") != -1){
                    res += "1";
                }
                else{
                    res += "0";
                }
                if(field.indexOf("生命科学") != -1){
                    res += "1";
                }
                else{
                    res += "0";
                }
                if(field.indexOf("能源化工") != -1){
                    res += "1";
                }
                else{
                    res += "0";
                }
                if(field.indexOf("哲学社会科学") != -1){
                    res += "1";
                }
                else{
                    res += "0";
                }
                return res;
            },

            sumbit_edit1() {
                if(this.name == ''){
                    this.$Message.error('修改失败：用户名不能为空！');
                    return;
                } 

                var rt = '000000';
                rt = '000000';
                rt = rt.split('');
                this.field.forEach(v=>{
                    rt[v.charCodeAt()-65]='1';
                })
                rt = rt.join('');

                let url = this.$baseURL + '/api/v1/change_info';
                // console.log(rt);
                this.$http.post(url,{
                    'mail': this.email,
                    'username':this.name,
                    'field':rt
                }).then(function(res){
                    if(res.body.state!=='fail'){
                        this.$Message.success('修改成功！');
                        this.tableData[this.index]['name'] = this.name;
                        this.tableData[this.index]['field'] = this.string2field(rt);
                    }else{
                        this.$Message.error('修改失败：' + res.body.reason);
                    }
                },function(res){
                    this.$Message.error('修改失败！');
                })
            },

            cancel_edit1() {
                this.$Message.error('取消编辑')
            },

            sumbit_edit2() {
                if(this.name == ''){
                    this.$Message.error('修改失败：用户名不能为空！');
                    return;
                } 

                var rt = '000000';
                rt = '000000';
                rt = rt.split('');
                this.field.forEach(v=>{
                    rt[v.charCodeAt()-65]='1';
                })
                rt = rt.join('');

                this.tableData[this.index]['name'] = this.name;
                this.tableData[this.index]['field'] = this.string2field(rt);
            },

            cancel_edit2() {
                this.$Message.error('取消编辑')
            },

            sumbit_import() {
                var expert_list = []
                for(var expert of this.tableData){
                    console.log(expert);
                    expert_list.push({
                        'name': expert['name'],
                        'email': expert['email'],
                        'field': this.field2string(expert['field'])
                    })
                }
                let params = {
                    'expert_list': expert_list
                }
                this.$http.post(this.$baseURL + '/api/v1/import_expert', params)
                    .then(function (res) {
                        var detail = res.body
                        if(detail.state == 'success'){
                            alert(detail['reason']);
                            this.table1 = true;
                            this.table2 = false;

                            //获取专家信息
                            var that = this;
                            this.$http.post(this.$baseURL + '/api/v1/get_expert_list', {})
                                .then(function (res) {
                                    var detail = res.body
                                    if(detail.state == 'success'){
                                        var temp_data = [];
                                        for(var expert of detail['list']){
                                            temp_data.push({
                                                'name': expert['name'],
                                                'email': expert['email'],
                                                'field': that.string2field(expert['field'])
                                            })
                                        }
                                        this.tableData = temp_data
                                    }
                                    else{
                                        this.$Message.error('获取专家列表失败 ' + detail.reason)
                                    }
                                },function (res) {
                                    this.$Message.error('Failed')
                            })
                        }
                        else{
                            this.$Message.error('导入失败 ' + detail.reason)
                        }
                    },function (res) {
                        this.$Message.error('Failed')
                })


            },

            cancel_import() {
                var that = this;
                this.$http.post(this.$baseURL + '/api/v1/get_expert_list', {})
                    .then(function (res) {
                        var detail = res.body
                        if(detail.state == 'success'){
                            var temp_data = [];
                            for(var expert of detail['list']){
                                temp_data.push({
                                    'name': expert['name'],
                                    'email': expert['email'],
                                    'field': that.string2field(expert['field'])
                                })
                            }
                            this.$Message.error('取消编辑')
                            this.table1 = true;
                            this.table2 = false;
                            this.tableData = temp_data;
                        }
                        else{
                            this.$Message.error('获取专家列表失败 ' + detail.reason)
                        }
                    },function (res) {
                        this.$Message.error('Failed')
                })
            },

            submit_delete() {
                if(this.table1){
                    let params = {
                        'expert_mail': this.email
                    }
                    var that = this;
                    this.$http.post(this.$baseURL + '/api/v1/delete_expert', params)
                        .then(function (res) {
                            var detail = res.body
                            if(detail.state == 'success'){
                                this.$Message.success('删除专家成功')
                                that.tableData.splice(that.index,1)
                            }
                            else{
                                alert('删除专家失败失败：' + detail.reason)
                            }
                        },function (res) {
                            this.$Message.error('Failed')
                        })
                }
                if(this.table2){
                    this.$delete(this.tableData,params.index);
                }
            },

            cancel_delete() {
                this.$Message.error('取消删除专家');
                this.delete_expert = false;
            }
        },

        mounted() {
            this.$Message.config({
                top: 100,
                duration: 1,
            });
            var that = this;
            this.$http.post(this.$baseURL + '/api/v1/get_expert_list', {})
                .then(function (res) {
                    var detail = res.body
                    if(detail.state == 'success'){
                        var temp_data = [];
                        for(var expert of detail['list']){
                            temp_data.push({
                                'name': expert['name'],
                                'email': expert['email'],
                                'field': that.string2field(expert['field'])
                            })
                        }
                        this.tableData = temp_data
                    }
                    else{
                        this.$Message.error('获取专家列表失败 ' + detail.reason)
                    }
                },function (res) {
                    this.$Message.error('Failed')
            })
        },

    }

    // 自定义列组件
    Vue.component('table-operation',{
        template:`<span>
        <a href="" @click.stop.prevent="update(rowData,index)">编辑</a>&nbsp;
        <a href="" @click.stop.prevent="deleteRow(rowData,index)">删除</a>
        </span>`,
        props:{
            rowData:{
                type:Object
            },
            field:{
                type:String
            },
            index:{
                type:Number
            }
        },
        methods:{
            update(){
                let params = {type:'edit',index:this.index,rowData:this.rowData};
                this.$emit('on-custom-comp',params);
            },

            deleteRow(){
                let params = {type:'delete',index:this.index,rowData:this.rowData};
                this.$emit('on-custom-comp',params);
            }
        }
    })
</script>

<style scoped>
    .body {  
        left: 280px;
        bottom: 200px;
        position: relative;
        top: 100px;
        border: 1px dashed black;
        border-radius: 20px;
        /*margin: 100px 0px 50px 30%;*/
        padding: 20px;
        width: 75%;
        /*text-align: center;*/
        min-height: 500px;
        min-width: 600px;
        color: black;
    }

    h2 {
        border-left: 5px solid dodgerblue;
        padding: 0 0 0 15px !important;
        font-size: 28px !important;
        margin: 24px 0 !important;
    }

    >>>.cell-edit-color{
        color:#2db7f5;
        font-weight: bold;
        word-wrap:break-word;
    }
</style>