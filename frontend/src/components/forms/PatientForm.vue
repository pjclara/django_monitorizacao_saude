<template>
  <v-card>
    <v-form v-model="isFormValid" @input="validationStatus">
      <v-tabs v-model="tab">
        <v-tab value="patient" class="tab-border mr-1">
          <span class="text-blue">
            <v-icon class="mr-2">mdi-account</v-icon>{{$t('Patient Data')}}
          </span>
        </v-tab>
        <template v-for="(dispositivo, i) in patient.dispositivos" :key="i">
          <v-tab :value="i" class="tab-border mr-1">
            <span class="text-blue">
              <v-icon class="mr-2">mdi-devices</v-icon> {{ patient.dispositivos[i].numeroSerie ? $t('Device') +" " +
                patient.dispositivos[i].numeroSerie : $t('New Device') }}
            </span>
          </v-tab>
        </template>
      </v-tabs>
      <v-card-text>
        <v-row class="justify-end mb-2"
          v-if="patient.sns && patient.nome && patient.dataNascimento && patient.peso && patient.altura && patient.genero && patient.telefone">
          <v-btn @click="addDevice(patient.dispositivos)" color="indigo-darken-3" :disabled="!isSnsFilled">
            <v-icon class="mr-2" color="white">mdi-plus</v-icon>
            {{ $t('Add device') }}
          </v-btn>
        </v-row>
        <v-window v-model="tab">
          <v-window-item value="patient">
            <v-row>
              <v-col :cols="smAndDown ? '12' : '4'">
                <v-text-field :label="$t('Health care number')" placeholder="999999999" color="primary" v-model="patient.sns"
                  :disabled="routeName == 'PatientEdit'" :rules="snsRules" maxlength="9" />
              </v-col>
              <v-col :cols="smAndDown ? '12' : '4'">
                <v-text-field :label="$t('Name')" placeholder="John" color="primary" v-model="patient.nome" :rules="nameRules"
                  maxlength="50" :disabled="!isSnsFilled" />
              </v-col>
              <v-col :cols="smAndDown ? '12' : '4'">
                <v-text-field :label="$t('Email')" placeholder="@email" color="primary" v-model="patient.email" type="email" :rules="emailRules"
                  maxlength="50" :disabled="!isSnsFilled" />
              </v-col>
              <v-col :cols="smAndDown ? '12' : '2'">
                <v-select :label="$t('Gender')" :items="['Masculino', 'Feminino']" v-model="patient.genero"
                  :rules="genderRules" :disabled="!isSnsFilled"></v-select>
              </v-col>
              <v-col :cols="smAndDown ? '12' : '3'">
                <v-text-field :label="$t('Birthdate')" placeholder="aaaa-mm-dd" color="primary"
                  v-model="patient.dataNascimento" :rules="dateRules" :disabled="!isSnsFilled" />
              </v-col>
              <v-col :cols="smAndDown ? '12' : '2'">
                <v-text-field :label="$t('Weight (kg)')" color="primary" v-model="patient.peso" :rules="weightRules"
                  maxlength="3" :disabled="!isSnsFilled" />
              </v-col>
              <v-col :cols="smAndDown ? '12' : '2'">
                <v-text-field :label="$t('Height (cm)')" color="primary" v-model="patient.altura" :rules="heightRules"
                  maxlength="3" :disabled="!isSnsFilled" />
              </v-col>
              <v-col :cols="smAndDown ? '12' : '3'">
                <v-text-field :label="$t('phoneNumber')" placeholder="910123456" color="primary" v-model="patient.telefone"
                  :rules="phoneRules" maxlength="9" :disabled="!isSnsFilled" />
              </v-col>
            </v-row>

          </v-window-item>
          <v-window-item :value="indexDispositivo">
            <div v-if="tab !== 'patient'">
              <v-row style="background-color: antiquewhite; padding: 10px;">
                <v-col xs="12" :cols="smAndDown ? '12' : '4'">
                  <v-text-field :label="$t('Serial Number')" color="primary"
                    v-model="patient.dispositivos[indexDispositivo].numeroSerie" />
                </v-col>
                <v-col :cols="smAndDown ? '12' : '4'">
                  <v-text-field :label="$t('manufacturer')" color="primary"
                    v-model="patient.dispositivos[indexDispositivo].fabricante" />
                </v-col>
                <v-col :cols="smAndDown ? '12' : '4'">
                  <v-text-field label="Model" color="primary" v-model="patient.dispositivos[indexDispositivo].modelo" />
                </v-col>
                <v-col :cols="smAndDown ? '12' : '4'">
                  <v-text-field label="Description" color="primary"
                    v-model="patient.dispositivos[indexDispositivo].descricao" />
                </v-col>
                <v-col :cols="smAndDown ? '12' : '4'">
                  <v-text-field label="Start Date" placeholder="yyyy-mm-dd" color="primary" :rules="dataInicioRules"
                    v-model="patient.dispositivos[indexDispositivo].data_inicio" />
                </v-col>
                <v-col :cols="smAndDown ? '12' : '4'">
                  <v-text-field label="End Date" placeholder="yyyy-mm-dd" color="primary" :rules="dataFimRules"
                    v-model="patient.dispositivos[indexDispositivo].data_fim" />
                </v-col>
                <v-col>
                  <v-btn color="red"
                    @click="deleteDevice(indexDispositivo)"><v-icon>mdi-trash-can-outline</v-icon></v-btn>
                </v-col>
                <v-btn @click="addSinalVital(patient.dispositivos[indexDispositivo].sinaisVitais)"
                  v-if="patient.dispositivos[indexDispositivo].numeroSerie" color="indigo-darken-3">
                  <v-icon class="mr-2" color="white">mdi-plus</v-icon>
                  {{$t('Add vital sign')}}
                </v-btn>
              </v-row>
              <v-row v-for="(vital, index) in patient.dispositivos[indexDispositivo].sinaisVitais" :key="index"
                style="background-color: lightcyan; padding: 10px;">

                <v-col :cols="smAndDown ? '12' : '4'">
                  <v-select v-model="vital.tipo" label="Vital Sign"
                    :items="['Frequência Cardíaca', 'Saturação Oxigênio', 'Temperatura']">
                  </v-select>
                </v-col>
                <v-col :cols="smAndDown ? '12' : '2'">
                  <v-text-field label="Unit" color="primary" v-model="vital.unidade"
                    :value="vital.unidade = unidade(vital.tipo)" />
                </v-col>

                <v-col :cols="smAndDown ? '12' : '1'">
                  <v-text-field label="Max" type="number" color="primary" v-model="vital.maximo" />
                </v-col>
                <v-col :cols="smAndDown ? '12' : '1'">
                  <v-text-field label="Min" type="number" color="primary" v-model="vital.minimo" />
                </v-col>
                <v-col :cols="smAndDown ? '12' : '3'">
                  <v-text-field :label="$t('readingFrequency')" type="number" color="primary" v-model="vital.readingFrequency" />
                </v-col>
                <v-col :cols="smAndDown ? '12' : '1'">
                  <v-btn color="red"
                    @click="deleteSinal(indexDispositivo, index)"><v-icon>mdi-trash-can-outline</v-icon></v-btn>
                </v-col>

              </v-row>
            </div>
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-form>
    <span v-if="test"></span>
  </v-card>

</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import { isBefore, isValid, isAfter, isSameDay } from 'date-fns'
import { useUsersStore } from '@/stores/users';
import { useDisplay } from 'vuetify'
const { smAndDown } = useDisplay()

const props = defineProps(['patient'])
const emit = defineEmits(['validationChanged', 'areAllFieldsNonEmpty'])

const route = useRoute()
const routeName = route.name

const user = useUsersStore().user

const isFormValid = ref(false)

const tab = ref('patient')

const indexDispositivo = ref('')

watch(tab, (changedTab) => {
  indexDispositivo.value = changedTab
});


const validationStatus = () => {
  emit('validationChanged', isFormValid.value)
  emit('areAllFieldsNonEmpty', test.value)
}

const addSinalVital = (vital) => {
  vital.push({
    tipo: null,
    unidade: null,
    maximo: null,
    minimo: null,
    valores: [],
    ativo: false,
    readingFrequency: 5
  })
}

const addDevice = (dispositivo) => {
  dispositivo.push({
    profissionais: [
      {
        id: user.user_id,
        role: user.groups[0]
      }
    ],
    fabricante: null,
    modelo: null,
    numeroSerie: null,
    descricao: null,
    data_inicio: today(),
    data_fim: tomorrow(),
    ativo: false,
    sinaisVitais: []
  })
  tab.value = dispositivo.length - 1
}

const tomorrow = () => {
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(today.getDate() + 1);
  const year = tomorrow.getFullYear();
  const month = String(tomorrow.getMonth() + 1).padStart(2, '0'); // Months are zero-based
  const day = String(tomorrow.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

const today = () => {
  return new Date().toISOString().split('T')[0]
}

const deleteDevice = (index) => {
  props.patient.dispositivos.splice(index, 1)
  tab.value = 'patient'
}

const deleteSinal = (indexDispositivo, index) => {
  props.patient.dispositivos[indexDispositivo].sinaisVitais.splice(index, 1)
}

const unidade = (tipo) => {
  if (tipo == 'Frequência Cardíaca') {
    return 'bpm'
  } else if (tipo == 'Blood pressure') {
    return 'mmHg'
  } else if (tipo == 'Saturação Oxigênio') {
    return '%'
  } else if (tipo == 'Temperatura') {
    return '°C'
  } else if (tipo == 'Calories burned') {
    return 'cal'
  } else {
    return ''
  }
}

//Validations

const nameRules = [
  v => !!v || 'Name is required',
  v => (v && v.length >= 3) || 'Name must be at least 3 characters'
]

const dateRules = [
  v => !!v || 'Date of birth is required',
  v => isValid(new Date(v)) || 'Date of birth is not valid',
  v => /^\d{4}-\d{2}-\d{2}$/.test(v) || 'Date must be in YYYY-MM-DD format',
  v => {
    const date = new Date(v)
    const today = new Date()
    return isBefore(date, today) || 'Date must be before or equal to today'
  }
]

const genderRules = [
  v => !!v || 'Gender is required'
]

const weightRules = [
  v => !!v || 'Weight is required',
  v => /^\d+(\.\d+)?$/.test(v) || 'Weight must be a number',
  v => (v >= 0 && v <= 1000) || 'Weight must be between 0 and 1000'
]

const heightRules = [
  v => !!v || 'Height is required',
  v => /^\d+(\.\d+)?$/.test(v) || 'Height must be a number',
  v => (v >= 0 && v <= 300) || 'Height must be between 0 and 300'
]

const phoneRules = [
  v => !!v || 'Phone number is required',
  v => /^\d{9}$/.test(v) || 'Phone number must have exactly 9 digits',
  v => /^\d+$/.test(v) || 'Phone number must contain only numbers'
]

const snsRules = [
  v => !!v || 'SNS number is required',
  v => /^\d{9}$/.test(v) || 'SNS number must have exactly 9 digits',
  v => /^\d+$/.test(v) || 'SNS number must contain only numbers'
]

const isSnsFilled = computed(() => {
  const errors = snsRules.map(rule => rule(props.patient.sns)).filter(result => result !== true);
  return errors.length === 0
})

const dataInicioRules = [
  v => !!v || 'Start date is required',
  v => isValid(new Date(v)) || 'Start date is not valid',
  v => /^\d{4}-\d{2}-\d{2}$/.test(v) || 'Date must be in YYYY-MM-DD format',
  v => {
    const date = new Date(v)
    const today = new Date()
    return (isAfter(date, today) || isSameDay(date, today)) || 'Date must be after or equal to today'
  }
]

const emailRules = [
  v => !!v || 'Email is required',
  v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
]

const dataFimRules = [
  v => !!v || 'End date is required',
  v => isValid(new Date(v)) || 'End date is not valid',
  v => /^\d{4}-\d{2}-\d{2}$/.test(v) || 'Date must be in YYYY-MM-DD format',
  v => {
    const date = new Date(v)
    const today = new Date()
    return isAfter(date, today) || 'Date must be after or equal to today'
  },
  v => {
    const date = new Date(v)
    const dataInicio = new Date(props.patient.dispositivos[indexDispositivo.value].data_inicio)
    return isAfter(date, dataInicio) || 'Date must be after beginning date'
  }
]

const test = computed(() => {
  for (const key in props.patient) {
    if (props.patient[key] === null || props.patient[key] === '') {
      emit('areAllFieldsNonEmpty', false)
      return false
    }
    if (key === 'dispositivos') {
      for (const dispositivo of props.patient[key]) {
        for (const key in dispositivo) {
          if (dispositivo[key] === null || dispositivo[key] === '') {
            emit('areAllFieldsNonEmpty', false)
            return false
          }
          if (key === 'sinaisVitais') {
            for (const vital of dispositivo[key]) {
              for (const key in vital) {
                if (vital[key] === null || vital[key] === '') {
                  emit('areAllFieldsNonEmpty', false)
                  return false
                }
              }
            }
          }
        }
      }
    }
  }
  emit('areAllFieldsNonEmpty', true)
  return true
});
</script>


<style scoped>
.card {
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px;
  border-color: blue;
}
</style>