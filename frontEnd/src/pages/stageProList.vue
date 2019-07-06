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
      <Step :title=t[4]  @click.native="jump(4)"></Step>
    </Steps>
      <Table  stripe border :columns="columns" :data="rows" ref="selection" style="margin-right: 9%;margin-left:6%"
              @on-selection-change="selectionChange"></Table>
      <div style="margin-right: 9%;margin-top:2%;overflow: hidden">
        <div style="float: right;">
          <Page :total="total_item" :current="pageNum" :page-size="pageSize"	 @on-change="changePage"></Page>
        </div>
      </div>
      <div v-if="(current==1&&com_status==1)||(current==3&&com_status==3)" style="background-color: #9acfea;margin-top:1%;width:85%;margin-left: 6%;border-radius: 3px;height:40px;
        line-height:40px;">
        <span style="margin-left: 2%">已选中 {{this.selectnum}} 项</span>
        <button style=";margin-left: 75%;background-color: #aeb7c4;border: none;width: 10%" @click="pass(com_status)">通过</button>
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
          total_item:1,
          pageSize:2,
          pageNum:1,
          current:-2,
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
          select:{type: 'selection', width: 48,align: 'center',},
          score:{title: '平均分',key: 'score',width:73,sortable: true},
          columns: [
            {
              title: '作品名称',
              key: 'project_name',
              width:263
            },
            {
              title: '作品类别',
              key: 'type',
              filters:[
                {
                  label:"机械控制",
                  value:1
                },
                {
                  label:"信息技术",
                  value:2
                },
                {
                  label:"数理",
                  value:3
                },
                {
                  label:"生命科学",
                  value:4
                },
                {
                  label:"能源化工",
                  value:5
                },
                {
                  label:"哲学社科",
                  value:6
                }
              ],
              filterMultiple: false,
              filterMethod (value, row) {
                if (value === 1) {
                  return row.type === '机械控制';
                } else if (value === 2) {
                  return row.type === '信息技术';
                } else if (value === 3) {
                  return row.type === '数理';
                } else if (value === 4) {
                  return row.type === '生命科学';
                } else if (value === 5) {
                  return row.type === '能源化工';
                } else {
                  return row.type === '哲学社科';
                }
              }
            },
            {
                title: '第一作者',
                key: 'author_name',
                width: 140
            },
            {
                title: '状态',
                key: 'project_status',
                width: 140
            },
            {
              title: '操作',
              key: 'oper',
              width: 197,
              align: 'center',
              render: (h, params) => {
                return h('div', [
                  h('Button', {
                    props: {
                      type: 'primary',
                      size: 'small',
                      disabled:(params.row.project_status=="编辑中")
                    },
                    style: {
                      marginRight:'5px',
                      //display:(this.current==4)?"none":"inline-block"
                    },
                    on: {
                      click: () => {
                        if(this.current==0||this.current==1){
                            this.check_table(params.row.project_code)
                        }
                        else if(this.current == 2||this.current == 3){
                          this.$router.push({
                            path: '/expTrialStat',
                            query: {
                                competition_id:this.competition_id,
                                competition_title:this.competition_title,
                                projectID: params.row.project_code,
                                projectName:params.row.project_name,
                                fromState:this.current
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
                      disabled:(params.row.project_status=="编辑中")||(this.com_status>0&&this.current==0)
                    },
                    style: {
                      marginRight:'5px',
                      display:(this.current==0||this.current==1||this.current==4)?"inline-block":"none"
                    },
                    on: {
                      click: () => {
                        if(this.com_status==0)
                          this.rejectPro(params.row.project_code);
                        else if(this.com_status==1){
                          this.downloadFile(params.row.project_code);
                        }
                      }
                    }
                    },this.current==0?"退回":"下载附件"),
                  h('Button', {
                    props: {
                      type: 'error',
                      size: 'small',
                      disabled:(params.row.project_status=="通过初审")
                    },
                    style: {
                      marginRight:'5px',
                      display:(this.com_status==1&&this.current==1)?"inline-block":"none"
                    },
                    on: {
                      click: () => {
                        this.selectItem=[{'proj_id':params.row.project_code,'re':'False'}];
                        this.pass(1);
                      }
                    }
                  },'拒绝'),
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
        changeTitle(){
            if(this.com_status ==0 && this.current==0){
              return "退回"
            }
          if(this.com_status ==1 && this.current==1){
            return "下载附件"
          }
        },
        selectionChange(data){
          this.selectnum=0;
          this.selectItem.length = 0;
          this.selectnum = data.length;
          if(this.com_status==1) {
            for (var i of data) {
              this.selectItem.push({'proj_id': i.project_code, 're': 'True'})
            }
          }
          else{
            for (var i of data) {
              this.selectItem.push(i.project_code)
            }
          }
        },
        rejectPro(id){
          let params = {'project_code':id};
          console.log(params);
          this.$http.post(this.$baseURL + "/api/v1/reject_project",params,{
            headers:{
              'Content-Type':"application/json",
            }
          }).then(function (res) {
            var detail = (res.body.state);
            console.log(detail);
            if(detail =="fail"){
              this.$Notice.open({title: "退回失败",duration:0.5});
            }
            else{
              this.$Notice.open({title: "退回完成",duration:0.5});
              location.reload();
            }
          }, function (res) {
            alert(res);
          });
        },
        downloadFile(id){
          this.$http.get(this.$baseURL + '/api/v1/download_files', {
            params: {
              project_code: id
            }
          }).then(function (res) {
            console.log(res);
            if (res.body.state === 'Success') {
              window.location.href = res.body.url;
            } else {
              this.$Message.error("下载失败" + res.body.reason)
            }
          }, function (res) {
            console.log(res)
          })
        },
        check_table(id){
          this.$http.get(this.$baseURL + '/api/v1/view_apply',{params:{'project_code': id}})
            .then(function (res) {
              var detail = res.body;
              console.log(detail);
              if(detail.state == 'fail'){
                this.$Message.error(detail.reason)
              }
              else{
                window.open(detail.html_url)
              }
            },function (res) {
              this.$Message.error('Failed')
            })
        },
        handleType(lst){
          for(var item of lst){
            switch (item.registration_form.type) {
              case "":
                item["type"] = "机械控制";
                break;
              case "A":
                item["type"] = "机械控制";
                break;
              case "B":
                item["type"] = "信息技术";
                break;
              case "C":
                item["type"] = "数理";
                break;
              case "D":
                item["type"] = "生命科学";
                break;
              case "E":
                item["type"] = "能源化工";
                break;
              case "F":
                item["type"] = "哲学社科";
                break;
            }
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
              //if(this.com_status!=1){this.columns.pop()}
              this.t[this.com_status] = this.t[this.com_status] + "(正在进行)";
              this.current = this.com_status;
              this.E_list = detail.E_List;
              this.A_list = detail.A_List;
              this.B_list = detail.B_List;
              this.C_list = detail.C_List;
              this.D_list = detail.D_List;
              this.handleType(this.E_list);
              this.handleType(this.A_list);
              this.handleType(this.B_list);
              this.handleType(this.C_list);
              this.handleType(this.D_list);
              this.changeList()
            }
          }, function (res) {
            alert(res);
          });
        },
        handelColumns(){
          if(this.current==1||this.current==3){
            if(this.columns[this.columns.length-1].type!="selection"){this.columns.push(this.select);}
            if(this.current==3&&this.columns[3].key!='score'){
              this.columns.splice(3,0,this.score);
            }
          }
          else{
            if(this.columns[this.columns.length-1].type=="selection"){this.columns.pop();}
            if(this.columns[3].key=='score'){this.columns.splice(3,1);}
          }
        },
        handleData(lst){
          for(let item of lst){
            if(this.current==1){
              if(this.com_status==1){
                if(item.project_status!="已提交") item._disabled = true;
              }
              else{item._disabled = true;}
            }
            else if(this.current==3){
              if(this.com_status==3) {
                if (item.project_status != "通过初审") item._disabled = true;
              }
              else{item._disabled = true;}
            }
          }
        },
        changeList(){
          this.selectnum = 0;
          this.selectItem.length=0;
          this.handelColumns();
          switch (this.current) {
            case 0:
              this.rows = this.E_list.slice(0,this.pageSize);
              this.total_item = this.E_list.length;
              break;
            case 1:
              this.handleData(this.A_list);
              this.rows = this.A_list.slice(0,this.pageSize);
              this.total_item = this.A_list.length;
              break;
            case 2:
              this.rows = this.B_list.slice(0,this.pageSize);
              this.total_item = this.B_list.length;
              break;
            case 3:
              this.handleData(this.C_list);
              this.rows = this.C_list.slice(0,this.pageSize);
              this.total_item = this.C_list.length;
              break;
            case 4:
              this.rows = this.D_list.slice(0,this.pageSize);
              this.total_item = this.D_list.length;
              break;
          }
          this.pageNum = 1;
        },
        jump(num){
          if(num != this.current && num <= this.com_status) {
            this.current = num;
            this.changeList();
          }
        },
        pass(num){
          if(this.selectItem.length==0)return;
          let params = {'projlst':this.selectItem};
          let url = this.$baseURL + (num==1?"/api/vi/first_trial_change":"/api/v1/enter_defense_list");
          this.$http.post(url ,params,{
            headers:{
              'Content-Type':"application/json",
            }
          }).then(function (res) {
            var detail = (res.body.state);
            console.log(detail);
            if(detail =="fail"){
              this.$Notice.open({title: "评审失败",duration:1});
            }
            else{
              //this.$Notice.open({title: "评审完成",duration:1});
              location.reload();
            }
          }, function (res) {
            alert(res);
          });
        },
        changePage(value){
          this.pageNum = value;
          let a = this.pageSize*(this.pageNum-1);
          let b = this.pageSize*this.pageNum;
          switch (this.current) {
            case 0:
              this.rows = this.E_list.slice(a,b);
              break;
            case 1:
              this.rows = this.A_list.slice(a,b);
              break;
            case 2:
              this.rows = this.B_list.slice(a,b);
              break;
            case 3:
              this.rows = this.C_list.slice(a,b);
              break;
            case 4:
              this.rows = this.D_list.slice(a,b);
              break;
          }
          document.body.scrollTop = 0;
          document.documentElement.scrollTop = 0;
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
