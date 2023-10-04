import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'
import HomeComponent from './components/HomeComponent.vue'
import ConsoleComponent from './components/ConsoleComponent.vue'
import LoginComponent from './components/LoginComponent.vue'
import ConsoleAdmin from './components/ConsoleAdmin.vue'


import { createRouter,createWebHistory } from 'vue-router'

const app = createApp(App)

const routes = [
    { path: '/home', component: HomeComponent },
    { path: '/console', component: ConsoleComponent },
    { path: '/login', component: LoginComponent },
    { path: '/consoleAdmin', component: ConsoleAdmin},
]


const router = createRouter({
    history: createWebHistory(),
    routes,
})

app.use(router)
app.mount('#app')