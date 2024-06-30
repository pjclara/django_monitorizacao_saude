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
    start.value[index] = false
    toast.success('Data creation stopped')
    loading.value[index] = false
  }

  const ativarSinal = async (patient, indexSinal, index) => {
    const max =
      patient.dispositivos[indexSinal].sinaisVitais[index].maximo +
      patient.dispositivos[indexSinal].sinaisVitais[index].maximo * 0.2
    const min =
      patient.dispositivos[indexSinal].sinaisVitais[index].minimo -
      patient.dispositivos[indexSinal].sinaisVitais[index].minimo * 0.2
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
    start.value[index] = true
  }

  let intervalId = []

  const startGenerateData = (patient, indexSinal, index) => {
    start.value[index] = true
    const readingFrequency = patient.dispositivos[indexSinal].sinaisVitais[index].readingFrequency
    toast.success('Data creation started')
    if (!intervalId[index]) {
      intervalId[index] = setInterval(async () => {
        await ativarSinal(patient, indexSinal, index)
      }, readingFrequency * 1000)
      console.log(intervalId)
    }
  }

  const stopGeneratingData = async (patient, indexSinal, index) => {
    if (intervalId[index]) {
      clearInterval(intervalId[index])
      await desativarSinal(patient, indexSinal, index)
      intervalId[index] = null
    }
  }

  return { activation, startGenerateData, stopGeneratingData, disabled, start, loading }
})
