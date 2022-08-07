<template>
  <slot name="btn"> </slot>
  <div ref="dropdowndiv" class="tw-rounded-xl tw-flex tw-flex-col tw-mb-2 tw-p-2 tw-flex-nowrap tw-overflow-hidden tw-max-h-screen dropdown-style" :class="{'fold-status': !props.expand}" :style="{'height': props.expand?mainStore.dropdownHeight+'px':'0', 'opacity':props.expand?1:0}"  @click="ddd" style="max-height: 400px">
    <el-scrollbar>
      <DropdownButton v-for="(item, i) in mainStore.myStyles" :id="i" :longname="item.name" :fontid="item.name" :selected="item.select"/>
    </el-scrollbar>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect } from 'vue'
import { useMainStore } from '@/stores' 
const mainStore = useMainStore();
import DropdownButton from "./DropdownButton.vue";

const props = defineProps({
  expand: {
    type: Boolean,
    default: false
  },
})

let dropdowndiv = ref()



let switch_display = (val) => {
  // console.log(val, mainStore.dropdownHeight)
}

watchEffect(() => {
  switch_display(props.expand)
})


</script>

<style scoped lang="scss">

.dropdown-style {
  width:150px;
  background-color: rgba(255,255,255,0.7);
  box-shadow:0 10px 20px rgb(64, 64, 64,.15);
  transition: .2s ease-in-out;
  backdrop-filter: blur(20px);
}

.fold-status {
  //height: 0;
}
</style>
