<template>
  <div class="tw-w-full tw-h-full tw-flex tw-flex-nowrap tw-flex-row">
    <!-- 全字体部分 -->
    <div v-show="fontsnotloaded" class="tw-absolute tw-h-full tw-rounded-lg text-display-v tw-flex tw-justify-center tw-items-center tw-text-3xl tw-border tw-border-solid indicate-cover tw-select-none" @click="userloadfonts">
      <div class="loop-words">
        点击加载本地字体库
      </div>
    </div>
    <div class="tw-flex-none tw-h-full tw-border tw-border-solid tw-rounded-lg tw-p-2" style="width:195px;border-color:#dcdfe6;">
      <el-scrollbar style="max-height: calc(100vh - 130px)">
        <div v-for="item in localfonts.value" :key="item" class="tw-select-none lst-item tw-px-3 tw-py-0.5 tw-rounded" @click="select_font(item.fullName)" :style="{'font-family': item.fullName}">{{item.fullName}}</div>
      </el-scrollbar>
    </div>
    <!-- 编辑器部分 -->
    <div class="tw-flex-none tw-flex-col tw-px-4 tw-pl-5 scroll-container" style="width: 400px; height: calc(100vh - 113px)">
      <div class="tw-w-full tw-flex-col" style="background-color: #ffff">
        <!-- 边框部署的副作用，在背景图层上有东西，需要新建一层重设背景取消 -->
        <div>
          <div class="tw-tracking-wider tw-select-none tw-text-lg tw-mb-2">样式名</div>
          <el-input v-model="stylename" maxlength="4" placeholder="输入一个名字" show-word-limit size="large"  @input="store_stat"/>
        </div>
        <div class="tw-mt-3">
          <div class="tw-tracking-wider tw-select-none tw-text-lg tw-mb-2 tw-font-light">字体</div>
          <el-input v-model="font" placeholder="从左侧选择" disabled  size="large" @input="store_stat"/>
        </div>
        <div class="tw-mt-3">
          
          <div class="tw-flex tw-flex-row">
            <div>
              <div class="tw-tracking-wider tw-select-none tw-text-lg tw-mb-2">字号</div>
              <el-input v-model="fontsize" placeholder="单位: px" type="number" @input="store_stat" :min="2"/>
            </div>
            <div  class="tw-ml-4">
              <div class="tw-tracking-wider tw-select-none tw-text-lg tw-mb-2">字间距</div>
            <el-input v-model="ltspacing" placeholder="单位: px" type="number" @input="store_stat"/>
            </div>
            <div  class="tw-ml-4">
              <div class="tw-tracking-wider tw-select-none tw-text-lg tw-mb-2">行间距</div>
            <el-input v-model="linespacing" placeholder="单位: px" type="number" @input="store_stat"/>
            </div>
          </div>
        </div>
        <div class="tw-flex tw-flex-row tw-mt-3">
          <div>
          <div class="tw-tracking-wider tw-select-none tw-text-lg tw-mb-2">颜色</div>
          <el-color-picker v-model="color1" />
          </div>
          <div class="" style="margin-left: 88px">
            <div class="tw-tracking-wider tw-select-none tw-text-lg tw-mb-2">字重</div>
            <el-radio-group v-model="weight" class="ml-4">
              <el-radio :label="200" size="large">中重</el-radio>
              <el-radio :label="400" size="large">大重</el-radio>
              <el-radio :label="700" size="large">超大重</el-radio>
            </el-radio-group>
          </div>
        </div>
        <div class="tw-flex tw-flex-row tw-mt-3">
          <div>
            <div class="tw-tracking-wider tw-select-none tw-text-lg tw-mb-2">有外边框</div>
            <el-switch
              v-model="outborder"
              class="mt-2"
              inline-prompt
            />
          </div>
          <div style="margin-left:46px">
            <div class="tw-tracking-wider tw-select-none tw-text-lg tw-mb-2">框颜色</div>
            <el-color-picker v-model="color2" :disabled="!outborder"/>
          </div>
          <div style="margin-left:64px">
            <div class="tw-tracking-wider tw-select-none tw-text-lg tw-mb-2">框粗细</div>
            <el-input v-model="outborderwidth" placeholder="单位: px" type="number" :disabled="!outborder"  style="width:110px" @input="store_stat" :min="1" :max="5"/>
          </div>
        </div>
        <div class="tw-mt-3">
          <div class="tw-tracking-wider tw-select-none tw-text-lg tw-mb-1">快速等比缩放</div>
          <el-slider v-model="scale1" :max="150" :format-tooltip="()=>scalerate.toFixed(2)+'x'" @input="scale_change"/>
        </div>
        <div ref="previewdiv" style="height: 328px" class="tw-overflow-hidden">
          <div class="tw-tracking-wider tw-select-none tw-text-lg tw-mb-1 tw-mt-5">预览</div>
          <div class="tw-w-full tw-h-full tw-flex tw-flex-row tw-items-start tw-flex-none">
            <el-slider v-model="displaytextbackground" vertical height="250px" class="tw-pb-16" :max="255" title="背景颜色"/>
          <div class="tw-flex tw-justify-center tw-items-center tw-flex-grow" :style="{'background-color': 'rgba('+displaytextbackground+','+displaytextbackground+','+displaytextbackground+',1)'}">
            <div class="text-display-v tw-select-none  minfont tt" :style="{'font-family': font+fonttail, 'font-size': fontsize+'px', 'font-weight': weight, 'letter-spacing': ltspacing+'px', 'line-height': lineheight+'px', 'color': color1, 'text-shadow': outborder?outborderstring:''}" v-html="demotext"> </div>
          </div>
          </div>
        </div>
        <div class="tw-mt-1 tw-flex tw-flex-row">
          <el-button type="primary" plain class="tw-w-full" @click="savefont">保存</el-button>
          <el-button type="warning" plain class="tw-flex-none tw-w-20" @click="resetfont">重设</el-button>
        </div> 
      </div>
    </div>
    <!-- 分割线 -->
    <div direction="vertical" class="tw-h-full" style="width:1px;background:#dcdfe6"/>
    <!-- 列表 -->
    <div class="tw-h-full tw-flex-grow tw-px-4 scroll-container" style="min-width:300px;max-width: calc(100vw - 880px);max-height: calc(100vh - 113px)">
      <el-table :data="mainStore.myStylesOrdered" style="width: 100%; ">
        <el-table-column prop="name" label="样式名"/>
        <el-table-column prop="font" label="字体"/>
        <el-table-column prop="fontsize" label="字号" width="55"/>
        <el-table-column prop="lns" label="行距" width="55"/>
        <el-table-column prop="color" label="颜色"  width="55">
          <template #default="scope">
            <div class="tw-w-5 tw-h-5 tw-rounded-full" :style="{'background': scope.row.color}"></div>
          </template>
        </el-table-column>
        <el-table-column prop="border" label="外框"  width="55">
          <template #default="scope">
            <el-icon v-if="scope.row.border"><Check /></el-icon>
            <el-icon v-if="!scope.row.border"><Close /></el-icon>
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="200">
          <template #default="scope">
            <el-button link type="primary" size="small" @click="edit(scope.row.name)"
              >编辑</el-button
            >
            <!-- 不知道为什么排序函数定义正反输出都是搞同样的下沉排序，索性干脆写下沉了 -->
            <el-button link type="info" size="small" @click="upup(scope.row.name)">下沉</el-button>
            <el-button link type="danger" size="small" style="color:#fff"  @click="deletefont(scope.row.name)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect, reactive, watch } from 'vue'
import { useMainStore } from '@/stores'
import { ElMessage } from 'element-plus' 
const mainStore = useMainStore();


let demotext = "这不是眼泪，<br>我不过是在用<br>双眼尿尿而已。<br>涙じゃない。<br>目から尿が出て<br>いるだけなんだ。"

let hasChinese = str => /[\u4E00-\u9FA5]+/g.test(str)

let localfonts = reactive({value: []})
let fontsnotloaded = ref(false)
let userloadfonts = () => {
  queryLocalFonts()
  .then(data => {
    let lst = Object.values(data);
    lst.sort((x, y) => {
      if (hasChinese(x.fullName) && !hasChinese(y.fullName)) {
        return -1
      } else if (!hasChinese(x.fullName) && hasChinese(y.fullName)) {
        return 1
      } else  {
        x.fullName>=y.fullName
      }
    })
    localfonts.value=lst
    fontsnotloaded.value =false
  })
  .catch((err)=>{
    fontsnotloaded.value = true
  })
}

let previewdiv = ref()
onMounted(() => {
  userloadfonts()
  previewdiv.value.addEventListener("wheel", (e)=>{
    e.preventDefault();
    let pbgc_step = 9
    console.log(displaytextbackground.value)
    if (e.deltaY >= 0) {
      displaytextbackground.value = Math.min(Math.max(Math.round(displaytextbackground.value - pbgc_step), 0),255)
    } else {
      displaytextbackground.value = Math.min(Math.max(Math.round(displaytextbackground.value + pbgc_step), 0),255)
    }
  })
})


let fonttail = ', 微软雅黑, 宋体, "Times New Roman"'
let font = ref("")
let stylename = ref("")
let fontsize = ref(28)
let ltspacing = ref()
let linespacing = ref(14)
let lineheight = computed(()=>parseInt(fontsize.value) + parseInt(linespacing.value))
let color1 = ref("#202020")
let color2 = ref("#ff0000")
let weight = ref(700)
let outborder = ref(false)
let outborderwidth = ref(3.6)
// let outborderstring = computed(() => outborderwidth.value+'px'+ " " + color2.value)
// -webkit-text-stroke实验性功能不支持图片边框内外选项，替代的方案
let outborderstring = computed(() => {
  let n = Math.ceil(2*Math.PI*outborderwidth.value) /* number of shadows */
  let str = ''
  for(let i=0;i<n;i++){
    /* append shadows in n evenly distributed directions */
    let theta = 2*Math.PI*i/n
    str += (outborderwidth.value*Math.cos(theta))+"px "+(outborderwidth.value*Math.sin(theta))+"px 0 "+color2.value+(i==n-1?"":",")
  }
  return str
})
let scale1 = ref(50)
let scalerate = computed(()=>(scale1.value-50)/100 + 1)

let nowstat = [28,0,1]
let displaytextbackground = ref(255)

let store_stat = () => {
  nowstat = [
    parseFloat(fontsize.value),
    parseFloat(ltspacing.value),
    Math.min(parseFloat(outborderwidth.value),5.0)
  ]
  scale1.value = 50;
}

let scale_change = (val) => {

  // 没有值的设置默认值
  if (font.value=="") { font.value="微软雅黑"}
  if (stylename.value=="") {stylename.value = font.value[0] + Math.round(Math.random()*899+100).toString()}
  if (nowstat[0] == NaN) { nowstat[0] = 28}
  if (nowstat[1] == NaN) { nowstat[1] = 0}
  if (nowstat[2] == NaN) { nowstat[2] = 1}
  
  fontsize.value = (nowstat[0] * scalerate.value).toFixed(1)
  ltspacing.value = (nowstat[1] * scalerate.value).toFixed(1)
  outborderwidth.value = Math.min((nowstat[2] * scalerate.value),5.0).toFixed(1)
}

let select_font = (font1) => {
  font.value = font1
}

let savefont = () => {
  // 没有值的设置默认值
  if (font.value=="") { font.value="微软雅黑"}
  if (stylename.value=="") {stylename.value = font.value[0] + Math.round(Math.random()*899+100).toString()}
  if (fontsize.value == undefined) { fontsize.value = 28}
  if (ltspacing.value == undefined) { ltspacing.value = 0}
  if (outborderwidth.value == undefined) { outborderwidth.value = 3.6}

  mainStore.updateStyle({
    name: stylename.value,
    font: font.value,
    fontsize: fontsize.value, 
    lts: ltspacing.value ,
    lns: linespacing.value ,
    color: color1.value ,
    weight: weight.value ,
    border: outborder.value ,
    borderw: Math.min(parseFloat(outborderwidth.value),5.0),
    borderc: color2.value,
    select: false,
  })
}
let resetfont = ()=> {
  font.value = ""
  stylename.value = ""
  fontsize.value = 28
  ltspacing.value=0
  linespacing.value=14
  color1.value = "#202020"
  color2.value = "#ff0000"
  weight.value = 700
  outborder.value = false
  outborderwidth.value = 3.6
  scale1.value = 50
  displaytextbackground.value = 255
}

let edit = (name) => {
  let cut1 = '1px'
  let tmp = mainStore.myStyles[name]
  font.value = tmp.font
  stylename.value = tmp.name,
  fontsize.value = tmp.fontsize,
  ltspacing.value = tmp.lts,
  linespacing.value = tmp.lns,
  color1.value = tmp.color,
  weight.value = tmp.weight,
  outborder.value = tmp.border 
  outborderwidth.value = tmp.borderw 
  color2.value = tmp.borderc
  scale1.value = 50
}

let upup = (name)=>{
  mainStore.upliftStyle(name)
}
let deletefont=(name)=>{
  let count = 0
  for (let [k,v] of Object.entries(mainStore.myStyles)) {
    count += 1;
  }
  if (count > 1) {
    mainStore.deleteStyle(name)
  } else {
    ElMessage({
      message: '至少需要有一个字体样式。',
      type: 'error',
    })
  }
}




</script>

<style scoped lang="scss">
  //.hide-scroll::-webkit-scrollbar {
  //  width: 0; 
  //  height: 0; 
  //}
  .lst-item {
    color: #777;
  }
  .lst-item:hover {
    background: #f5f7fa;
    color: #333;
  }
  .minfont {
    font-size: 30px
  }
  

  .indicate-cover {
    width:195px;
    max-height: calc(100vh - 114px);
    background:rgba(245,247,250,1);
    border-color:#dcdfe6;
    z-index:10;
  }

  .indicate-cover:hover {
    cursor: pointer;
  }

  .indicate-cover:active {
    background: rgba(240,242,245,1)
  }

  .loop-words {
    font-family:楷体;
    animation: 2s wordsLoopAnimation linear infinite normal;
  }

  @keyframes wordsLoopAnimation {
    0% {
      transform: scale(1);
      -webkit-transform: scale(1);
    }

    70% {
      transform: scale(1.05);
      -webkit-transform: scale(1.05);
    }

    90% {
      transform: scale(1.05);
      -webkit-transform: scale(1.05);
    }

    100% {
      transform: scale(1.0);
      -webkit-transform: scale(1.0);
    }
  }
</style>
