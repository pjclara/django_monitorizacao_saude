<template>
    <v-row>
      <v-col cols="12" class="d-flex flex-column align-center">
        <v-row class="d-flex my-2">
          <div class="text-h4 text-center font-weight-bold text-deep-purple-darken-4">Create a 'Patient' (dinamico)</div>
        </v-row>
        <v-col>
            <v-text-field label="First Name" placeholder="John" color="primary"/>
            <v-text-field label="Last Name" placeholder="Doe" color="primary"/>
            <v-select
                label="Gender"
                :items="['Male', 'Female']"
            ></v-select>
            <v-text-field label="Email" placeholder="example@mail.com" color="primary" :disabled="routeName == 'EditUser'"/>
            <v-text-field label="Address" placeholder="Street, Region, Country" color="primary"/>
            <v-text-field label="Phone Number" placeholder="910000000" color="primary"/>
            <v-select
                label="Marital Status"
                :items="['Single', 'Maried', 'Divorced', 'Widowed']"
            ></v-select>       
        </v-col>
            
        <v-row class="w-25 mt-6 justify-space-between" no-gutters>
          <v-btn class="bg-blue text-white" rounded="lg" size="large">Cancel</v-btn>
          <v-btn class="bg-blue text-white" rounded="lg" size="large">Create Patient</v-btn>
        </v-row>
      </v-col>
    </v-row>
   </template>
   
   <script setup>
    import { ref } from 'vue'
  
    const vitalSigns = ref([])
  
    const showCreateVital = ref(false)
    const selectedVital = ref(null)
  
    const addNewVitalSign = () => {
      vitalSigns.value.push({ type: selectedVital.value })
    }
   </script>
   
   <style scoped>
      
   </style>