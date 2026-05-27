import { defineStore } from 'pinia'
import { ref } from 'vue'
export const useNotificationStore = defineStore('notification', () => {
  const message = ref('')
  const type = ref('info') // 'info', 'success', 'warning', 'danger', 'dark'
  const isVisible = ref(false)
  const duration = ref(10000)
  const id = ref(0)
  const timeoutId = ref(null)
  const isConfirmation = ref(false)
  let acceptCallback = null
  let declineCallback = null

  function showNotification(msg, notificationType = 'info', durationValue = 10000, onAccept = null, onDecline = null) {
    message.value = msg
    type.value = notificationType
    duration.value = durationValue
    id.value = Date.now()
    isVisible.value = true

    acceptCallback = onAccept
    declineCallback = onDecline
    isConfirmation.value = !!(onAccept || onDecline)

    if (timeoutId.value) {
      clearTimeout(timeoutId.value)
    }

    if (durationValue > 0) {
      timeoutId.value = setTimeout(() => {
        hideNotification()
      }, durationValue)
    }
  }

  function hideNotification() {
    isVisible.value = false
    message.value = ''
    type.value = 'info'
    acceptCallback = null
    declineCallback = null
    isConfirmation.value = false
  }

  function acceptNotification() {
    if (acceptCallback) {
      acceptCallback()
    }
    hideNotification()
  }

  function declineNotification() {
    if (declineCallback) {
      declineCallback()
    }
    hideNotification()
  }

  return {
    message,
    type,
    isVisible,
    duration,
    id,
    isConfirmation,
    showNotification,
    hideNotification,
    acceptNotification,
    declineNotification
  }
})