<script setup lang="ts">
import { ref } from 'vue';
import api from '../api/api';
import { useRouter } from 'vue-router';
import { useNotificationStore } from '../stores/notification';

const form = ref({
    name: '',
    department: '',
    purpose: '',
    from_location: '',
    to_location: '',
    date: ''
})


const departmentOptions = [
    {id: 1, label: "Operations", value: "operations"},
    {id: 2, label: "IT", value: "iT"},
    {id: 3, label: "HR", value: "hr"},
    {id: 4, label: "Audit", value: "audit"},
]

const router = useRouter()
const notificationStore = useNotificationStore()

const handleSubmit = async () => {
    try {
        await api.post('vehicles/requests/', form.value)
        notificationStore.setNotification('Request sent successfully!', true)
        router.push('/my-requests')
    } catch (error) {
        console.error('Server validation details:', error.response?.data);
        notificationStore.setNotification('Error sending Request!', false)
    }
}
</script>
<template>
    <form @submit.prevent="handleSubmit" class="space-y-4">
        <h2 class='text-green-700'>Vehicle Request Form</h2>
        <div class="grid grid-cols-2 gap-4">
            <div class='flex flex-col gap-2'>
                <label htmlFor="name" class="text-sm font-medium text-gray-700">Name:</label>
                <input
                    id="name"
                    v-model="form.name"
                    class="w-full bg-white border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    placeholder="Enter the Name..."
                />
            </div>
            <div class='flex flex-col gap-2'>
                <label htmlFor="department" class="text-sm font-medium text-gray-700">Department:</label>
                <select v-model="form.department" name="department" class="border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500">
                    <option value="">Select Department</option>
                    <option v-for="department in departmentOptions" :key="department.id" :value="department.value">
                        {{ department.label }}
                    </option>
                </select>
            </div>
            <div class='flex flex-col gap-2 col-span-2'>
                <label htmlFor="purpose" class="text-sm font-medium text-gray-700">Purpose:</label>
                <textarea
                    id="purpose"
                    v-model="form.purpose"
                    class="w-full bg-white border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    placeholder="Enter the Purpose..."
                />
            </div>
            <div class='flex flex-col gap-2'>
                <label htmlFor="from" class="text-sm font-medium text-gray-700">From:</label>
                <input
                    id="from"
                    v-model="form.from_location"
                    class="w-full bg-white border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    placeholder="Enter departure location..."
                />
            </div>
            <div class='flex flex-col gap-2'>
                <label htmlFor="to" class="text-sm font-medium text-gray-700">To:</label>
                <input
                    id="to"
                    v-model="form.to_location"
                    class="w-full bg-white border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    placeholder="Enter departure location..."
                />
            </div>
            <div class='flex flex-col gap-2'>
                <label htmlFor="date" class="text-sm font-medium text-gray-700">Date:</label>
                <input
                    id="date"
                    type='date'
                    v-model="form.date"
                    class="w-full bg-white border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    placeholder="Enter Date..."
                />
            </div>
        </div>
        <button type="submit" class="bg-green-900 text-white px-4 py-2 rounded-md flex items-center gap-2 hover:bg-green-700">Submit to Approval</button>
    </form>
</template>