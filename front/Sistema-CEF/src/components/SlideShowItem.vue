<template>
  <transition name="slide-in">
    <div class="slideshow-item" v-if="currentSlide === index">
      <!-- El componente entero es un enlace que lleva al detalle del artículo -->
      <RouterLink :to="'/articulo/' + slide.id" class="slide-link">
        <img :src="slide.imagenUrl" :alt="slide.titulo" />
        <div class="slide-caption">
          <h3>{{ slide.titulo }}</h3>
          <a>Por: {{ slide.autor }}</a>
        </div>
      </RouterLink>
    </div>
  </transition>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  /**
   * Objeto con los datos de la diapositiva (id, titulo, imagenUrl).
   * @type {Object}
   */
  slide: Object,
  /**
   * El índice de esta diapositiva en el array.
   * @type {Number}
   */
  index: Number,
  /**
   * El índice de la diapositiva actualmente activa.
   * @type {Number}
   */
  currentSlide: Number
})
</script>

<style scoped>
.slideshow-item {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.slide-link {
  position: relative;
  display: block;
  width: 100%;
  height: 100%;
  color: inherit;
  text-decoration: none;
}

.slideshow-item img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover; /* Asegura que la imagen llene el contenedor sin deformarse */
}

/* Título superpuesto sobre la imagen */
.slide-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 2rem 1.5rem 1.5rem;
  color: white;
  text-align: left;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0) 100%);
}

.slide-caption h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: bold;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
}

/* Transiciones de entrada y salida */
.slide-in-enter-active,
.slide-in-leave-active {
  transition: all 1s ease;
}

.slide-in-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.slide-in-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>