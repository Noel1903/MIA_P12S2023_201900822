<template>
    <div class="navbar">
    <div class="logo">
      
      <span class="logo-title"><i class="uil uil-hdd"></i>Disk Manager</span>
    </div>
    <div class="navigation">
      <RouterLink to="/"><a href="#"><i class="uil uil-home"></i>Home</a></RouterLink>
      <RouterLink to="/consoleAdmin"><a href="#"><i class="uil uil-caret-right"></i>Console</a></RouterLink>
      <RouterLink to="/reports"><a href="#"><i class="uil uil-file-graph"></i>Reports</a></RouterLink>
      <RouterLink to="/linkReports"><a href="#"><i class="uil uil-link"></i>Link Reports</a></RouterLink>
      <button @click="showDialog()" class="logoutB"><i class="uil uil-signout" ></i>Log out</button>
      <DialogComponent v-if="show" :message="dialogMessage" @confirmed="handleConfirmation"></DialogComponent>
    </div>
  </div>    
</template>

<script>
    import axios from 'axios';
    import DialogComponent from './DialogComponent.vue';
    const apiurl = process.env.VUE_APP_API_URL;
    export default {
        name: 'MenuAdmin',
        components: {
            DialogComponent,
        },
        data(){
            return {
                show: false,
                dialogMessage: '¿Seguro que quiere salir cerrar sesión?',
            }
        },
        methods:{
            showDialog() {
                this.show = true;
            },
            handleConfirmation(response) {
                this.show = false;
                console.log(response);
                axios.defaults.baseURL = apiurl;
                axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';  // Configura el origen permitido
                axios.defaults.headers.common['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE';  // Configura los métodos permitidos
                axios.defaults.headers.common['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, Authorization';
                
                if (response){
                    axios
                    .post(apiurl+"/source",{content:"logout"})
                    .then((res) => {
                        console.log(res.data);                      
                    })
                    this.$router.push('/');
                }else{
                    return;
                }
                
            },
            
        }
    }

</script>

<style>
@import url("https://unicons.iconscout.com/release/v4.0.8/css/line.css");
  
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #0335ff;
  padding: 5px;
  color: #fff;
}

.logo {
  display: flex;
  align-items: center;
}

.logo-title {
  font-weight: bold;
  font-size: 25px;
}


.navigation {
  background-color: #0335ff;
  padding: 10px;
  text-align: center;
}

.logoutB{
  background-color: #0335ff;
  color: #fff;
  border: none;
  font-size: 20px;
  cursor: pointer;
}
.navigation a{
  text-decoration: none;
      color: #fffcfc;
      padding: 10px 20px;
      margin: 0 10px;
      font-size: 20px;
}


.navigation a:hover{
  background-color: #fff;
  color: #0335ff;
}

</style>