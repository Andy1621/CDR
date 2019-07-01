<template>
  <div>
    <NavBar></NavBar>
    <div class="body">
      <Breadcrumb style="text-align: left">
        <BreadcrumbItem to="/competitionList">竞赛列表</BreadcrumbItem>
        <BreadcrumbItem>{{this.competition_title}}</BreadcrumbItem>
      </Breadcrumb>
      <h3>
        {{competition_title}}
      </h3>
      <Steps :current="current" style="margin: 30px">
        <Step :title=t[0]  @click.native="jump(0)"></Step>
        <Step :title=t[1]  @click.native="jump(1)"></Step>
        <Step :title=t[2]  @click.native="jump(2)"></Step>
        <Step :title=t[3]  @click.native="jump(3)"></Step>
      </Steps>
      <Table stripe border :columns="columns" :data="rows" ref="table" style="margin-right: 9%;margin-left:6%"></Table>
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
          btshow:[],
          current:3,
          competition_id:'5d1862380a21e6053e46c958',//''5d170bd90a21e6053e45f3eb,
          competition_title: "",
          com_status:0,
          t:["校团委初审","专家初评","进入答辩","最终结果"],
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
              key: 'project_name',
              width:320
            },
            {
              title: '第一作者',
              key: 'author_name'
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
                      size: 'small',
                      disabled:this.btshow[params.index]
                    },
                    style: {
                      marginRight:'5px'
                    },
                    on: {
                      click: () => {
                        if(this.current == 0) {
                          this.$router.push({
                            path: '/firstTrial',
                            query: {
                              competition_id:this.competition_id,
                              competition_title:this.competition_title,
                              projectID: params.row.project_code,

                            }
                          })
                        }
                        else if(this.current == 1){
                          this.$router.push({
                            path: '/expTrialStat',
                            query: {
                              competition_id:this.competition_id,
                              competition_title:this.competition_title,
                              projectID: params.row.project_code,
                              projectName:params.row.project_name
                            }
                          })
                        }
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
        this.competition_id = this.$route.query.competitionID;
        //this.competition_title = this.$route.query.competitionTitle;
        this.getProList();
      },
      methods:{
        getProList(){
          let params = {'competition_id':this.competition_id};
          this.$http.post(this.$baseURL + "/api/v1/stageprolist",params,{
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
              this.competition_title = detail.competition_name;
              this.com_status = detail.com_status-1;
              this.t[this.com_status] = this.t[this.com_status] + "(正在进行)";
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
          if(this.btshow.length>0){
            this.btshow.length = 0;
          }
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
          for(let item of this.rows){
            if(item.project_status=="编辑中"){
              this.btshow.push(true)
            }
            else
              this.btshow.push(false)
          }
          console.log(this.btshow)
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
    margin: 20px 0!important;
  }
  step{
    cursor:pointer;
  }

</style>
