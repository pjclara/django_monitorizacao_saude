<template>
  <v-container>
    <div v-if="showSuccess" class="success-message">
      {{ $t('SuccessYourActionWasCompleted') }}
    </div>
    <div v-if="showErrors" class="error-message">
      {{ $t('ErrorYourActionWasNotCompleted') }}

    </div>
    <v-row class="d-flex my-2 justify-center" no-gutters>
      <div class="text-h4 text-center font-weight-bold text-deep-purple-darken-4">{{ $t('CreatePatient') }}</div>
    </v-row>
    <PatientForm :patient="patient" ref="form" @validationChanged="updateButtonState" @areAllFieldsNonEmpty="areAllFieldsNonEmpty"></PatientForm>
    <v-row class="d-flex my-2 justify-space-around">
      <v-btn @click="voltar()" color="blue-darken-3">Return</v-btn>
      <v-btn :disabled="!isFormValid || !isValid" @click="criarPaciente" color="indigo-darken-3">Save</v-btn>
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

const loaderStore = useLoaderStore();

const showSuccess = ref(false)
const showErrors = ref(false)

const patient = ref({
  sns: null,
  nome: null,
  dataNascimento: null,
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
    const response = await fetch(window.URL + '/api/documentos/buscar_por_sns/' + sns + '/');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    if (data.sns) {
      router.push({ name: 'PatientEdit', params: { patientSns: sns } })
      patient.value = formatData(data)
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
  try {
    loaderStore.setLoading(true);
    const response = await fetch(window.URL + '/api/documentos/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(patient.value)
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    // response 200 OK
    if (response.status === 201) {
      toast.success('Patient created successfully')
      router.push({ name: 'PatientsListing' })
    } else {
      toast.error('Error creating patient')
    }
  } catch (error) {
    toast.error('Error creating patient')
  }
  loaderStore.setLoading(false);
}

const formattedDate = (date) => format(date, 'dd-MM-yyyy')

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
    telefone: data.telefone,
    dispositivos: [
      ...devices
    ]
  }
};


</script>
