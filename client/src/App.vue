<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'
import AppLayout from './layouts/AppLayout.vue'

const route = useRoute()

// Check if the current route explicitly asks for the AppLayout
const layout = computed(() => {
  return route.meta.layout === 'AppLayout' ? AppLayout : null
})
</script>

<template>
  <!-- If the layout is requested, wrap RouterView with it -->
  <component :is="layout" v-if="layout" :title="(route.meta.title as string)">
    <RouterView />
  </component>
  
  <!-- Otherwise, render the page naked (e.g., Login screen) -->
  <RouterView v-else />
</template>
