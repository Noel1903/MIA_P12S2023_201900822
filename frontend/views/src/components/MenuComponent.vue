<template>
    <div class="navbar">
    <div class="logo">
      
      <span class="logo-title"><i class="uil uil-hdd"></i>Disk Manager</span>
    </div>
    <div class="navigation">
      <RouterLink to="/"><a href="#"><i class="uil uil-home"></i>Home</a></RouterLink>
      <RouterLink to="/console"><a href="#"><i class="uil uil-caret-right"></i>Console</a></RouterLink>
      <!--RouterLink to="/reports"><a href="#"><i class="uil uil-file-graph"></i>Reports</a></RouterLink-->
      <RouterLink to="/login"><a href="#"><i class="uil uil-signin"></i>Log in</a></RouterLink>
      </div>
  </div>    
</template>

<script>
    export default {
        name: 'MenuComponent'
    }

</script>

<style>
@import url("https://unicons.iconscout.com/release/v4.0.8/css/line.css");
  
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #831eff;
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
  background-color: #831eff;
  padding: 10px;
  text-align: center;
}
.navigation a {
  text-decoration: none;
      color: #fffcfc;
      padding: 10px 20px;
      margin: 0 10px;
      font-size: 20px;
}


.navigation a:hover {
  background-color: #fff;
  color: #831eff;
}

</style>