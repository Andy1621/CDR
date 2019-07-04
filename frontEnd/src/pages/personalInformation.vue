<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <h2>个人主页</h2>
            <div style="float:left;height:100%;width:70%;">
                <Row style="margin-bottom:20px; font-size:16px;" align="middle" type="flex">
                    <Col span="4" style="text-align:right; padding-right:30px;">
                        <b>用户名</b>
                    </Col>
                    <Col span="16" >
                        <Input v-model="username" placeholder="请输入您的用户名" size="large" :disabled="disabled"></Input>
                    </Col>
            </Row>
            <Row v-if="role === 'professor'" style="margin-bottom:20px; font-size:16px;">
                <Col span="4" style="text-align:right; padding-right:30px;">
                    <b>领域</b>
                </Col>
                <Col span="20">
                    <CheckboxGroup v-model="field" >
                        <Checkbox label="A" size="large" :disabled="disabled">机械与控制（包括机械、仪器仪表、自动化控
制、工程、交通、建筑等）</Checkbox><br>
                        <Checkbox label="B" size="large" :disabled="disabled">信息技术（包括计算机、电信、通讯、电子等）</Checkbox><br>
                        <Checkbox label="C" size="large" :disabled="disabled">数理（包括数学、物理、地球与空间科学等）</Checkbox><br>
                        <Checkbox label="D" size="large" :disabled="disabled">生命科学（包括生物､农学､药学､医学､健
康､卫生､食品等）</Checkbox><br>
                        <Checkbox label="E" size="large" :disabled="disabled">能源化工（包括能源、材料、石油、化学、化
工、生态、环保等）</Checkbox><br>
                        <Checkbox label="F" size="large" :disabled="disabled">哲学社会科学（包括哲学、经济、社会、法律、教育、管理）</Checkbox><br>
                    </CheckboxGroup>
                </Col>
            </Row>
            </div>
            <div style="float:right;height:100%;width:10%;margin-right:30px;">
                <Button type="info" style="margin-bottom:20px;" @click="revise">
                    {{revise_text}}
                </Button>
                <br>
                <Button type="success" @click="change_password = true">
                    修改密码
                </Button>
                <Modal
                    v-model="change_password"
                    title="修改密码"
                    ok-text="提交"
                    width="460"
                    :mask-closable="false">
                    <LInput v-model="oldPassword" labelContent="旧密码：" inputType="password"></LInput>
                    <LInput v-model="newPassword" labelContent="新密码：" inputType="password"></LInput>
                    <LInput v-model="passwordConform" labelContent="确认密码：" inputType="password"></LInput>
                    <div slot="footer">
                        <Button type="text" size="large" @click="cp_cancel">取消</Button>
                        <Button type="primary" size="large" @click="cp_ok">确定</Button>
                    </div>
                </Modal>
            </div>

        </div>
    </div>
</template>

<script>
    import NavBar from '../components/NavBar'
    import LInput from '../components/InputWithLabel'
    export default {
        components:{
            NavBar,
            LInput
        },
        data(){
            return{
                field:[],
                username:'',
                disabled: true,
                role:'',
                revise_text: '',
                change_password: false,
                oldPassword:'',
                newPassword:'',
                passwordConform:'',
            }
        },
        created() {
            this.role = this.$cookie.get('role');
            this.revise_text = '修改信息';
            // this.$Message.info('点击修改信息或修改密码可以进行修改');
            let url = this.$baseURL + '/api/v1/get_user_info';
            this.$http.post(url,{'mail':this.$cookie.get('mail')}).then(function(res){
                // console.log(res.body)
                this.username = res.body.username;
                if(this.role === 'professor'){
                    var field = res.body.field;
                    for(var i = 0;i<6; i++){
                        if (field[i] === '1'){
                            this.field.push(String.fromCharCode(65+i));
                        }
                    }
                    //console.log(this.field);
                }

            },function(res){
                // console.log(res.body)
            })
        },
        methods: {
            revise(){
                if(this.disabled === true){
                    this.disabled = false;
                    this.revise_text = '完成修改';
                }
                else{
                    this.revise_text = '修改信息';
                    this.disabled = true;
                    var rt = '';
                    if(this.role === 'professor'){
                        rt = '000000';
                        rt = rt.split('');
                        this.field.forEach(v=>{
                            //console.log(v);
                            rt[v.charCodeAt()-65]='1';
                        })
                        rt = rt.join('');
                    }
                    let url = this.$baseURL + '/api/v1/change_info';
                    // this.$Message.info('')
                    this.$http.post(url,{
                        'mail': this.$cookie.get('mail'),
                        'username':this.username,
                        'field':rt
                    }).then(function(res){
                        //console.log(res);
                        if(res.body.state!=='fail'){
                            this.$Message.success('修改成功！');
                        }else{
                            this.$Message.error('修改失败！' + res.body.reason);
                        }
                    },function(res){
                        //console.log(res);
                        this.$Message.error('修改失败！');
                    })
                }
            },
            cp_ok(){
                // this.$Message.info('')
                if (this.newPassword !== this.passwordConform) {
                    this.$Message.error("两次输入的密码不相同！");
                    return;
                }
                let url = this.$baseURL + '/api/v1/change_password';
                this.$http.post(url, {
                    'mail':this.$cookie.get('mail'),
                    'old_password':this.oldPassword,
                    'new_password':this.newPassword
                }).then(function(res){
                    if(res.body.state!=='fail'){
                            this.$Message.success('修改成功！');
                            this.cp_cancel();
                    }else{
                        this.$Message.error('修改失败！' + res.body.reason);
                    }
                },function(res){
                    this.$Message.error('修改失败！');
                })
            },
            cp_cancel(){
                this.change_password = false;
                this.oldPassword = '';
                this.newPassword = '';
                this.passwordConform = '';
            }
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
    >>>.ivu-checkbox-large{
        margin-bottom: 10px;
        text-align: center;
        font-weight: 400;
    }

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
