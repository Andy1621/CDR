<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <h2>添加竞赛</h2>
            <div class="form">
                <Form :label-width="100" :model="competitionInfo" :rules="ruleCompetitionInfo" ref="competition">
                    <FormItem label="竞赛名称" prop="competition_name">
                        <Input placeholder="请输入竞赛名称" v-model="competitionInfo.competition_name"></Input>
                    </FormItem>
                    <Row>
                        <Col span="12">
                            <FormItem label="开始时间">
                                <Row>
                                    <Col span="12">
                                        <FormItem prop="begin_time_date">
                                            <DatePicker :options="date_option1" @on-change="disabled_begin_hour" placeholder="日期选择" type="date"
                                                        v-model="competitionInfo.begin_time_date"></DatePicker>
                                        </FormItem>
                                    </Col>
                                    <Col span="12">
                                        <FormItem prop="begin_time_time">
                                            <TimePicker :disabled="competitionInfo.begin_time_date.length==0" :disabled-hours="disabled_hours" format="HH:mm"
                                                        hide-disabled-options placeholder="时间选择"
                                                        v-model="competitionInfo.begin_time_time"></TimePicker>
                                        </FormItem>
                                    </Col>
                                </Row>
                            </FormItem>
                        </Col>
                        <Col span="12">
                            <FormItem label="提交截止">
                                <Row>
                                    <Col span="12">
                                        <FormItem prop="submission_ddl_date">
                                            <DatePicker :disabled="competitionInfo.begin_time_date.length==0" :options="date_option2" placeholder="日期选择" type="date"
                                                        v-model="competitionInfo.submission_ddl_date"></DatePicker>
                                        </FormItem>
                                    </Col>
                                    <Col span="12">
                                        <FormItem prop="submission_ddl_time">
                                            <TimePicker :disabled="competitionInfo.submission_ddl_date.length==0" format="HH:mm" placeholder="时间选择"
                                                        v-model="competitionInfo.submission_ddl_time"></TimePicker>
                                        </FormItem>
                                    </Col>
                                </Row>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="12">
                            <FormItem label="初审截止">
                                <Row>
                                    <Col span="12">
                                        <FormItem prop="first_review_ddl_date">
                                            <DatePicker :disabled="competitionInfo.submission_ddl_date.length==0" :options="date_option3" placeholder="日期选择" type="date"
                                                        v-model="competitionInfo.first_review_ddl_date"></DatePicker>
                                        </FormItem>
                                    </Col>
                                    <Col span="12">
                                        <FormItem prop="first_review_ddl_time">
                                            <TimePicker :disabled="competitionInfo.first_review_ddl_date.length==0" format="HH:mm" placeholder="时间选择"
                                                        v-model="competitionInfo.first_review_ddl_time"></TimePicker>
                                        </FormItem>
                                    </Col>
                                </Row>
                            </FormItem>
                        </Col>
                        <Col span="12">
                            <FormItem label="专家初评截止">
                                <Row>
                                    <Col span="12">
                                        <FormItem prop="expert_comments_ddl_date">
                                            <DatePicker :disabled="competitionInfo.first_review_ddl_date.length==0" :options="date_option4" placeholder="日期选择" type="date"
                                                        v-model="competitionInfo.expert_comments_ddl_date"></DatePicker>
                                        </FormItem>
                                    </Col>
                                    <Col span="12">
                                        <FormItem prop="expert_comments_ddl_time">
                                            <TimePicker :disabled="competitionInfo.expert_comments_ddl_date.length==0" format="HH:mm" placeholder="时间选择"
                                                        v-model="competitionInfo.expert_comments_ddl_time"></TimePicker>
                                        </FormItem>
                                    </Col>
                                </Row>
                            </FormItem>
                        </Col>
                    </Row>
                    <Row>
                        <Col span="12">
                            <FormItem label="现场赛选拔截止">
                                <Row>
                                    <Col span="12">
                                        <FormItem prop="live_selection_ddl_date">
                                            <DatePicker :disabled="competitionInfo.expert_comments_ddl_date.length==0" :options="date_option5" placeholder="日期选择" type="date"
                                                        v-model="competitionInfo.live_selection_ddl_date"></DatePicker>
                                        </FormItem>
                                    </Col>
                                    <Col span="12">
                                        <FormItem prop="live_selection_ddl_time">
                                            <TimePicker :disabled="competitionInfo.live_selection_ddl_date.length==0" format="HH:mm" placeholder="时间选择"
                                                        v-model="competitionInfo.live_selection_ddl_time"></TimePicker>
                                        </FormItem>
                                    </Col>
                                </Row>
                            </FormItem>
                        </Col>
                        <Col span="12">
                            <FormItem label="结束时间">
                                <Row>
                                    <Col span="12">
                                        <FormItem prop="end_time_date">
                                            <DatePicker :disabled="competitionInfo.live_selection_ddl_date.length==0" :options="date_option6" placeholder="日期选择" type="date"
                                                        v-model="competitionInfo.end_time_date"></DatePicker>
                                        </FormItem>
                                    </Col>
                                    <Col span="12">
                                        <FormItem prop="end_time_time">
                                            <TimePicker :disabled="competitionInfo.end_time_date.length==0" format="HH:mm" placeholder="时间选择"
                                                        v-model="competitionInfo.end_time_time"></TimePicker>
                                        </FormItem>
                                    </Col>
                                </Row>
                            </FormItem>
                        </Col>
                    </Row>
                    <FormItem label="竞赛简介" prop="introduction">
                        <Input :autosize="{minRows: 6,maxRows: 6}" :maxlength="800" :rows="6" placeholder="请输入竞赛简介（不超过800字）"
                               type="textarea" v-model="competitionInfo.introduction"></Input>
                    </FormItem>
                </Form>
            </div>
            <Button @click="add_competition" style="margin-left: 45%" type="primary">新建竞赛</Button>
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
                begin_time: '',
                submission_ddl: '',
                first_review_ddl: '',
                expert_comments_ddl: '',
                live_selection_ddl: '',
                end_time: '',
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
                date_option1: {
                    disabledDate(date) {
                        return date && date.valueOf() < Date.now() - 86400000;//86400000表示一天
                    }
                },
                date_option2: {
                    disabledDate: ( function (date) {
                        return date && date.valueOf() < new Date(this.competitionInfo.begin_time_date.valueOf() + 86400000);
                    }).bind(this)
                },
                date_option3: {
                    disabledDate: ( function (date) {
                        return date && date.valueOf() < new Date(this.competitionInfo.submission_ddl_date.valueOf() + 86400000);
                    }).bind(this)
                },
                date_option4: {
                    disabledDate: ( function (date) {
                        return date && date.valueOf() < new Date(this.competitionInfo.first_review_ddl_date.valueOf() + 86400000);
                    }).bind(this)
                },
                date_option5: {
                    disabledDate: ( function (date) {
                        return date && date.valueOf() < new Date(this.competitionInfo.expert_comments_ddl_date.valueOf() + 86400000);
                    }).bind(this)
                },
                date_option6: {
                    disabledDate: ( function (date) {
                        return date && date.valueOf() < new Date(this.competitionInfo.live_selection_ddl_date.valueOf() + 86400000);
                    }).bind(this)
                },
                disabled_hours: [],
            }
        },
        methods: {
            add_competition() {
                // this.format_change(this.competitionInfo.begin_time_date, this.competitionInfo.begin_time_time)
                this.$refs['competition'].validate((valid) => {
                    if (valid) {
                        this.begin_time = this.format_change(this.competitionInfo.begin_time_date, this.competitionInfo.begin_time_time)
                        this.submission_ddl = this.format_change(this.competitionInfo.submission_ddl_date, this.competitionInfo.submission_ddl_time)
                        this.first_review_ddl = this.format_change(this.competitionInfo.first_review_ddl_date, this.competitionInfo.first_review_ddl_time)
                        this.expert_comments_ddl = this.format_change(this.competitionInfo.expert_comments_ddl_date, this.competitionInfo.expert_comments_ddl_time)
                        this.live_selection_ddl = this.format_change(this.competitionInfo.live_selection_ddl_date, this.competitionInfo.live_selection_ddl_time)
                        this.end_time = this.format_change(this.competitionInfo.end_time_date, this.competitionInfo.end_time_time)
                        if(this.check_date()){
                            let params = {
                            'competition_name': this.competitionInfo.competition_name,
                            'begin_time': this.begin_time,
                            'submission_ddl': this.submission_ddl,
                            'first_review_ddl': this.first_review_ddl,
                            'expert_comments_ddl': this.expert_comments_ddl,
                            'live_selection_ddl': this.live_selection_ddl,
                            'end_time': this.end_time,
                            'introduction': this.competitionInfo.introduction
                        }
                        this.$http.post(this.$baseURL + '/api/v1/add_competition', params)
                            .then(function (res) {
                                console.log(res)
                                var detail = res.body
                                if (detail.state == 'success') {
                                    console.log(detail.competition_id)
                                    this.$Message.success('新建竞赛成功')
                                    this.$router.push({
                                        path: '/competitionList'
                                    })
                                } else {
                                    this.$Message.error('新建竞赛失败 ' + detail.reason)
                                }
                            }, function (res) {
                                this.$Message.error('Failed')
                            })
                        }
                    } else {
                        this.$Message.error('信息有误');
                    }
                });
            },
            check_date() {
                var res = true
                if(new Date(this.begin_time).getTime() >= new Date(this.submission_ddl).getTime()
                || new Date(this.submission_ddl).getTime() >= new Date(this.first_review_ddl).getTime()
                || new Date(this.first_review_ddl).getTime() >= new Date(this.expert_comments_ddl).getTime()
                || new Date(this.expert_comments_ddl).getTime() >= new Date(this.live_selection_ddl).getTime()
                || new Date(this.live_selection_ddl).getTime() >= new Date(this.end_time).getTime()){
                    this.$Notice.error({
                        title: '日期填写错误',
                        desc: '后者日期不能提前于前者日期'
                    });
                    res = false
                }
                return res
            },
            disabled_begin_hour() {
                var res = []
                var nowHour = new Date().getHours()
                for (var i = 0; i <= nowHour; i++) {
                    res.push(i)
                }
                if(new Date(this.competitionInfo.begin_time_date).valueOf() > Date.now())
                    res = []
                this.disabled_hours = res
            },
            format_change(date, time) {
                var nowdate = new Date(date)
                var rightdate = nowdate.getFullYear() + '-' + (nowdate.getMonth() + 1) + '-' + nowdate.getDate()
                time = time + ':00'
                var res = rightdate + ' ' + time
                console.log(res)
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