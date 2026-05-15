<template>
    <v-container class="home-view" fluid>
        <v-containeer class="slideshow-container" fluid>

        <SlideShow />
        </v-containeer>
    </v-container>
</template>

<script setup>
import SlideShow from '@/components/SlideShow.vue'
</script>

<style scoped>
.home-view {
  
}
.slideshow-container {
    position: inherit;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
}
</style>