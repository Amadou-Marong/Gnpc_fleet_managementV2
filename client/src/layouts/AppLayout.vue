<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { LogOut, Settings } from '@lucide/vue'
import Sidebar from '../components/Sidebar.vue'
import UserAvatar from '../components/UserAvatar.vue'

// Assume useAuth is a composable or Pinia store equivalent in Vue
import { useAuthStore } from '../stores/auth.ts'

defineProps({
  title: String
})

const menuOpen = ref(false)
const { currentUser, logout } = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  logout()
  router.push('/login')
}
</script>

<template>
  <div class="flex min-h-screen">
    <Sidebar />
    <div class="flex-1 flex flex-col">
      <header class="p-3 bg-white border-b border-gray-200 shadow-md flex items-center justify-between">
        <h1 class="text-xl font-bold mb-4">{{ title }}</h1>
        <button 
          @click="menuOpen = !menuOpen" 
          class="flex items-center gap-2 border-2 border-gray-300 hover:bg-gray-100 px-3 py-2 rounded-md text-sm font-medium"
        >
          <UserAvatar :currentUser="currentUser" />
        </button>

        <div v-if="menuOpen" class="absolute right-3 top-16 bg-white border border-gray-300 rounded-md shadow-lg p-2">
          <div class="flex flex-col p-5 gap-4">
            <button class="cursor-pointer flex items-center gap-2 text-gray-700 hover:text-gray-900 border border-gray-100 px-3 py-2 rounded-md text-sm font-medium">
              <Settings /> Settings
            </button>
            <button 
              @click="handleLogout" 
              class="cursor-pointer flex items-center gap-2 text-red-500 hover:text-red-700 border border-gray-100 px-3 py-2 rounded-md text-sm font-medium"
            >
              <LogOut /> Logout
            </button>
          </div>
        </div>
      </header>

      <!-- Main content / Slot equivalent -->
      <main class="p-4 flex-1" @click="menuOpen = false">
        <slot />
      </main>
    </div>
  </div>
</template>
