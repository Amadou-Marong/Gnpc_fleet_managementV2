<script setup lang="ts">
import { Car, Plus } from '@lucide/vue';
import { onMounted, ref } from 'vue';
import api from '../api/api';
import { useRouter } from 'vue-router';
import { useNotificationStore } from '../stores/notification';
import Badge from '../components/Badge.vue';


const activeTab = ref('user')
const loading = ref(false)
const users = ref([])
const vehicles = ref([])


const getUsers = async () => {
    loading.value = true
    try {
        const response = await api.get('auth/users/')
        users.value = response.data
    } catch (error) {
        console.log(error);
    } finally {
        loading.value = false
    }
}

const getVehicles = async () => {
    loading.value = true
    try {
        const response = await api.get('/vehicles/')
        vehicles.value = response.data
    } catch (error) {
        console.log(error);
    } finally {
        loading.value = false
    }
}


onMounted(async () => {
    await getUsers()
    await getVehicles()
})

const router = useRouter()

const handleCreateUser = () => {
    router.push({name: 'create-user'})
}

const handleEditUser = (userId: number) => {
    console.log(userId);
    router.push({name: 'edit-user', params: {id: userId}})
}

const handleCreateVehicle = () => {
    router.push({name: 'create-vehicle'})
}

const handleEditVehicle = (vehicleId: number) => {
    console.log(vehicleId);
    router.push({name: 'edit-vehicle', params: {id: vehicleId}})
}



const STATUS_STYLES = {
    completed: "bg-emerald-100 text-emerald-700",
    approved: "bg-sky-100 text-sky-700",
    Assigned: "bg-blue-100 text-blue-800",
    pending: "bg-amber-100 text-amber-700",
    rejected: "bg-rose-100 text-rose-700",
    draft: "bg-slate-200 text-slate-600",
};


const notificationStore = useNotificationStore()
   
</script>
<template>
    <div class="mb-6 flex border-b border-gray-200">
        <button
            type="button"
            @click="activeTab = 'user'"
           :class="`border-b-2 px-4 py-3 text-sm font-medium ${activeTab === 'user' ? 'border-green-700 text-green-800' : 'border-transparent text-gray-500 hover:text-gray-700'}`"
        >
            User
        </button>
        
        <button
            type="button"
            @click="activeTab='vehicle'"
            :class="`border-b-2 px-4 py-3 text-sm font-medium ${activeTab === 'vehicle' ? 'border-green-700 text-green-800' : 'border-transparent text-gray-500 hover:text-gray-700'}`"
        >
            Vehicle
        </button>
        
        <!-- <button
            type="button"
            @click="activeTab='department'"
            :class="`border-b-2 px-4 py-3 text-sm font-medium ${activeTab === 'department' ? 'border-green-700 text-green-800' : 'border-transparent text-gray-500 hover:text-gray-700'}`"
        >
            Department
        </button> -->
    </div>

    <!-- Notification Banner -->
    <div v-if="notificationStore.message">
        <p :class="`mt-4 p-2 rounded-md text-sm ${notificationStore.isSuccess ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`">{{ notificationStore.message }}</p>
        <button @click="notificationStore.clearNotification()">Close</button>
    </div>


    <div v-if="activeTab=='user'" class='overflow-x-auto mt-6'>
        <div class="flex flex-col gap-3 bg-white sm:flex-row sm:items-center sm:justify-between">
            <div class="flex items-center gap-2">
                <label htmlFor="search" class="text-sm font-medium text-gray-700">Search:</label>
                <input
                    id="search"
                    class="w-96 border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    placeholder="Search requests..."
                />
            </div>

            <button
                type="button"
                @click="handleCreateUser"
                class="bg-green-900 text-white font-medium px-4 py-2 text-sm rounded-md flex items-center gap-2 hover:bg-green-700"
            >
                <Plus :size="16" /> Add User
            </button>
        </div>

        <div class="mt-8 shadow overflow-hidden border-b border-gray-200 sm:rounded-lg mb-4">
            <table class="min-w-full divide-y divide-gray-200 border border-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Department</th>
                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="loading">
                        <td colSpan="6" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center">
                            Loading users...
                        </td>
                    </tr>
                    <tr v-show="users.length === 0">
                        <td colSpan="6" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center">
                            No users found.
                        </td>
                    </tr>

                    <tr v-for="user in users as any" :key="user.id">
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{user.full_name}}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{user.email}}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{user.role}}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{user.department}}</td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <Badge :status="user.is_active" />
                        </td>
                        <td class="p-2 text-sm text-gray-700">
                            <button @click="handleEditUser(user.id)" class="text-gray-700 font-bold py-1 px-2 rounded">Edit</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    <div v-if="activeTab=='vehicle'" class='overflow-x-auto mt-6'>
            <div class='flex'>
                <button
                    type="button"
                    @click="handleCreateVehicle"
                    class="ml-auto flex mb-2 items-center gap-1.5 rounded-md bg-green-900 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-green-900"
                >
                    <Plus :size="16" /> Add Vehicle
                </button>
            </div>
            <div className="grid grid-cols-1 gap-5 p-5 md:grid-cols-2 xl:grid-cols-3">
                <div v-if="loading">

                </div>
                <div v-show="users.length === 0">

                </div>
                <div v-for="v in vehicles as any"  :key="v?.id" class="rounded-lg border border-slate-200 bg-white p-5 shadow-sm transition-shadow hover:shadow-md">
                    <div class="flex items-start justify-between">
                        <div class="flex items-center gap-3">
                            <div class="flex h-11 w-11 items-center justify-center rounded-md bg-slate-50 text-slate-400">
                                <Car :size="20" />
                            </div>
                            <div>
                                <!-- <div class="text-sm font-semibold text-slate-800">{{v.id}}</div>  -->
                                <div class="text-xs text-slate-400">{{v.model_name}}</div>
                            </div>
                        </div>
                        <button @click="handleEditVehicle(v.id)" type="button" class="text-slate-300 hover:text-slate-500">
                            <MoreHorizontal :size="18" />
                        </button>
                    </div>
            
                    <div class="mt-4">
                        <!-- <span :class="`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ${STATUS_STYLES[v.status] ?? 'bg-slate-100 text-slate-600'}`">
                        {{v.status}}
                        </span> -->
                        <Badge :status="v.status" />
                    </div>
            
                    <div class="mt-4 space-y-2 text-xs text-slate-500">
                        <div class="flex items-center gap-1.5">
                            <Gauge :size="12" class="text-slate-400" /> {{v.mileage}}
                        </div>
                    </div>
            
                    
                    <div v-show="v.assigned_to_name" class="mt-4 flex items-center gap-2 rounded-md bg-slate-50 px-3 py-2 text-xs text-slate-600">
                        <div class="flex h-6 w-6 items-center justify-center rounded-full bg-green-600 text-[10px] font-semibold text-white">
                            {{v.assigned_to_name.split(" ").map((n: any) => n[0]).join("")}}
                        </div>
                        Currently driven by {{v.assigned_to_name}}
                    </div>
                    
            
                    <button
                        type="button"
                        @click="handleEditVehicle(v.id)"
                        class="mt-4 w-full rounded-md border border-slate-200 py-2 text-xs font-medium text-slate-600 transition-colors hover:bg-slate-50"
                    >
                        View details
                    </button> 
            </div>
        </div>
    </div>
    <!-- <div v-if="activeTab=='department'" class='overflow-x-auto mt-6'>
        <div class='flex '>
            <button
                type="button"
                class="ml-auto flex mb-2 items-center gap-1.5 rounded-md bg-green-900 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-green-900"
            >
                <Plus :size="16" /> Add Department
            </button>
        </div>
    </div> -->
</template>