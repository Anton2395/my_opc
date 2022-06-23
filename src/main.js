import { createApp } from 'vue'
import App from './App'
import './common/font.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'

import axios from 'axios'
import VueAxios from 'vue-axios'



const app = createApp(App)

app.use(ElementPlus, VueAxios, axios)
app.mount('#app')

