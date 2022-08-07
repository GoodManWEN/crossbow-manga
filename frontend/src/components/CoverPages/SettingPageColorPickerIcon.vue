<template>
  <div class="color-icon-class" :style="{'background': props.background, 'width':props.width+'px', 'height':props.height+'px'}">
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect } from 'vue'
import { useMainStore } from '@/stores' 
const mainStore = useMainStore();

const props = defineProps({
  background: String,
  width: {
    type: Number, 
    default: 20
  },
  height: {
    type: Number, 
    default: 20
  }
})
</script>

<style scoped lang="scss">
  .color-icon-class:hover {
    box-shadow:0 0 6px rgba(0,0,0,1); 
    z-index: 1;
  }

</style>
