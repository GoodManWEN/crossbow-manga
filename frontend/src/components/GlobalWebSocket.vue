<template>
  <div></div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect } from 'vue'
import { useMainStore } from '@/stores' 
const mainStore = useMainStore();
import { ElMessage } from 'element-plus'

let backend_ready = false
let normal_count = 0
let acuumulated_failcount = 0
// 离线状态300毫秒检测一次，在线状态20*300=6秒检测一次, 断线3分钟后不再占用多余的系统资源
window.setInterval(() => {
  if (acuumulated_failcount < 600 && (!backend_ready || normal_count == 0)) {
    try {
      axios.post("http://127.0.0.1:39921/api/ready", {}, {timeout: backend_ready?1000:200})
      .then((resp)=>{
        if (resp.data.ready) {
          backend_ready=true
          mainStore.switchReadyStatus(true)
          acuumulated_failcount = 0
        } else {
          backend_ready=false
          mainStore.switchReadyStatus(false)
          acuumulated_failcount += 1
        }
      })
      .catch((err)=>{
        backend_ready=false
        mainStore.switchReadyStatus(false)
        acuumulated_failcount += 1
      })
    } catch {
      backend_ready=false
      mainStore.switchReadyStatus(false)
      acuumulated_failcount += 1
    }
  }
  normal_count = (normal_count + 1) % 20
}, 300)

let make_connect = ()=>{

  let wsurl = 'ws://127.0.0.1:39921/ws/hold'
  let ws = null
  try {
    let tws = new WebSocket(wsurl)
    ws = tws
  } catch {
    mainStore.wsClosed()
  }
  
  ws.onmessage = (event) => {
    let carry = JSON.parse(event.data)
    if (carry.type == 0) {return}
    else if (carry.type == 1) {
      // 图片列表更新
      mainStore.backendImageUpdate(carry.new_files)
    } else if (carry.type == 2) {
      // 原文更新
      mainStore.appendSrcDstText(carry.imgMD5, carry.text, carry.carry, 'src')
    } else if (carry.type == 3) {
      // 译文更新
      mainStore.appendSrcDstText(carry.imgMD5, carry.text, carry.carry, 'dst')
    } else if (carry.type == 4){
      mainStore.updateWordExplain(carry.imgMD5, carry.text, carry.iid) 
    } else {

    }
  }
  ws.onopen = () => {
    ws.send(mainStore.wsUUID)
    axios.get('http://127.0.0.1:39921/api/require-img-init?ws_uuid='+mainStore.wsUUID)
      .then()
      .catch()
  }
  ws.onclose = () => {
    mainStore.wsClosed()
  }
}

onMounted(make_connect)

</script>

<style scoped lang="scss">
</style>
