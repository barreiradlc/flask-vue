<template>
  <div class="todo-filter">
    <div class="filter-buttons">
      <button
        v-for="filter in filters"
        :key="filter.value"
        @click="updateFilter(filter.value as FilterType)"
        :class="['filter-button', { active: modelValue === filter.value }]"
      >
        {{ filter.label }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'

type FilterType = 'all' | 'active' | 'completed'

interface FilterOption {
  value: string;
  label: string;
}

const props = defineProps({
  modelValue: {
    type: String as PropType<FilterType>,
    required: true
  },
  filters: {
    type: Array as PropType<FilterOption[]>,
    required: true
  }
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: FilterType): void
}>()

const updateFilter = (value: FilterType) => {
  emit('update:modelValue', value)
}
</script>

<style scoped>
.todo-filter {
  margin-bottom: 1.5rem;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
  background: #f1f5f9;
  padding: 0.5rem;
  border-radius: 8px;
}

.filter-button {
  flex: 1;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-button:hover {
  background: #e2e8f0;
}

.filter-button.active {
  background: white;
  color: #667eea;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>