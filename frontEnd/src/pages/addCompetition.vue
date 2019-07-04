<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <h2>添加竞赛</h2>
            <div class="form">
                <Form ref="competition" :model="competitionInfo" :rules="ruleCompetitionInfo" :label-width="120">
                    <FormItem label="竞赛名称" prop="competition_name">
                        <Input v-model="competitionInfo.competition_name" placeholder="请输入竞赛名称"></Input>
                    </FormItem>
                    <FormItem label="开始时间">
                        <DatePicker type="date" placeholder="日期选择" v-model="competitionInfo.begin_time_date"
                                    prop="begin_time_date"></DatePicker>
                        <TimePicker format="HH:mm" placeholder="时间选择" v-model="competitionInfo.begin_time_time"
                                    prop="begin_time_time"></TimePicker>
                    </FormItem>
                    <FormItem label="提交截止">
                        <DatePicker type="date" placeholder="日期选择" v-model="competitionInfo.submission_ddl_date"
                                    prop="submission_ddl_date"></DatePicker>
                        <TimePicker format="HH:mm" placeholder="时间选择" v-model="competitionInfo.submission_ddl_time"
                                    prop="submission_ddl_time"></TimePicker>
                    </FormItem>
                    <FormItem label="初审截止">
                        <DatePicker type="date" placeholder="日期选择" v-model="competitionInfo.first_review_ddl_date"
                                    prop="first_review_ddl_date"></DatePicker>
                        <TimePicker format="HH:mm" placeholder="时间选择" v-model="competitionInfo.first_review_ddl_time"
                                    prop="first_review_ddl_time"></TimePicker>
                    </FormItem>
                    <FormItem label="专家初评截止">
                        <DatePicker type="date" placeholder="日期选择" v-model="competitionInfo.expert_comments_ddl_date"
                                    prop="expert_comments_ddl_date"></DatePicker>
                        <TimePicker format="HH:mm" placeholder="时间选择" v-model="competitionInfo.expert_comments_ddl_time"
                                    prop="expert_comments_ddl_time"></TimePicker>
                    </FormItem>
                    <FormItem label="现场赛选拔截止">
                        <DatePicker type="date" placeholder="日期选择" v-model="competitionInfo.live_selection_ddl_date"
                                    prop="live_selection_ddl_date"></DatePicker>
                        <TimePicker format="HH:mm" placeholder="时间选择" v-model="competitionInfo.live_selection_ddl_time"
                                    prop="live_selection_ddl_time"></TimePicker>
                    </FormItem>
                    <FormItem label="结束时间">
                        <DatePicker type="date" placeholder="日期选择" v-model="competitionInfo.end_time_date"
                                    prop="end_time_date"></DatePicker>
                        <TimePicker format="HH:mm" placeholder="时间选择" v-model="competitionInfo.end_time_time"
                                    prop="end_time_time"></TimePicker>
                    </FormItem>
                    <FormItem label="竞赛简介" prop="introduction">
                        <Input v-model="competitionInfo.introduction" type="textarea" :maxlength="800" :rows="6"
                               :autosize="{minRows: 6,maxRows: 6}" placeholder="请输入竞赛简介（不超过800字）"></Input>
                    </FormItem>
                </Form>
            </div>
            <Divider/>
            <div style="margin-left: 50px">
                <h5 style="margin-bottom: 20px">附件上传</h5>
                <div v-if="readonly" class="show-upload">
                    <ul>
                        <li v-for="item in uploadDocList" @click="docView(item)">
                            <Icon type="md-document"></Icon>
                            {{item.name}}
                        </li>
                    </ul>
                </div>
                <Upload
                        ref="uploadDoc"
                        v-show="!readonly"
                        :show-upload-list="true"
                        :default-file-list="defaultDocList"
                        :on-success="handleSuccessDoc"
                        :on-remove="handleRemoveDoc"
                        :on-preview="docView"
                        :max-size="20480"
                        :on-format-error="handleFormatErrorDoc"
                        :on-exceeded-size="handleMaxSizeDoc"
                        :before-upload="handleBeforeUploadDoc"
                        :action="up_url"
                        style="display: inline-block">
                    <Button icon="ios-document" style="width: 100px">上传</Button>
                </Upload>
            </div>
            <Button type="primary" @click="add_competition" style="margin-left: 45%">新建竞赛</Button>
        </div>
    </div>
</template>

<script>
    import NavBar from '../components/NavBar.vue'

    export default {
        components: {
            NavBar
        },
        name: 'addCompetition',
        data() {
            return {
                readonly: false,
                competitionInfo: {
                    competition_name: '',
                    begin_time_date: '',
                    begin_time_time: '',
                    submission_ddl_date: '',
                    submission_ddl_time: '',
                    first_review_ddl_date: '',
                    first_review_ddl_time: '',
                    expert_comments_ddl_date: '',
                    expert_comments_ddl_time: '',
                    live_selection_ddl_date: '',
                    live_selection_ddl_time: '',
                    end_time_date: '',
                    end_time_time: '',
                    introduction: '',
                },
                ruleCompetitionInfo: {
                    competition_name: [
                        {required: true, message: '竞赛名称不能为空', trigger: 'blur'}
                    ],
                    begin_time_date: [
                        {required: true, type: 'date', message: '选择不能为空', trigger: 'change'}
                    ],
                    begin_time_time: [
                        {required: true, type: 'string', message: '选择不能为空', trigger: 'change'}
                    ],
                    submission_ddl_date: [
                        {required: true, type: 'date', message: '选择不能为空', trigger: 'change'}
                    ],
                    submission_ddl_time: [
                        {required: true, type: 'string', message: '选择不能为空', trigger: 'change'}
                    ],
                    first_review_ddl_date: [
                        {required: true, type: 'date', message: '选择不能为空', trigger: 'change'}
                    ],
                    first_review_ddl_time: [
                        {required: true, type: 'string', message: '选择不能为空', trigger: 'change'}
                    ],
                    expert_comments_ddl_date: [
                        {required: true, type: 'date', message: '选择不能为空', trigger: 'change'}
                    ],
                    expert_comments_ddl_time: [
                        {required: true, type: 'string', message: '选择不能为空', trigger: 'change'}
                    ],
                    live_selection_ddl_date: [
                        {required: true, type: 'date', message: '选择不能为空', trigger: 'change'}
                    ],
                    live_selection_ddl_time: [
                        {required: true, type: 'string', message: '选择不能为空', trigger: 'change'}
                    ],
                    end_time_date: [
                        {required: true, type: 'date', message: '选择不能为空', trigger: 'change'}
                    ],
                    end_time_time: [
                        {required: true, type: 'string', message: '选择不能为空', trigger: 'change'}
                    ],
                    introduction: [
                        {required: true, message: '竞赛简介不能为空', trigger: 'blur'}
                    ],
                },
            }
        },
        methods: {
            add_competition() {
                this.$refs['competition'].validate((valid) => {
                    if (valid) {
                        let params = {
                            'competition_name': this.competitionInfo.competition_name,
                            'begin_time': this.format_change(this.competitionInfo.begin_time_date, this.competitionInfo.begin_time_time),
                            'submission_ddl': this.format_change(this.competitionInfo.submission_ddl_date, this.competitionInfo.submission_ddl_time),
                            'first_review_ddl': this.format_change(this.competitionInfo.first_review_ddl_date, this.competitionInfo.first_review_ddl_time),
                            'expert_comments_ddl': this.format_change(this.competitionInfo.expert_comments_ddl_date, this.competitionInfo.expert_comments_ddl_time),
                            'live_selection_ddl': this.format_change(this.competitionInfo.live_selection_ddl_date, this.competitionInfo.live_selection_ddl_time),
                            'end_time': this.format_change(this.competitionInfo.end_time_date, this.competitionInfo.end_time_time),
                        }
                        this.$http.post(this.$baseURL + '/api/v1/add_competition', params)
                            .then(function (res) {
                                console.log(res)
                                var detail = res.body
                                if (detail.state == 'success') {
                                    this.$Message.success('新建竞赛成功,' + detail.competition_id)
                                    this.$router.push({
                                        path: '/competitionList'
                                    })
                                } else {
                                    this.$Message.error('新建竞赛失败 ' + detail.reason)
                                }
                            }, function (res) {
                                this.$Message.error('Failed')
                            })
                    } else {
                        this.$Message.error('信息有误');
                    }
                });
            },
            format_change(date, time) {
                var res = date.toString() + time.toString()
                return res
            },
        },
        mounted() {
            this.$Message.config({
                top: 100,
                duration: 1,
            });
        },
        created() {

        },
    }
</script>

<style scoped>
    .body {
        left: 280px;
        bottom: 50px;
        position: relative;
        top: 100px;
        border: 1px dashed black;
        border-radius: 20px;
        margin-bottom: 80px;
        padding: 20px;
        width: 75%;
        /*text-align: center;*/
        min-height: 470px;
        min-width: 600px;
        color: black;
    }

    h2 {
        border-left: 5px solid green;
        padding: 0 0 0 15px !important;
        font-size: 28px !important;
        margin: 24px 0 !important;
    }
</style>