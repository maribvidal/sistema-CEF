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
    <v-list nav density="compact">

      <v-list-item title="Inicio" :prepend-icon="appMenuIcons.home" to="/" />
      <v-list-item title="Iniciar Sesión" :prepend-icon="appMenuIcons.login" to="/inicioSesion" />
      <v-list-item title="Clases" :prepend-icon="appMenuIcons.classes" to="/clases" />
      <v-list-item title="NOSOTROS" :prepend-icon="appMenuIcons.about" to="/sobre-nosotros" />
      
      <!-- Botón de Registro modificado con ícono, block para estirarse y márgenes -->
      <v-btn variant="flat" color="red" class="text-none text-subtitle-1 mt-2 ml-1 px-6" to="/registro">
                <v-icon start>mdi-account-plus</v-icon>
                Registrarse
            </v-btn>
            
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { computed } from 'vue'

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
  background: #fff;
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
  margin-bottom: 8px; /* Separación entre botones */
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
}

/* Fuerza a que el menú desaparezca del todo si no está activo */
.is-closed {
  opacity: 0 !important;
  pointer-events: none !important;
  visibility: hidden !important; /* Asegura que no estorbe los clics en el fondo */
  transform: translateX(-150%) !important; /* Lo empuja bien fuera de la pantalla */
}
</style>