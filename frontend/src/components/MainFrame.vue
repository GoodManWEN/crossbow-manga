<template>
  <div ref="maindiv" class="tw-absolute tw-min-h-screen tw-bg-gray-200 tw-overflow-hidden" style="min-width: 100vw">
    <div ref="bgdiv" class="tw-absolute custom-bg tw-w-ul tw-h-ul" style="opacity:0.7"></div>
    <div ref="framediv" class="tw-absolute" style="transform: translate(0px,0px)">
      <div id="cimg" ref="imgdiv" style="width:0;height:0" class="tw-absolute tw-bg-red-200 tw-m-12 tw-select-none" :class="{'custom-img': !right_active_flag, 'custom-img-right': right_active_flag}" @mousedown.native="mouse_down" @contextmenu="cm_clicked">
        <BasicText v-for="(item, i) in mainStore.mainStruct.hasOwnProperty(mainStore.currentImage)?mainStore.mainStruct[mainStore.currentImage].textBoxes:[]" :text="item.text" :tbid="item.id" :img="item.img" :fontstyle="item.style" :translate_x="item.translate_x" :translate_y="item.translate_y" :divheight="item.height"></BasicText>
        <div ref="rightseldiv" class="tw-absolute tw-bg-green-300" style="opacity:0.6"></div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect, watch } from 'vue'
import { useMainStore } from '@/stores' 
import BasicText from './TextBoxes/BasicText.vue'
const mainStore = useMainStore();
import { ElMessage } from 'element-plus'
import hotkeys from 'hotkeys-js';


let maindiv = ref()
let bgdiv = ref()
let framediv = ref()
let imgdiv = ref()
let rightseldiv = ref()
const orn_scale = 1
let current_scale = orn_scale;
let scale_step = 0.05
let scale_step2 = 0.04
let img_src = ref("")
let img_full_w = ref(0);
let img_full_h = ref(0);
let translate_x=0;
let translate_y=0


let keyboard_reset_lock = false
let mouse_reset_lock = false

let cm_clicked = (e) => {
  e.preventDefault()
}
let load_image = (src) => {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.addEventListener('load', () => resolve(img));
    img.addEventListener('error', () => reject(img));
    img.src = src;
  });
}

let refresh_bg_image = (src) => {
  load_image(src)
    .then((img) => {
      imgdiv.value.style.background = "url("+src+") no-repeat scroll left top transparent";
      [img_full_w.value, img_full_h.value] = [img.width, img.height];
      mainStore.updateImageSizeLimit(img.width, img.height)
      imgdiv.value.style.width = img.width+'px'
      imgdiv.value.style.height = img.height+'px'
      maindiv.value.style.width = (img.width + 100) + 'px'
      maindiv.value.style.height = (img.height + 100) + 'px'
    })
    .catch((img) => {
      imgdiv.value.style.background = "url('')";
      console.log('load image error')
      mainStore.updateImageSizeLimit(0, 0)
    });
}

let frame_reset = () => {
  console.log('main frame reset')
  translate_x = 0
  translate_y = 0
  current_scale = orn_scale
  mainStore.updateScaleRatio(current_scale)
  imgdiv.value.style.setProperty("transform-origin", 0+"px "+0+"px", "important");
  imgdiv.value.style.setProperty("transform", "matrix("+current_scale+", 0, 0, "+current_scale+", 0, 0)", "important");
  framediv.value.style.setProperty("transform", "translate("+translate_x+"px,"+translate_y+"px)", "important");
}

let get_new_image = (md5) => {
  img_src.value = "http://127.0.0.1:39921/img/"+ mainStore.currentImage +"?=" + new Date().getTime()
  refresh_bg_image(img_src.value)
}

let tmp_watch = ref('')

watch(tmp_watch, (new_val, old_val) => {
  if (new_val != "") {
    get_new_image(new_val)
    frame_reset()
  } else {
    refresh_bg_image("")
  }
})

watchEffect(() => {
  tmp_watch.value = mainStore.currentImage // 不知道为什么watch监听不到pinia的对象，需要中转一步才行
})

onMounted(() => {
  // 滚轮缩放相关逻辑
  imgdiv.value.addEventListener("wheel", (e)=>{
    e.preventDefault();

    let previous_scale = current_scale
    if (e.deltaY >= 0) {
      current_scale -= scale_step2
    } else {
      current_scale += scale_step
    }
    if (current_scale >= (orn_scale*2.0)) {
      current_scale = orn_scale*2.0;return
    } else if (current_scale <= (orn_scale*0.6)) {
      current_scale = orn_scale*0.6;return
    }
    mainStore.updateScaleRatio(current_scale)
    let current_scale_rounded = Math.round(current_scale * 1000.0)/1000.0
    maindiv.value.style.width = (img_full_w.value * current_scale).toFixed(1)+'px'
    maindiv.value.style.height = (img_full_h.value * current_scale).toFixed(1)+'px'

    imgdiv.value.style.setProperty("transform-origin", e.offsetX.toFixed(1)+"px "+e.offsetY.toFixed(1)+"px", "important");
    imgdiv.value.style.setProperty("transform", "matrix("+current_scale_rounded+", 0, 0, "+current_scale_rounded+", 0, 0)", "important");
  })
})


let left_prevent = false;
let right_active_flag = ref(false)
let click_times = 0
let click_timer = null
let dbclick_flag = false
let tmp_img_src = ""

// 识图相关网络请求
let smart_range_detect = (offsetX, offsetY) => {
  axios.post('http://127.0.0.1:39921/api/smart-range-detect', {
    offsetX: offsetX,
    offsetY: offsetY,
    imageMD5: mainStore.currentImage,
    wsUUID: mainStore.wsUUID
  })
  .then(res=>{
    if (res.status==200 && res.data.success==true) {
      ElMessage({
        message: '区域被正常识别！',
        type: 'success',
      })
      img_src.value = "http://127.0.0.1:39921/img/"+mainStore.currentImage+"?=" + new Date().getTime()
      // 重设原图显示相关内容
      if (dbclick_flag) {
        click_times = 0
        click_timer = null
        // dbclick_flag = false
        tmp_img_src = img_src.value
      }
      // 
      refresh_bg_image(img_src.value)
    }
  })
  .catch(err=>{
    ElMessage({
      message: '区域识别错误，检查区域是否正确！',
      type: 'warning',
    })
    console.log(err)
  })
}

let manual_range_detect = (offsetX, offsetY, moveX, moveY) => {
  axios.post('http://127.0.0.1:39921/api/manual-range-detect', {
    offsetX: offsetX,
    offsetY: offsetY,
    moveX: moveX,
    moveY: moveY,
    imageMD5: mainStore.currentImage,
    wsUUID: mainStore.wsUUID
  })
  .then(res=>{
    if (res.status==200 && res.data.success==true) {
      ElMessage({
        message: '区域被正常识别！',
        type: 'success',
      })
      img_src.value = "http://127.0.0.1:39921/img/"+mainStore.currentImage+"?=" + new Date().getTime()
      // 重设原图显示相关内容
      if (dbclick_flag) {
        click_times = 0
        click_timer = null
        // dbclick_flag = false
        tmp_img_src = img_src.value
      }
      // 
      refresh_bg_image(img_src.value)
    }
  })
  .catch(err=>{
    ElMessage({
      message: '区域识别错误，检查区域是否正确！',
      type: 'warning',
    })
    console.log(err)
  })
}


// mouse drag logic
let mouse_down = (e) => {
  let orn_mousedown = document.onmousedown
  if (e.button==0) {
    // left button
    if (left_prevent) {
      rightseldiv.value.style.width = '0px'
      rightseldiv.value.style.height = '0px'
      document.onmousemove = null;
      document.onmouseup = null;
      document.onmousedown = orn_mousedown;
      left_prevent = false;
      return
    }
    // 双击检索逻辑
    // 还原图片的逻辑有两个，鼠标双击与键盘R键执行的是相同操作。设置双锁之后，虽然没有详细检查逻辑，但使用上大体无冲，
    // 双方交错调用也不会保证各自功能正常。但是遇到一个问题是鼠标和R键同时狂点的话背景图频繁刷新过程中会出现加载失败的情况
    // 通常这种情况下原图会立即被归正，但是我注意到一次加载失败后整体拖动逻辑不太顺滑，虽然还能用但是长短按反过来了
    // 考虑到实际使用过程中双击查看原图的情况可能也比较少，干脆注释掉了。想启用的话把下面这段逻辑和mouseup部分的逻辑
    // 取消注释即可,与其他部分不冲突.
    // if (!dbclick_flag&&!keyboard_reset_lock) {
    //   mouse_reset_lock = true
    //   click_times += 1
    //   if (click_times===1) {
    //     click_timer = window.setTimeout(() => {
    //       click_times = 0
    //       click_timer = null
    //       dbclick_flag = false
    //       tmp_img_src = ""
    //     }, 250)
    //   } else {
    //     window.clearTimeout(click_timer)
    //     click_times = 0
    //     click_timer = null
    //     dbclick_flag = true
    //     // 发送查看原图请求。
    //     tmp_img_src = img_src.value
    //     refresh_bg_image("http://127.0.0.1:39921/img-src/"+mainStore.currentImage)
    //   }
    // }
    
    // 移动逻辑
    let downX = e.clientX;
    let downY = e.clientY;
    let orn_translate_x = translate_x;
    let orn_translate_y = translate_y
    let mouseMoveHandler = (e) => {
      let moveX = e.clientX - downX
      let moveY = e.clientY - downY
      translate_x = moveX + orn_translate_x
      translate_y = moveY + orn_translate_y
      framediv.value.style.setProperty("transform", "translate("+translate_x+"px,"+translate_y+"px)", "important");
    }
    let mouseUpHandler = () => {
      document.onmousemove = null;
      document.onmouseup = null;
      document.onmousedown = orn_mousedown;
      // if (dbclick_flag) {
      //   // 还原图片
      //   if (!keyboard_reset_lock) {
      //     refresh_bg_image(tmp_img_src)
      //     click_times = 0
      //     click_timer = null
      //     tmp_img_src = ""
      //     dbclick_flag = false
      //     mouse_reset_lock=false
      //   }
      // }
    }
    document.onmousemove = mouseMoveHandler;
    document.onmouseup = mouseUpHandler;
    document.onmousedown = ()=>{};
  } else if (e.button == 2) {
    // right button
    // 左键双击交互过程中禁用右键功能
    if (dbclick_flag) {return}
    //
    right_active_flag.value = true
    left_prevent = true
    let downX = e.offsetX;
    let downY = e.offsetY;
    downX = Math.min(Math.max(downX, 0), img_full_w.value);
    downY = Math.min(Math.max(downY, 0), img_full_h.value);
    rightseldiv.value.style.left = downX + 'px'
    rightseldiv.value.style.top = downY + 'px'
    rightseldiv.value.style.width = '0px'
    rightseldiv.value.style.height = '0px'
    let moveX = 0 
    let moveY = 0
    let mouseMoveHandler = (e) => {
      moveX = Math.max(e.offsetX - downX, moveX)
      moveY = Math.max(e.offsetY - downY, moveY)
      rightseldiv.value.style.width = moveX + 'px'
      rightseldiv.value.style.height = moveY + 'px'
    }
    let mouseUpHandler = () => {
      right_active_flag.value = false
      rightseldiv.value.style.width = '0px'
      rightseldiv.value.style.height = '0px'
      document.onmousemove = null;
      document.onmouseup = null;
      document.onmousedown = orn_mousedown;
      left_prevent = false;
      if ((-5 <= moveX && moveX <= 10) && (-5 <= moveY && moveY <= 10)) {
        smart_range_detect(downX, downY)
      } else if (moveX < 0 || moveY < 0 || downX < 0 || downY < 0) {
        ElMessage({
          message: '区域框选有抖动，再试一次!',
          type: 'warning',
        })
      } else {
        manual_range_detect(downX, downY, moveX, moveY)
      }
      mainStore.updateLastRequestPos(downX+moveX, downY+moveY)
    }
    document.onmousemove = mouseMoveHandler;
    document.onmouseup = mouseUpHandler;
    document.onmousedown = ()=>{};
  }
}


// 捕获键盘的逻辑
hotkeys('ctrl+z,ctrl+y,ctrl+s', function (event, handler){
  switch (handler.key) {
    case 'ctrl+z': console.log('you pressed ctrl+z!');
      break;
    case 'ctrl+y': console.log('you pressed ctrl+y!');
      break;
    case 'ctrl+s': console.log('you pressed ctrl+s!');
      break;
    default: () => {}
  }
});

hotkeys('r', {keyup: true, keydown: true}, function(event, handler) {
  if (event.type === 'keydown') {
    if (mouse_reset_lock) return {}
    keyboard_reset_lock = true
    click_times = 0
    click_timer = null
    dbclick_flag = true
    // 发送查看原图请求。
    tmp_img_src = img_src.value
    refresh_bg_image("http://127.0.0.1:39921/img-src/"+mainStore.currentImage)
  }

  if (event.type === 'keyup') {

    if (mouse_reset_lock) return {}
    keyboard_reset_lock = false
    refresh_bg_image(tmp_img_src)
    click_times = 0
    click_timer = null
    tmp_img_src = ""
    dbclick_flag = false
  }
});


</script>

<style scoped lang="scss">
  $bg-url: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAIAAACRXR/mAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAABnSURBVHja7M5RDYAwDEXRDgmvEocnlrQS2SwUFST9uEfBGWs9c97nbGtDcquqiKhOImLs/UpuzVzWEi1atGjRokWLFi1atGjRokWLFi1atGjRokWLFi1af7Ukz8xWp8z8AAAA//8DAJ4LoEAAlL1nAAAAAElFTkSuQmCC";
  $bg-orn-size: 50px;


  .custom-bg {
    background: url($bg-url) repeat 0 0;
    transform-origin: top left;
    transform: scale(0.8,);
  }

  .custom-img:active {
    cursor: -webkit-grab; cursor: grab;
  }

  .custom-img-right:active {
    cursor: copy;
  }

  .test-class {
    //margin-top:100px;
   // margin-left: 100px;
    //background: url($bg-url) repeat 0 0;
    background-position: 50% 50%;
    background-image: url(http://127.0.0.1:39921/img.jpg);
    background-repeat:no-repeat;
    width: 500px;
    height: 500px;
    overflow: none;
    //transform-origin: 0px 0px;
    //transform: matrix(1.1, 0, 0, 1.1, 0, 0);
    //transform: translate(-20%, -20%)
  }
</style>
