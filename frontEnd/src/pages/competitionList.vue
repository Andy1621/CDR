<template>
    <div>
        <NavBar></NavBar>
        <div class="body">
            <h2>竞赛列表</h2>
            <Table stripe border :columns="columns" :data="rows" ref="table" style="width:100%"></Table>
        </div>
        <router-view v-if="isRouterAlive"></router-view>
    </div>
</template>

<script>
    import NavBar from '../components/NavBar.vue'
    export default {
        components:{
            NavBar
        },
        name: 'competitionList',
        inject: ['reload'],
        data () {
            return {
                columns:[
                    {
                        title: '竞赛名称',
                        key: 'competition_name',
                        width: 210
                    },
                    {
                        title: '开始时间',
                        key: 'begin_time',
                        width: 90
                    },
                    {
                        title: '结束时间',
                        key: 'end_time',
                        width: 90
                    },
                    {
                        title: '参赛作品总数',
                        key: 'count',
                        width: 120
                    },
                    {
                      title: '竞赛状态',
                      key: 'com_status',
                      width: 160
                    },
                    {
                        title: '操作',
                        key: 'oper',
                        align: 'center',
                        render: (h, params) => {
                            return h('div', [
                              h('Button', {
                                props: {
                                  type: 'error',
                                  size: 'small',
                                  disabled: (params.row.com_status == "校团委初审")
                                },
                                style: {
                                  marginRight: '5px'
                                },
                                on: {
                                  click: () => {
                                    let param = {proj_id: params.row.competition_id, op: "back"};
                                    this.$http.post(this.$baseURL + "/api/v1/changeCompStat",param).then(function (res) {
                                      var detail = res.body.state;
                                      if(detail == "fail"){
                                        this.$Notice.open({title: "操作失败"});
                                        this.reload();
                                      }
                                      else{
                                        this.$Notice.open({title: "已退回上一阶段"});
                                        this.reload();
                                      }
                                    }, function (res) {
                                      alert(res);
                                    });
                                  }
                                }
                              }, '返回上阶段'),
                              h('Button', {
                              props: {
                                type: 'primary',
                                size: 'small'
                              },
                              style: {
                                marginRight: '5px'
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
                            }, '竞赛入口'),
                            h('Button', {
                              props: {
                                type: 'success',
                                size: 'small',
                                disabled: (params.row.com_status == "已结束")
                              },
                              style: {
                                marginRight: '5px'
                              },
                              on: {
                                click: () => {
                                  let param = {proj_id: params.row.competition_id, op: "go"};
                                  this.$http.post(this.$baseURL + "/api/v1/changeCompStat",param).then(function (res) {
                                    var detail = res.body.state;
                                    if(detail == "fail"){
                                      this.$Notice.open({title: "操作失败"});
                                      this.reload();
                                    }
                                    else{
                                      this.$Notice.open({title: "成功进入下一阶段"});
                                      this.reload();
                                    }
                                  }, function (res) {
                                    alert(res);
                                  });
                                }
                              }
                            }, '进入下阶段')
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
                isRouterAlive: true,
            }
        },
      created() {
        this.getcomList()
      },
      methods:{
        getcomList(){
          let params = {};
          this.$http.post(this.$baseURL + "/api/v1/contestlist",params,{
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
                  case 1:
                    item.com_status = "校团委初审";
                    break;
                  case 2:
                    item.com_status = "专家初评";
                    break;
                  case 3:
                    item.com_status = "进入答辩";
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
