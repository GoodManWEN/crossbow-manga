<template>
  <div ref="textboxdiv" class="tw-absolute tw-z-20 box-color-pos" style="" @mousedown.native="mouse_down">
    <button class="tw-absolute tw-w-5 tw-h-5 tw-rounded-full tw-flex tw-justify-center tw-items-center box-post-close" style="right:-6px;top:-6px" @click="text_delete">
      <el-icon><Close /></el-icon>
    </button>
    <div class="tw-absolute tw-w-full tw-h-1.5 bottom-bar" style="bottom:0" @mousedown.native="mouse_down_resize"></div>
    <div ref="reltextdiv" class="text-display-v tw-text-3xl tw-px-3 tw-py-3" lang="zh-Hant" :style="{'font-family': textstyles.font+fonttail, 'font-size': textstyles.fontsize+'px', 'font-weight': textstyles.weight, 'letter-spacing': textstyles.lts+'px', 'line-height': (parseFloat(textstyles.fontsize)+parseFloat(textstyles.lns))+'px', 'color': textstyles.color, 'text-shadow': textstyles.border?textborderstring:0}"><div v-html="text_replaced"></div>
    <!-- <div ref="reltextdiv" class="text-display-v tw-text-3xl tw-px-3 tw-py-3" lang="zh-Hant" :style="{'font-family': textstyles.font+fonttail, 'font-size': textstyles.fontsize+'px', 'font-weight': textstyles.weight, 'letter-spacing': textstyles.lts+'px', 'line-height': (parseFloat(textstyles.fontsize)+parseFloat(textstyles.lns))+'px', 'color': textstyles.color, 'text-shadow': ''}" > -->
      <!-- {{textborderstring}} -->
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect } from 'vue'
import { useMainStore } from '@/stores' 
const mainStore = useMainStore();

const props = defineProps({
  img: String,
  text: {
    type: String,
    default: ''
  },
  fontstyle: String,
  tbid: String,
  translate_x: {
    type: Number,
    default: 0,
  } ,
  translate_y: {
    type: Number,
    default : 0,
  },
  divheight: {
    type: Number,
    default : 60,
  }
})

let text_replaced= computed(() => props.text.replace(/\n/g, '<br>'))
let text_delete = () => {
  mainStore.removeTextBox(props.img, props.tbid)
}

let borderw = ref(false)
let borderc = ref('#FF0000')
let fonttail = ', 微软雅黑, 宋体, "Times New Roman"'
let textstyles = computed(() => {
  if (mainStore.myStyles.hasOwnProperty(props.fontstyle)) {
    borderw.value = mainStore.myStyles[props.fontstyle].borderw
    borderc.value = mainStore.myStyles[props.fontstyle].borderc
    return mainStore.myStyles[props.fontstyle]
  } else {
    borderw.value = mainStore.myStyles[props.fontstyle].borderw
    borderc.value = mainStore.myStyles[props.fontstyle].borderc
    return mainStore.defaultTextStyle
  }
})

let textborderstring = computed(() => {
  let r = parseFloat(borderw.value)
  let n = Math.ceil(2*Math.PI*r) /* number of shadows */
  let str = ''
  for(let i=0;i<n;i++){
    // append shadows in n evenly distributed directions 
    let theta = 2*Math.PI*i/n
    str += (r*Math.cos(theta))+"px "+(r*Math.sin(theta))+"px 0 "+borderc.value+(i==n-1?"":",")
  }
  return str
})


let textsize = 20;
let textboxdiv = ref()
let reltextdiv = ref()
let textdirection = ref(0)
// let translate_x = 0;
// let translate_y = 0;

let allow_flag = false
onMounted(() => {
  allow_flag = true
  textboxdiv.value.style.setProperty("transform", "translate("+props.translate_x.toFixed(1)+"px,"+props.translate_y.toFixed(1)+"px)", "important");
  textboxdiv.value.style.setProperty("height", props.divheight.toFixed(1)+'px', "important");
})
watchEffect(() => {
  props.translate_x
  props.translate_y // 这里必须加这么两句，要不然不知道是因为反射签名还是啥原因它就不更新了
  if (!allow_flag) {
    return
  }
  textboxdiv.value.style.setProperty("transform", "translate("+props.translate_x.toFixed(1)+"px,"+props.translate_y.toFixed(1)+"px)", "important");
})

watchEffect(() => {
  props.divheight
  if (!allow_flag) {
    return
  }
  textboxdiv.value.style.setProperty("height", props.divheight.toFixed(1)+'px', "important");
})


// drag logic
// 文字框本身的位移能力
let mouse_down = (e) => {
  e.preventDefault();
  e.stopPropagation();
  if (e.button != 0) {return}
  let display_react = textboxdiv.value.getBoundingClientRect()
  let real_width_now = display_react.width
  let real_height_now = display_react.height
  let real_width_unscaled = real_width_now / mainStore.scaleRatio
  let real_height_unscaled = real_height_now / mainStore.scaleRatio
  let translate_x_lim_range = mainStore.imgWidthLimit - real_width_unscaled
  let translate_y_lim_range = mainStore.imgHeightLimit - real_height_unscaled
  let orn_mousedown = document.onmousedown
  
  let downX = e.clientX;
  let downY = e.clientY;
  let orn_translate_x = props.translate_x;
  let orn_translate_y = props.translate_y;
  let mouseMoveHandler = (e) => {
    let moveX = e.clientX - downX
    let moveY = e.clientY - downY
    moveX = moveX / mainStore.scaleRatio
    moveY = moveY / mainStore.scaleRatio
    let t_translate_x = Math.min(Math.max(moveX + orn_translate_x, 0), translate_x_lim_range)
    let t_translate_y = Math.min(Math.max(moveY + orn_translate_y, 0), translate_y_lim_range)
    mainStore.updateTextBoxPos(props.img, props.tbid, t_translate_x, t_translate_y)
    // watchEffect update
  }
  let mouseUpHandler = () => {
    document.onmousemove = null;
    document.onmouseup = null;
    document.onmousedown = orn_mousedown;
  }
  document.onmousemove = mouseMoveHandler;
  document.onmouseup = mouseUpHandler;
  document.onmousedown = ()=>{};
}

// 困高调整
let mouse_down_resize = (e) =>{
  e.preventDefault();
  e.stopPropagation();
  if (e.button != 0) {return}
  let display_react = textboxdiv.value.getBoundingClientRect()
  let real_height_now = display_react.height
  let real_height_unscaled = real_height_now / mainStore.scaleRatio
  let translate_y_lim_range = mainStore.imgHeightLimit - props.translate_y
  let orn_mousedown = document.onmousedown

  let downY = e.clientY;
  let mouseMoveHandler = (e) => {
    let moveY = e.clientY - downY
    moveY = moveY / mainStore.scaleRatio
    let new_height = real_height_unscaled + moveY
    new_height = Math.min(Math.max(new_height, textsize+2), translate_y_lim_range)
    mainStore.updateTextBoxHeight(props.img, props.tbid, new_height)
    // watch effect update
  }
  let mouseUpHandler = () => {
    document.onmousemove = null;
    document.onmouseup = null;
    document.onmousedown = orn_mousedown;
  }
  document.onmousemove = mouseMoveHandler;
  document.onmouseup = mouseUpHandler;
  document.onmousedown = ()=>{};
}

</script>

<style scoped lang="scss">



.box-color-pos {
  background-color:rgba(125,211,252,.05);
  transform: translate(0px, 0px)
}

.box-color-pos:hover {
  background-color:rgba(125,211,252,.55);
}

.bottom-bar:hover {
  cursor: n-resize;
  background-color: rgba(0,117,255,.4)
}
.bottom-bar:active {
  // cursor: n-resize; 无效
  // cursor: copy;
  // cursor: -webkit-grab; cursor: grab;
  // cursor: move;
  background-color: rgba(0,117,255,.4)
}

.box-post-close {
  background-color:rgba(125,211,252,.29);
}

.box-post-close:hover {
  background-color: rgba(0,117,255,.4)
}

.box-post-close:active {
  transition: .07s ease-in-out;
  transform: scale(0.98)
}
</style>
