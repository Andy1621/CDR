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
                    <div class="box-body-foot" v-if="role=='student'">没有账号？<span style="color: #2db7f5;cursor:pointer" @click="register=!register">点击注册</span></div>
                    <div class="box-body-foot" v-if="role=='professor'">邀请码失效？<span style="color: #2db7f5;cursor:pointer" @click="professorRegister=!professorRegister">点击注册</span></div>
                    <Modal
                        v-model="register"
                        title="注册"
                        ok-text="注册"
                        width="460"
                        :mask-closable="false"
                        @on-ok="ok">
                        <LInput v-model="idRegister" labelContent="用户名：" :disabled="isProfessor?true:false"></LInput>
                        <LInput v-model="passwordRegister" labelContent="密码：" inputType="password"></LInput>
                        <LInput v-model="passwordConform" labelContent="确认密码：" inputType="password"></LInput>
                        <br>
                        <LInput v-if="!isProfessor" v-model="stuID" labelContent="学号："></LInput>
                        <LInput v-if="!isProfessor" v-model="name" labelContent="姓名："></LInput>
                        <LInput v-if="!isProfessor" v-model="school" labelContent="院系："></LInput>
                        <LInput v-if="!isProfessor" v-model="major" labelContent="专业："></LInput>
                        <LInput v-if="!isProfessor" v-model="enterYear" labelContent="入学年份："></LInput>
                        <LInput v-if="!isProfessor" v-model="tel" labelContent="联系电话："></LInput>
                        <LInput v-if="!isProfessor" v-model="email" labelContent="电子邮箱："></LInput>
                    </Modal>
                    <Modal
                        v-model="professorRegister"
                        title="请输入您的邮箱"
                        ok-text="确认"
                        width="460"
                        :mask-closable="false"
                        @on-ok="okPro">
                        <LInput v-model="professorEmail" labelContent="邮箱："></LInput>
                    </Modal>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import LInput from '../components/InputWithLabel.vue'
    export default {
        components:{
            LInput
        },
        name: "login",
        data(){
            return{
                role: 'student',
                register: false,
                professorRegister: false,
                professorEmail: '',
                id:'',
                idRegister:'',
                isProfessor: false,
                password:'',
                passwordRegister:'',
                passwordConform:'',
                stuID:'',
                name:'',
                school:'',
                major:'',
                enterYear:'',
                tel:'',
                email:'',
            }
        },
        created(){
            if(this.$route.query.token)
            {
                /*let url = "";
                this.$http.get(url, {params:{token: this.$route.query.token}}).then(function (res) {
                    console.log(res);
                },function (res) {
                    console.log(res);
                });*/
                this.register = true;
                this.idRegister = 'test';
                this.isProfessor = true;
            }
        },
        methods:{
            login(){
                /*this.$router.push({
                    path: '/index'
                })*/
                let data = {
                    id: this.id,
                    password: this.password,
                    role: this.role,
                };
                this.$http.post("http://127.0.0.1:5000/api/v1/login",data).then(function (res) {
                    console.log(res);
                    /*this.$cookie.set('id',*);
                    this.$cookie.set('name',*);
                    this.$cookie.set('role',*);*/
                    /*this.$router.push({
                        path: '/index',
                    });*/
                },function (res) {
                    console.log(res)
                })
            },
            ok () {
                if (this.passwordRegister!=this.passwordConform)
                {
                    alert("两次输入的密码不相同！")
                    return;
                }
                let data = {
                    ID: this.idRegister,
                    password: this.passwordRegister,
                    mail: this.email,
                    username: this.name,
                    department: this.school,
                    field: this.major,
                    admission_year: this.enterYear,
                    phone: this.tel
                };
                this.$http.post("http://127.0.0.1:5000/api/v1/registerstudent",data).then(function (res) {
                    console.log(res)
                    /*this.$cookie.set('id',*);
                    this.$cookie.set('name',*);
                    this.$cookie.set('role',*);
                    this.$router.push({
                        path: '/index'
                    })*/
                },function (res) {
                    console.log(res)
                })
                /*this.$router.push({
                    path:'/index'
                })*/
            },
            okPro(){
                let url = '';
                /*this.$http.post(url, {email: this.professorEmail}, {emulateJSON: true}).then(function (res) {
                    console.log(res)
                },function (res) {
                    console.log(res)
                })*/
            },
        }
    }
</script>

<style scoped>
    .box-login{
        width: 20%;
        height: 53%;
        min-height: 400px;
        min-width: 320px;
        position: absolute;
        left: 40%;
        top: 23%;
        text-align: center;
        font-weight: lighter;
    }
    .box-body{
        width: 100%;
        height: 100%;
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
    .ivu-row-flex{
        margin-bottom: 7px;
    }
</style>
