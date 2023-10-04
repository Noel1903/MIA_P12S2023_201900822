<!-- Dialog.vue -->
<template>
    <div class="dialog">
      <div class="dialog-content">
        <p>{{ message }}</p>
        <button @click="confirm">Sí</button>
        <button @click="cancel">No</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      message: String,
    },
    methods: {
      confirm() {
        this.$emit('confirmed', true);
      },
      cancel() {
        this.$emit('confirmed', false);
      },
    },
  };
  </script>
  
  <style scoped>
  /* Estilos CSS del componente de diálogo */
  .dialog {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .dialog-content {
    background: rgb(0, 162, 255);
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
    text-align: center;
  }
  
  button {
    margin: 5px;
  }
  </style>
  