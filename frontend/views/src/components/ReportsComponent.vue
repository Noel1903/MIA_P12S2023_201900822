<template>
    <MenuAdmin/>
    <div>
        <button @click="getMounted()" class="btn btn-outline-warning btn-lg" ><i class="uil uil-list-ul"></i> Get List Partitions Mounted</button>
    </div>
    <div>
    <label for="mounted">Select the partition mounted:</label>
    <select id="mounted" v-model="mountSelected">
      <option value="">-- Select an option --</option>
      <option v-for="mount in mounted" :key="mount" :value="mount">{{mount}}</option>
    </select>
    
    </div>
    <div>
        <label>Select report type:</label>
        <select id="reportType">
            <option value="">-- Select an option --</option>
            <option value="mbr">MBR</option>
            <option value="disk">DISK</option>
            <option value="bm_inode">BM_INODE</option>
            <option value="bm_block">BM_BLOCK</option>
            <option value="tree">TREE</option>
            <option value="sb">SB</option>
            <option value="file">FILE</option>

        </select>
    </div>
    <div>
        <button class="btn btn-outline-primary btn-lg" @click="getImage()"><i class="uil uil-download-alt"></i> Generate Report</button>
    </div>
    <div v-if="imagenURL">
        <img :src="imagenURL" alt="Reporte Generado">
    </div>
</template>

<script>
import axios from 'axios';
import MenuAdmin from './MenuAdmin.vue';
const apiurl = process.env.VUE_APP_API_URL;

export default{
    name: "ReportsComponent",
    components: { MenuAdmin },
    methods : {
        getMounted : function(){
            axios
                .get(apiurl + "/mounts")
                .then((response) => {
                    this.mounted = response.data["data"];
                })
                .catch((error) => {
                    console.log(error);
                })
        },
        getImage : function(){
            var mounted = document.getElementById("mounted");
            var reportType = document.getElementById("reportType");
            var content = {
                "mount": mounted.value,
                "type": reportType.value
            }
            console.log(content);
            axios
            .post(apiurl+"/reports",content)
            .then((response) => {
                console.log(response.data);
                if (reportType.value =="bm_inode" || reportType.value =="bm_block" || reportType.value =="file"){
                    window.open(response.data["data"],'_blank');
                    return;
                }
                this.imagenURL = response.data["data"];
                return
            })
            .catch((error) => {
                console.log(error);
            })
        }
    },
    
    data(){
        return {
            mountSelected: '',
            mounted: [],
            imagenURL: null
        }
    }
    
}

    
</script>

<style>
/* Estilo base para el elemento select */
select {
  padding: 10px; /* Añade un espacio de relleno alrededor del select */
  font-size: 16px; /* Tamaño de fuente */
  border: 1px solid #ccc; /* Borde */
  border-radius: 5px; /* Bordes redondeados */
  background-color: #fff; /* Fondo blanco */
  width: 100%; /* Ancho completo */
}

/* Estilo para las opciones dentro del select */
select option {
  padding: 5px; /* Espacio de relleno para las opciones */
  font-size: 14px; /* Tamaño de fuente para las opciones */
}

/* Estilo para el hover (cuando el usuario pasa el mouse) en las opciones */
select option:hover {
  background-color: #f2f2f2; /* Color de fondo en hover */
}

/* Estilo para el foco (cuando el usuario selecciona la lista) en el select */
select:focus {
  border-color: #007bff; /* Color de borde cuando se selecciona */
  box-shadow: 0 0 5px #007bff; /* Sombra cuando se selecciona */
  outline: none; /* Quita el contorno predeterminado del navegador */
}

</style>