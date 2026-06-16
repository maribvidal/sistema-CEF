<template>
    <v-container>
        <h1 >Confirmar Reserva</h1>
        <p>¿Desea confirmar su reserva para la clase {{ $route.params.clase_id }}?</p>
        <button @click="confirmarReserva">Confirmar</button>
    </v-container>
</template>

<script setup>

</script>

<style scoped>



</style>