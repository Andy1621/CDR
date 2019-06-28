<template>
    <div class="body">
        <h1>作品提交内容填写</h1>
        <Steps :current="current" style="margin: 30px">
            <Step title="作品基本信息" content=""></Step>
            <Step title="申请者信息" content=""></Step>
            <Step title="作品详细信息" content=""></Step>
            <Step title="附件上传" content=""></Step>
        </Steps>
        <Divider/>
        <div class="form" v-show="current == 0">
            <Form ref="basicInfo" :model="basicInfo" :rules="ruleBasicInfo" :label-width="80">
                <FormItem label="作品名称">
                    <Input v-model="basicInfo.project" placeholder="请输入作品名称"></Input>
                </FormItem>
                <FormItem label="院系名称">
                    <Input v-model="basicInfo.college" placeholder="请输入院系名称"></Input>
                </FormItem>
                <FormItem label="Select">
                    <Select v-model="basicInfo.type">
                        <Option value="beijing">New York</Option>
                        <Option value="shanghai">London</Option>
                        <Option value="shenzhen">Sydney</Option>
                    </Select>
                </FormItem>
            </Form>
            <Row>
                <Col span="10">作品名称</Col>
                <Col span="13" offset="1">

                </Col>
            </Row>
            <Row>
                <Col span="10">院系名称</Col>
                <Col span="13" offset="1">

                </Col>
            </Row>
            <Row>
                <Col span="10">类别</Col>
                <Col span="13" offset="1">

                </Col>
            </Row>
        </div>
        <div class="form" v-show="current == 1">
            <Row>
                <Col span="10">姓名</Col>
                <Col span="13" offset="1">

                </Col>
            </Row>
        </div>
        <div class="form" v-show="current == 2">
            <Row>
                <Col span="10">作品全称</Col>
                <Col span="13" offset="1">

                </Col>
            </Row>
        </div>
        <div class="form" v-show="current == 3">
            <Row>
                <Col span="10">图片</Col>
                <Col span="13" offset="1">

                </Col>
            </Row>
        </div>
        <Button type="primary" :disabled="current == 0" @click="pre_step">上一步</Button>
        <Button type="primary" :disabled="current == 3" @click="next_step">下一步</Button>
        <br>
        <Button type="primary" @click="save_data">保存</Button>
        <Button type="success" v-show="current == 3">提交</Button>
    </div>
</template>

<script>
    export default {
        name: "apply",
        data(){
            return{
                current: 0,
                basicInfo:{
                    project: '',
                    college: '',
                    type: '',
                },
                ruleBasicInfo:{

                }
            }
        },
        methods:{
            next_step(){
                this.current += 1;
                this.save_data();
            },
            pre_step(){
                this.current -= 1;
                this.save_data();
            },
            save_data(){
                // save data function
            }
        }
    }
</script>

<style scoped>
    .body{
        margin-left: 24%;
        border: 1px dashed black;
        margin-top: 60px;
        padding: 20px;
        width: 50%;
        text-align: center;
        min-height: 470px;
        min-width: 600px;
        color: black;
    }
    .form{
        min-height: 300px;
        padding: 10px;
        margin-bottom: 30px;
        font-size: 15px;
    }
</style>
