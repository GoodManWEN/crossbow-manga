import { createApp } from "vue";
import { createPinia } from 'pinia'
import App from "./App.vue";
import router from './routers/route.ts'

import "./styles/reset.css";
import "./styles/tailwind.css";
import 'animate.css';

import "element-plus/theme-chalk/src/message.scss";
import "element-plus/theme-chalk/src/loading.scss";

import * as ElementPlusIconsVue from '@element-plus/icons-vue'
// import VueHtml2Canvas from 'vue-html2canvas'

const pinia = createPinia();
const app = createApp(App);
app.use(router).use(pinia)
// app.use(VueHtml2Canvas)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.mount("#app");
