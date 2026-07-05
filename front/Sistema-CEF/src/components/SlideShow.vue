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
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import SlideshowItem from '@/components/SlideShowItem.vue'

// Opcional: Si quieres que Vite empaquete las imágenes, impórtalas o usa de forma estática su ruta.
// Asegúrate de agregar las imágenes correspondientes en la carpeta src/assets/assetsHome/
import img1 from '@/assets/assetsHome/slide1.jpg'
import img2 from '@/assets/assetsHome/slide2.jpg'
import img1phone from '@/assets/assetsHome/slide1phone.png'
import img2phone from '@/assets/assetsHome/slide2phone.png'
//import placeholderImage from '@/assets/images/placeholder.png'

// --- CONFIGURACIÓN ---
const SLIDESHOW_INTERVAL = 10000 // en milisegundos

// --- ESTADO DEL COMPONENTE ---
const isMobile = ref(false)
const slides = computed(() => {
  if (isMobile.value) {
    return [
      {
        id: 'estatico-1',
        titulo: 'Título de prueba 1',
        imagenUrl: img1phone,
        autor: 'Autor 1'
      },
      {
        id: 'estatico-2',
        titulo: 'Título de prueba 2',
        imagenUrl: img2phone,
        autor: 'Autor 2'
      }
    ]
  }
  return [
    {
      id: 'estatico-1',
      titulo: 'Título de prueba 1',
      imagenUrl: img1, 
      autor: 'Autor 1'
    },
    {
      id: 'estatico-2',
      titulo: 'Título de prueba 2',
      imagenUrl: img2,
      autor: 'Autor 2'
    }
  ]
})
const currentSlide = ref(0)
const isLoading = ref(true)
const error = ref(null)
let slideInterval = null

const handleResize = () => {
  isMobile.value = window.innerWidth <= 768
}

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
    // Array estático de prueba manejado por la propiedad computada 'slides'.
  } catch (err) {
    console.error('Error al cargar datos locales para el slideshow:', err)
    error.value = 'No se pudieron cargar los artículos estáticos.'
  } finally {
    isLoading.value = false
  }
}

// --- HOOKS DE CICLO DE VIDA ---
onMounted(() => {
  handleResize()
  window.addEventListener('resize', handleResize)
  
  fetchLatestArticles()
  if (!error.value) {
    startSlideshow()
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
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
  height: 500px;
  overflow: hidden;
  background-color: var(--bg-main);
  color: var(--text-main);
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