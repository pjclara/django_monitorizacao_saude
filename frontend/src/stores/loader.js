import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useLoaderStore = defineStore('loader', () => {
  const showLoading = ref(false)

  const setLoading = (value) => {
    showLoading.value = value
  }

  const createData = ref(false)

  const toggleCreateData = () => {
    createData.value = !createData.value
  }

  const url = 'backend-projecto.fly.dev'
  window.URL = 'https://' + url

/*
  const url = '127.0.0.1:8000'
  window.URL = 'http://' + url
*/

  return {
    showLoading,
    setLoading,
    createData,
    toggleCreateData,
    url
  }
})
