import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useVitalSignsStore } from './vitalSigns'
import { toast } from 'vue3-toastify';
import { useI18n } from 'vue-i18n'

export const usePatientsStore = defineStore('patients', () => {
  const patients = ref([])
  const patient = ref({})
  const devices = ref([])
  const devicesActive = ref([])
  const vitalSigns = ref([])
  const vitalSignActive = ref([])

  const { t } = useI18n()

  const fetchPatients = async (user_id) => {
    const response = await fetch(
      window.URL + '/api/patients/listar_documentos_com_profissionais/' + user_id + '/'
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
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(patient)
      }
    )
    if (!response.ok) {
      console.log('Error updating patient')
      return
    }
    const data = await response.json()
    // update patient in patients
    const index = patients.value.findIndex((p) => p.sns === data.data.sns)
    patients.value[index] = data.data
    toast.success(t('Patient updated successfully'))
  }

  const getPaciente = (sns) => {
    patient.value = patients.value.find((p) => p.sns == sns)
    return patient.value
    
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
    atualizarPaciente
  }
})
