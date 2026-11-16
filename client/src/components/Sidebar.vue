<script setup lang="ts">
import { 
  Car, CheckSquare, ClipboardList, 
  FilePlus2, LayoutDashboard, NotebookText, 
  Settings, Users2 
} from '@lucide/vue'
import { RouterLink } from 'vue-router'
import logo from '../assets/Images/gnpc-logo.jpg'

const NAV_ITEMS = [
  { label: 'Dashboard', icon: LayoutDashboard, url: '/dashboard' },
  { label: 'New Request', icon: FilePlus2, url: '/create-request' },
  { label: 'My Requests', icon: ClipboardList, active: true, url: '/my-requests' },
  // { label: 'Approvals', icon: CheckSquare, url: '/Approval' },
  { label: 'Assignments', icon: Users2, url: '/assignments' },
  // { label: 'Trip Logs', icon: NotebookText, url: '/trip-logs' },
  // { label: 'Trips', icon: Car, url: '/trips' },
  { label: 'Admin', icon: Settings, url: '/admin' },
]
</script>

<template>
  <div class="w-52 bg-green-900 text-white shadow-lg">
    <div class="space-y-4 p-4">
      <div class="flex items-center gap-2 mb-4">
        <img :src="logo" alt="Logo" class="h-10 w-auto" />
        <span class="text-lg font-bold">GNPC Fleet</span>
      </div>
      <ul class="space-y-4">
        <li v-for="(item, index) in NAV_ITEMS" :key="index" class="mb-6">
          <RouterLink :to="item.url || ''" class="flex items-center gap-2 text-white hover:text-gray-300">
            <component :is="item.icon" class="h-5 w-5" />
            <span class="text-sm font-medium">{{ item.label }}</span>
          </RouterLink>
        </li>
      </ul>
    </div>
  </div>
</template>
