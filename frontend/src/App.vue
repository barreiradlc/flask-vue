  <template>
  <div id="app">
    <div class="container">
      <header class="header">
        <h1>📝 Vue Todo App</h1>
        <p class="subtitle">A simple todo app with TypeScript</p>
      </header>

      <main class="main-content">
        <TodoInput @add-todo="addTodo" />
        
        <div class="stats">
          <span>Total: {{ todos.length }}</span>
          <span>Completed: {{ completedCount }}</span>
          <span>Pending: {{ pendingCount }}</span>
        </div>

        <TodoFilter 
          v-model:filter="currentFilter"
          :filters="availableFilters"
        />

        <TodoList
          :todos="filteredTodos"
          @toggle-todo="toggleTodo"
          @delete-todo="deleteTodo"
          @edit-todo="editTodo"
        />

        <div v-if="todos.length === 0" class="empty-state">
          <p>No todos yet. Add one above!</p>
        </div>
      </main>

      <footer class="footer">
        <p>Double-click to edit a todo</p>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import TodoInput from './components/TodoInput.vue'
import TodoList from './components/TodoList.vue'
import TodoFilter from './components/TodoFilter.vue'
import type { Todo, NewTodo } from './types/todo'

// Available filter options
type FilterType = 'all' | 'active' | 'completed'

const availableFilters = [
  { value: 'all', label: 'All' },
  { value: 'active', label: 'Active' },
  { value: 'completed', label: 'Completed' }
]

const todos = ref<Todo[]>([])
const currentFilter = ref<FilterType>('all')

// Load todos from localStorage on mount
onMounted(() => {
  const savedTodos = localStorage.getItem('vue-todos')
  if (savedTodos) {
    todos.value = JSON.parse(savedTodos).map((todo: any) => ({
      ...todo,
      createdAt: new Date(todo.createdAt)
    }))
  }
})

// Save todos to localStorage whenever they change
const saveTodos = () => {
  localStorage.setItem('vue-todos', JSON.stringify(todos.value))
}

// Computed properties
const completedCount = computed(() => 
  todos.value.filter(todo => todo.completed).length
)

const pendingCount = computed(() => 
  todos.value.filter(todo => !todo.completed).length
)

const filteredTodos = computed(() => {
  switch (currentFilter.value) {
    case 'active':
      return todos.value.filter(todo => !todo.completed)
    case 'completed':
      return todos.value.filter(todo => todo.completed)
    default:
      return todos.value
  }
})

// Todo operations
const addTodo = (newTodo: NewTodo) => {
  if (newTodo.text.trim()) {
    const todo: Todo = {
      id: Date.now(),
      text: newTodo.text.trim(),
      completed: false,
      createdAt: new Date()
    }
    todos.value.unshift(todo)
    saveTodos()
  }
}

const toggleTodo = (id: number) => {
  const todo = todos.value.find(todo => todo.id === id)
  if (todo) {
    todo.completed = !todo.completed
    saveTodos()
  }
}

const deleteTodo = (id: number) => {
  todos.value = todos.value.filter(todo => todo.id !== id)
  saveTodos()
}

const editTodo = (payload: { id: number; text: string }) => {
  const todo = todos.value.find(todo => todo.id === payload.id)
  if (todo && payload.text.trim()) {
    todo.text = payload.text.trim()
    saveTodos()
  }
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.container {
  max-width: 600px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  text-align: center;
}

.header h1 {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 700;
}

.subtitle {
  margin: 0.5rem 0 0;
  opacity: 0.9;
  font-size: 1rem;
}

.main-content {
  padding: 2rem;
}

.stats {
  display: flex;
  justify-content: space-around;
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin: 1.5rem 0;
  font-weight: 600;
  color: #667eea;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
  font-style: italic;
}

.footer {
  text-align: center;
  padding: 1rem;
  background: #f8f9fa;
  color: #6c757d;
  font-size: 0.875rem;
  border-top: 1px solid #e9ecef;
}
</style>