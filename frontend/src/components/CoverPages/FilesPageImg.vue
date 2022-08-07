<template>
  <div style="width: 200px; height: 250px;" class="tw-flex tw-justify-center tw-items-center tw-select-none img-thumb tw-m-5 tw-flex-col" @click="img_clicked">
    <div>
      <div class="tw-relative tw-w-5 tw-h-5 tw-rounded-full img-thumb-close tw-flex tw-justify-center tw-items-center" @click.stop="img_close" style="top:14px;left: -6px;">
        <el-icon class="tw-text-gray-50" :size="10"><CloseBold /></el-icon>
      </div>
      <div class="img-thumb-rect">
        <img :src="img_src" style="max-width: 200px; max-height: 240px;"/>
      </div>
    </div>
    <div class="tw-w-full tw-flex tw-justify-center tw-items-center" style="opacity:2!important;max-width: 200px;">
      <div class="tw-overflow-hidden tw-whitespace-nowrap tw-text-ellipsis">
        {{imgStat.realName}}
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect } from 'vue'
import { useMainStore } from '@/stores' 
import { UploadFilled } from '@element-plus/icons-vue'

const mainStore = useMainStore();

const props = defineProps({
  imgStat: Object
})

let img_src = computed(() => 'http://127.0.0.1:39921/img-thumb/'+props.imgStat.img)

let img_close = (e) => {
  axios.post('http://127.0.0.1:39921/api/remove-img', {'md5': props.imgStat.img})
  if (props.imgStat.img==mainStore.currentImage){
    mainStore.switchMainFrameImg("")
  }
}

let img_clicked = () => {
  mainStore.lockWindow('files', true)
  mainStore.switchWindowPreclose('files', true)
  mainStore.switchMainFrameImg(props.imgStat.img)
  window.setTimeout(() => {
    mainStore.activateWindow('files', 'close')
    mainStore.switchWindowPreclose('files', false)
    mainStore.lockWindow('files', false)
  }, 350)
}

</script>

<style scoped lang="scss">
  .img-thumb {
    opacity: 0.75;
    .img-thumb-rect {
      transition: .1s ease-in-out;
      box-sizing: content-box;
      border-style: solid;
      border-width: 1.5px;
      border-color: rgba(64,158,255,0);
    }
    
    .img-thumb-close {
      opacity:0;
      background:rgba(99,99,99,1);
    }
  }
  .img-thumb:hover {
    .img-thumb-close {
      opacity: 1;
    }
    .img-thumb-rect {
      border-color: rgba(64,158,255,1);
    }
    opacity: 1;
  }
  .img-thumb:active {
    .img-thumb-rect {
      transition: .05s ease-in-out;
      border-width: 3px;
    }
  }
  .img-thumb-close:hover {
    background: rgba(66,66,66,1)
  }
  .img-thumb-close:active {
    transition: .05s ease-in-out;
    tramsform: scale(0.96)
  }
</style>
