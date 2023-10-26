<template>
    <MenuComponent/>
    <div class="inputfile">
        <div class="mb-3">
            <input class="form-control" type="file" id="formFile" v-on:change="changeInput()">
            <input type="submit" value="Open File" v-on:click="showFile()" class="openfile">
        </div>
    </div>
    <div class="buttons">
        <button type="button" class="btn btn-success" v-on:click="sendResponse()">Run</button>
        <button type="button" class="btn btn-danger" v-on:click="clear()">Clear</button>
    </div>
    <div class="textAreas">
        <div class="input">
            <textarea id="input" name="input" rows="18" cols="70" v-model="input"></textarea>
        </div>
        <div class="output">
            <textarea id="output" name="output" rows="18" cols="70" v-model="output"></textarea>
        </div>
    </div>
</template>

<script>
    import MenuComponent from './MenuComponent.vue';
    import axios from 'axios';
    var textFile = "";
    
    const apiurl = process.env.VUE_APP_API_URL;
    export default {
        name: "ConsoleComponent",
        components: { MenuComponent },
        methods:{
            sendResponse: function(){
                textFile = document.getElementById("input").value;
                console.log(apiurl);
                axios.defaults.baseURL = process.env.VUE_APP_API_URL;
                axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';  // Configura el origen permitido
                axios.defaults.headers.common['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE';  // Configura los métodos permitidos
                axios.defaults.headers.common['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, Authorization';
                axios
                    .post(apiurl+"/source",{content:textFile})
                    .then((response) => {
                        console.log(response.data);
                        var consoleOut = document.getElementById("output");
                        var linesArr = response.data["data"].split("\n");
                        for (var i = 0; i < linesArr.length; i++) {
                            console.log(linesArr[i]);
                            if (linesArr[i] == "pause") {
                                alert("Programa pausado");
                                continue;
                            }
                            if (linesArr[i] == "") {
                                continue;
                            }
                            consoleOut.value += linesArr[i] + "\n";
                        }
                        
                        //consoleOut.value = response.data["data"];
                    })
            }, 
            changeInput(){
                var input = document.getElementById("formFile");
                var reader = new FileReader();
                reader.onload = function(){
                    textFile = reader.result;
                    console.log(textFile);
                };
                reader.readAsText(input.files[0]);
                textFile = reader.result;
            },
            showFile(){
                var consoleIn = document.getElementById("input");
                consoleIn.value = textFile;

            },
            clear(){
                var consoleIn = document.getElementById("input");
                var consoleOut = document.getElementById("output");
                consoleIn.value = "";
                consoleOut.value = "";
            }


        }
    }

    

    
</script>


<style>
    textarea {
        resize: none;
        background-color: #e0d8b0;
    }
    .buttons {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0 10px;
    }
    .textAreas{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0 10px;
    }
    .openfile{
        background-color: #831eff;
        color: #fff;
        border: none;
        padding: 10px 20px;
        margin: 0 10px;
        font-size: 20px;
        border-radius: 5px;
    }

    

</style>