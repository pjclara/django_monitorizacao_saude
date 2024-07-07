import { ref } from 'vue'
import { defineStore } from 'pinia'
import { toast } from 'vue3-toastify';
import { useI18n } from 'vue-i18n';
import { usePatientsStore } from './patients';
import { useVitalSignsStore } from './vitalSigns';
import { useNotificationsStore } from './notifications';


export const useUsersStore = defineStore('users', () => {
  const user = ref(null)
  const users = ref([])
  const token = ref(null)
  const refreshToken = ref(null)
  const isLogged = ref(!!user.value)
  const isAdmin = ref(false)
  const isPatient = ref(false)

  const { t } = useI18n()

  const groups = ref([])

  const loopAtivo = ref(false)

  const logOut = () => {
    usePatientsStore().reset()
    useVitalSignsStore().reset()
    useNotificationsStore().reset()
    user.value = null
    token.value = null
    refreshToken.value = null
    isLogged.value = false
    localStorage.removeItem('user')
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')

    
  }

  const logIn = async (email, password) => {
    const response = await fetch(window.URL + '/api/token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    })
    if (response.status !== 200) {
      toast.error(t('Username or password is invalid!'))
      return
    }
    const data = await response.json()
    const userData = JSON.parse(atob(data.access.split('.')[1]))
    token.value = data.access
    localStorage.setItem('token', data.access)
    refreshToken.value = data.refresh
    localStorage.setItem('refreshToken', data.refresh)
    user.value = userData
    isLogged.value = true
    isAdmin.value = userData.groups.includes('admin') ? true : false
    isPatient.value = userData.groups.includes('paciente') ? true : false
    localStorage.setItem('user', JSON.stringify(userData))
  }

  if (localStorage.getItem('user')) {
    user.value = JSON.parse(localStorage.getItem('user'))
    isLogged.value = true
    isAdmin.value = user.value.groups.includes('admin') ? true : false
    isPatient.value = user.value.groups.includes('paciente') ? true : false
    token.value = localStorage.getItem('token')
    refreshToken.value = localStorage.getItem('refreshToken')
  }else{ 

    logIn(JSON.parse(localStorage.getItem('user')))
  }

  const fetchUsers = async () => {
    const response = await fetch(window.URL + '/api/users/', {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    if (response.status !== 200) {
      return
    }
    users.value = await response.json()

    return users.value
  }

  const fetchRoles = async () => {
    const response = await fetch(window.URL + '/api/get_groups/', {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    if (response.status !== 200) {
      return
    }
    groups.value = await response.json()

    return groups.value
  }

  const fetchUserData = async (id) => {
    
    const response = await fetch(window.URL + `/api/users/${id}/`, {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    if (response.status !== 200) {
      return
    }
    const data = await response.json()
    return data
  }

  return {
    user,
    isLogged,
    logOut,
    logIn,
    isAdmin,
    loopAtivo,
    isPatient,
    token,
    refreshToken,
    fetchUsers,
    users,
    fetchRoles,
    groups,
    fetchUserData
  }
})
