<template>
    <button
        class="handburger-button"
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
.handburger-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 60px;
    height: 60px;
    background-color: #333;
    border: none;
    cursor: pointer;
    padding: 10px;
    gap: 6px;
    border-radius: 50%;
}
.line {
    width: 40px;
    height: 5px;
    background-color: #fff;
    border-radius: 2px;
}
</style>
