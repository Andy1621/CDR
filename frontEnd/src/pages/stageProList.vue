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
        <Step :title=t[0]  @click.native="jump(4)"></Step>
      </Steps>
      <Table stripe border :columns="columns" :data="rows" ref="selection" style="margin-right: 9%;margin-left:6%"
      @on-select-all="selectAll" @on-selection-change="selectionChange"></Table>
      <div v-if="com_status==1" style="background-color: #6ecadc;margin-top: 10px;width:85%;margin-left: 6%;border-radius: 3px;height:40px;
        line-height:40px;">
        <span style="margin-left: 2%">已选中{{this.selectnum}}</span>
        <button style=";margin-left: 75%;background-color: red;border: none;width: 10%" @click="pass">通过</button>
      </div>
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
          selectnum:0,
          selectItem:[],
          competition_id:'5d1862380a21e6053e46c958',//''5d170bd90a21e6053e45f3eb,
          competition_title: "",
          com_status:0,//只有012345能进来
          t:["报名提交","校团委初审","专家初评","进入答辩","最终结果"],
          E_list:[],
          A_list:[],
          B_list:[],
          C_list:[],
          D_list:[],
          select:{
            type: 'selection',
            width: 60,
            align: 'center',
          },
          columns: [
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
                  h('Button', {
                    props: {
                      type: 'primary',
                      size: 'small',
                    },
                    style: {
                      marginRight:'5px'
                    },
                    on: {
                      click: () => {

                      }
                    }
                  }, this.current == -1?'退回':'通过'),
                ])
              }
            },
         {
            type: 'selection',
            width: 60,
            align: 'center',
         },
          ],
          rows:[]
        }
      },
      created() {
        this.competition_id = this.$route.query.competitionID;
        this.getProList();
      },
      methods:{
        selectAll(data){
          this.selectnum = data.length;
        },
        selectionChange(data){
          this.selectnum=0;
          this.selectItem.length = 0;
          this.selectnum = data.length;
          for(var i of data){
            this.selectItem.push({'proj_id':i.project_code,'re':'True'})
          }
        },
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
              this.com_status = detail.com_status == 5? 4:detail.com_status;
              if(this.com_status!=1){this.columns.pop()}
              this.t[this.com_status] = this.t[this.com_status] + "(正在进行)";
              this.current = this.com_status;
              this.E_list = detail.E_List;
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
          this.selectnum = 0;
          this.selectItem.length=0;
          if(this.com_status==1&&this.current==0)this.columns.pop();
          else if(this.com_status==1&&this.columns.length==4)this.columns.push(this.select);
          if(this.btshow.length>0){
            this.btshow.length = 0;
          }
          switch (this.current) {
            case 0:
              this.rows = this.E_list;
              break;
            case 1:
              this.rows = this.A_list;
              break;
            case 2:
              this.rows = this.B_list;
              break;
            case 3:
              this.rows = this.C_list;
              break;
            case 4:
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
        },
        pass(){
          let params = {'projlst':this.selectItem};
          this.$http.post(this.$baseURL + "/api/vi/first_trial_change",params,{
            headers:{
              'Content-Type':"application/json",
            }
          }).then(function (res) {
            var detail = (res.body.state);
            console.log(detail);
            if(detail =="fail"){
              this.$Message.info("评审失败")
            }
            else{
              this.$Notice.open({title: "评审完成",duration:0.5});
            }
          }, function (res) {
            alert(res);
          });
        },
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
