<template>
  <div class="tw-fixed tw-flex tw-flex-col-reverse tw-z-30" style="left:30px;bottom: 30px">
    <HoverButtonsButton :label="'设置选项'" :icon="'setting'" :xcolor="'--btn-bg-color1'" :xsize="30" xcolortext="#F7F8F9" @click="settings_clicked"/>
    <div class="tw-h-4"></div>
    <HoverButtonsButton :label="'文件列表'" :icon="'plus'" :xcolor="'--btn-bg-color3'" :xsize="26" xcolortext="#fff" @click="files_clicked"/>
    <div class="tw-h-4"></div>
    <HoverButtonsButton :label="'导出图片'" :icon="'download'" :xcolor="'--btn-bg-color4'" :xsize="26" xcolortext="#fff" @click="export_img"/>
    <div class="tw-h-4"></div>
    <div class="tw-flex tw-flex-col-reverse" @mouseover="dropdown_mouseover" @mouseleave="dropdown_mouseleave">
      <Dropdown :expand="dropdown_expand">
        <template #btn>
          <HoverButtonsButton :label="'选择样式'" :icon="'magic'" :xcolor="'--btn-bg-color2'" :xsize="26" xcolortext="#444" :hasDropout="mainStore.styleSolution==null?false:true"/>
        </template>
      </Dropdown>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect } from 'vue'
import { useMainStore } from '@/stores' 
const mainStore = useMainStore();
import HoverButtonsButton from "./HoverButtonsButton.vue";
import Dropdown from "./Dropdown.vue";
import { ElMessage } from 'element-plus'
import html2canvas from "html2canvas"

let settings_clicked = () => {
  mainStore.activateWindow('settings', 'open')
  // axios.post('http://127.0.0.1:39921/test/reset')
  // .then(()=>{})
}
let files_clicked = () => {
  mainStore.activateWindow('files', 'open')
}

let dropdown_expand = ref(false)

let dropdown_mouseover = () => {
  dropdown_expand.value = true
}

let dropdown_mouseleave = () => {
  dropdown_expand.value = false
}

let export_img = () => {
  if (mainStore.currentImage.length>0) {
    html2canvas(document.getElementById("cimg"))
    .then(canvas => {
      canvas.toBlob((blob) => {
        saveAs(blob, mainStore.searchImgRealFileName(mainStore.currentImage) + '.png')
      })
    })
  } else {
    ElMessage({
      message: '当前画布为空。',
      type: 'warning'
    })
  }
}

</script>

<style scoped lang="scss">
</style>
