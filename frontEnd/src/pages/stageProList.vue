<template>
  <div>
    <NavBar></NavBar>
    <div class="body">
      <h3>第29届冯如杯</h3>
      <Steps :current="current" style="margin: 30px">
        <Step title="校团委初审" status="finish"  @click.native="jump(0)"></Step>
        <Step title="专家初评" status="finish"  @click.native="jump(1)"></Step>
        <Step title="进入答辩" status="process"  @click.native="jump(2)"></Step>
        <Step title="最终结果" status="wait" @click.native="jump(3)"></Step>
      </Steps>
      <Table stripe border :columns="columns" :data="rows" ref="table" ></Table>
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
          current:0,
          competition_id:'1',
          com_status:2,
          A_list:[],
          B_list:[],
          C_list:[],
          D_list:[],
          columns: [
            {
              title: '作品id',
              key: 'project_code'
            },
            {
              title: '作品名称',
              key: 'name'
            },
            {
              title: '第一作者',
              key: 'first-author'
            },
            {
              title: '状态',
              key: 'status'
            },
          ],
          rows:[]
        }
      },
      created() {
        this.getProList();
        this.current = this.com_status;
        this.changeList();
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
              this.A_list = detail.A_list;
              this.B_list = detail.B_list;
              this.C_list = detail.C_list;
              this.D_list = detail.D_list;
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
