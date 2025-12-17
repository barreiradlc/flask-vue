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
import axios from 'axios'
import { computed, onMounted, ref } from 'vue'
import TodoFilter from './components/TodoFilter.vue'
import TodoInput from './components/TodoInput.vue'
import TodoList from './components/TodoList.vue'
import type { NewTodo, Todo } from './types/todo'

const apiUrl = import.meta.env.VITE_API_URL;

// Available filter options
type FilterType = 'all' | 'active' | 'completed'

type FilterOption = {
  value: FilterType
  label: string
}

const availableFilters: FilterOption[] = [
  { value: 'all', label: 'All' },
  { value: 'active', label: 'Active' },
  { value: 'completed', label: 'Completed' }
]

const todos = ref<Todo[]>([])
const currentFilter = ref<FilterType>('all')

const loadTodos = async () => {
  try {
    const url = `${apiUrl}/api/todos`
    const { data } = await axios.get(url)

    todos.value = data.map((todo: Todo) => ({
      ...todo,
      createdAt: new Date(todo.createdAt)
    }))
  } catch ( error) {
    console.error("Error loading todos:", error)
  }
}

// Load todos on mount
onMounted(async () => {
  loadTodos()
})

// Save todos to localStorage whenever they change
const saveTodos = async (todo?: Todo) => {
  localStorage.setItem('vue-todos', JSON.stringify(todo ? todos.value.unshift(todo) : todos.value))
  
  await loadTodos()
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
const addTodo = async (newTodo: NewTodo) => {
  try {
    
    const url = `${apiUrl}/api/todos`
    const { data } = await axios.post(url, 
      { description: newTodo.description.trim() }
    )
  
    saveTodos()
  } catch ( error) {
    console.error("Error adding todo:", error)
  }
}

const deleteTodo = async (id: number) => {
  todos.value = todos.value.filter(todo => todo.id !== id)
  const url = `${apiUrl}/api/todos/${id}`
  await axios.delete(url)

  saveTodos()
}

const toggleTodo = async (payload: { id: number; completed: boolean }) => {
  console.log("Toggling todo:", payload);
  try {
    const url = `${apiUrl}/api/todos/check/${payload.id}`
    await axios.put(url, { completed: !payload.completed })
    
    saveTodos()
  } catch (error) {
    console.error("Error toggling todo:", error)
  }
}

const editTodo = async (payload: { id: number; text: string }) => {
  const url = `${apiUrl}/api/todos/${payload.id}`
  await axios.put(url, { description: payload.text.trim() })

  saveTodos()
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  font-family: "Nunito Sans", sans-serif;
  font-optical-sizing: auto;
  font-weight: <weight>;
  font-style: normal;
  font-variation-settings:
    "wdth" 100,
    "YTLC" 500;
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