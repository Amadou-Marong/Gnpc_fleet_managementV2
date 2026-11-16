<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock, Loader } from '@lucide/vue'
import { useAuthStore } from '../stores/auth'
import logo from '../assets/Images/gnpc-logo.jpg'

// Initialize Vue Router and Pinia Store
const router = useRouter()
const authStore = useAuthStore()

// State management variables (Replaces useState)
const email = ref('')
const password = ref('')
const submitting = ref(false)

const handleLogin = async () => {
  submitting.value = true
  try {
    const success = await authStore.login({ 
      email: email.value, 
      password: password.value 
    })
    
    if (success) {
      router.push('/dashboard')
    }
  } catch (err) {
    // Errors are already handled globally by authStore.error
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center p-6">
    <div class="w-full max-w-md bg-white rounded-3xl shadow-2xl p-10">

      <!-- Logo -->
      <div class="flex justify-center mb-6 h-28">
        <img :src="logo" alt="logo" />
      </div>

      <!-- Heading -->
      <div class="text-center">
        <h1 class="text-4xl font-bold text-gray-800">Welcome Back</h1>
        <p class="text-gray-500 mt-2">Sign in to your account</p>
      </div>

      <!-- Global Auth Error Message -->
      <p v-if="authStore.error" class="text-red-500 text-sm mt-2 text-center">
        {{ authStore.error }}
      </p>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="mt-8 space-y-5">
        
        <!-- Username / Email Field -->
        <div class="relative">
          <User class="absolute left-4 h-4 w-4 mt-3 text-gray-400" />
          <input
            v-model="email"
            type="text"
            placeholder="Email"
            class="w-full border border-gray-300 rounded-xl pl-12 pr-4 py-3 outline-none focus:border-green-700 focus:ring-2 focus:ring-green-200"
          />
        </div>

        <!-- Password Field -->
        <div class="relative">
          <Lock class="absolute left-4 mt-3 h-4 w-4 text-gray-400" />
          <input
            v-model="password"
            type="password"
            placeholder="Password"
            class="w-full border border-gray-300 rounded-xl pl-12 pr-4 py-3 outline-none focus:border-green-700 focus:ring-2 focus:ring-green-200"
          />
        </div>

        <!-- Remember Me & Forgot Password -->
        <div class="flex justify-between items-center">
          <label class="flex items-center gap-2">
            <input
              type="checkbox"
              class="accent-green-700 w-4 h-4"
            />
            <span class="text-gray-700">Remember me</span>
          </label>
          <a href="#" class="text-blue-700 hover:underline">
            Forgot Password?
          </a>
        </div>

        <!-- Submit Button -->
        <button
          :disabled="!email || !password || submitting"
          type="submit"
          class="w-full bg-green-900 text-white py-3 px-4 rounded-lg flex items-center justify-center hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 transition-opacity duration-200"
          :class="{ 'opacity-50 cursor-not-allowed': !email || !password }"
        >
          <Loader v-if="submitting" class="animate-spin h-5 w-5" />
          <span v-else>Sign In</span>
        </button>

      </form>
    </div>
  </div>
</template>
