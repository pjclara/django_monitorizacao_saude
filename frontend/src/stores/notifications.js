import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useNotificationsStore = defineStore('notifications', () => {
  const notifications = ref([])
  const notification = ref({})
  const notificationsRead = ref([])
  const notificationsNotRead = ref([])

  const fetchNotifications = async (user_id) => {
    const response = await fetch(
      window.URL + '/api/listar_notificacoes/' + user_id + '/'
    )
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

  return { notification, notifications, fetchNotifications, notificationsRead, notificationsNotRead, getNotificationsRead, getNotificationsNotRead }
})
