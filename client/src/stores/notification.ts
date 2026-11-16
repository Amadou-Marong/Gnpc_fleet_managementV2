import { defineStore } from "pinia";
import { ref } from "vue";

export const useNotificationStore = defineStore('notification', () => {
    const message = ref<string>('')
    const isSuccess = ref<boolean>(true)
    let timeoutId: ReturnType<typeof setTimeout> | null = null // Track the active timer ID

    function setNotification(text: string, success=true): void {
        // 1. Reset any active timer if a new notification comes in early
        if (timeoutId) {
            clearTimeout(timeoutId)
        }

        // 2. Set the message and status
        message.value = text
        isSuccess.value = success

        // 3. Start the timer to hide the notification
        timeoutId = setTimeout(() => {
            clearNotification()
        }, 5000)
    }
    
    function clearNotification(): void {
        message.value = ''
        if(timeoutId){
            clearInterval(timeoutId)
            timeoutId = null
        }
    }

    return {
        message,
        isSuccess,
        setNotification,
        clearNotification
    }
})