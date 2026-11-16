<script setup lang="ts">
import { ArrowLeft } from '@lucide/vue';
import { computed, onMounted, ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import api from '../api/api';
import { useNotificationStore } from '../stores/notification';

const props = defineProps({ 
    id: {
        type: [String, Number],
        default: null
    },
})



const form = ref({
    model_name: '',
    status: true,
    assigned_to: null,
    mileage: 0.0
})

const statusOptions = [
    {id: 1, label: "Available", value: "available"},
    {id: 2, label: "In Use", value: "in_use"},
    {id: 3, label: "Out of service", value: "out_of_service"},
    {id: 4, label: "Maintenance", value: "maintenance"},
]

const loading = ref(false)
const submitting = ref(false)
const isEditMode = computed(() => Boolean(props.id))
const userOptions = ref([])
const notificationStore = useNotificationStore()
const router = useRouter()

const getUserOptions = async () => {
    loading.value = true
    try {
        const response = await api.get('auth/users/')
        userOptions.value = response.data
    } catch (error) {
        console.log(error);
    } finally {
        loading.value = false
    }
}

const getVehicleDetails = async () => {
    if (!isEditMode.value) return;
    try {
        const response = await api.get(`vehicles/${props.id}/`);
        // Populate form with existing user data (excluding password)
        form.value = {
            ...form.value,
            model_name: response.data.model_name,
            status: response.data.status,
            assigned_to: response.data.assigned_to,
            mileage: response.data.mileage
        }
    } catch (error) {
        console.error('Failed to load user:', error);
    }
}

onMounted(async () => {
    await getUserOptions()
    await getVehicleDetails()
})

const handleSubmit = async () => {
    submitting.value = true;
    try {
        if (!isEditMode.value) {
            await api.post('vehicles/', form.value);
            notificationStore.setNotification('Vehicle created successfully!', true)
            router.push('/admin')
        } else {
            await api.patch(`vehicles/${props.id}/`, form.value);
            notificationStore.setNotification('Vehicle updated successfully!', true)
            router.push('/admin')
        }
    } catch (error) {
        console.error('Server validation details:', error.response?.data);
        notificationStore.setNotification('Error Creating Vehicle!', false)
        router.push('/admin')
    } finally {
        submitting.value = false;
    }
}

</script>
<template>
     <div class='overflow-x-auto mt-6 space-y-6'>
        <RouterLink to="/admin" class="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground mb-6">
        <ArrowLeft class="w-4 h-4" />
        Back to Admin
        </RouterLink>
        <h1 class="text-2xl font-bold">{{ isEditMode ? 'Update Vehicle' : 'Create Vehicle' }}</h1>
        <!-- <form @submit.prevent="handleSubmit" class="grid grid-cols-1 gap-3 border-y border-gray-200 bg-gray-50 p-4 md:grid-cols-2">
            
        </form> -->
        <div class="p-4 bg-white border rounded-lg border-gray-200 my-4 shadow-md">
            <form @submit.prevent="handleSubmit" class="space-y-4 p-2">
                <div class="grid grid-cols-2 gap-4">
                    <div class='flex flex-col gap-2'>
                        <label htmlFor="modelName" class="text-sm font-medium text-gray-700">Model Name:</label>
                        <input
                            v-model="form.model_name"
                            id="modelName"
                            class="w-full bg-white border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                            placeholder="Enter the Model Name..."
                        />
                    </div>
                    <div class='flex flex-col gap-2'>
                        <label htmlFor="status" class="text-sm font-medium text-gray-700">Status:</label>
                        <select
                            v-model="form.status"
                            name="status"
                            class="border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                        >
                            <option value="">Select Status</option>
                            <option v-if="!loading" v-for="status in statusOptions" :key="status.id" :value="status?.value">
                                {{ status.label }}
                            </option>
                        </select>
                    </div>
                    <div class='flex flex-col col-span-2 gap-2'>
                        <label htmlFor="role" class="text-sm font-medium text-gray-700">Assigned To:</label>
                        <select v-model="form.assigned_to" name="role" class="border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500">
                            <option value="">Select User</option>
                            <option v-if="!loading" v-for="user in userOptions" :key="user?.id" :value="user?.id">
                                {{ user?.full_name }}
                            </option>
                        </select>
                    </div>
                    <div class='flex flex-col gap-2'>
                        <label htmlFor="password" class="text-sm font-medium text-gray-700">Mileage:</label>
                        <input
                            type="number"
                            v-model="form.mileage"
                            placeholder="Mileage"
                            class="border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                        />    
                    </div>
                </div>
                <!-- <button class="bg-green-900 text-white px-4 py-2 rounded-md flex items-center gap-2 hover:bg-green-700">Submit to Approval</button> -->
                <button type="submit" :disabled="submitting" class="bg-green-900 text-white px-4 py-2 rounded-md flex items-center gap-2 hover:bg-green-700 disabled:opacity-50">
                    {{isEditMode ? 'Update Vehicle' : 'Add Vehicle'}}
                </button>
            </form>
        </div>
    </div>
</template>