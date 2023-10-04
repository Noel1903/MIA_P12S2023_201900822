<template>
  
   <div class="container" v-if="$route.path === '/'">
      
      <div class="backgroundcontainer"></div>
      <div class="startbutton">
        <h1>WELCOME TO THE DISK MANAGER</h1>
        <RouterLink to="/home"><button type="button" class="btn btn-success">Start →</button></RouterLink>
      </div>
        
    </div>
    <RouterView></RouterView>
</template>

<script>

export default {
  name: 'App',
  
}
</script>

<style>

    .backgroundcontainer {
      position: absolute;
      width: 120%;
      height: 100%;
      background-image:url("@/assets/background.jpg");
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;

      filter: blur(3px);
    }
    .container{
      position: relative;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .startbutton{
      position: absolute;
      top: 300px;
      left: 50%;
      transform: translate(-50%, -50%);
      text-align: center;
      
      margin-bottom: 100px;
      padding: 200px 50px;
    }
    .startbutton h1{
      color: #f7a000;
      font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
      font-size: 60px;
      font-weight: bold;
    }
    .startbutton button{
      font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
      font-size: 30px;
      font-weight: bold;
      padding: 10px 20px;
    }
</style>
