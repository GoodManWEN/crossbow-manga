<template>
  <BasicPage v-slot:content winname="files" title="文件列表" :lsize="26" :preclose="mainStore.windows['files'].preclose">
    <div class="tw-w-full tw-flex tw-p-3" style="min-width:788px">
      <div class="tw-w-full tw-h-full tw-p-10 tw-rounded-xl tw-flex tw-flex-row" style="background-color: #fff">
        <div class="tw-flex-none" style="min-width: 360px">
          <div class="tw-flex tw-flex-col">
            <el-popconfirm title="整个工作区将被完全清除，确认吗？" @confirm="img_clear_all">
              <template #reference>
                <el-button type="warning" plain class="tw-mb-5"> 点此清空图片工作区 </el-button>
              </template>
            </el-popconfirm>
            
            <el-upload
              class="upload-demo tw-w-full"
              drag
              action="http://127.0.0.1:39921/test/post"
              list-type="picture"
              :on-success="success"
              multiple
              accept="image/*"
              :before-upload="handleBeforeUpload"
            >
              <el-icon class="el-icon--upload tw-relative" style="top: -5vh"><upload-filled /></el-icon>
              <div class="el-upload__text tw-relative"  style="top: -5vh">
                在此拖入文件或文件夹 <em>或点击打开</em>
              </div>
              <template #tip>
              </template>
            </el-upload>
            
          </div>
        </div>
        <div class="tw-h-full tw-bg-gray-200 tw-mx-10" style="width:1px"></div>
        <div class="tw-flex-grow tw-w-full tw-h-full tw-flex tw-flex-row tw-flex-wrap tw-overflow-scroll no-scroll-x" :class="{'scroll-activate':scroll_show_flag}" style="overflow:hidden">
          <!-- <el-scrollbar class="tw-w-full"> -->
            <div class="tw-w-full tw-h-full scroll-container" >
              <div class="tw-w-32 tw-h-32 tw-bg-red-200">{{'hello world'}}</div>
              <div class="tw-w-32 tw-h-32 tw-bg-red-200">{{'hello world'}}</div>
              <div class="tw-w-32 tw-h-32 tw-bg-red-200">{{'hello world'}}</div>
              <div class="tw-w-32 tw-h-32 tw-bg-red-200">{{'hello world'}}</div>
              <div class="tw-w-32 tw-h-32 tw-bg-red-200">{{'hello world'}}</div>
            </div>
            <!-- <FilesPageImg v-for="(item, i) in mainStore.mainStruct" :imgStat="item" /> -->
          <!-- </el-scrollbar> -->
        </div>
      </div>
    </div>
  </BasicPage>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect } from 'vue'
import { useMainStore } from '@/stores' 
import BasicPage from "./BasicPage.vue";
import FilesPageImg from "./FilesPageImg.vue";
import { UploadFilled } from '@element-plus/icons-vue'

const mainStore = useMainStore();

let success = () => {

}

let handleBeforeUpload = (file) => {
  const formdata = new FormData()
  formdata.append('file', file)
  formdata.append('name', file.name)
  formdata.append('size', file.size)
  formdata.append('ftype', file.type)
  formdata.append('ws_uuid', mainStore.wsUUID)
  axios.post('http://127.0.0.1:39921/api/file-upload', formdata)
    .then(res => console.log(res))
  return false
}

let img_clear_all = () => {
  axios.post("http://127.0.0.1:39921/api/remove-img-all")
  .then(()=>{})
  .catch(()=>{})
}
let scroll_show_flag = ref(false)
let mfmouseover = () => {
  console.log(123)
  scroll_show_flag.value = true
}
let mfmouseleave = () => {
  scroll_show_flag.value = false
}
</script>

<style scoped lang="scss">
</style>

<style>
  .el-upload-dragger {
    min-width:  360px;
    height:  calc(100vh - 200px) ;
    /*height:  calc(100vh - 140px) ;*/
    display:  flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  /*.no-scroll-x {
    transition: .4s ease-in-out;
    max-height: calc(100vh - 144px);
    overflow-x: hidden !important;
  }
  .no-scroll-x::-webkit-scrollbar {
    width: 16px;
  }
  .no-scroll-x::-webkit-scrollbar-track {
      background: rgba(255,255,255,0); 
  }
  .no-scroll-x::-webkit-scrollbar-thumb {
      background: rgba(255,255,255,0);
  }
  .scroll-activate::-webkit-scrollbar {
    transition: .4s ease-in-out;
  }
  .scroll-activate::-webkit-scrollbar-track {
    background: red !important; 
  }
  .scroll-activate::-webkit-scrollbar-thumb {
    background: green !important;
  }*/


  .scroll-container {
    overflow-y: scroll;
    overflow-x: hidden;
    background: red;
  }
  .scroll-container:hover {
    color: green;
    background-color: rgba(0,0,0,1);  
  }
  /*// trick to only apply in webkit 
  // uncomment following line to see the trick in actions 
  // -webkit-text-fill-color: transparent; */
  @media screen and (-webkit-min-device-pixel-ratio:0) { 
    .scroll-container {
        background-color: rgba(0,0,0,0);
        -webkit-background-clip: text;
        transition: background-color .8s;
    }
    .scroll-container:hover {
      color: green;
      background-color: rgba(0,0,0,1);  
    }
    .scroll-container::-webkit-scrollbar {

        width: 80px;
        height: 80px;
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
