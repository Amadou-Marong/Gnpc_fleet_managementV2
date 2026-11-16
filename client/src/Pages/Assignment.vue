<script setup lang="ts">
import { ref } from 'vue'
import { AVAILABILITY, DRIVERS, VEHICLES, VEHICLE_STATUS_STYLES } from '../data/dummyData.ts';
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const FLEET_TOTAL = AVAILABILITY.reduce((sum, s) => sum + s.count, 0)

const TRIPS = [
  { id: 'TRIP-001', destination: 'Basse Station' },
  { id: 'TRIP-002', destination: 'Farafenni Station' },
  { id: 'TRIP-003', destination: 'Sanyang Station' },
]

// {
//   "assigned_vehicle": 1,
//   "assigned_driver": 2
// }

// Reactive State
const activeTab = ref('assign')
const tripSelections = ref({})
const assignedTrips = ref({})

// Methods
const updateSelection = (tripId, field, value) => {
  tripSelections.value[tripId] = {
    ...(tripSelections.value[tripId] || {}),
    [field]: value,
  }
}

const handleAssign = (tripId) => {
  const selection = tripSelections.value[tripId] || {}

  if (!selection.vehicleId || !selection.driverName) {
    toast.error('Select both a vehicle and a driver first.')
    return
  }

  const conflictingTrip = Object.entries(assignedTrips.value).find(
    ([assignedTripId, assignment]) =>
      assignedTripId !== tripId &&
      (assignment.vehicleId === selection.vehicleId ||
        assignment.driverName === selection.driverName)
  )

  if (conflictingTrip) {
    toast.error('A driver or vehicle can only be assigned to one trip at a time.')
    return
  }

  assignedTrips.value[tripId] = { ...selection }
  toast.success('Trip assigned successfully!')
}

const isAssignedElsewhere = (tripId, field, value) => {
  return Object.entries(assignedTrips.value).some(
    ([assignedTripId, assignment]) =>
      assignedTripId !== tripId && assignment[field] === value
  )
}
</script>

<template>
    <!-- Availability Cards -->
    <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
      <div
        v-for="a in AVAILABILITY"
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
            <tr v-for="trip in TRIPS" :key="trip.id">
              <td class="whitespace-nowrap px-6 py-4">
                <div class="text-sm font-medium text-gray-700">{{ trip.id }}</div>
                <div class="text-xs text-gray-500">{{ trip.destination }}</div>
              </td>
              <td class="px-6 py-4">
                <select
                  :value="tripSelections[trip.id]?.vehicleId || ''"
                  @change="updateSelection(trip.id, 'vehicleId', $event.target.value)"
                  class="w-full rounded-md border border-gray-300 p-2 text-sm text-gray-700 focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="">Select vehicle</option>
                  <option
                    v-for="vehicle in VEHICLES"
                    :key="vehicle.id"
                    :value="vehicle.id"
                    :disabled="isAssignedElsewhere(trip.id, 'vehicleId', vehicle.id)"
                  >
                    {{ vehicle.id }} - {{ vehicle.model }}
                  </option>
                </select>
              </td>
              <td class="px-6 py-4">
                <select
                  :value="tripSelections[trip.id]?.driverName || ''"
                  @change="updateSelection(trip.id, 'driverName', $event.target.value)"
                  class="w-full rounded-md border border-gray-300 p-2 text-sm text-gray-700 focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="">Select driver</option>
                  <option
                    v-for="driver in DRIVERS"
                    :key="driver.name"
                    :value="driver.name"
                    :disabled="isAssignedElsewhere(trip.id, 'driverName', driver.name)"
                  >
                    {{ driver.name }}
                  </option>
                </select>
              </td>
              <td class="px-6 py-4">
                <button
                  type="button"
                  class="rounded-md bg-green-800 px-3 py-2 text-sm font-medium text-white hover:bg-green-700"
                  @click="handleAssign(trip.id)"
                >
                  Assign
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
          <tr v-for="vehicle in VEHICLES" :key="vehicle.id">
            <td class="whitespace-nowrap px-6 py-4">
              <div class="text-sm font-medium text-gray-700">{{ vehicle.id }}</div>
              <div class="text-xs text-gray-500">{{ vehicle.model }}</div>
            </td>
            <td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
              <span
                :class="[
                  'inline-flex items-center rounded-full px-2 py-0.5 text-[11px] font-medium',
                  VEHICLE_STATUS_STYLES[vehicle.status],
                ]"
              >
                {{ vehicle.status }}
              </span>
            </td>
            <td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">{{ vehicle.assignedTo }}</td>
            <td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">{{ vehicle.mileage }}</td>
          </tr>
        </tbody>
      </table>
    </div>
</template>
