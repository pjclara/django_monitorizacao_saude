import './assets/main.css'
import '@mdi/font/css/materialdesignicons.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import en from './locale/en.js'
import pt from './locale/pt.js'

import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const i18n = createI18n({
    legacy: false,
    locale: 'PT',
    globalInjection: true,
    messages: {
        EN: en,
        PT: pt
    },
    fallbackLocale: 'EN'
})

const vuetify = createVuetify({
    components,
    directives
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)
app.use(vuetify)


app.mount('#app')
