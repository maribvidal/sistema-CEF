<template>
  <v-navigation-drawer
    v-model="localMenuOpen"
    class="menu-drawer"
    :class="{ 'is-closed': !localMenuOpen }"
    temporary
    location="left"
    rail
    :rail-width="60"
    width="280" 
    expand-on-hover
  >
    <v-list nav density="compact" class="menu-content">
      <v-btn density="comfortable" rounded="circle" class="theme-btn" color="blue-darken-3" variant="flat" @click="toggleTheme">
                <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-moon-waning-crescent' }}</v-icon>
            </v-btn>
      <v-list-item class="menu-link-item" to="/">
        <v-btn variant="text" class="menu-link menu-button text-none text-subtitle-1" color="blue-darken-3">
          <v-icon start>{{ appMenuIcons.home }}</v-icon>
          Inicio
        </v-btn>
      </v-list-item>

    

      <v-list-item class="menu-link-item" to="/clases">
        <v-btn variant="text" class="menu-link menu-button text-none text-subtitle-1" color="blue-darken-3">
          <v-icon start>{{ appMenuIcons.classes }}</v-icon>
          Clases
        </v-btn>
      </v-list-item>

      <v-list-item class="menu-link-item" to="/sobre-nosotros">
        <v-btn variant="text" class="menu-link menu-button text-none text-subtitle-1" color="blue-darken-3">
          <v-icon start>{{ appMenuIcons.about }}</v-icon>
          Nosotros
        </v-btn>
      </v-list-item>
      <v-btn variant="flat" class="menu-register text-none text-subtitle-1 mt-2 ml-1 px-6" color="blue-darken-3" to="/inicioSesion" v-if="!isLoggedIn">
          <v-icon start>{{ appMenuIcons.login }}</v-icon>
          Iniciar Sesión
        </v-btn>
      <v-btn variant="flat" color="red-darken-2" class="menu-register text-none text-subtitle-1 mt-2 ml-1 px-6" to="/registro" v-if="!isLoggedIn">
        <v-icon start>mdi-account-plus</v-icon>
        Registrarse
      </v-btn>
      <v-btn variant="text" class="text-none text-subtitle-1 mx-1" color="blue-darken-3" to="/clases">
        <v-icon start>{{ appMenuIcons.classes }}</v-icon>
        Clases
      </v-btn>
      <v-btn variant="text" class="text-none text-subtitle-1 mx-1" color="blue-darken-3" to="/administracionEmpleados" v-if="userProfile?.rol === 1 || userRole === 1">Administracion de empleados</v-btn>
      

      <!-- Mostrar nombre de usuario si está autenticado -->
            <v-btn variant="text" class="text-none text-subtitle-1 mx-1" color="blue-darken-3"  :to="{ name: 'perfil', params: { id: userProfile?.id } }" v-if="isLoggedIn">
                <v-avatar size="32" class="mr-2" v-if="userProfile?.avatarUrl">
                    <v-img :src="userProfile?.avatarUrl" alt="Foto de perfil" cover></v-img>
                </v-avatar>
                <v-icon size="32" class="mr-2" v-else>mdi-account-circle</v-icon>
                Mi Perfil: {{ userProfile?.nombre || 'Usuario' }}
            </v-btn>

      <v-btn variant="flat" color="red-darken-2" class="menu-register text-none text-subtitle-1 mt-2 ml-1 px-6" @click="handleLogout" v-if="isLoggedIn">
        <v-icon start>mdi-logout</v-icon>
        Cerrar Sesión
      </v-btn>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/services/UsuariosServices.js'
import { useTheme } from 'vuetify'

const theme = useTheme()
const isDark = computed(() => theme.global.name.value === 'dark')

function toggleTheme() {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
  // Si también querés aplicar el data-theme en html para custom properties (por si se usan)
  document.documentElement.setAttribute('data-theme', theme.global.name.value)
}

const router = useRouter()
const { isLoggedIn, userProfile, logout } = useAuth()
const userRole = computed(() => userProfile.value?.rol || null)
const handleLogout = async () => {
    await logout()
    router.push('/inicioSesion')
}
const props = defineProps({
  modelValue: { type: Boolean, default: false },
  appMenuIcons: { type: Object, required: true },
})

const emit = defineEmits(['update:modelValue'])

const localMenuOpen = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})
</script>

<style scoped>
.menu-drawer {
  top: 20px !important;
  left: 16px !important;
  bottom: auto !important;   /* evita que se estire hasta abajo */
  height: auto !important;   /* alto según contenido */
  max-height: calc(100vh - 48px);
  border-radius: 9px;
  overflow: hidden;
  background: var(--bg-card);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
  transition-property: all; /* Suaviza la animación */
  transition-duration: 600ms;

  margin-top: 60px; /* Separación del botón */
}

/* Sobrescribe la clase .is-closed para que se oculte hacia arriba y baje al abrirse */
.menu-drawer.is-closed {
  transform: translateY(-150%) !important;
}

.menu-drawer .close-item {
  justify-content: center;
}

.menu-drawer :deep(.v-list) {
  padding-block: 8px;
}

.menu-content {
  gap: 4px;
}

.menu-link-item {
  padding-inline: 0 !important;
  min-height: auto !important;
}

.menu-link {
  width: 100%;
  justify-content: flex-start;
  padding-inline: 12px;
  border-radius: 8px;
  transition: background-color 0.2s ease, color 0.2s ease, transform 0.2s ease;
}

.menu-button:hover {
  background-color: rgba(25, 118, 210, 0.08);
  transform: translateX(2px);
}

.menu-register {
  width: calc(100% - 8px);
  align-self: center;
  border-radius: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.menu-register:hover {
  transform: translateX(2px);
}

.menu-drawer :deep(.close-item .v-list-item__prepend) {
  margin-inline-end: 0 !important;
}

.menu-drawer :deep(.close-item .v-list-item__content) {
  display: none !important; /* El botón de cerrar nunca muestra texto */
}

.menu-drawer :deep(.close-item.v-list-item) {
  padding-inline: 0 !important;
  justify-content: center !important;
}

.menu-drawer :deep(.v-navigation-drawer__content) {
  border-radius: 9px;
  height: auto !important;
  overflow: hidden;
}

.menu-drawer :deep(.v-list-item) {
  margin-bottom: 4px; /* Separación entre botones */
}

.menu-drawer :deep(.v-list-item__content) {
    font-weight: 600;
    letter-spacing: 1px;
    font-size: 0.875rem;
}

@media (max-width: 768px) {
  .menu-drawer {
    top: 16px !important;
    left: auto !important;
    bottom: auto !important;
    right: 16px !important;
    width: auto !important;
    max-width: 90vw;
    height: auto !important;
    max-height: 60vh;
  }

  .menu-register {
    width: 100%;
  }
}

.theme-btn {
    border-radius: 100% !important;
    transition: background-color 0.3s ease, color 0.3s ease;
    max-block-size: 50px;
    max-width: 30px;
    margin-right: 30px;
}

/* Fuerza a que el menú desaparezca del todo si no está activo */
.is-closed {
  opacity: 0 !important;
  pointer-events: none !important;
  visibility: hidden !important; /* Asegura que no estorbe los clics en el fondo */
  transform: translateX(-150%) !important; /* Lo empuja bien fuera de la pantalla */
}
</style>