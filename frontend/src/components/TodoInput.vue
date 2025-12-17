<template>
  <div class="todo-input-container">
    <form @submit.prevent="handleSubmit" class="input-form">
      <input
        v-model="newTodoText"
        type="text"
        placeholder="What needs to be done?"
        class="todo-input"
        @keydown.enter="handleSubmit"
      />
      <button type="submit" class="add-button" :disabled="!newTodoText.trim()">
        <span class="button-text">Add</span>
        <span class="button-icon">+</span>
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { NewTodo } from '../types/todo'

const emit = defineEmits<{
  (e: 'add-todo', todo: NewTodo): void
}>()

const newTodoText = ref('')

const handleSubmit = () => {
  if (newTodoText.value.trim()) {
    emit('add-todo', { description: newTodoText.value })
    newTodoText.value = ''
  }
}
</script>

<style scoped>
.todo-input-container {
  margin-bottom: 1.5rem;
}

.input-form {
  display: flex;
  gap: 0.5rem;
}

.todo-input {
  flex: 1;
  padding: 1rem 1.5rem;
  font-size: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  transition: all 0.3s ease;
  outline: none;
}

.todo-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.add-button {
  padding: 0 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.add-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.add-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.button-icon {
  font-size: 1.25rem;
  font-weight: 700;
}
</style>