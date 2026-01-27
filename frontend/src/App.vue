<template>
  <div id="app">
    <Navigation v-if="!isPublicPassbook" />
    <router-view />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Navigation from './components/Navigation.vue'

const route = useRoute()

const isPublicPassbook = computed(() => {
  return route.path.includes('/passbook/public/')
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  background: #f5f7fa;
}

body {
  margin: 0;
  padding: 0;
}
</style>