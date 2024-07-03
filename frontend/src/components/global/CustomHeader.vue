<template>
   <v-app-bar style="background-color: #E0E0E0;">
      <v-row class="ma-2 align-center">
         <v-btn class="sidebar-icon" @click="layoutStore.toggleSidebar">
            <v-icon class="text-h3 text-indigo-accent-4">mdi-menu</v-icon>
         </v-btn>

         <v-col class="d-flex justify-center">
            <span class="header-text">{{ $t('HealthMonitor') }}</span>
         </v-col>
      </v-row>
   </v-app-bar>
</template>

<script setup>
import { useLayoutStore } from '@/stores/layout'
const layoutStore = useLayoutStore() 

</script>

<style scoped>
.sidebar-icon{
   position: absolute;
   height: 3rem !important;
   width: 3rem;
   min-width: 0;
   padding: 0;
   margin-left: 0.5rem;
}


.header-text{
   font-size: 2rem;
   color: darkgreen;
}

@media screen and (max-width: 55rem) {
   .header-text{
      visibility: hidden;
      color: darkgreen;
   }
}


</style>