<template>
    <button
        class="hamburger-button"
        type="button"
        aria-label="Abrir menú"
        @click="$emit('toggle')"
    >
        <span class="line"></span>
        <span class="line"></span>
        <span class="line"></span>
    </button>

</template>

<script setup>
defineEmits(['toggle'])
</script>

<style scoped>
.hamburger-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 50px;
    height: 50px;
    background-color: #ffffff;
    border: 1.5px solid #dce4f0;
    cursor: pointer;
    padding: 0;
    gap: 6px;
    border-radius: 12px;
    transition: all 0.3s ease;
    
}
.hamburger-button:hover {
    background-color: #f7f9fc;
}
.hamburger-button.active{
    transform: translateY(7px) rotate(45deg);
}
.line {
    width: 24px;
    height: 3px;
    background-color: #000000;
    border-radius: 2px;
}

@media (min-width: 960px) {
    .hamburger-button {
        display: none !important;
    }
}

@media (max-width: 959px) {
    .hamburger-button {
        position: fixed;
        /* Reseteamos el top y left que vienen de App.vue */
        left: auto !important;
        
        /* Lo posicionamos abajo a la derecha */
        top: 8px;
        right: 16px;
        z-index: 9999;
    }
}
</style>
