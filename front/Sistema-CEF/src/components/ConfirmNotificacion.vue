<template>
  <Transition name="fade">
    <div
      v-if="store.isVisible && store.isConfirmation"
      class="notification-card"
      :class="store.type"
      role="alert"
    >

    <div class="notification-content">
      <span class="notification-title">{{ "Advertencia" }}</span> {{ store.message }}
      </div>
      <button
        @click="store.hideNotification"
        class="close-btn"
        aria-label="Close"
      >
        <svg class="icon" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
        </svg>
      </button>
      <div class="actions">
        <button
          @click="store.acceptNotification"
          class="accept-btn"
          aria-label="Accept"
        >
          Sí
        </button>
        <button
          @click="store.declineNotification"
          class="decline-btn"
          aria-label="Decline"
        >
          No
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
  import { useNotificationStore } from '@/stores/notificationStore.js'

  const store = useNotificationStore()
</script>

<style scoped>
.notification-card {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10000;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 90%;
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-size: 1rem;
  line-height: 1.5;
  background-color: white;
}

.notification-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.notification-title {
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 5px;
  display: block;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.2s;
}

.close-btn:hover {
  opacity: 1;
}

.icon {
  width: 20px;
  height: 20px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 15px;
}

.accept-btn, .decline-btn {
  padding: 8px 20px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.accept-btn {
  background-color: #10b981; /* Emerald 500 */
  color: white;
}
.accept-btn:hover {
  background-color: #059669; /* Emerald 600 */
}

.decline-btn {
  background-color: #ef4444; /* Red 500 */
  color: white;
}
.decline-btn:hover {
  background-color: #dc2626; /* Red 600 */
}

/* Variants - matching FloatingNotification but adapted for modal style */
.info {
  border-top: 5px solid #3b82f6;
  background-color: #ffffff;
  color: #1f2937;
}

.success {
  border-top: 5px solid #22c55e;
  background-color: #ffffff;
  color: #1f2937;
}

.warning {
  border-top: 5px solid #eab308;
  background-color: #ffffff;
  color: #1f2937;
}

.danger {
  border-top: 5px solid #ef4444;
  background-color: #ffffff;
  color: #1f2937;
}

.dark {
  border-top: 5px solid #4b5563;
  background-color: #1f2937;
  color: #f3f4f6;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -60%);
}
</style>