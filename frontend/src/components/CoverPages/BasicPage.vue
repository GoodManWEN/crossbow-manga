<template>
  <div ref="winref" v-show="mainStore.windows[props.winname].show" class="tw-fixed tw-w-screen tw-h-screen tw-z-50 animate__animated animate__fadeInBottomLeft animate__faster tw-flex tw-flex-col" style="background-color:#F8F8F8">
    <div class="tw-flex tw-flex-none tw-h-12 tw-w-full tw-z-30 tw-items-center tw-select-none" style="background-color:#fcfcfc;box-shadow: 0 3px 16px 2px rgba(16, 16, 16, .05)">
      <div class="tw-h-full tw-flex tw-items-center tw-text-gray-800">
        <el-icon :size="props.lsize" class="tw-ml-4">
          <Setting v-if="props.winname=='settings'"/>
          <FolderOpened v-if="props.winname=='files'"/>
        </el-icon>
        <div class="tw-pl-3 tw-text-lg tw-tracking-widest tw-font-bold tw-text-gray-800"> {{title}} </div>
      </div>
      <div class="tw-flex-grow tw-h-full tw-flex tw-flex-row-reverse tw-items-center tw-select-none">
        <div class="tw-flex tw-flex-none tw-w-12 tw-h-full tw-justify-center tw-items-center tw-pl-1 close-button" @click="close_button_clicked">
          <img :src="getAssetsImages('b2.svg')" style="transform: scale(1.1)"/>
        </div>
      </div>
    </div>
    <div class="tw-flex-grow tw-w-full tw-flex ">
      <slot name="content"></slot>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect } from 'vue'
import { useMainStore } from '@/stores' 
const mainStore = useMainStore();

let getAssetsImages = (fileName) => {
  return new URL(`/src/assets/images/${fileName}`, import.meta.url).href;
}

const props = defineProps({
  winname: String,
  title: String,
  preclose: {
    type: Boolean,
    default: false
  },
  lsize: {
    type: Number,
    default: 30
  }
})

let winref = ref()

watchEffect(() => {
  try {
    if (props.preclose) {
      winref.value.classList.remove('animate__fadeInBottomLeft')
      winref.value.classList.add('animate__fadeOutBottomLeft')
    } else {
      winref.value.classList.add('animate__fadeInBottomLeft')
      winref.value.classList.remove('animate__fadeOutBottomLeft')
    }
  } catch {
    
  }
})

let close_button_clicked = () => {
  document.body.style.overflowY = ''
  mainStore.lockWindow(props.winname, true)
  mainStore.switchWindowPreclose(props.winname, true)
  window.setTimeout(() => {
    mainStore.activateWindow(props.winname, 'close')
    mainStore.switchWindowPreclose(props.winname, false)
    mainStore.lockWindow(props.winname, false)
  }, 350)
}


</script>

<style scoped lang="scss">
  .close-button {
    transition: .05s ease-in-out;
  }
  .close-button:hover {
    background-color: #F3F3F3;
  }
  .close-button:active {
    transform: scale(.97)
  }
</style>
