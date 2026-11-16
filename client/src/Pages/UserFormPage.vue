<script setup lang="ts">
import { ArrowLeft } from '@lucide/vue';
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../api/api';
import { useNotificationStore } from '../stores/notification';

interface Option {
  value: string;
  label: string;
}

const props = defineProps({ 
    id: {
        type: [String, Number],
        default: null
    },
})


const form = ref({
    full_name: '',
    email: '',
    department: '',
    role: '',
    is_active: true,
    password: '',
    confirm_password: ''
})

const loading = ref(false)
const submitting = ref(false)
const departmentOptions = ref<Option[]>([])
const roleOptions = ref<Option[]>([])

// const router = useRoute()


const isEditMode = computed(() => Boolean(props.id))

const getUserOptions = async () => {
  loading.value = true;
  try {
    const response = await api.get('auth/user-options');
    roleOptions.value = response.data.roles;
    departmentOptions.value = response.data.departments;
  } catch (error) {
    console.error('Failed to load options:', error);
  } finally {
    loading.value = false;
  }
};

const getUserDetails = async () => {
    if (!isEditMode.value) return;
    try {
        const response = await api.get(`auth/users/${props.id}/`);
        // Populate form with existing user data (excluding password)
        form.value = {
            ...form.value,
            full_name: response.data.full_name,
            email: response.data.email,
            department: response.data.department,
            role: response.data.role,
            is_active: response.data.is_active
        }
    } catch (error) {
        console.error('Failed to load user:', error);
    }
}


onMounted(async () => {
  await getUserOptions();
  await getUserDetails();
})

const router = useRouter()
const notificationStore = useNotificationStore()

const handleSubmit = async () => {
  submitting.value = true;
  try {
    if(form.value.password == form.value.confirm_password) {
        if (!isEditMode.value) {
            await api.post('auth/users/', form.value);
            notificationStore.setNotification('User created successfully!', true)
            router.push('/admin')
        } else {
            // Destructure password out so it isn't sent as an empty string
            const { password, ...updatePayload } = form.value;
            await api.patch(`auth/users/${props.id}/`, updatePayload);
            notificationStore.setNotification('User updated successfully!', true)
            router.push('/admin')
        }
    } else {
        notificationStore.setNotification('Password do not Match the Confirm Password!', false)
    }
  } catch (error) {
    console.error('Server validation details:', error.response?.data);
    notificationStore.setNotification('Error Creating User!', false)
    router.push('/admin')
  } finally {
    submitting.value = false;
  }
};

</script>
<template>
    <div class='overflow-x-auto mt-6 space-y-6'>
        <RouterLink to="/admin" class="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground mb-6">
        <ArrowLeft class="w-4 h-4" />
            Back to Admin
        </RouterLink>
        <h1 class="text-2xl font-bold">{{ isEditMode ? 'Update User' : 'Create User' }}</h1>
        
        <div v-if="notificationStore.message">
            <p :class="`mt-4 p-2 rounded-md text-sm ${notificationStore.isSuccess ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`">{{ notificationStore.message }}</p>
            <button @click="notificationStore.clearNotification()">Close</button>
        </div>
        <div class="p-4 bg-white border rounded-lg border-gray-200 my-4 shadow-md">
            <form @submit.prevent="handleSubmit" class="space-y-4 p-2">
                <div class="grid grid-cols-2 gap-4">
                    <div class='flex flex-col gap-2'>
                        <label htmlFor="full_name" class="text-sm font-medium text-gray-700">Full Name:</label>
                        <input
                            v-model="form.full_name"
                            placeholder="Full name"
                            class="border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                        />    
                    </div>
                    <div class='flex flex-col gap-2'>
                        <label htmlFor="email" class="text-sm font-medium text-gray-700">Email:</label>
                        <input
                            type="email"
                            v-model="form.email"
                            placeholder="Email address"
                            class="border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                        />
                    </div>
                    
                    <div class='flex flex-col gap-2'>
                        <label htmlFor="password" class="text-sm font-medium text-gray-700">Password:</label>
                        <input v-if="!isEditMode"
                            type='password'
                            v-model="form.password"
                            placeholder="Password"
                            class="border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                        />    
                    </div>
                    <div class='flex flex-col gap-2'>
                        <label htmlFor="confirm_password" class="text-sm font-medium text-gray-700">Confirm Password:</label>
                        <input v-if="!isEditMode"
                            type='password'
                            v-model="form.confirm_password"
                            placeholder="Password"
                            class="border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                        />    
                    </div>
                    
                    <div class='flex flex-col gap-2'>
                        <label htmlFor="role" class="text-sm font-medium text-gray-700">Role:</label>
                        <select v-model="form.role" name="role" class="border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500">
                            <option value="">Select role</option>
                            <option v-if="!loading" v-for="(role, index) in roleOptions" :key="index" :value="role?.value">
                                {{ role?.label }}
                            </option>
                        </select>
                    </div>
                    
                    <div class='flex flex-col gap-2'>
                        <label htmlFor="department" class="text-sm font-medium text-gray-700">Department:</label>
                        <select v-model="form.department" name="department" class="border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500">
                            <option value="">Select department</option>
                            <option v-if="!loading" v-for="(department, index) in departmentOptions" :key="index" :value="department?.value">
                                {{ department?.label }}
                            </option>
                        </select>
                    </div>

                    <div class='flex flex-col gap-2'>
                        <label htmlFor="is_active" class="text-sm font-medium text-gray-700">Status:</label>
                        <select
                            v-model="form.is_active"
                            name="is_active"
                            class="border border-gray-300 p-2 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                        >
                            <option :value="true">Active</option>
                            <option :value="false">Inactive</option>
                        </select>
                    </div>
                    
                </div>

                <button type="submit" :disabled="submitting" class="bg-green-900 text-white px-4 py-2 rounded-md flex items-center gap-2 hover:bg-green-700 disabled:opacity-50">
                    {{isEditMode ? 'Update User' : 'Add User'}}
                </button>
            </form>
        </div>
    </div>    
</template>