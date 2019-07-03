<template>
  <div>
    <NavBar></NavBar>
    <div class="body">
      <Breadcrumb style="text-align: left">
        <BreadcrumbItem to="/competitionList">竞赛列表</BreadcrumbItem>
        <BreadcrumbItem :to="{path:'/stageProList',query: {competitionID:this.$route.query.competition_id,}}">
          {{this.$route.query.competition_title}}</BreadcrumbItem>
        <BreadcrumbItem> "{{this.basicInfo.project}}" 作品申请表</BreadcrumbItem>
      </Breadcrumb>
      <h3>作品申请表</h3>
      <Steps :current="current" style="margin: 30px">
        <Step title="作品基本信息" content="" @click.native="jump_0"></Step>
        <Step title="申请者信息" content="" @click.native="jump_1"></Step>
        <Step title="作品详细信息" content="" @click.native="jump_2"></Step>
      </Steps>
      <div class="form" v-show="current == 0">
        <Form ref="basicInfo" :model="basicInfo" :rules="ruleBasicInfo" :label-width="80">
          <FormItem label="作品名称" prop="project">
            <Input v-model="basicInfo.project" readonly></Input>
          </FormItem>
          <FormItem label="院系名称" prop="college">
            <Input v-model="basicInfo.college" readonly></Input>
          </FormItem>
          <FormItem label="作品类别" prop="type">
            <Input v-model="basicInfo.type" readonly></Input>
          </FormItem>
        </Form>
      </div>
      <div class="form" v-show="current == 1">
        <h4 style="margin-bottom: 20px">第一作者信息</h4>
        <Form ref="authorInfo" :model="authorInfo" :rules="ruleAuthorInfo" :label-width="80">
          <Row>
            <Col span="12">
              <FormItem label="姓名" prop="name">
                <Input v-model="authorInfo.name" readonly></Input>
              </FormItem>
            </Col>
            <Col span="12">
              <FormItem label="学号" prop="stu_id">
                <Input v-model="authorInfo.stu_id" readonly></Input>
              </FormItem>
            </Col>
          </Row>
          <FormItem label="出生年月" prop="birth">
            <DatePicker v-model="authorInfo.birth" type="month" readonly></DatePicker>
          </FormItem>
          <Row>
            <Col span="12">
              <FormItem label="现学历" prop="edu_background">
                <Input v-model="authorInfo.edu_background" readonly></Input>
              </FormItem>
            </Col>
            <Col span="12">
              <FormItem label="专业" prop="major">
                <Input v-model="authorInfo.major" readonly></Input>
              </FormItem>
            </Col>
          </Row>
          <FormItem label="入学时间" prop="school_date">
            <Row>
              <Col span="12">
                <DatePicker v-model="authorInfo.school_date" type="month" readonly></DatePicker>
              </Col>
            </Row>
          </FormItem>
          <FormItem label="作品全称" prop="project" >
            <Input v-model="authorInfo.project" readonly></Input>
          </FormItem>
          <FormItem label="通讯地址" prop="address">
            <Input v-model="authorInfo.address" readonly></Input>
          </FormItem>
          <Row>
            <Col span="12">
              <FormItem label="联系电话" prop="phone" >
                <Input v-model="authorInfo.phone" readonly></Input>
              </FormItem>
            </Col>
            <Col span="12">
              <FormItem label="邮箱" prop="email">
                <Input v-model="authorInfo.email" readonly></Input>
              </FormItem>
            </Col>
          </Row>
          <h4 style="margin-bottom: 20px">合作者信息</h4>
          <h5 v-show="authorInfo.cooperators.length==0">暂无合作者</h5>
          <Row v-for="(item,index) in authorInfo.cooperators" :key="index">
            <h5>合作者{{index+1}}</h5>
            <Col span="8">
              <FormItem label="姓名" :key="index" :prop="'cooperators.'+ index +'.name'" :rules="{required: false, message:'姓名不能为空', trigger: 'blur'}">
                <Input v-model="item.name" readonly></Input>
              </FormItem>
            </Col>
            <Col span="8">
              <FormItem label="学号" :key="index" :prop="'cooperators.'+ index +'.stu_id'" :rules="{required: false, message:'学号不能为空', trigger: 'blur'}">
                <Input v-model="item.stuId" readonly></Input>
              </FormItem>
            </Col>
            <Col span="8">
              <FormItem label="现学历" :key="index" :prop="'cooperators.'+ index +'.edu'" :rules="{required: false, message:'请选择现学历', trigger: 'change'}">
                <Input v-model="item.education" readonly></Input>
                <!--<Select v-model="item.edu" :disabled="readonly">-->
                  <!--<Option value="A">A.专科</Option>-->
                  <!--<Option value="B">B.大学本科</Option>-->
                  <!--<Option value="C">C.硕士研究生</Option>-->
                  <!--<Option value="D">D.博士研究生</Option>-->
                <!--</Select>-->
              </FormItem>
            </Col>
            <Col span="12">
              <FormItem label="联系电话" :key="index" :prop="'cooperators.'+ index +'.phone'" :rules="{required: false, message:'联系电话不能为空', trigger: 'blur'}">
                <Input v-model="item.phone" readonly></Input>
              </FormItem>
            </Col>
            <Col span="12">
              <FormItem label="邮箱"  :key="index" :prop="'cooperators.'+ index +'.email'" :rules="{required: false, message:'邮箱为空或格式错误', type: 'email', trigger: 'blur'}">
                <Input v-model="item.email" readonly></Input>
              </FormItem>
            </Col>
          </Row>
        </Form>
      </div>
      <div class="form" v-show="current == 2">
        <Form ref="projectInfo" :model="projectInfo" :rules="ruleProjectInfo" :label-width="80">
          <FormItem label="作品全称" prop="project">
            <Input v-model="projectInfo.project"readonly style="color: black"></Input>
          </FormItem>
          <FormItem label="作品分类" prop="type">
            <Input v-model="projectInfo.type"readonly style="color: black"></Input>
          </FormItem>
          <FormItem label="作品情况" prop="introduction">
            <Input v-model="projectInfo.introduction" readonly type="textarea" :maxlength="800" :rows="4" :autosize="{minRows: 4,maxRows: 4}" placeholder="请输入作品整体情况说明（不超过800字）"></Input>
          </FormItem>
          <FormItem label="创新点" prop="innovation">
            <Input v-model="projectInfo.innovation" readonly type="textarea" :rows="3" :autosize="{minRows: 3,maxRows: 3}" placeholder="1-5条体现作品主要创意的创新点"></Input>
          </FormItem>
          <FormItem label="关键词" prop="keyword">
            <Input v-model="projectInfo.keyword" readonly type="textarea" :rows="3" :autosize="{minRows: 3,maxRows: 3}" placeholder="4-7个体现作品核心技术和问题的关键词"></Input>
          </FormItem>
        </Form>
      </div>
      <!--<Button type="" v-show="current == 2" @click="check_table">预览表格</Button>-->
      <Button type="primary" shape="circle" :disabled="current == 0" @click="pre_step" icon="ios-arrow-back" style="margin-right: 30%"></Button>
      <Button type="primary" shape="circle" :disabled="current == 2" @click="next_step" icon="ios-arrow-forward"></Button>
      <div style="margin-top: 10px">
        <Button type="primary" v-show="current == 2" :disabled="show" style="margin-right:6%" @click="pass('True')" >通过</Button>
        <Button type="error" v-show="current == 2" :disabled="show" @click="pass('False')">不通过</Button>
      </div>
    </div>
  </div>
</template>

<script>
    import NavBar from '../components/NavBar.vue'
    import Divider from "../../static/css/iview/iview";
    export default {
      name: "firstTrial",
      components:{
        Divider,
        NavBar
      },
      data(){
        return {
          readonly: true,
          current: 0,
          show:false,
          basicInfo: {
            id:'1',
            project: 'ZebraScience',
            college: 'BUAA',
            type: '科技发明制作',
          },
          ruleBasicInfo:{
            project: [
              { required: false, message: '作品名称不能为空', trigger: 'blur' }
            ],
            college: [
              { required: false, message: '院系名称不能为空', trigger: 'blur' }
            ],
            type: [
              { required: false, message: '请选择作品类别', trigger: 'change' }
            ],
          },
          authorInfo:{
            name: 'lkc',
            stu_id: '1621',
            birth: '1997-09',
            edu_background: 'D.博士研究生',
            major: 'Soft Engineering',
            school_date: '2019-2',
            project: 'Zebra',
            address: '708',
            phone: '12',
            email: '1@1.com',
            cooperators: []
          },
          ruleAuthorInfo:{
            name: [
              { required: false, message: '姓名不能为空', trigger: 'blur' }
            ],
            stu_id: [
              { required: false, message: '学号不能为空', trigger: 'blur' }
            ],
            birth: [
              { required: false, type:'date', message: '出生年月不能为空', trigger: 'change' }
            ],
            edu_background: [
              { required: false, message: '现学历不能为空', trigger: 'change' }
            ],
            major: [
              { required: false, message: '专业不能为空', trigger: 'blur' }
            ],
            school_date: [
              { required: false, type:'date', message: '入学时间不能为空', trigger: 'change' }
            ],
            project: [
              { required: false, message: '作品全称不能为空', trigger: 'blur' }
            ],
            address: [
              { required: false, message: '通讯地址不能为空', trigger: 'blur' }
            ],
            phone: [
              { required: false, message: '联系电话不能为空', trigger: 'blur' }
            ],
            email: [
              { required: false, message: '邮箱不能为空', trigger: 'blur' },
              { type: 'email', message: '邮箱格式错误', trigger: 'blur' }
            ],
            cooperators: [
              { required:false, message: '不能为空', trigger: 'blur' }
            ]
          },
          projectInfo:{
            project: 'ZebraScience',
            type: 'A.机械与控制（包括机械、仪器仪表、自动化控制、工程、交通、建筑等）',
            introduction: 'Zebra is a zebra',
            innovation: 'No idea',
            keyword: 'nothing',
          },
          ruleProjectInfo:{
            project: [
              { required: false, message: '作品全称不能为空', trigger: 'blur' }
            ],
            type: [
              { required: false, message: '请选择作品类别', trigger: 'change' }
            ],
            introduction: [
              { required: false, message: '作品情况不能为空', trigger: 'blur' }
            ],
            innovation: [
              { required: false, message: '创新点不能为空', trigger: 'blur' }
            ],
            keyword: [
              { required: false, message: '关键词不能为空', trigger: 'blur' }
            ]
          },
        }
      },
      created() {
        this.basicInfo.id = this.$route.query.projectID;
        console.log(this.basicInfo.id);
        this.getFormMess();
      },
      methods:{
        next_step(){
          console.log(this.authorInfo.cooperators);
          if(this.readonly){
            this.current += 1;
          }
          else{
            var check_name;
            switch (this.current){
              case 0:
                check_name = 'basicInfo';
                break;
              case 1:
                check_name = 'authorInfo';
                break;
              case 2:
                check_name = 'projectInfo';
                break;
            }
            this.$refs[check_name].validate((valid) => {
              if (valid) {
                // this.$Message.success('Success!');
                this.current += 1;
              } else {
                this.$Message.error('信息有误');
              }
            });
            this.save_data();
          }
        },
        pre_step(){
          if(this.readonly){
            this.current -= 1;
          }
          else{
            this.current -= 1;
            this.save_data();
          }
        },
        check_table(){
          // check table
          this.$Message.info('Check Table')
        },
        save_data(){
          // save data function
          this.$Message.info('Save Data')
        },
        getFormMess(){
          let params = {'proj_id':this.basicInfo.id};
          this.$http.post(this.$baseURL + "/api/vi/get_table_info",params,{
            headers:{
              'Content-Type':"application/json",
            }
          }).then(function (res) {
             var detail = (res.body.msg);
            console.log(detail);
            if(res.body.state=="fail"){
              this.$Message.info("获取数据失败")
            }
            else{
              if(detail.com_status > 1)
                this.show=true;
              this.basicInfo.project = detail.mainTitle;
              this.basicInfo.college = detail.department;
              this.basicInfo.type = detail.mainType;
              this.authorInfo.name = detail.name;
              this.authorInfo.stu_id = detail.stuId;
              this.authorInfo.birth = detail.birthday;
              this.authorInfo.edu_background = detail.education;
              this.authorInfo.major = detail.major;
              this.authorInfo.school_date = detail.enterTime;
              this.authorInfo.project = detail.totalTitle;
              this.authorInfo.address = detail.address;
              this.authorInfo.phone = detail.phone;
              this.authorInfo.email = detail.email;
              this.authorInfo.cooperators = detail.applier;
              this.projectInfo.project = detail.title;
              this.projectInfo.type = detail.type;
              this.projectInfo.introduction = detail.description;
              this.projectInfo.innovation = detail.creation;
              this.projectInfo.keyword = detail.keyword;
              this.authorInfo.cooperators = detail.applier;
              switch (detail.type) {
                case 'A':
                  this.projectInfo.type = '机械与控制（包括机械、仪器仪表、自动化控制、工程、交通、建筑等）';
                      break;
                case 'B':
                  this.projectInfo.type = '信息技术（包括计算机、电信、通讯、电子等）';
                  break;
                case 'C':
                  this.projectInfo.type = '数理（包括数学、物理、地球与空间科学等）';
                  break;
                case 'D':
                  this.projectInfo.type = '生命科学（包括生物､农学､药学､医学､健康､卫生､食品等）';
                  break;
                case 'E':
                  this.projectInfo.type = '能源化工（包括能源、材料、石油、化学、化工、生态、环保等）';
                  break;
                case 'F':
                  this.projectInfo.type = '哲学社会科学（包括哲学、经济、社会、法律、教育、管理）';
                  break
              }
            }
          }, function (res) {
            alert(res);
          });
        },
        pass(re){
          let params = {'projlst':[{'proj_id':this.basicInfo.id,'result':re}]};
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
              this.$router.push({
                path: '/stageProList',
                query: {
                  competitionID:this.$route.query.competition_id,
                }
              })
            }
          }, function (res) {
            alert(res);
          });
        },
        jump_0(){
          this.current = 0;
        },
        jump_1(){
          this.current = 1;
        },
        jump_2(){
          this.current = 2;
        }
        },
      mounted () {
        //设置Message默认属性
        this.$Message.config({
          top: 100,
          duration: 1,
        });
      }
    }
</script>

<style scoped>
  .body{
    margin-left: 30%;
    margin-bottom: 50px;
    position: relative;
    top: 100px;
    border: 1px dashed black;
    border-radius: 20px;
    /*margin: 100px 0px 50px 30%;*/
    padding: 20px;
    width: 50%;
    text-align: center;
    min-height: 470px;
    min-width: 600px;
    color: black;
  }
  .form{
    text-align: left;
    padding: 3px;
    margin-bottom: 5px;
    font-size: 15px;
  }
  #sidebar-nav.sidebar{
    padding-top: 0px;
  }

  /*input:disabled{*/
    /*opacity: 1;*/
    /*-webkit-text-fill-color: red;*/
  /*}*/

</style>
