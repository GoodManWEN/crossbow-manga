<template>
  <div v-if="props.idx!=0" class="tw-h-0.5"></div>
  <div class="tw-flex-none tw-h-12 tw-w-full tw-rounded-xl tw-flex tw-items-center tw-px-6 sb-unselected tw-select-none sb-active-amime" :class="{'sb-selected':props.focus}" @click="switchSettingFocus"> 
    <el-icon v-if="props.icon=='avatar'" :size="24" class="tw-flex-none"><Avatar /></el-icon>
    <el-icon v-if="props.icon=='star'" :size="24" class="tw-flex-none"><Star /></el-icon>
    <div class="tw-flex-grow tw-flex tw-items-center tw-pl-3 tw-text-lg tw-tracking-wider tw-font-normal"> {{label}} </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect } from 'vue'
import { useMainStore } from '@/stores' 
const mainStore = useMainStore();

const props = defineProps({
  label: String,
  icon: String,
  focus: {
    type: Boolean,
    default: false,
  },
  idx: Number,
})


let switchSettingFocus = () => {
  mainStore.switchSettingFocus(props.idx)
}

</script>

<style scoped lang="scss">
  .sb-unselected {
    color: var(--page-text-color1);
  }
  .sb-unselected:hover {
    background: rgba(227,227,227,1)
  }
  .sb-active-amime:active {
    transition: .07s ease-in-out;
    transform: scale(0.98)
  }
  .sb-selected {
    background: rgba(0,129,255,1) !important;
    color: #fff !important;
  }
  .sb-selected:hover {
    background: rgba(50,150,244,1) !important;
  }
</style>
