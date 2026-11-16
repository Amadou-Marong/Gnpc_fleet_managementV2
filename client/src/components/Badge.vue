<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: [String, Boolean],
    required: true
  }
})

const STATUS_STYLES: Record<string, string> = {
  true: 'bg-emerald-100 text-emerald-700',
  false: 'bg-gray-100 text-gray-700',
  completed: 'bg-emerald-100 text-emerald-700',
  approved: 'bg-sky-100 text-sky-700',
  Assigned: 'bg-blue-100 text-blue-800',
  pending: 'bg-amber-100 text-amber-700',
  rejected: 'bg-rose-100 text-rose-700',
  draft: 'bg-slate-200 text-slate-600',
}

const displayLabel = computed(() => {
  if (props.status === true || props.status === 'true') return 'Active'
  if (props.status === false || props.status === 'false') return 'Inactive'
  return String(props.status)
})

const statusClass = computed(() => {
  return STATUS_STYLES[String(props.status)] ?? 'bg-emerald-100 text-emerald-700'
})
</script>

<template>
  <span
    :class="[
      'inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium capitalize',
      statusClass
    ]"
  >
    {{ displayLabel }}
  </span>
</template>
