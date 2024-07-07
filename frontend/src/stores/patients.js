import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useVitalSignsStore } from './vitalSigns'
import { toast } from 'vue3-toastify'
import { useUsersStore } from './users'
import router from '@/router'
import { useI18n } from 'vue-i18n';



export const usePatientsStore = defineStore('patients', () => {
  const patients = ref([])
  const patient = ref({})
  const devices = ref([])
  const devicesActive = ref([])
  const vitalSigns = ref([])
  const vitalSignActive = ref([])
  const token = useUsersStore().token

  const { t } = useI18n()


  const fetchPatients = async (user_id) => {
    const response = await fetch(
      window.URL + '/api/patients/listar_documentos_com_profissionais/' + user_id + '/',
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + token
        }
      }
    )
    if (!response.ok) {
      console.log('Error loading patients')
      return
    }
    const data = await response.json()
    patients.value = data

    useVitalSignsStore().createStart(data)

    getAllAtiveDevicesAndVitalSigns()
  }

  const getAllAtiveDevicesAndVitalSigns = () => {
    devices.value = []
    vitalSigns.value = []
    devicesActive.value = []
    vitalSignActive.value = []
    patients.value.forEach(async (patient) => {
      patient.dispositivos.forEach(async (device) => {
        devices.value.push(device)
        if (device.ativo) {
          devicesActive.value.push(device)
        }
        device.sinaisVitais.forEach(async (vitalSign) => {
          vitalSigns.value.push(vitalSign)
          if (vitalSign.ativo) {
            vitalSignActive.value.push(vitalSign)
          }
        })
      })
    })
  }

  const atualizarPaciente = async (patient) => {
    const response = await fetch(
      window.URL + '/api/documentos/atualizar_dados_paciente_por_sns/' + patient.sns + '/',
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + token
        },
        body: JSON.stringify(patient)
      }
    )
    if (!response.ok) {
      const data = await response.json()
      console.log('Error updating patient', data)
      return
    }
    const data = await response.json()
    // update patient in patients
    const index = patients.value.findIndex((p) => p.sns === data.data.sns)
    patients.value[index] = data.data
    toast.success(t('Patient updated successfully'))
  }

  const criarPaciente = async (patient) => {
    const response = await fetch(window.URL + '/api/documentos/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + token
      },
      body: JSON.stringify(patient)
    })
    if (!response.ok) {
      console.log('Error creating patient')
      return
    }
    // get the new patient created
    const data = await buscarPaciente(patient.sns)
    patients.value.push(data)
    toast.success('Patient created successfully')
    router.push({ name: 'PatientsListing' });
  }

  const getPaciente = (sns) => {
    patient.value = patients.value.find((p) => p.sns == sns)
    return patient.value
  }

  const buscarPaciente = async (sns) => {
    try {
      const response = await fetch(window.URL + '/api/documentos/buscar_por_sns/' + sns + '/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + localStorage.getItem('token')
        }
      })
      const data = await response.json()
      return data
    } catch (error) {
      console.log('Error loading patient')
      return
    }
  }

  const reset = () => {
    patient.value = {}
    patients.value = []
    devices.value = []
    devicesActive.value = []
    vitalSigns.value = []
    vitalSignActive.value = []
  }

  return {
    patient,
    patients,
    fetchPatients,
    devices,
    devicesActive,
    vitalSigns,
    vitalSignActive,
    getAllAtiveDevicesAndVitalSigns,
    getPaciente,
    atualizarPaciente,
    buscarPaciente,
    criarPaciente,
    reset
  }
})
