<template>
    <div style="background: #4d5669; position: fixed; height:100%;width: 100%;">
        <div class="box-login">
            <div class="box-body">
                <div class="box-body-head">登录</div>
                <div class="box-body-main">
                    <Tabs value="student" v-model="role">
                        <TabPane label="学生" name="student"></TabPane>
                        <TabPane label="专家" name="professor"></TabPane>
                        <TabPane label="校团委" name="school"></TabPane>
                    </Tabs>
                    <Input v-model="id" prefix="md-person" placeholder="请输入账号" clearable size="large"/>
                    <Input v-model="password" type="password" @keyup.enter.native="login" prefix="md-lock" placeholder="请输入密码" clearable size="large"/>
                    <Button type="primary" class="btn" size="large" shape="circle" @click="login">登录</Button>
                    <div class="box-body-foot">没有账号？<span style="color: #2db7f5" @click="register=!register">点击注册</span></div>
                    <Modal
                        v-model="register"
                        title="注册"
                        ok-text="注册"
                        width="460"
                        @on-ok="ok">
                        <Row style="margin-bottom: 7px;" align="middle" type="flex">
                            <Col span="4" class-name="vertical-middle">用户名：</Col>
                            <Col span="20" ><Input class="register-input"></Input></Col>
                        </Row>
                        <Row style="margin-bottom: 7px;" align="middle" type="flex">
                            <Col span="4" style="">密码：</Col>
                            <Col><Input class="register-input"></Input></Col>
                        </Row>
                        <Row style="margin-bottom: 7px;" align="middle" type="flex">
                            <Col span="4" style=""> 确认密码：</Col>
                            <Col><Input class="register-input"></Input></Col>
                        </Row>
                    </Modal>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "login",
        data(){
            return{
                role: '',
                register: false,
                id:'',
                password:'',
            }
        },
        methods:{
            login(){

            },
            ok () {
                this.$Message.info('Clicked ok');
            }
        }
    }
</script>

<style scoped>
    .box-login{
        width: 310px;
        height: 420px;
        position: absolute;
        left: 590px;
        top: 200px;
        text-align: center;
        font-weight: lighter;
    }
    .box-body{
        width: 340px;
        height: 380px;
        margin: 10px;
        padding: 10px;
        border-radius: 8px;
        background-color: #FFFFFF;
        box-shadow: 2px 2px 20px #9ea7b4;
    }
    .box-body-head{
        font-size: x-large;
        margin: 15px;
        padding: 10px;
    }
    .box-body-main{
        margin: 10px;
    }
    .box-body-foot{
        color: #9ea7b4;
        padding: 5px;
        font-size: small;
    }
    .box-body-main >>>.ivu-input-wrapper{
        margin: 10px 0 10px 0;
        width:95%;
    }
    .box-body-main>>>.ivu-input{
        border-top: 0;
        border-left: 0;
        border-right: 0;
        border-bottom: #9ea7b4 1px solid;
        border-radius: 0;
    }
    .box-body-main>>>.ivu-input:focus{
        box-shadow: 0 0 0 ;
        border-bottom:#9137F3 1px solid;
    }
    .btn{
        color: #FFFFFF;
        width:90%;
        padding: 10px;
        margin-top: 30px;
    }
    .register-input{
        width: 300px;
    }
    .vertical-middle{
        vertical-align: middle;
    }
</style>