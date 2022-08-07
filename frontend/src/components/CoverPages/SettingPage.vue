<template>
  <BasicPage winname="settings" title="设置选项" :preclose="mainStore.windows['settings'].preclose">
    <template v-slot:content>
    <div class="tw-flex-none tw-h-full tw-w-52 tw-p-4 tw-flex tw-flex-col" style="background-color: #fff">
      <SettingBtn v-for="(item, i) in mainStore.settings" :label="item.label" :icon="item.icon" :focus="item.focus" :idx="item.idx" />
    </div>
    <div class="tw-flex-grow tw-flex tw-p-3">
      <div class="tw-w-full tw-h-full tw-p-6 tw-rounded-xl" style="background-color: #fff">
        <SettingPageFonts />
      </div>
    </div>
    </template>
  </BasicPage>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watchEffect } from 'vue'
import { useMainStore } from '@/stores' 
import BasicPage from "./BasicPage.vue";
import SettingBtn from "./SettingBtn.vue";
import SettingPageFonts from "./SettingPageFonts.vue";
const mainStore = useMainStore();


</script>

<style scoped lang="scss">
</style>
