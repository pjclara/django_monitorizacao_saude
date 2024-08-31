import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useI18n } from 'vue-i18n'
import { usePatientsStore } from './patients'
import { useVitalSignsStore } from './vitalSigns'
import { useNotificationsStore } from './notifications'
import { toast } from 'vue3-toastify'

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
        // get user data from token
        const userData = JSON.parse(atob(data.access.split('.')[1]))
        // store token and user data in local storage
        token.value = data.access
        // store token and user data in local storage
        localStorage.setItem('token', data.access)
        // store refresh token in local storage
        refreshToken.value = data.refresh
        // store refresh token in local storage
        localStorage.setItem('refreshToken', data.refresh)
        // store user data in local storage
        user.value = userData
        isLogged.value = true
        // check if user is admin
        isAdmin.value = userData.groups.includes('admin') ? true : false
        // check if user is patient
        isPatient.value = userData.groups.includes('paciente') ? true : false
        // store user data in local storage
        localStorage.setItem('user', JSON.stringify(userData))
  }

  if (localStorage.getItem('user')) {
    user.value = JSON.parse(localStorage.getItem('user'))
    isLogged.value = true
    isAdmin.value = user.value.groups.includes('admin') ? true : false
    isPatient.value = user.value.groups.includes('paciente') ? true : false
    token.value = localStorage.getItem('token')
    refreshToken.value = localStorage.getItem('refreshToken')
  } else {
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

  const deleteUser = async (id) => async () => {
    try {
      const response = await fetch(window.URL + '/api/users/', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify({ email: user.value.email })
      })

      if (response.ok) {
        const data = await response.json()
        // remove user from users list
        users.value = users.value.filter((user) => user.id !== id)
        console.log(users.value)
        return
      } else {
        const errorData = await response.json()
      }
    } catch (error) {
      toast.error('Error deleting user: ' + error)
    }
  }

  const updateUser = async (id, data) => {
    const response = await fetch(window.URL + `/api/users/${id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + localStorage.getItem('token')
      },
      body: JSON.stringify(data)
    })

    if (response.ok) {
      const data = await response.json()
      // update user in users list
      users.value = users.value.map((user) => {
        if (user.id == id) {
          return data
        }
        return user
      })
      return data
    } else {
      const errorData = await response.json()
      return errorData
    }
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
    fetchUserData,
    deleteUser,
    updateUser
  }
})
