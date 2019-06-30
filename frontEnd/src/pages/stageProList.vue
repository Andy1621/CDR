<template>
  <div>
    <NavBar></NavBar>
    <div class="body">
      <h3>第29届冯如杯</h3>
      <Circle :size="250" :trail-width="4" :stroke-width="5" :percent="75" stroke-linecap="square" stroke-color="#43a3fb">
        <div class="demo-Circle-custom">
          <p>消费人群规模</p>
        </div>
      </Circle>
      <Steps :current="current" style="margin: 30px">
        <Step title="校团委初审"  @click.native="jump(0)"></Step>
        <Step title="专家初评"  @click.native="jump(1)"></Step>
        <Step title="进入答辩"  @click.native="jump(2)"></Step>
        <Step title="最终结果"  @click.native="jump(3)"></Step>
      </Steps>
      <Table stripe border :columns="columns" :data="rows" ref="table" style="margin-right: 9%"></Table>
    </div>
  </div>
</template>

<script>
  import NavBar from '../components/NavBar.vue'
    export default {
      name: "stageProList",
      components:{
        NavBar
      },
      data(){
        return{
          current:3,
          competition_id:'5d1862380a21e6053e46c958',
          // status_1:'finish',
          // status_2:'process',
          // status_3:'wait',
          A_list:[],
          B_list:[],
          C_list:[],
          D_list:[],
          columns: [
            // {
            //   title: '作品id',
            //   key: 'project_code'
            // },
            {
              title: '作品名称',
              key: 'project_name'
            },
            {
              title: '第一作者',
              key: 'first-author'
            },
            {
              title: '状态',
              key: 'project_status'
            },
            {
              title: '操作',
              key: 'oper',
              width: 200,
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
                          path: '/firstTrial',
                          query: {
                            projectID: params.row.project_code
                          }
                        })
                      }
                    }
                  }, '查看'),
                ])
              }
            }
          ],
          rows:[]
        }
      },
      created() {
        this.getProList();
      },
      methods:{
        getProList(){
          let domin_url = 'http://127.0.0.1:5000';
          let params = {'competition_id':this.competition_id};
          this.$http.post(domin_url + "/api/v1/stageprolist",params,{
            headers:{
              'Content-Type':"application/json",
            }
          }).then(function (res) {
            var detail = res.body;
            console.log("列表数据 ",detail);
            if(detail.state =="fail"){
              this.$Message.info("获取数据失败")
            }
            else{
              this.com_status = detail.com_status-1;
              this.current = this.com_status;
              this.A_list = detail.A_List;
              this.B_list = detail.B_List;
              this.C_list = detail.C_List;
              this.D_list = detail.D_List;
              this.changeList()
            }
          }, function (res) {
            alert(res);
          });
        },
        changeList(){
          switch (this.current) {
            case 0:
              this.rows = this.A_list;
              break;
            case 1:
              this.rows = this.B_list;
              break;
            case 2:
              this.rows = this.C_list;
              break;
            case 3:
              this.rows = this.D_list;
              break;
          }
        },
        jump(num){
          if(num <= this.com_status) {
            this.current = num;
            this.changeList();
          }
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
  h3{
    border-left: 5px solid purple;
    padding: 0 0 0 15px!important;
    font-size: 28px!important;
    margin: 24px 0!important;
  }
  step{
    cursor:pointer;
  }

</style>
