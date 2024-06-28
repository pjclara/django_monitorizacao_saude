<template>
    <v-alert
        density="compact"
        :text="alertText"
        :title="alertTitle"
        type="warning"
        class="bottom-left-component"
    ></v-alert>
</template>
   
<script setup>
import { ref } from 'vue'

const alertText = ref('test text')
const alertTitle = ref('test title')

</script>

<style scoped>
    .bottom-left-component {
        position: fixed;      
        bottom: 0;
        right: 0;
        margin: 20px; 
        background-color: #ffffff; 
        padding: 10px; 
        border: 1px solid #ccc; 
        border-radius: 5px;
    }
</style>