<template>
  <div class="slideshow">
    <!-- Estado de carga -->
    <div v-if="isLoading" class="loading-state">Cargando artículos...</div>

    <!-- Estado de error -->
    <div v-else-if="error" class="error-state">{{ error }}</div>

    <!-- Contenido del Slideshow -->
    <div v-else-if="slides.length > 0" class="slideshow-inner">
      <SlideshowItem
        v-for="(slide, idx) in slides"
        :key="`${slide.id}-${idx}`"
        :slide="slide"
        :current-slide="currentSlide"
        :index="idx"
      />
      <div v-if="slides.length > 1" class="navigation">
        <button @click="prev" class="nav-btn prev-btn" aria-label="Anterior">&#10094;</button>
        <button @click="next" class="nav-btn next-btn" aria-label="Siguiente">&#10095;</button>
      </div>
    </div>

    <!-- Estado vacío -->
    <div v-else class="empty-state">No hay artículos para mostrar.</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import SlideshowItem from '@/components/SlideShowItem.vue'

// Opcional: Si quieres que Vite empaquete las imágenes, impórtalas o usa de forma estática su ruta.
// Asegúrate de agregar las imágenes correspondientes en la carpeta src/assets/assetsHome/
import img1 from '@/assets/assetsHome/slide1.jpg'
import img2 from '@/assets/assetsHome/slide2.jpg'
import img3 from '@/assets/assetsHome/slide3.jpg'
//import placeholderImage from '@/assets/images/placeholder.png'

// --- CONFIGURACIÓN ---
const SLIDESHOW_INTERVAL = 10000 // en milisegundos

// --- ESTADO DEL COMPONENTE ---
const slides = ref([])
const currentSlide = ref(0)
const isLoading = ref(true)
const error = ref(null)
let slideInterval = null

// --- LÓGICA DE NAVEGACIÓN ---
/**
 * Avanza a la siguiente diapositiva y reinicia el intervalo.
 */
const next = () => {
  if (slides.value.length > 1) {
    currentSlide.value = (currentSlide.value + 1) % slides.value.length
    resetInterval()
  }
}

/**
 * Retrocede a la diapositiva anterior y reinicia el intervalo.
 */
const prev = () => {
  if (slides.value.length > 1) {
    currentSlide.value = (currentSlide.value - 1 + slides.value.length) % slides.value.length
    resetInterval()
  }
}

// --- CONTROL DEL SLIDESHOW ---
/**
 * Inicia el temporizador para el cambio automático de diapositivas.
 */
const startSlideshow = () => {
  clearInterval(slideInterval)
  if (slides.value.length > 1) {
    slideInterval = setInterval(next, SLIDESHOW_INTERVAL)
  } else {
    slideInterval = null
  }
}

/**
 * Limpia el intervalo actual y lo reinicia.
 */
const resetInterval = () => {
  clearInterval(slideInterval)
  startSlideshow()
}

// --- CARGA DE DATOS ---
/**
 * Carga los artículos de forma estática usando imágenes locales de assetsHome.
 */
const fetchLatestArticles = () => {
  try {
    // Array estático de prueba para el slideshow. 
    // Puedes reemplazar las imágenes usando imports o rutas directas si están en /public/
    slides.value = [
      {
        id: 'estatico-1',
        titulo: 'Título de prueba 1',
        // imagenUrl: img1, // Descomentar cuando tengas la imagen importada
        imagenUrl: img1, 
        autor: 'Autor 1'
      },
      {
        id: 'estatico-2',
        titulo: 'Título de prueba 2',
        imagenUrl: img2,
        autor: 'Autor 2'
      },
      {
        id: 'estatico-3',
        titulo: 'Título de prueba 3',
        imagenUrl: img3,
        autor: 'Autor 3'
      }
    ]
  } catch (err) {
    console.error('Error al cargar datos locales para el slideshow:', err)
    error.value = 'No se pudieron cargar los artículos estáticos.'
  } finally {
    isLoading.value = false
  }
}

// --- HOOKS DE CICLO DE VIDA ---
onMounted(() => {
  fetchLatestArticles()
  if (!error.value) {
    startSlideshow()
  }
})

onBeforeUnmount(() => {
  clearInterval(slideInterval)
})
</script>

<style scoped>
.slideshow {
  position: relative; /* Necesario para posicionar los botones */
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 600px;
  overflow: hidden;
  background-color: #f0f0f0;
  color: #333;
  border-radius: 8px;
}
.slideshow-inner {
  position: relative;
  width: 100%;
  height: 100%;
}
.loading-state,
.error-state,
.empty-state {
  font-size: 1.2rem;
  font-style: italic;
}

.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.3);
  color: white;
  border: none;
  padding: 10px 15px;
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: background-color 0.3s ease;
  z-index: 10;
}

.nav-btn:hover {
  background-color: rgba(0, 0, 0, 0.6);
}

.prev-btn {
  left: 20px;
}

.next-btn {
  right: 20px;
}
@media (max-width: 768px) {
  .slideshow{
    width: 100%;
  }
    
}
</style>