<template>
  <div class="tw-fixed tw-w-16 tw-h-screen tw-z-40 tw-rounded-bl-2xl right-nav" :style="{'padding-right': mainStore.sideBarExpanded?0:0}" @mouseover="mainStore.expandSideBar(true)" @mouseleave="mainStore.expandSideBar(false)" :class="{'tw-rounded-tl-2xl':!mainStore.sideBarExpanded, 'locked-width': mainStore.sideBarLocked}">
    <div class="tw-w-12 tw-h-12 tw-absolute tw-rounded-tl-xl tw-overflow-hidden xlock-btn tw-select-none" :style="{'opacity':mainStore.sideBarExpanded?1:0}" @click="switchSideBarLock"  title='锁定/解锁侧边栏'>
      <div class="tw-w-full tw-h-full tw-flex tw-justify-center tw-items-center">
        <el-icon class="tw-absolute lock-transition" :size="23" :style="{'opacity': mainStore.sideBarLocked?0:1}"><Unlock /></el-icon>
        <el-icon class="tw-absolute lock-transition" :size="23" :style="{'opacity': mainStore.sideBarLocked?1:0, 'color': 'var(--item-focus-col1)'}"><Lock /></el-icon>
      </div>
    </div>
    <div class="tw-w-12 tw-h-12 tw-absolute xcls-btn tw-flex tw-justify-center tw-items-center tw-rounded-bl-xl" :style="{'opacity':mainStore.sideBarExpanded?1:0}" @click="remove_all_clicked" title='清除所有语句'>
      <el-icon :size="22"><DeleteFilled /></el-icon>
    </div>
    <div class="tw-w-full tw-h-full tw-flex tw-flex-col tw-py-4 tw-pl-4 tw-flex-nowrap tw-overflow-scroll hide-scroll">
      <SideBarItem v-for="(item, i) in mainStore.mainStruct.hasOwnProperty(mainStore.currentImage)?mainStore.mainStruct[mainStore.currentImage].pouch:[]" :key="i" :first="i==0" :img="mainStore.currentImage" :id="item.id" :focus="item.focus" :category="item.category" :text="item.text" :removing="item.removing" :removingProtect="item.removingProtect" :carry="item.carry"/>
    </div>
  </div>
  <div id="audionode" class="tw-absolute" style="z-index:-5000;opacity:0;bottom:0right:0"></div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect } from 'vue'
import SideBarItem from "./SideBarItem.vue";
import { useMainStore } from '@/stores' 

const mainStore = useMainStore();
let switchSideBarLock = () => {
  mainStore.switchSideBarLock()
}
let remove_all_clicked = () => {
  let allids = Object.keys(mainStore.mainStruct.hasOwnProperty(mainStore.currentImage)?mainStore.mainStruct[mainStore.currentImage].pouch:[])
  for (let itemid in allids) {
    mainStore.delayRemove(mainStore.currentImage, itemid)
  }
}
</script>

<style scoped lang="scss">
  //#ED716B
  //#877069
  //#5B8184
  //#FCF5C7

  //#98EDC4
  //#25C1E8
  //#786C6D
  //#908F89
  //#AC9BBF
  //#8DF0B0
  //
  //
  //
  //
  //
  //
  //
  //
  .right-nav {
    //width: 480px;
    transition: 0.25s ease-in-out;
    backdrop-filter: blur(30px);
    right:0;
    background: var(--default-sidebar-background);
    box-shadow:0 0px 15px var(--default-shadow-color); 
  }


  .right-nav:hover {
    width: 480px;
  }
  .hide-scroll::-webkit-scrollbar {
    width: 0; 
    height: 0; 
  }
  .xlock-btn {
    top: 0px ;
    left: -48px;
    color:white;
    transition: 0.25s ease-in-out;
    background: rgba(77,77,77,1);
    box-shadow:0 0px 8px var(--default-shadow-color); 
  }
  .xlock-btn:hover {
    transition: 0.1s ease-in-out;
    background: rgba(99,99,99,1);
  }
  .xlock-btn:active {
    transition: 0.05s ease-in-out;
    transform: scale(0.96) translate(1px, -1px);
  }
  .lock-transition {
    transition: 0.15s ease-in-out;
  }
  .locked-width{
    width: 480px !important;
  }
  .xcls-btn {
    left:-48px;
    top:48px;
    color:white;
    background:#e5375e;
    box-shadow:-2px 4px 8px rgba(16,16,16,.3); 
    transition: 0.25s ease-in-out;
  }
  .xcls-btn:hover {
    transition: 0.1s ease-in-out;
    background: #ff567c;
  }
  .xcls-btn:active {
    transition: 0.05s ease-in-out;
    transform: scale(0.96) translate(1px, -1px);
  }
</style>
