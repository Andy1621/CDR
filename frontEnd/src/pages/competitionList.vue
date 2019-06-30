<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <h2>竞赛列表</h2>
            <Table stripe border :columns="columns" :data="rows" ref="table" ></Table>
        </div>
    </div>
</template>

<script>
    import NavBar from '../components/NavBar.vue'
    export default {
        components:{
            NavBar
        },
        name: 'competitionList',
        data () {
            return {
                columns:[
                    {
                        title: '竞赛名称',
                        key: 'competitionName'
                    },
                    {
                        title: '开始时间',
                        key: 'startTime'
                    },
                    {
                        title: '结束时间',
                        key: 'endTime'
                    },
                    {
                        title: '参赛组数',
                        key: 'groupNumber'
                    },
                    {
                        title: '操作',
                        key: 'oper',
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
                                            /*this.$router.push({
                                                path: '/apply',
                                                query: {
                                                    projectID: params.row.projectID
                                                }
                                            })*/
                                        }
                                    }
                                }, '查看参赛作品')
                            ])
                        }
                    }
                ],
                rows:[
                    {
                        competitionName: '冯如杯',
                        startTime: '2019-06-29',
                        endTime: '2018-07-10',
                        groupNumber: 233
                    }
                ],
            }
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
</style>