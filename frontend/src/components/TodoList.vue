<template>
  <div class="todo-list">
    <div v-for="todo in todos" :key="todo.id" class="todo-item">
      <div class="todo-content">
        <input
          type="checkbox"
          :checked="todo.completed"
          @change="toggleTodo(todo.id)"
          class="todo-checkbox"
        />
        
        <div 
          v-if="!todo.isEditing"
          :class="['todo-text', { completed: todo.completed }]"
          @dblclick="startEditing(todo)"
        >
          {{ todo.text }}
        </div>
        
        <input
          v-else
          type="text"
          v-model="todo.editText"
          @blur="saveEdit(todo)"
          @keydown.enter="saveEdit(todo)"
          @keydown.escape="cancelEdit(todo)"
          class="todo-edit-input"
          v-focus
        />
        
        <div class="todo-meta">
          <span class="todo-date">{{ formatDate(todo.createdAt) }}</span>
          <span v-if="todo.completed" class="todo-status">✓ Done</span>
        </div>
      </div>
      
      <button @click="deleteTodo(todo.id)" class="delete-button" title="Delete">
        ×
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Todo } from '../types/todo'

interface EditingTodo extends Todo {
  isEditing?: boolean;
  editText?: string;
}

const props = defineProps<{
  todos: Todo[]
}>()

const emit = defineEmits<{
  (e: 'toggle-todo', id: number): void
  (e: 'delete-todo', id: number): void
  (e: 'edit-todo', payload: { id: number; text: string }): void
}>()

// Create a local copy for editing
const editingTodos = ref<EditingTodo[]>([])

const formatDate = (date: Date) => {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const toggleTodo = (id: number) => {
  emit('toggle-todo', id)
}

const deleteTodo = (id: number) => {
  emit('delete-todo', id)
}

const startEditing = (todo: Todo) => {
  const editingTodo = todo as EditingTodo
  editingTodo.isEditing = true
  editingTodo.editText = todo.text
}

const saveEdit = (todo: EditingTodo) => {
  if (todo.editText?.trim() && todo.isEditing) {
    emit('edit-todo', { id: todo.id, text: todo.editText })
  }
  todo.isEditing = false
  todo.editText = ''
}

const cancelEdit = (todo: EditingTodo) => {
  todo.isEditing = false
  todo.editText = ''
}

// Custom directive for auto-focus
const vFocus = {
  mounted: (el: HTMLElement) => el.focus()
}
</script>

<style scoped>
.todo-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.todo-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.todo-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.todo-content {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.todo-checkbox {
  width: 1.25rem;
  height: 1.25rem;
  cursor: pointer;
  accent-color: #667eea;
}

.todo-text {
  flex: 1;
  font-size: 1.1rem;
  cursor: pointer;
  transition: color 0.3s ease;
}

.todo-text.completed {
  text-decoration: line-through;
  color: #94a3b8;
}

.todo-edit-input {
  flex: 1;
  padding: 0.5rem;
  font-size: 1.1rem;
  border: 2px solid #667eea;
  border-radius: 4px;
  outline: none;
}

.todo-meta {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: #64748b;
}

.todo-status {
  color: #10b981;
  font-weight: 600;
}

.delete-button {
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 4px;
  width: 2rem;
  height: 2rem;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.delete-button:hover {
  background: #dc2626;
  transform: scale(1.1);
}
</style>