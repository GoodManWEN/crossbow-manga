<template>
  <BasicPage winname="files" title="文件列表" :lsize="26" :preclose="mainStore.windows['files'].preclose">
    <template v-slot:content>
      <div class="tw-w-full tw-h-full tw-flex tw-flex-row tw-flex-none">
        <div class="tw-h-full tw-flex tw-flex-col-reverse tw-p-3" style="width:280px;background:#fff">
          <el-popconfirm title="整个工作区将被完全清除，确认吗？" @confirm="img_clear_all">
            <template #reference>
              <el-button type="warning" plain class="tw-mb-3"> 点此清空工作区 </el-button>
            </template>
          </el-popconfirm>
          <div class="tw-h-5"></div>
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
              在此拖入文件或文件夹<br> <em>或点击打开</em>
            </div>
            <template #tip>
            </template>
          </el-upload>
        </div>
        <div class="tw-h-full tw-flex-grow tw-p-3">
          <div class="tw-w-full tw-h-full tw-flex-none tw-rounded-xl" style="background:#fff">
            <div class="tw-p-2 tw-w-full tw-h-full"  style="width: calc(100vw - 324px); height: calc(100vh - 104px)">
              <div class="scroll-container tw-flex tw-m-3 tw-flex-wrap" style="width: calc(100vw - 324px); height: calc(100vh - 104px)">
                <FilesPageImg v-for="(item, i) in mainStore.mainStruct" :imgStat="item" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </BasicPage>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect } from 'vue'
import { useMainStore } from '@/stores' 
import BasicPage from "./BasicPage.vue";
// import FilesPageImg from "./FilesPageImg.vue";
import { UploadFilled } from '@element-plus/icons-vue'

const mainStore = useMainStore();

let success = () => {}

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
</script>

<style scoped lang="scss">
</style>

<style>
  .el-upload-dragger {
    width:  257px;
    height:  calc(100vh - 140px) ;
    display:  flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transition: .15s ease-in-out;
  }
  .el-upload-dragger:hover {
    background: rgba(66,66,66,.02);
  }

</style>
