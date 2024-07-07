import { ref } from 'vue'
import { defineStore } from 'pinia'
import { toast } from 'vue3-toastify'
import { useUsersStore } from './users'

export const useNotificationsStore = defineStore('notifications', () => {
  const notifications = ref([])
  const notification = ref({})
  const notificationsRead = ref([])
  const notificationsNotRead = ref([])
  const token = useUsersStore().token


  const fetchNotifications = async (user_id) => {
    const response = await fetch(window.URL + '/api/listar_notificacoes/' + user_id + '/',{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      }
    
    })
    if (!response.ok) {
      console.log('Error loading notifications')
      return
    }
    const data = await response.json()
    notifications.value = data
    getNotificationsRead()
    getNotificationsNotRead()
  }

  const getNotificationsRead = () => {
    notificationsRead.value = []
    notifications.value.forEach((notification) => {
      if (notification.read) {
        notificationsRead.value.push(notification)
      }
    })
  }

  const getNotificationsNotRead = () => {
    notificationsNotRead.value = []
    notifications.value.forEach((notification) => {
      if (!notification.read) {
        notificationsNotRead.value.push(notification)
      }
    })
  }

  const markAsRead = async (id) => {
    const data = notificationsNotRead.value.find((notification) => notification._id === id)
    data.read = true
    try {
      const response = await fetch(window.URL + '/api/update_notificacao/' + data._id + '/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token,
          
        },
        body: JSON.stringify(data)
      })
      if (!response.ok) {
        throw new Error('Failed to fetch data')
      } else {
        toast.success('Notification read')
        getNotificationsRead()
        getNotificationsNotRead()
      }
    } catch (error) {
      console.error(error)
    }
  }

  const reset = () => {
    notifications.value = []
    notification.value = {}
    notificationsRead.value = []
    notificationsNotRead.value = []
  }

  return {
    notification,
    notifications,
    fetchNotifications,
    notificationsRead,
    notificationsNotRead,
    getNotificationsRead,
    markAsRead,
    getNotificationsNotRead,
    reset
  }
})
