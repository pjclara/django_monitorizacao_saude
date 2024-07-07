<template>
  <v-container>
    <v-row class="d-flex my-2 justify-center" no-gutters>
      <div class="text-h4 text-center font-weight-bold text-deep-purple-darken-4">{{ $t('CreatePatient') }}</div>
    </v-row>
    <PatientForm :patient="patient" ref="form" @validationChanged="updateButtonState"
      @areAllFieldsNonEmpty="areAllFieldsNonEmpty"></PatientForm>
    <v-row class="d-flex my-2 justify-space-around">
      <v-btn @click="voltar()" color="blue-darken-3"><v-icon class="mr-2">mdi-keyboard-backspace</v-icon>{{ $t('Return')
        }}</v-btn>
      <v-btn :disabled="!isFormValid || !isValid" @click="criarPaciente" color="indigo-darken-3"><v-icon class="mr-2">mdi-content-save</v-icon>{{ $t('Save')
        }}</v-btn>
    </v-row>
  </v-container>
</template>

<script setup>
import PatientForm from '@/components/forms/PatientForm.vue'
import router from '@/router';
import { ref, computed, watch } from 'vue'
import { useLoaderStore } from '@/stores/loader'
import { toast } from 'vue3-toastify';
import { format } from 'date-fns';
import { usePatientsStore } from '@/stores/patients';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const loaderStore = useLoaderStore();

const patient = ref({
  sns: null,
  nome: null,
  dataNascimento: null,
  email: null,
  genero: null,
  peso: null,
  altura: null,
  telefone: null,
  dispositivos: [
  ]
})

const isValid = ref(false);

const areAllFieldsNonEmpty = (data) => {
  isValid.value = data;
}

const patientId = computed(() => {
  return patient.value.sns;
});

watch(patientId, (newSns) => {
  if (validateSns(newSns)) {
    findPatient(newSns)
  }
})

const snsRules = [
  v => !!v || 'SNS number is required',
  v => /^\d{9}$/.test(v) || 'SNS number must have exactly 9 digits',
  v => /^\d+$/.test(v) || 'SNS number must contain only numbers'
]

const voltar = () => {
  router.push({ name: 'PatientsListing' })
}

const validateSns = (sns) => {
  const errors = snsRules.map(rule => rule(sns)).filter(result => result !== true);
  return errors.length === 0
}

// find patient by sns
const findPatient = async (sns) => {
  try {
    loaderStore.setLoading(true);
    const response = await fetch(window.URL + '/api/documentos/buscar_por_sns/' + sns + '/',
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + localStorage.getItem('token')
        }
      }
    );
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    if (data.sns) {
      patient.value = formatData(data)
      router.push({ name: 'PatientEdit', params: { patientSns:  patient.value.sns } });
    }
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
  }
  loaderStore.setLoading(false);
}

const form = ref(null)

const isFormValid = ref(false)

const updateButtonState = (isValid) => {
  isFormValid.value = isValid
}

const criarPaciente = async () => {
  // chek if patient has at least one device e at least one vital sign
  if (patient.value.dispositivos.length === 0) {
    toast.error(t('Patient must have at least one device'))
    return
  }

  loaderStore.setLoading(true);
  // check if patient already exists
  const patientExists = await usePatientsStore().buscarPaciente(patient.value.sns);
  console.log(patientExists)
  if (patientExists.length > 0) {
    usePatientsStore().atualizarPaciente(patient.value);
  } else {
    usePatientsStore().criarPaciente(patient.value);
  }
  loaderStore.setLoading(false);
}

const formattedDate = (date) => format(date, 'yyyy-MM-dd')

const formatData = (data) => {
  const devices = [];
  if (data) {
    if (data.dispositivos) {
      for (const device of data.dispositivos) {
        const sinaisVitais = [];
        for (const vital of device.sinaisVitais) {
          sinaisVitais.push({
            tipo: vital.tipo,
            unidade: vital.unidade,
            maximo: vital.maximo,
            minimo: vital.minimo,
            readingFrequency: vital.readingFrequency,
            valores: []
          })
        }
        devices.push({
          fabricante: device.fabricante,
          modelo: device.modelo,
          numeroSerie: device.numeroSerie,
          descricao: device.descricao,
          data_inicio: formattedDate(device.data_inicio),
          data_fim: formattedDate(device.data_fim),
          ativo: device.ativo,
          sinaisVitais: [
            ...sinaisVitais
          ]
        })
      }
    }
  }
  return {
    sns: data.sns,
    nome: data.nome,
    dataNascimento: formattedDate(data.dataNascimento),
    genero: data.genero,
    peso: data.peso,
    altura: data.altura,
    email: data.email,
    telefone: data.telefone,
    dispositivos: [
      ...devices
    ]
  }
};

</script>
