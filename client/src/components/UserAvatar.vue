<script setup lang="ts">
import { Type, User } from '@lucide/vue'

// Define type
type UserType = {
  full_name: string
  email: string
  department: string
  // Add other properties as needed
}

defineProps({
  currentUser: {
    type: Object as () => UserType,
    required: true
  }
})
</script>

<template>
  <div class="flex items-center gap-2">
    <User class="h-5 w-5" />
    <span class="text-sm font-medium text-gray-700">
      {{ currentUser?.full_name || 'User' }}
    </span>
  </div>
</template>
