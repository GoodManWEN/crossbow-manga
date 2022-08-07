<template>
  <div class="tw-flex-none tw-h-12 tw-w-full tw-rounded-lg tw-overflow-hidden dropdown-button tw-select-none" :class="{'selected-status': props.selected}">
    <div class="tw-w-full tw-h-full tw-text-xl tw-flex tw-justify-center tw-items-center tw-font-light" style="white-space: nowrap; text-overflow: ellipsis; overflow: hidden" @click="fontswitch">
      {{longname}}
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect } from 'vue'
import { useMainStore } from '@/stores' 
const mainStore = useMainStore();
const props = defineProps({
  longname: String,
  fontid: String,
  selected: {
    type: Boolean,
    default: false,
  }
})

let fontswitch = () => {
  mainStore.switchStyle(props.fontid)
  // console.log(props.fontid)
}
</script>

<style scoped lang="scss">

.selected-status {
  color: rgba(55,55,55);
  background-color: rgba(77, 77, 77, .15);
}

.dropdown-button {
  transition: .1s ease-in-out;
  color: rgba(137, 140, 148);
}

.dropdown-button:hover {
  color: rgba(55,55,55);
  background-color: rgba(77, 77, 77, .15);
}
.dropdown-button:active {
  transition: .06s ease-in-out;
  transform: scale(.97);
}
</style>
