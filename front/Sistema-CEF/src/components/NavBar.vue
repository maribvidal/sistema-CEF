<template>
    <v-navigation-drawer v-model="localMenuOpen" temporary location="left">
        <v-list>
          <v-list-item title="Inicio" :prepend-icon="appMenuIcons.home" to="/" />
          <v-list-item title="Inicio de sesión" :prepend-icon="appMenuIcons.login" to="/inicioSesion" />
          <v-list-item title="Sobre Nosotros" :prepend-icon="appMenuIcons.about" />
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

</style>