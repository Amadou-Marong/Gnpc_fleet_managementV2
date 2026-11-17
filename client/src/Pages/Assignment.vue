<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
// import { AVAILABILITY, DRIVERS, VEHICLES, VEHICLE_STATUS_STYLES } from '../data/dummyData.ts';
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import api from '../api/api.ts';
import Badge from '../components/Badge.vue';


// Reactive State
const trips = ref<any[]>([])
const vehicles = ref<any[]>([])
const drivers = ref<any[]>([])
const FLEET_TOTAL = ref<number>(0)
const isSubmitting = ref<Record<number, boolean>>({})
const activeTab = ref('assign')

const stats = ref({
  available: 0,
  in_use: 0,
  maintenance: 0,
  out_of_service: 0,
  total: 0,
})

const availability = computed(() => [
  { label: 'Available', count: stats.value.available, color: 'bg-emerald-500', text: 'text-emerald-700', bg: 'bg-emerald-50' },
  { label: 'In use', count: stats.value.in_use, color: 'bg-[#123a63]', text: 'text-[#123a63]', bg: 'bg-blue-50' },
  { label: 'Maintenance', count: stats.value.maintenance, color: 'bg-amber-500', text: 'text-amber-700', bg: 'bg-amber-50' },
  { label: 'Out of service', count: stats.value.out_of_service, color: 'bg-rose-500', text: 'text-rose-700', bg: 'bg-rose-50' },
])

// Fetch Data
const getDispatchData = async () => {
  try {
    const response = await api.get('vehicles/dispatch-data/')
    vehicles.value = response.data.vehicles
    drivers.value = response.data.drivers
    stats.value = response.data.stats
    FLEET_TOTAL.value = response.data.stats.total

    // Map backend fields (assigned_vehicle_id / assigned_driver_id) to draft dropdown fields
    trips.value = response.data.trips.map((trip: any) => ({
      ...trip,
      draftVehicleId: trip.assigned_vehicle_id ?? '',
      draftDriverId: trip.assigned_driver_id ?? '',
    }))
  } catch (error: any) {
    console.error(error.response?.data || error)
    toast.error('Failed to load dispatch data.')
  }
}

onMounted(getDispatchData)

// Check if vehicle/driver is already assigned to another trip ON THE SAME DATE
const isAssignedElsewhere = (
  currentTrip: any,
  field: 'assigned_vehicle_id' | 'assigned_driver_id',
  id: number
) => {
  return trips.value.some(
    (t) =>
      t.id !== currentTrip.id &&
      t.date === currentTrip.date &&
      t[field] === id
  )
}

// Assign or Reassign Trip
const handleAssign = async (trip: any) => {
  if (!trip.draftVehicleId || !trip.draftDriverId) {
    toast.error('Select both a vehicle and a driver first.')
    return
  }

  const hasConflict =
    isAssignedElsewhere(trip, 'assigned_vehicle_id', trip.draftVehicleId) ||
    isAssignedElsewhere(trip, 'assigned_driver_id', trip.draftDriverId)

  if (hasConflict) {
    toast.error(`This vehicle or driver is already assigned to another trip on ${trip.date}.`)
    return
  }

  try {
    isSubmitting.value[trip.id] = true
    await api.patch(`vehicles/requests/${trip.id}/`, {
      assigned_vehicle: trip.draftVehicleId,
      assigned_driver: trip.draftDriverId,
    })

    toast.success('Trip assigned successfully!')
    await getDispatchData()
  } catch (error: any) {
    toast.error(error.response?.data?.error || 'Failed to assign trip.')
  } finally {
    isSubmitting.value[trip.id] = false
  }
}


</script>

<template>
    <!-- Availability Cards -->
    <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
      <div
        v-for="a in availability"
        :key="a.label"
        class="rounded-lg border border-slate-200 bg-white p-4 shadow-sm"
      >
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-slate-400">{{ a.label }}</span>
          <span :class="['h-2 w-2 rounded-full', a.color]" />
        </div>
        <div class="mt-2 flex items-end gap-1.5">
          <span class="text-2xl font-semibold text-slate-800">{{ a.count }}</span>
          <span class="mb-0.5 text-xs text-slate-400">/ {{ FLEET_TOTAL }}</span>
        </div>
        <div class="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-slate-100">
          <div
            :class="['h-full', a.color]"
            :style="{ width: `${(a.count / FLEET_TOTAL) * 100}%` }"
          />
        </div>
      </div>
    </div>

    <h1 class="mb-3 font-bold">Vehicle Assignment</h1>

    <!-- Tabs -->
    <div class="mb-6 flex border-b border-gray-200">
      <button
        type="button"
        @click="activeTab = 'assign'"
        :class="[
          'border-b-2 px-4 py-3 text-sm font-medium',
          activeTab === 'assign'
            ? 'border-green-700 text-green-800'
            : 'border-transparent text-gray-500 hover:text-gray-700',
        ]"
      >
        Assign to Trips
      </button>
      <button
        type="button"
        @click="activeTab = 'status'"
        :class="[
          'border-b-2 px-4 py-3 text-sm font-medium',
          activeTab === 'status'
            ? 'border-green-700 text-green-800'
            : 'border-transparent text-gray-500 hover:text-gray-700',
        ]"
      >
        Vehicle Status
      </button>
    </div>

    <!-- Tab 1: Assign to Trips -->
    <div
      v-if="activeTab === 'assign'"
      class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm"
    >
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Trip</th>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Vehicle</th>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Driver</th>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 bg-white">
            <tr v-for="trip in trips" :key="trip.id">
              <td class="whitespace-nowrap px-6 py-4">
                <div class="text-sm font-medium text-gray-700">#{{ trip.id }} {{ trip.name }}</div>
                <div class="text-xs text-gray-500">
                  {{ trip.from_location }} -> {{ trip.to_location }} • {{ trip.date }}
                </div>
              </td>

              <!-- Vehicle Dropdown -->
              <td class="px-6 py-4">
                <select
                  v-model="trip.draftVehicleId"
                  class="w-full rounded-md border border-gray-300 p-2 text-sm text-gray-700 focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="">Select vehicle</option>
                  <option
                    v-for="vehicle in vehicles"
                    :key="vehicle.id"
                    :value="vehicle.id"
                    :disabled="vehicle.status === 'maintenance' || vehicle.status === 'out_of_service' || isAssignedElsewhere(trip, 'assigned_vehicle_id', vehicle.id)"
                  >
                    {{ vehicle.id }} - {{ vehicle.model_name }} ({{ vehicle.status }})
                  </option>
                </select>
              </td>

              <!-- Driver Dropdown -->
              <td class="px-6 py-4">
                <select
                  v-model="trip.draftDriverId"
                  class="w-full rounded-md border border-gray-300 p-2 text-sm text-gray-700 focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="">Select driver</option>
                  <option
                    v-for="driver in drivers"
                    :key="driver.id"
                    :value="driver.id"
                    :disabled="isAssignedElsewhere(trip, 'assigned_driver_id', driver.id)"
                  >
                    {{ driver.full_name }}
                  </option>
                </select>
              </td>

              <!-- Action Button -->
              <td class="px-6 py-4">
                <button
                  type="button"
                  :disabled="isSubmitting[trip.id]"
                  class="rounded-md bg-green-800 px-3 py-2 text-sm font-medium text-white hover:bg-green-700 disabled:opacity-50"
                  @click="handleAssign(trip)"
                >
                  {{ trip.assigned_vehicle_id && trip.assigned_driver_id ? 'Reassign' : 'Assign' }}
                </button>
              </td>
            </tr>
          </tbody>


        </table>
      </div>
    </div>

    <!-- Tab 2: Vehicle Status -->
    <div
      v-if="activeTab === 'status'"
      class="mb-4 mt-8 overflow-hidden border-b border-gray-200 shadow sm:rounded-lg"
    >
      <table class="min-w-full divide-y divide-gray-200 border border-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Vehicle</th>
            <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Assigned To</th>
            <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Mileage</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 bg-white">
          <tr v-for="vehicle in vehicles" :key="vehicle.id">
            <td class="whitespace-nowrap px-6 py-4">
              <div class="text-sm font-medium text-gray-700">{{ vehicle.id }}</div>
              <div class="text-xs text-gray-500">{{ vehicle.model_name }}</div>
            </td>
            <td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
              <!-- <span
                :class="[
                  'inline-flex items-center rounded-full px-2 py-0.5 text-[11px] font-medium',
                  VEHICLE_STATUS_STYLES[vehicle.status],
                ]"
              >
                {{ vehicle.status }}
              </span> -->
              <Badge :status="vehicle.status" />
            </td>
            <td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">{{ vehicle.assigned_to__full_name }}</td>
            <td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">{{ vehicle.mileage }}</td>
          </tr>
        </tbody>
      </table>
    </div>
</template>
