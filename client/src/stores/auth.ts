// import { defineStore } from 'pinia'
// import { ref, onMounted } from 'vue'
// import api from '../api/api'

// type Payload = {
//   email: string
//   password: string
// }

// export const useAuthStore = defineStore('auth', () => {
//   const currentUser = ref(null)
//   const error = ref(null)
//   const isLoading = ref(true)

//   // Equivalent to React's useEffect with empty dependency array
//   onMounted(() => {
//     const storedUser = localStorage.getItem('auth_user')
//     if (storedUser) {
//       try {
//         currentUser.value = JSON.parse(storedUser)
//       } catch (e) {
//         console.error("Error parsing stored user data", e)
//       }
//     }
//     isLoading.value = false
//   })

//   const login = async (payload: Payload) => {
//     try {
//       error.value = null
//       const response = await api.post('auth/login/', payload)

//       const user = response.data?.user
      
//       const accessToken = response.data?.access
//       const refreshToken = response.data?.refresh

//       if (user) {
//         localStorage.setItem('auth_user', JSON.stringify(user))
//         localStorage.setItem('access_token', accessToken)
//         localStorage.setItem('refresh_token', refreshToken)
        
//         currentUser.value = user
//         return true
//       }
//       return false
//     } catch (err: any) {
//       console.error(err)
//       error.value = err.response?.data?.detail || 'Login failed'
//       return false
//     }
//   }

//   const logout = async () => {
//     const refreshToken = localStorage.getItem('refresh_token')
//     try {
//       await api.post('auth/logout/', { refresh: refreshToken })
//     } catch (err: any) {
//       console.error("Backend logout clearance failed:", err)
//     } finally {
//       localStorage.removeItem('auth_user')
//       localStorage.removeItem('access_token')
//       localStorage.removeItem('refresh_token')
//       currentUser.value = null
//     }
//   }

//   // Return everything you want components to access
//   return {
//     currentUser,
//     error,
//     isLoading,
//     login,
//     logout
//   }
// })


import { defineStore } from 'pinia'
import { ref } from 'vue' // ❌ Removed onMounted
import api from '../api/api'

type Payload = {
  email: string
  password: string
}

export const useAuthStore = defineStore('auth', () => {
  const currentUser = ref(null)
  const error = ref(null)
  const isLoading = ref(true)

  // Sync state synchronously right when the store initializes
  const storedUser = localStorage.getItem('auth_user')
  if (storedUser) {
    try {
      currentUser.value = JSON.parse(storedUser)
    } catch (e) {
      console.error("Error parsing stored user data", e)
      localStorage.removeItem('auth_user') // Clean up corrupt data
    }
  }
  isLoading.value = false // Set loading to false immediately after checking

  const login = async (payload: Payload) => {
    try {
      error.value = null
      const response = await api.post('auth/login/', payload)
      const user = response.data?.user
      const accessToken = response.data?.access
      const refreshToken = response.data?.refresh

      if (user) {
        localStorage.setItem('auth_user', JSON.stringify(user))
        localStorage.setItem('access_token', accessToken)
        localStorage.setItem('refresh_token', refreshToken)
        currentUser.value = user
        return true
      }
      return false
    } catch (err: any) {
      console.error(err)
      error.value = err.response?.data?.detail || 'Login failed'
      return false
    }
  }

  const logout = async () => {
    const refreshToken = localStorage.getItem('refresh_token')
    try {
      await api.post('auth/logout/', { refresh: refreshToken })
    } catch (err: any) {
      console.error("Backend logout clearance failed:", err)
    } finally {
      localStorage.removeItem('auth_user')
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      currentUser.value = null
    }
  }

  return { currentUser, error, isLoading, login, logout }
})
