<script setup lang="ts">
import { onMounted, ref } from 'vue';
import api from '../api/api';
import { useRouter } from 'vue-router';
import { useNotificationStore } from '../stores/notification';
import ConfirmDialog from '../components/ConfirmDialog.vue';

const STATUS_STYLES = {
    completed: "bg-emerald-100 text-emerald-700",
    approved: "bg-sky-100 text-sky-700",
    Assigned: "bg-blue-100 text-blue-800",
    pending: "bg-amber-100 text-amber-700",
    rejected: "bg-rose-100 text-rose-700",
    draft: "bg-slate-200 text-slate-600",
};

export interface CreatedBy {
  id: number;
  full_name: string;
  email: string;
  role: string;
  department: string;
  is_active: boolean;
  is_staff: boolean;
}

export type Status = "pending" | "approved" | "rejected"

export interface VehicleRequest {
  id: number;
  name: string;
  department: string;
  purpose: string;
  from_location: string;
  to_location: string;
  date: string; // or Date if you parse it
  status: Status;
  created_by: CreatedBy;
}

const requests = ref<VehicleRequest[]>([])
const showConfirm = ref(false)
const selectedRequest = ref<VehicleRequest | null>(null)
const currentAction = ref<'approved' | 'rejected' | "">("")

const getRequests = async () => {
    try {
        const response = await api.get('vehicles/requests/')
        // console.log(response.data);
        requests.value = response.data
    } catch (error: any) {
        console.error(error.response?.data);
    }
}

onMounted(async () => {
    await getRequests()
})

// const router = useRouter()
const notificationStore = useNotificationStore()

const openDialog = (actionType: "approved" | "rejected", selectedValue: VehicleRequest) => {
    selectedRequest.value = selectedValue
    currentAction.value = actionType
    showConfirm.value = true
}

const handleConfirm = async () => {
    if (!selectedRequest.value) return
    const selectedRequestId = selectedRequest.value.id
    try {
        const response = await api.patch(`vehicles/requests/${selectedRequest.value.id}/`, { status: currentAction.value })
        notificationStore.setNotification(`Request has been ${currentAction.value}`, true)
        requests.value = requests.value.map(req => 
            req.id === selectedRequestId ? response.data : req
        )
    } catch (error: any) {
        // handle error
        console.error('Server validation details:', error.response?.data);
        notificationStore.setNotification(`Error ${error.response?.data.status}`, false)
    }
    showConfirm.value = false
}

const handleCancel = () => {
    showConfirm.value = false
}

</script>
<template>
    <h1 class="text-2xl font-bold">My Requests</h1>
    <div class="bg-white my-6">
        <div class="flex items-center gap-4">
            <div class="flex items-center gap-2">
                <label htmlFor="search" class="text-sm font-medium text-gray-700">Search:</label>
                <input
                  id="search"
                  class="w-96 border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  placeholder="Search requests..."
                />
              </div>
              <div class="flex items-center gap-2">
                <label htmlFor="department" class="text-sm font-medium text-gray-700">Department:</label>
                <select class="w-auto border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500">
                    <option value="">All Departments</option>
                    <option value="IT" >IT</option>
                    <option value="HR">HR</option>
                    <option value="Finance">Finance</option>
                    <option value="Operations">Operations</option>
                    <option value="Commance">Commance</option>
                </select>
                </div>
                <div class="flex items-center gap-2">
                <label htmlFor="vehicle" class="text-sm font-medium text-gray-700">Vehicle:</label>
                <select class="w-auto border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500">
                    <option value="">All Vehicles</option>
                    <option value="Sedan">Sedan</option>
                    <option value="SUV">SUV</option>
                    <option value="Truck">Truck</option>
                    <option value="Van">Van</option>
                    <option value="Toyota">Toyota</option>
                </select>
            </div>
        </div>
        <div v-if="notificationStore.message">
            <p :class="`mt-4 p-2 rounded-md text-sm ${notificationStore.isSuccess ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`">{{ notificationStore.message }}</p>
            <button @click="notificationStore.clearNotification()">Close</button>
        </div>
        <div class="mt-8 shadow overflow-hidden border-b border-gray-200 sm:rounded-lg mb-4">
            <table class="min-w-full divide-y divide-gray-200 border border-gray-200">
            <thead class="bg-gray-50">
                <tr>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Request ID</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Staff Name</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Department</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="request in requests" :key="request.id">
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{request.id}}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{request.name}}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{request.department}}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{request.date}}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <span :class="`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${STATUS_STYLES[request.status]}`">
                            {{request.status}}
                        </span>
                    </td>
                    <td class="p-2 text-sm text-gray-700">
                        <button @click="openDialog('approved', request)" class="bg-green-500 hover:bg-green-700 text-white font-bold py-1 px-2 rounded">Approve</button>
                        <button @click="openDialog('rejected', request)" class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded ml-2">Reject</button>
                    </td>
                </tr>
            </tbody>
        </table>
        </div>
        <ConfirmDialog 
            v-show="showConfirm"
            :action="currentAction"
            @confirm="handleConfirm"
            @cancel="handleCancel"
        />
    </div>
</template>
