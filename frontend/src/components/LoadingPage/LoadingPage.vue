<template>
  <div ref="loadingdiv" class="tw-fixed tw-w-screen tw-h-screen tw-overflow-hidden background-style-loading">
    <div class='demo'>
      <div class='circle'>
        <div class='inner'></div>
      </div>
      <div class='circle'>
        <div class='inner'></div>
      </div>
      <div class='circle'>
        <div class='inner'></div>
      </div>
      <div class='circle'>
        <div class='inner'></div>
      </div>
      <div class='circle'>
        <div class='inner'></div>
      </div>
    </div>
    <a class="bottom-atag" href='http://baidu.com'>CrossBow Manga, Copy Right 2022.</a>

  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect } from 'vue'
import { useMainStore } from '@/stores' 
const mainStore = useMainStore();

let loadingdiv = ref()
onMounted(() => {
  watchEffect(() => {
    if (mainStore.loaded==true) {
      loadingdiv.value.style.setProperty('opacity', '0', 'important')
      window.setTimeout(() => {
        loadingdiv.value.style.setProperty('z-index', '-5000', 'important')
      }, 1000)
    }
  })
})




</script>

<style scoped lang="scss">
  @import url(https://fonts.googleapis.com/css?family=Lato);
  .bottom-atag {
    position: fixed;
    bottom: 2%;
    display: block;
    text-align: center;
    color: #0fa;
    font-family: "Lato", sans-serif;
    text-decoration: none !important;
    width: 100%;
  }

  .background-style-loading {
    transition: 1.1s ease-in-out;
    z-index: 6000;
    background: linear-gradient(90deg, #00b377, #00d68f);
    box-shadow: inset 0px 0px 90px rgba(0, 0, 0, 0.5);
    margin: 0px;
    padding: 0px;
    opacity: 1;
  }

  .demo {
    width: 100px;
    height: 102px;
    border-radius: 100%;
    position: absolute;
    top: 45%;
    left: calc(50% - 50px);
  }

  .circle {
    width: 100%;
    height: 100%;
    position: absolute;
  }
  .circle .inner {
    width: 100%;
    height: 100%;
    border-radius: 100%;
    border: 5px solid rgba(0, 255, 170, 0.7);
    border-right: none;
    border-top: none;
    backgroudn-clip: padding;
    box-shadow: inset 0px 0px 10px rgba(0, 255, 170, 0.15);
  }

  @-webkit-keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }

  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
  .circle:nth-of-type(0) {
    transform: rotate(0deg);
  }
  .circle:nth-of-type(0) .inner {
    -webkit-animation: spin 2s infinite linear;
            animation: spin 2s infinite linear;
  }

  .circle:nth-of-type(1) {
    transform: rotate(70deg);
  }
  .circle:nth-of-type(1) .inner {
    -webkit-animation: spin 2s infinite linear;
            animation: spin 2s infinite linear;
  }

  .circle:nth-of-type(2) {
    transform: rotate(140deg);
  }
  .circle:nth-of-type(2) .inner {
    -webkit-animation: spin 2s infinite linear;
            animation: spin 2s infinite linear;
  }

  .demo {
    -webkit-animation: spin 5s infinite linear;
            animation: spin 5s infinite linear;
  }
</style>
