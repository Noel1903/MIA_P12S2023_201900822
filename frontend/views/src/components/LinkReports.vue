<template>
    <MenuAdmin/>
    <div>
        <button @click="getReports()" class="btn btn-outline-warning btn-lg" ><i class="uil uil-list-ul"></i> Get List Reports</button>
    </div>
    <div v-for="report in reports" :key="report" :value="report">
        <b>{{report.slice(47)}}</b><br>
        <a :href="report" target="_blank">{{report}}</a>
    </div>
</template>

<script>
    import axios from 'axios';
    import MenuAdmin from './MenuAdmin.vue';
    const apiurl = process.env.VUE_APP_API_URL;
    export default {
        name: "LinkReports",
        components: { MenuAdmin },
        methods:{
            getReports : function(){
                axios
                    .get(apiurl + "/allreports")
                    .then((response) => {
                        this.reports = response.data["data"];
                    })
                    .catch((error) => {
                        console.log(error);
                    })
            }
        },
        data(){
            return {
                reports: []
            }
        },
        
    }
</script>