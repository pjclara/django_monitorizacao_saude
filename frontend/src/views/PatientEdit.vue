<template>
  <v-container>
    <PatientForm :patient="patient" @areAllFieldsNonEmpty="areAllFieldsNonEmpty"></PatientForm>
    <v-row class="d-flex my-2 justify-space-around">
      <v-btn @click="voltar()" color="blue-darken-3"><v-icon class="mr-2">mdi-keyboard-backspace</v-icon>{{ $t("Return") }}</v-btn>

      <v-btn @click="atualizarPaciente" :disabled="!isValid" color="green-darken-3"><v-icon class="mr-2">mdi-content-save</v-icon>{{ $t("Save") }}</v-btn>
    </v-row>
  </v-container>

</template>

<script setup>
import PatientForm from '@/components/forms/PatientForm.vue'
import { ref, onMounted} from 'vue'
import { useRoute } from 'vue-router';
import { useLoaderStore } from '@/stores/loader'
import { usePatientsStore } from '@/stores/patients';
import router from '@/router';
import { useUsersStore } from '@/stores/users';
import { toast } from 'vue3-toastify';

const user = useUsersStore().user

const loaderStore = useLoaderStore();

const patient = ref([
])

const isValid = ref(false);

const areAllFieldsNonEmpty = (data) => {
  isValid.value = data; 
}

const patientSns = useRoute().params.patientSns;

onMounted(() => {
  if(usePatientsStore().patients.length == 0){
    usePatientsStore().fetchPatients(user.user_id);
  }
  const patientData = usePatientsStore().getPaciente(patientSns);
  if (patientData) {
    patient.value = {
      ...patientData,
      dataNascimento: patientData.dataNascimento.split('T')[0],
      dispositivos: patientData.dispositivos.map(dispositivo => {
        return { ...dispositivo, data_inicio: dispositivo.data_inicio.split('T')[0], data_fim: dispositivo.data_fim.split('T')[0] }
      })
    };
  } else {
    router.push({ name: 'PatientsListing' });
    toast.error('Patient not found');
  } 
});

const atualizarPaciente = () => {
  loaderStore.setLoading(true);
  usePatientsStore().atualizarPaciente(patient.value);
  loaderStore.setLoading(false);
}

const voltar = () => {
  window.history.back();
}
</script>
