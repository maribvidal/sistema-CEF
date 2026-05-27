<template>
  <Transition name="fade">
    <div
      v-if="store.isVisible && !store.isConfirmation"
      class="notification-card"
      :class="store.type"
      role="alert"
    >

      <div class="notification-content">
        <span class="notification-icon">
          <svg class="icon" fill="currentColor" :viewBox="icons[store.type]?.viewBox || '0 0 20 20'" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" :d="icons[store.type]?.d" clip-rule="evenodd"></path>
          </svg>
        </span>
        <span class="message-text">{{ store.message }}</span>
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
    </div>
  </Transition>
</template>

<script setup>
import { useNotificationStore } from '@/stores/notificationStore.js'

const store = useNotificationStore()

const icons = {
  info: {
    viewBox: '0 0 20 20',
    d: 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z'
  },
  success: {
    viewBox: '0 0 20 20',
    d: 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z'
  },
  warning: {
    viewBox: '0 0 20 20',
    d: 'M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z'
  },
  danger: {
    viewBox: '0 0 20 20',
    d: 'M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z'
  },
  dark: {
    viewBox: '0 0 20 20',
    d: 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z'
  }
}
</script>

<style scoped>
.notification-card {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  padding: 16px;
  margin-bottom: 16px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 24rem;
  width: 100%;
  display: flex;
  align-items: flex-end;
  font-size: 0.875rem;
  line-height: 1.25rem;
  transition: all 0.3s ease;
}

.notification-content {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
}

.notification-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-icon .icon {
  width: 24px;
  height: 24px;
}

.message-text {
  font-weight: 500;
}

.close-btn {
  margin-left: 12px;
  background: transparent;
  border: none;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
  padding: 0;
  display: flex;
  align-items: center;
}

.close-btn:hover {
  opacity: 1;
}

.icon {
  width: 16px;
  height: 16px;
}



/* Variants */
.info {
  background-color: #eff6ff;
  color: #1e40af;
  border-left: 4px solid #3b82f6;
}

.success {
  background-color: #f0fdf4;
  color: #166534;
  border-left: 4px solid #22c55e;
}

.warning {
  background-color: #fefce8;
  color: #854d0e;
  border-left: 4px solid #eab308;
}

.danger {
  background-color: #fef2f2;
  color: #991b1b;
  border-left: 4px solid #ef4444;
}

.dark {
  background-color: #1f2937;
  color: #f3f4f6;
  border-left: 4px solid #4b5563;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}


.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-20px);
}

.progress-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 4px;
  background-color: rgba(0, 0, 0, 0.15);
  width: 100%;
  animation: progress linear forwards;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}

@keyframes progress {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}
</style>