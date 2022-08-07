<template>
  <button class="animation-button tw-rounded-full" @mouseover="mouseover" @mouseleave="mouseleave" :style="{'background-color': 'var('+xcolor+')', 'box-shadow': shadows[icon]}">
    <div ref="rotateicon" class="tw-relative tw-flex tw-justify-center tw-items-center animation-button-icon" :style="{'color': xcolortext}">
      <el-icon v-if="!hasDropout" :size="xsize">
        <Setting v-if="icon=='setting'"/>
        <Plus v-if="icon=='plus'"/>
        <MagicStick v-if="icon=='magic'"/>
        <Download v-if="icon=='download'"/>
      </el-icon>
      <div v-if="hasDropout" class="tw-text-xl tw-select-none">
        {{mainStore.styleSolution==null?"":mainStore.styleSolution[0]}}
      </div>
    </div>
    <div v-show="show_label" class="tw-relative tw-flex tw-justify-center tw-items-center" style="height:58px;top:-60px;left:16px"><div class="tw-text-xl pat-text tw-tracking-wider tw-select-none" :style="{'opacity': show_label_delay?1:0, 'color': xcolortext}">{{label}}</div></div>
  </button>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect } from 'vue'
import { useMainStore } from '@/stores' 
const mainStore = useMainStore();

let shadows = {
  plus: '0 3px 12px 2px rgba(35, 218, 244, .4)',
  setting: '0 3px 12px 2px rgba(229, 55, 94, .4)',
  magic: '0 3px 12px 2px rgba(242, 190, 31, .55)',
}
const props = defineProps({
  label: String,
  icon: String,
  xcolor: String,
  xsize: Number,
  xcolortext: String,
  hasDropout: {
    type:Boolean,
    default: false,
  }
})
let rotateicon = ref()

let show_label = ref(false)
let show_label_delay = ref(false)
let show_label_ptr = null
let mouseover = ()=>{
  show_label.value = true
  rotateicon.value.style.transform = 'rotate(90deg)'
  if (show_label_ptr===null) {
    show_label_ptr = window.setTimeout(()=>{
      show_label_delay.value = true;
      show_label_ptr = null
    }, 150)
  }
}

let mouseleave = ()=>{
  rotateicon.value.style.transform = 'rotate(0deg)'
  show_label.value = false
  if (show_label_ptr!==null) {
    window.clearTimeout(show_label_ptr)
    show_label_ptr=null
    show_label_delay.value = false;
  } else {
    show_label_delay.value = false;
  }
}



</script>

<style scoped lang="scss">
  .animation-button {
    transition: .2s ease-in-out;
    width: 60px;
    height: 60px;
    //box-shadow:0 3px 12px 2px rgba(229, 55, 94, .4);
  }

  .animation-button:hover {
    width:150px;
  }

  .animation-button:active {
    transition: .05s ease-in-out;
    transform: scale(.96)
  }

  .animation-button-icon {
    transition: .2s ease-in-out;
    width: 60px;
    height: 60px;
  }

  //.animation-button-icon:hover {
  //  transform: rotate(90deg);
  //}

  .pat-text {
    transition: .14s ease-in-out;
  }
</style>
