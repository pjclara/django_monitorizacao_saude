import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUsersStore = defineStore('patients', () => {
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

    return { patient }
})