import { ref } from 'vue'
import { defineStore } from 'pinia'
import { toast } from 'vue3-toastify'
import { useUsersStore } from './users'
import { useLoaderStore } from '@/stores/loader'

export const useNotificationsStore = defineStore('notifications', () => {
  const notifications = ref([])
  const notification = ref({})
  const notificationsRead = ref([])
  const notificationsNotRead = ref([])
  const token = useUsersStore().token
  const loaderStore = useLoaderStore()


  

  const fetchNotifications = async (user_id) => {
    const response = await fetch(window.URL + '/api/listar_notificacoes/' + user_id + '/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + token
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

  const processedNotifications = ref([])

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
        //console.log(notification)
      }
    })
  }

  const markAsRead = async (id) => {
    loaderStore.setLoading(true)
    const data = notificationsNotRead.value.find((notification) => notification._id === id)
    data.read = true
    try {
      const response = await fetch(window.URL + '/api/update_notificacao/' + data._id + '/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + token
        },
        body: JSON.stringify(data)
      })
      if (!response.ok) {
        throw new Error('Failed to fetch data')
      } else {
        toast.success('Notification read')
        // delete from notificationsNotRead
        const index = notificationsNotRead.value.findIndex((notification) => notification._id === id)
        notificationsNotRead.value.splice(index, 1)
        // add to notificationsRead
        notificationsRead.value.push(data)
      }
      loaderStore.setLoading(false)
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
