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
                        key: 'competition_name'
                    },
                    {
                        title: '开始时间',
                        key: 'begin_time'
                    },
                    {
                        title: '结束时间',
                        key: 'end_time'
                    },
                    {
                      title: '竞赛状态',
                      key: 'com_status'
                    },
                    {
                        title: '作品数量',
                        key: 'count'
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
                                            this.$router.push({
                                                path: '/stageProList',
                                                query: {
                                                    competitionID: params.row.competition_id,
                                                    // competitionTitle: params.row.competition_name
                                                }
                                            })
                                        }
                                    }
                                }, '竞赛入口')
                            ])
                        }
                    }
                ],
                rows:[
                    // {
                    //     competitionName: '冯如杯',
                    //     startTime: '2019-06-29',
                    //     endTime: '2018-07-10',
                    //     groupNumber: 233
                    // }
                ],
            }
        },
      created() {
        this.getcomList()
      },
      methods:{
        getcomList(){
          let domin_url = 'http://127.0.0.1:5000';
          let params = {};
          this.$http.post(domin_url + "/api/v1/contestlist",params,{
            headers:{
              'Content-Type':"application/json",
            }
          }).then(function (res) {
            var detail = res.body;
            console.log("请求反回数据 ",detail);
            if(detail.state =="fail"){
              this.$Message.info("获取数据失败")
            }
            else{
              for (let item of detail.contests) {
                switch (item.com_status) {
                  case 0:
                    item.com_status = "学生作品提交";
                    break;
                  case 1:
                    item.com_status = "校团委初审";
                    break;
                  case 2:
                    item.com_status = "专家初评";
                    break;
                  case 3:
                    item.com_status = "筛选作品及现场答辩";
                    break;
                  case 4:
                    item.com_status = "已结束";
                    break;
                }
              }
              this.rows = detail.contests
            }
          }, function (res) {
            alert(res);
          });
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
