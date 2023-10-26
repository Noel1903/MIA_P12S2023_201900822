import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'
import HomeComponent from './components/HomeComponent.vue'
import ConsoleComponent from './components/ConsoleComponent.vue'
import LoginComponent from './components/LoginComponent.vue'
import ConsoleAdmin from './components/ConsoleAdmin.vue'
import ReportsComponent from './components/ReportsComponent.vue'
import LinkReports from './components/LinkReports.vue'


import { createRouter,createWebHistory } from 'vue-router'

const app = createApp(App)

const routes = [
    { path: '/home', component: HomeComponent },
    { path: '/console', component: ConsoleComponent },
    { path: '/login', component: LoginComponent },
    { path: '/consoleAdmin', component: ConsoleAdmin},
    { path: '/reports', component: ReportsComponent},
    { path: '/linkReports', component: LinkReports},
]


const router = createRouter({
    history: createWebHistory(),
    routes,
})

app.use(router)
app.mount('#app')