import { ref } from 'vue'
import { defineStore } from 'pinia'
import { toast } from 'vue3-toastify'

export const useVitalSignsStore = defineStore('vitalSigns', () => {
  const activation = ref([])
  const disabled = ref(false)
  const start = ref([])
  const loading = ref([])

  const desativarSinal = async (patient, indexSinal, index) => {
    const response = await fetch(
      window.URL + `/api/documentos/desativar_sinal_vital/${patient.sns}/`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          dispositivo_idx: indexSinal,
          sinal_idx: index
        })
      }
    )
    if (!response.ok) {
      throw new Error('Failed to fetch data')
    }
    toast.success('Data creation stopped')
  }

  const ativarSinal = async (patient, indexSinal, index) => {
    const max =
      patient.dispositivos[indexSinal].sinaisVitais[index].maximo +
      patient.dispositivos[indexSinal].sinaisVitais[index].maximo * 0.1
    const min =
      patient.dispositivos[indexSinal].sinaisVitais[index].minimo -
      patient.dispositivos[indexSinal].sinaisVitais[index].minimo * 0.1
    const randomValue = Math.floor(Math.random() * (max - min + 1) + min)
    const response = await fetch(
      window.URL + `/api/documentos/ativar_sinal_vital/${patient.sns}/`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          dispositivo_idx: indexSinal,
          sinal_idx: index,
          valor: randomValue
        })
      }
    )
    if (!response.ok) {
      throw new Error('Failed to fetch data')
    }
  }

  let intervalId = []

  const startGenerateData = (patient, indexSinal, index) => {
    const readingFrequency = patient.dispositivos[indexSinal].sinaisVitais[index].readingFrequency
    toast.success('Data creation started')
    if (!intervalId[index]) {
      intervalId[index] = setInterval(async () => {
        await ativarSinal(patient, indexSinal, index)
      }, readingFrequency * 1000)
    }
  }

  const stopGeneratingData = async (patient, indexSinal, index) => {
    if (intervalId[index]) {
      clearInterval(intervalId[index])
      await desativarSinal(patient, indexSinal, index)
      intervalId[index] = null
    }
  }

  const updateStart = (sns, indexSinal, index, value) => {
    const item = start.value.find(
      (item) => item.patient === sns && item.indexSinal === indexSinal && item.index === index
    )
    if (item) {
      item.start = value
    } else {
      console.log('Error updating start')
    }
  }

  const createStart = (patients) => {
    if (start.value.length > 0) {
      return
    }
    const items = []
    patients.forEach((patient) => {
      patient.dispositivos.forEach((dispositivo, indexSinal) => {
        dispositivo.sinaisVitais.forEach((sinal, index) => {
          items.push({
            patient: patient.sns,
            start: false,
            indexSinal: indexSinal,
            index: index
          })
        })
      })
    })
    start.value = items
  }

  return {
    activation,
    startGenerateData,
    stopGeneratingData,
    disabled,
    start,
    loading,
    updateStart,
    createStart
  }
})
