<template>
    <div style="background: #4d5669; position: fixed; height:100%;width: 100%;">
        <div class="box-login">
            <div class="box-body">
                <div class="box-body-head">登录</div>
                <div class="box-body-main">
                    <Tabs value="student" v-model="role">
                        <TabPane label="学 生" name="student"></TabPane>
                        <TabPane label="专 家" name="professor"></TabPane>
                        <TabPane label="校 团 委" name="school"></TabPane>
                    </Tabs>
                    <Input v-model="email" prefix="md-person" placeholder="请输入账号" clearable size="large"></Input>
                    <Input v-model="password" type="password" @keyup.enter.native="login" prefix="md-lock"
                           placeholder="请输入密码" clearable size="large"></Input>
                    <Button type="primary" class="btn" size="large" shape="circle" @click="login">登录</Button>
                    <div class="box-body-foot" v-if="role==='student'">
                        没有账号？
                        <span style="color: #2db7f5;cursor:pointer" @click="register=!register">
                            点击注册
                        </span>
                    </div>
                    <div style="display: none" class="box-body-foot" v-if="role==='professor'">邀请码失效？<span
                        style="color: #2db7f5;cursor:pointer" @click="professorRegister=!professorRegister">点击注册</span>
                    </div>
                    <Modal
                        v-model="register"
                        title="注册"
                        ok-text="注册"
                        width="460"
                        :mask-closable="false"
                        @on-ok="ok">
                        <LInput v-model="emailRegister" labelContent="邮箱：" :disabled="isProfessor"></LInput>
                        <LInput v-model="passwordRegister" labelContent="密码：" inputType="password"></LInput>
                        <LInput v-model="passwordConform" labelContent="确认密码：" inputType="password"></LInput>
                        <br>
                        <LInput v-if="!isProfessor" v-model="ID" labelContent="学号："></LInput>
                        <LInput v-if="!isProfessor" v-model="username" labelContent="姓名："></LInput>
                        <LInput v-if="!isProfessor" v-model="department" labelContent="院系："></LInput>
                        <LInput v-if="!isProfessor" v-model="field" labelContent="专业："></LInput>
                        <LInput v-if="!isProfessor" v-model="admission_year" labelContent="入学年份："></LInput>
                        <LInput v-if="!isProfessor" v-model="phone" labelContent="联系电话："></LInput>
                    </Modal>
                    <Modal
                        v-model="professorRegister"
                        title="请输入您的邮箱"
                        ok-text="确认"
                        width="460"
                        :mask-closable="false">
                        <LInput v-model="professorEmailRegister" labelContent="邮箱：" :disabled=true></LInput>
                        <LInput v-model="professorPasswordRegister" labelContent="设置密码：" inputType="password"></LInput>
                        <LInput v-model="professorPasswordConfirm" labelContent="确认密码：" inputType="password"></LInput>
                        <div slot="footer">
                            <Button type="primary" @click="okPro">确定</Button>
                        </div>
                    </Modal>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import LInput from '../components/InputWithLabel.vue'

    export default {
        components: {
            LInput
        },
        name: "login",
        data() {
            return {
                role: 'student',
                register: false,
                professorRegister: false,
                professorEmail: '',
                professorEmailRegister: '',
                professorPasswordRegister: '',
                professorPasswordConfirm: '',
                email: '',
                emailRegister: '',
                isProfessor: false,
                password: '',
                passwordRegister: '',
                passwordConform: '',
                ID: '',
                username: '',
                department: '',
                field: '',
                admission_year: '',
                phone: '',
            }
        },
        created() {
            let temp = this.$cookie.get('mail');
            let route = this.$route.query;
            let messageContent = ["", "您已经接收该作品的评审", "您已经拒绝该作品的评审", "您已经评审过该作品"];
            messageContent[0] = route.is_accept == 'true' ? '成功接收评审' : '成功拒绝评审';
            if (route.token) {
                let url = this.$baseURL + "/api/v1/multi_check_code";
                this.$http.post(url, {
                    mail: route.email,
                    invitation_code: route.token,
                    project_code: route.project_code,
                    is_accept: route.is_accept === 'true'
                }).then(function (res) {
                    console.log(res);

                    if (res.body.state === 'fail') {
                        this.$Message.error('抱歉，系统出现问题，请稍后再试！');
                        return
                    }
                    if (!res.body.registered) {
                        this.professorRegister = true;
                        this.professorEmailRegister = route.email;
                        messageContent[0] += '，请注册后评审';
                        messageContent[1] += '，请注册后评审';
                        messageContent[2] += '，您可以修改密码或者退出该页面';
                    } else {
                        this.email = route.email;
                        messageContent[0] += '，请登录后评审';
                        messageContent[1] += '，请登录后评审';
                        messageContent[2] += '，您可以登录或者退出';
                        this.role = 'professor'
                    }
                    this.$Message.info(messageContent[res.body.old_status + 1])
                }, function (res) {
                    console.log(res);
                });
                /*this.register = true;
                this.emailRegister = 'test';
                this.isProfessor = true;*/
            } else if (temp != '') {
                this.email = temp;
            }
        },
        methods: {
            login() {
                let data = {
                    mail: this.email,
                    password: this.password,
                    role: this.role,
                };
                this.$http.post(this.$baseURL + "/api/v1/login", data).then(function (res) {
                    console.log(res);
                    if (res.body.state === 'success') {
                        this.$cookie.set('mail', this.email);
                        this.$cookie.set('role', this.role);
                        this.$cookie.set('username', res.body.username);
                        this.$router.push({
                            path: '/index',
                        });
                    } else {
                        this.$Message.error(res.body.reason)
                    }
                }, function (res) {
                    console.log(res)
                })
            },
            ok: function () {
                if (this.passwordRegister !== this.passwordConform) {
                    this.$Message.error("两次输入的密码不相同！");
                    return;
                }
                let data = {
                    mail: this.emailRegister.trim(),
                    password: this.passwordRegister,
                    ID: this.ID,
                    username: this.username,
                    department: this.department,
                    field: this.field,
                    admission_year: this.admission_year,
                    phone: this.phone
                };
                this.$http.post(this.$baseURL + "/api/v1/registerstudent", data).then(function (res) {
                    console.log(res);
                    if (res.body.state === 'fail') {
                        this.$Message.error(res.body.reason);
                        return
                    }
                    this.$cookie.set('mail', this.emailRegister);
                    this.$cookie.set('username', this.username);
                    this.$cookie.set('role', 'student');
                    this.$router.push({
                        path: '/index',
                    });
                }, function (res) {
                    console.log(res)
                })
            },
            okPro() {
                let url = this.$baseURL + '/api/v1/expert_set_password';
                let data = {
                    mail: this.professorEmailRegister,
                    password: this.professorPasswordRegister
                }
                if (this.professorPasswordRegister !== this.professorPasswordConfirm) {
                    this.$Message.error("两次输入的密码不相同！");
                    return;
                }
                this.$http.post(url, data).then(function (res) {
                    console.log(res);
                    this.$cookie.set('mail', this.professorEmailRegister);
                    this.$cookie.set('role', 'professor');
                    this.$cookie.set('username', this.professorEmailRegister);
                    this.$router.push({
                        path: '/index',
                    });
                }, function (res) {
                    console.log(res)
                })

            },
        }
    }
</script>

<style scoped>
    .box-login {
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

    .box-body {
        width: 100%;
        height: 100%;
        padding: 10px;
        border-radius: 8px;
        background-color: #FFFFFF;
        box-shadow: 2px 2px 20px #9ea7b4;
    }

    .box-body-head {
        font-size: x-large;
        margin: 15px;
        padding: 10px;
    }

    .box-body-main {
        margin: 10px;
    }

    .box-body-foot {
        color: #9ea7b4;
        padding: 5px;
        font-size: small;
    }

    .box-body-main >>> .ivu-input-wrapper {
        margin: 10px 0 10px 0;
        width: 95%;
    }

    .box-body-main >>> .ivu-input {
        border-top: 0;
        border-left: 0;
        border-right: 0;
        border-bottom: #9ea7b4 1px solid;
        border-radius: 0;
    }

    .box-body-main >>> .ivu-input:focus {
        box-shadow: 0 0 0;
        border-bottom: #9137F3 1px solid;
    }

    .btn {
        color: #FFFFFF;
        width: 90%;
        padding: 10px;
        margin-top: 30px;
    }

    .register-input {
        width: 300px;
    }

    .ivu-row-flex {
        margin-bottom: 7px;
    }
</style>
