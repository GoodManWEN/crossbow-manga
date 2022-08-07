<template>
  <div ref="itemself" class="tw-flex-none tw-w-full tw-overflow-hidden tw-flex animate__animated animate__faster " :style="{'margin-top': first?'0':'16px'}" :class="{'animate__fadeInUpBig': !props.removing && !already_exists, 'animate__fadeOutRightBig': props.removing}">
    <div :class="{'tw-select-none': true, 'item-custom-style-minimized': !mainStore.sideBarExpanded, 'item-custom-style': mainStore.sideBarExpanded, 'item-custom-style-none-focus': !focus, 'item-custom-style-focus': focus, 'item-custom-style-color-src': focus && category=='src', 'item-custom-style-color-dst': focus && category=='dst', 'tw-py-5':mainStore.sideBarExpanded, 'tw-px-8': mainStore.sideBarExpanded,'tw-py-1':!mainStore.sideBarExpanded, 'tw-px-2': !mainStore.sideBarExpanded,  'tw-w-full': true, 'tw-h-full': true}" @mouseover="mouse_hover" @mouseleave="mouse_leave">
      <!-- 折叠显示逻辑 -->
      <div class="tw-flex" v-show="!mainStore.sideBarExpandedDone" >
        <span 
          class="tw-text-2xl tw-tracking-wider tw-font-semibold tw-flex-none"
          :style="{'color': focus?category=='dst'?'var(--focus-text-color-item1)':'var(--focus-text-color-item2)':category=='dst'?'var(--item-focus-col1)':'var(--item-focus-col2)'}"
        > {{ category=='dst'?'Tr':'Or'}} </span>
      </div>
      <!-- 以下都是展开显示逻辑 -->
      <div class="tw-flex" v-show="mainStore.sideBarExpandedDone" >
        <span 
          class="tw-text-2xl tw-tracking-wider tw-font-semibold tw-flex-none"
          :style="{'color': focus?category=='dst'?'var(--focus-text-color-item1)':'var(--focus-text-color-item2)':category=='dst'?'var(--item-focus-col1)':'var(--item-focus-col2)'}"
        > {{ category=='dst'?'Translated':'Original'}} </span>
        <div class="tw-w-12 tw-h-5 tw-p-1 tw-mt-2 tw-ml-1 tw-rounded-md tw-flex tw-justify-center tw-items-center" style="font-family: 微软雅黑;color:#222" :style="{'background-color':carry.translatorColor}"> {{carry.translator}} </div>
        <div v-show="mainStore.sideBarExpandedDone" class="tw-flex tw-flex-row-reverse tw-flex-grow">
          <el-button :type="focus?null:'info'" circle class="tw-ml-4" @click="remove_clicked" title="删除该条目">
            <el-icon><Delete /></el-icon>
          </el-button>
          <el-button v-if="category=='dst'" :type="focus?null:'info'" circle @click="append_text"  title="添加到工作区">
            <el-icon style="transform: rotateY(180deg)"><Promotion /></el-icon>
          </el-button>
          <el-button v-if="category=='src'" :type="focus?null:'info'" circle @click="request_retranslate"  title="重新翻译">
            <el-icon><Refresh /></el-icon>
          </el-button>
          <el-button v-if="category=='src'" :type="focus?null:'info'" circle @click="read_source"  class="tw-mr-1.5"  title="朗读">
            <el-icon><Phone /></el-icon>
          </el-button>
        </div>
      </div>
      
      <hr 
        v-show="mainStore.sideBarExpandedDone" 
        class="tw-mb-2 tw-mt-4"
        :style="{'height': '1px','background-color':focus?category=='dst'?'var(--focus-text-color-item1)':'var(--focus-text-color-item2)':'var(--focus-text-color-item2)','color':focus?category=='dst'?'var(--focus-text-color-item1)':'var(--focus-text-color-item2)':'var(--focus-text-color-item2)','border': '0 none'}"
      >
      <!-- v-if="display_or_input||props.category=='dst'" -->
      <span 
        v-if="display_or_input"
        v-show="mainStore.sideBarExpandedDone" 
        class="tw-text-xl item-text-style tw-tracking-wider"
        :class="{'tw-font-light': !focus, 'tw-font-semibold': focus, 'tw-select-text': props.category=='src'}" 
        :style="{'color': focus&&category=='dst'?'var(--focus-text-color-item1)':'var(--focus-text-color-item2)'}" 
        @click="handle_clicks"
        v-html="render_text"
      ></span>
      <!-- <div v-if="display_or_input&&props.category=='src'" class="tw-w-full tw-h-full tw-flex tw-flex-row tw-flex-wrap"> -->
        
      <!-- </div> -->
      <el-input
        ref="elinput"
        v-if="!display_or_input"
        v-model="textarea_input"
        type="textarea"
        :rows="textarea_rows"
        :input-style="{'font-size': '1.25rem', 'font-weight': 600, 'line-height': '1.75rem', 'letter-spacing': '0.05em', 'background-color': category=='dst'?'var(--item-focus-col1)':'var(--item-focus-col2)', 'color': category=='dst'?'var(--focus-text-color-item1)':'var(--focus-text-color-item2)', 'padding':'0', 'border': 'none'}"
        @blur="textarea_blur"
        @input="update_text"
      />

      <hr 
        v-if="category=='src' && showdict"
        v-show="mainStore.sideBarExpandedDone"
        class="tw-my-2"
        style="height: 1px; background-color: var(--focus-text-color-item2); color: var(--focus-text-color-item2); border: 0 none"
      >
      <div 
        v-if="category=='src' && showdict"
        v-show="mainStore.sideBarExpandedDone"
        class="tw-w-full tw-mb-2"
      >
        <div v-if="carry.loading" class="tw-w-full tw-h-full tw-flex tw-items-center" style="min-height: 40px">
          <SrcReqLoading />
        </div>
        <div v-if="!carry.loading" class="tw-w-full" style="color:var(--focus-text-color-item2)" v-html="carry.dicthtml">
        </div>
      </div>
      
      <span v-if="display_or_input&&!showdict">&nbsp;</span>
    </div>
    <div class="tw-w-3 item-label-style" :style="{'opacity': focus?1:0, 'height': mainStore.sideBarExpanded?'100%':'40px', 'background': category=='dst'?'var(--item-focus-lba-col1)':'var(--item-focus-lba-col2)'}"></div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect, toRefs } from 'vue'
import { useMainStore } from '@/stores' 
const mainStore = useMainStore();
import { ElMessage } from 'element-plus'
import SrcReqLoading from './SrcReqLoading.vue'

const props = defineProps({
  first: Boolean,
  img: String,
  id: String,
  focus: {
    type: Boolean,
    default: false
  },
  category: String,
  text: String,
  carry: Object,
  removing: {
    type: Boolean,
    default: false
  },
  removingProtect: {
    type: Boolean,
    default: false
  },
})

let already_exists = ref(false)
window.setTimeout(() => {
  already_exists.value = true
}, 500)
let itemself = ref()
let render_text = computed(() => {return props.text.replace(/\n/g, '<br>')})

let display_or_input = ref(true)

let textarea_input = ref(props.text)

watchEffect(() => {
  textarea_input.value = props.text
})

let showdict = computed(()=>{
  if (props.category == 'dst') {
    return false
  } else {
    if (props.carry?.loading==true || (props.carry?.dicthtml != undefined && props.carry?.dicthtml != "")) {
      return true
    } else {
      return false
    }
  }
})

let textarea_rows = computed(()=>Math.ceil(textarea_input.value.length / 18.0))

let textarea_focus = ()=>{
  display_or_input.value = false
}
let textarea_blur = () =>{
  display_or_input.value = true
}

let mouse_hover = (e) => {
  mainStore.switchFocus(mainStore.currentImage, props.id, true)
}
let mouse_leave = (e) => {
  mainStore.switchFocus(mainStore.currentImage, props.id, false)
  textarea_blur()
}

let remove_lock = false // you can only remove once
let update_text = () => {
  let delete_flag = mainStore.updatePouchText(mainStore.currentImage, props.id, textarea_input.value)
  if (props.category == 'dst') {
    if (delete_flag.remove) {
      textarea_blur()
      remove_lock = true
      window.setTimeout(() => {
        remove_lock = false
      }, 500)
    }
  } else if (props.category=='src') {
    // textarea_blur()
    textarea_input.value = textarea_input.value.replace(/\n/g, '')
  }
}

let remove_clicked = () => {
  mainStore.delayRemove(props.img, props.id)
  textarea_blur()
}

let request_word_translate = (word) => {
  mainStore.requestWordTranslate(mainStore.currentImage, props.id)
  axios.post("http://127.0.0.1:39921/api/request-word-translate", {
    word: word,
    wsUUID: mainStore.wsUUID,
    imageMD5: mainStore.currentImage,
    iid: props.id,
  })
  .then(() => {})
  .catch((err) => {console.log(err)})
} 

// handle click & double click
let clicks = 0
let timer = null
let dd = null
let handle_clicks = () => {
  clicks += 1;
  if (clicks===1) {
    timer = window.setTimeout(() => {
      console.log('clicked')
      let select_string = window.getSelection().toString()
      if (props.category == 'src' && select_string != ""){
        request_word_translate(select_string)
      }
      clicks=0
      timer=null
    }, 220)
  } else {
    window.clearTimeout(timer)
    textarea_focus()
    clicks=0
    timer=null
  }
}

let append_text = () => {
  if (mainStore.styleSolution == null) {
    ElMessage({
      message: '请先选择一种字体样式。',
      type: 'warning'
    })
    return
  }
  mainStore.appendTextBox(props.img, textarea_input.value, mainStore.styleSolution)
}

let read_source = () => {
  axios.get('http://127.0.0.1:39921/api/tts-read',{
    params: {
      text: props.text
    },
    responseType: 'blob'
  })
    .then(res=>{
      let audio = document.createElement("audio");
      let tree_node = document.getElementById('audionode')
      tree_node.appendChild(audio);
      const reader = new FileReader();
      reader.onload = (e) => {
          const srcUrl = e.target.result;
          audio.src = srcUrl;
      };
      reader.readAsDataURL(res.data); //blob
      audio.addEventListener("ended", (e)=>{
        audio.remove()
      })
      audio.play()
    })
}

let request_retranslate = () => {
  axios.post('http://127.0.0.1:39921/api/request-retranslate',{
    text: props.text,
    wsUUID: mainStore.wsUUID,
    imageMD5: mainStore.currentImage
  })
  .then(()=>{
    ElMessage({
      message: '重新翻译请求发送成功。',
    })
  })
  .catch(err=>console.log(err))
}

</script>

<style scoped lang="scss">

  .item-custom-style {
    background: var(--default-item-unfocus);
    transition: 0.15s ease-in-out;
    border-top-left-radius: 0.75rem;
    border-bottom-left-radius: 0.75rem;
  }
  .item-custom-style-focus {
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
  }
  .item-custom-style-color-src {
    background: var(--item-focus-col2) !important;
  }
  .item-custom-style-color-dst {
    background: var(--item-focus-col1) !important;
  }
  .item-custom-style-none-focus {
    border-top-right-radius: 0.75rem;
    border-bottom-right-radius: 0.75rem;
  }
  .item-custom-style-minimized {
    height: 40px;
    transition: 0.15s ease-in-out;
    background: var(--default-item-unfocus);
    border-top-left-radius: 0.75rem;
    border-bottom-left-radius: 0.75rem;
  }
  .item-label-style {
    transition: 0.15s ease-in-out;
  }

  .item-text-style {
    color: var(--default-text-color);
  }

  .el-textarea{
    background-color: #333;
  }
</style>
