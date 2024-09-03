<template>
  <v-container>
    <v-row class="d-flex my-2 justify-center" no-gutters>
      <div class="text-h4 text-center font-weight-bold text-deep-purple-darken-4">{{ $t('EditPatient') }}</div>
    </v-row>
    <PatientForm :patient="patient" @areAllFieldsNonEmpty="areAllFieldsNonEmpty"></PatientForm>
    <v-row class="d-flex my-2 justify-space-around">
      <v-btn @click="voltar()" color="blue-darken-3"><v-icon class="mr-2">mdi-keyboard-backspace</v-icon>{{ $t("Return")
        }}</v-btn>

      <v-btn @click="atualizarPaciente" :disabled="!isValid" color="green-darken-3"><v-icon
          class="mr-2">mdi-content-save</v-icon>{{ $t("Save") }}</v-btn>
    </v-row>
  </v-container>

</template>

<script setup>
import PatientForm from '@/components/forms/PatientForm.vue'
import { ref, onMounted } from 'vue'
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
  if (usePatientsStore().patients.length == 0) {
    usePatientsStore().fetchPatients(user.user_id);
  }


  const patientData = usePatientsStore().getPaciente(patientSns);
  console.log(patientData);
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
  let erroEncontrado = false;
  loaderStore.setLoading(true);

  // Confirmar se todos os valores máximos são maiores que os mínimos para cada sinal vital
  for (let dispositivo of patient.value.dispositivos) {

    if (new Date(dispositivo.data_inicio) > new Date(dispositivo.data_fim)) {
      //erroEncontrado = true;
      //toast.error('End date must be greater than start date');
    }

    // data de início do dispositivo deve ser igual ou superior à data de hoje
    const dataAtual = new Date();
    const dataAtualFormatada = new Date(dataAtual.getFullYear(), dataAtual.getMonth(), dataAtual.getDate());

    const dataInicio = new Date(dispositivo.data_inicio);
    const dataInicioFormatada = new Date(dataInicio.getFullYear(), dataInicio.getMonth(), dataInicio.getDate());

    if (dataInicioFormatada < dataAtualFormatada) {
      //erroEncontrado = true;
      //toast.error('Data de início do dispositivo deve ser igual ou superior à data de hoje');
    }

    dispositivo.sinaisVitais.forEach(element => {
      if (element.maximo < element.minimo) {
        erroEncontrado = true;
        toast.error($t('The maximum value must be greater than the minimum value.'));
      }

    });
  }

  if (erroEncontrado) {
    loaderStore.setLoading(false);
    return; // Se houver um erro, interrompe a atualização
  }

  usePatientsStore().atualizarPaciente(patient.value);
  
  loaderStore.setLoading(false);
}


const voltar = () => {
  window.history.back();
}
</script>
