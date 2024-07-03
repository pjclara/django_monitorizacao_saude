import {  ref } from 'vue'
import { defineStore } from 'pinia'
import { useVitalSignsStore } from './vitalSigns'

export const usePatientsStore = defineStore('patients', () => {
    const patients = ref([])
    const patient = ref({})
    const devices = ref([])
    const devicesActive = ref([])
    const vitalSigns = ref([])
    const vitalSignActive = ref([])

    const fetchPatients = async (user_id) => {
      const response = await fetch(window.URL + '/api/patients/listar_documentos_com_profissionais/' + user_id + '/');
      if (!response.ok) {
        console.log('Error loading patients')
        return
      }
      const data = await response.json()
      patients.value = data

      useVitalSignsStore().createStart(data);

      getAllAtiveDevicesAndVitalSigns()

    }

    const fetchPatient = async (patient_id) => {
      const response = await fetch(window.URL + '/api/patients/listar_documentos_com_profissionais/' + patient_id + '/');
      if (!response.ok) {
        console.log('Error loading patient')
        return
      }
      const data = await response.json()
      patient.value = data
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
    
    return { patient, patients, fetchPatients, fetchPatient, devices, devicesActive, vitalSigns, vitalSignActive, getAllAtiveDevicesAndVitalSigns }
})