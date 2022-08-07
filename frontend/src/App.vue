<template>
  <KomiLoading />
  <SideBar v-if="backend_ready"/>
  <FontPanel v-if="backend_ready" />
  <HoverButtons v-if="backend_ready" />
  <SettingPage v-if="backend_ready" />
  <FilesPage  v-if="backend_ready"/>
  <MainFrame  v-if="backend_ready"/>
  <!-- ws模块负责检测活性，始终挂载 -->
  <GlobalWebSocket  />
  <div class="tw-fixed tw-w-screen tw-h-screen" style="z-index:-10;background:#F7F8F9"></div>
</template>

<script setup>
import MainFrame from "./components/MainFrame.vue";
import HoverButtons from "./components/HoverButtons/HoverButtons.vue";
import SideBar from "./components/SideBar/SideBar.vue";
import FontPanel from "./components/FontPanel/FontPanel.vue";
import SettingPage from "./components/CoverPages/SettingPage.vue";
import FilesPage from "./components/CoverPages/FilesPage.vue";
import TestBasic from "./components/Tests/TestBasic.vue";
import GlobalWebSocket from "./components/GlobalWebSocket.vue";
import KomiLoading from "./components/LoadingPage/KomiLoading.vue";

import { ref, onMounted, computed, watchEffect } from 'vue'
import { useMainStore } from '@/stores' 
const mainStore = useMainStore();

let backend_ready = ref(false)

watchEffect(() => {
  if (mainStore.ready === null) {
  } else if (!mainStore.ready) {
    backend_ready.value = false
  } else {
    backend_ready.value = true
  }
})

</script>

<style lang="scss">
  :root{
    --default-shadow-color: rgba(16,16,16,.6);
    --default-sidebar-background: rgba(0,0,0,.71);
    //--default-sidebar-background: #2A2B3D;
    --default-sidebar-background: rgba(4, 1, 23, .82);
    --default-text-color: #fefefe;
    //--default-item-unfocus: rgba(91, 91, 91, .9);
    //--default-item-unfocus: rgba(48, 50, 74, .88);
    --default-item-unfocus: #34364B;
    //--item-focus-col1: rgba(116, 235, 159, .9);
    --item-focus-col1: #A3DE45;
    //--item-focus-col1: rgba(116, 235, 159, .9);
    --item-focus-lba-col1: #DBF20C;
    --item-focus-col2: rgba(32, 191, 233, .9);
    --item-focus-lba-col2: #00A0FF;
    --focus-text-color-item1: #494949;
    --focus-text-color-item2: #fefefe;
    --focus-text-color-item3: #FC7999;
    --focus-text-color-item4: #FC9816;

    --icon-color1: #dc3545;
    --icon-color1: rgba(248, 62, 136, .95);

    --btn-bg-color1: #E5375E;
    --btn-bg-color2: #FF7260;
    --btn-bg-color2: #FFDC74;
    --btn-bg-color3: #26c9f4;
    --btn-bg-color4: #8C285A;
    --btn-bg-color4: #FFE1E0;
    --btn-bg-color4: #574347;
    --btn-bg-color4: #F25D4A;
    --btn-bg-color4: #F0D8C0;
    --btn-bg-color4: #F4E6D0;
    --btn-bg-color4: #FF8552;
    --btn-bg-color4: #553AAB;


    --page-text-color1: rgba(66,77,104,1);
  }

  body {
    //overflow-y: hidden; /* Hide vertical scrollbar */
    overflow-x: hidden; /* Hide horizontal scrollbar */
  }
  body::-webkit-scrollbar {
    width: 10px;
    height: 10px;
  }
  body::-webkit-scrollbar-thumb {
      border-radius: 10px;
      background-color: rgba(77,77,77,.5);
      
  }
  body::-webkit-scrollbar-track {
            background-color: #f7f8f9;
        }
  :lang(zh-Hant) { font-family: Verdana, Arial, Helvetica, sans-serif, times, Heiti TC, PMingLiU, PMingLiu-ExtB, SimSun, SimSun-ExtB, HanaMinA, HanaMinB; }

  /*
  textarea::-webkit-scrollbar {
    width: 1em;
  }

  textarea::-webkit-scrollbar-track {
      -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
  }

  textarea::-webkit-scrollbar-thumb {
    background-color: darkgrey;
    outline: 1px solid slategrey;
  }
  #DBC046
  #F7F793
  #F1D38B
  #F1D38B
  #F5FC86
  #685C4E
  */

  .text-display-v {
    writing-mode: vertical-rl;
    text-orientation: upright;
  }

  .scroll-container {
    height: 100%;
    width: 100%;
    overflow-y: scroll;
    overflow-x: none !important;
  }
  /* trick to only apply in webkit */
  @media screen and (-webkit-min-device-pixel-ratio:0) { 
    .scroll-container {
        background-color: rgba(0,0,0,0);
        -webkit-background-clip: text;
        /*-webkit-text-fill-color: transparent; 这一行和上一行是原理魔法，取消注释可以看到实现细节*/
        transition: background-color .6s;
    }
    .scroll-container:hover {
       background-color: rgba(0,0,0,0.18);  
    }
    .scroll-container::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    .scroll-container::-webkit-scrollbar-track {
        display: none;
    }
    .scroll-container::-webkit-scrollbar-thumb {
        border-radius: 10px;
        background-color: inherit;
    }
  }

  
</style>
