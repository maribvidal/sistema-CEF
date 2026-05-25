
<script setup>
import { ref } from 'vue'
import { Cropper } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'


const props = defineProps({
  currentAvatar: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['image-cropped'])

const fileInput = ref(null)
const imageSrc = ref(null)
const showCropper = ref(false)
const cropper = ref(null)

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Validate file type if needed
    if (file.size > 5 * 1024 * 1024) { // 5MB limit
      alert('El archivo es demasiado grande. Por favor selecciona una imagen menor a 5MB.')
      return
    }
    if (!file.type.startsWith('image/')) {
      alert('Por favor selecciona un archivo de imagen.')
      return
    }

    const reader = new FileReader()
    reader.onload = (e) => {
      imageSrc.value = e.target.result
      showCropper.value = true
    }
    reader.readAsDataURL(file)
  }
  // Reset input
  event.target.value = ''
}

const cropImage = () => {
  const { canvas } = cropper.value.getResult()
  if (canvas) {
    canvas.toBlob((blob) => {
      // Create a File object from the Blob
      const file = new File([blob], "avatar.png", { type: "image/png" })
      emit('image-cropped', file)
      showCropper.value = false
      imageSrc.value = null
    }, 'image/png')
  }
}

const cancelCrop = () => {
  showCropper.value = false
  imageSrc.value = null
}
</script>

<template>
  <div class="avatar-input-wrapper">
    <!-- Avatar Preview with Click to Upload -->
    <div class="avatar-preview"  title="Click para cambiar imagen">
      <img :src="currentAvatar" alt="Avatar" class="avatar-img" />
    </div>
    <button class="btn btn-secondary change-avatar-btn " @click="triggerFileInput" type="button">Cambiar Avatar</button>
    <input
      type="file"
      ref="fileInput"
      class="hidden-input"
      accept="image/*"
      @change="handleFileChange"
    />

    <!-- Cropper Modal -->
    <div v-if="showCropper" class="cropper-modal-overlay">
      <div class="cropper-modal-content">
        <h3>Recortar Imagen</h3>
        <div class="cropper-wrapper">
          <Cropper
            ref="cropper"
            class="cropper"
            :src="imageSrc"
            :stencil-props="{
              aspectRatio: 1/1
            }"
          />
        </div>
        <div class="cropper-actions">
          <button @click="cancelCrop" class="btn btn-secondary" type="button">Cancelar</button>
          <button @click="cropImage" class="btn btn-primary" type="button">Recortar y Guardar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.avatar-input-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.avatar-preview {
  position: relative;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  cursor: pointer;
  overflow: hidden;
  border: 2px solid var(--header-border, #ccc);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.avatar-preview:hover .avatar-overlay {
  opacity: 1;
}

.camera-icon {
  font-size: 2rem;
  color: white;
}

.hidden-input {
  display: none;
}

/* Modal Styles */
.cropper-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.cropper-modal-content {
  background: var(--header-bg, white);
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.cropper-wrapper {
  height: 400px;
  background: #333;
}

.cropper {
  height: 100%;
  width: 100%;
}

.cropper-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.btn-primary {
  background-color: var(--title-color, #007bff);
  color: var(--bg-color, white);
}

.btn-secondary {
  background-color: #6c757d;
  color: white;

}
</style>