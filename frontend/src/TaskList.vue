<template>
  <div class="task-list">
    <!-- Loading state -->
    <div v-if="loading" class="loading">
      Loading tasks...
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="fetchTasks" class="retry-btn">Retry</button>
    </div>
    
    <!-- Task list -->
    <div v-else>
      <div class="task-filters">
        <button 
          v-for="status in statusOptions" 
          :key="status.value"
          @click="filterTasks(status.value)"
          :class="{ active: currentFilter === status.value }"
          class="filter-btn"
        >
          {{ status.label }}
        </button>
      </div>
      
      <ul v-if="filteredTasks.length" class="task-items">
        <li 
          v-for="task in filteredTasks" 
          :key="task.id"
          :class="['task-item', `status-${task.status}`]"
        >
          <div class="task-content">
            <h3>{{ task.title }}</h3>
            <span class="task-status">{{ getStatusLabel(task.status) }}</span>
            <small class="task-date">{{ formatDate(task.created_at) }}</small>
          </div>
          <div class="task-actions">
            <button 
              v-if="task.status !== 'completed'"
              @click="markComplete(task.id)"
              class="complete-btn"
            >
              Mark Complete
            </button>
          </div>
        </li>
      </ul>
      
      <div v-else class="no-tasks">
        No tasks found for the selected filter.
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'TaskList',
  setup() {
    const tasks = ref([])
    const loading = ref(false)
    const error = ref(null)
    const currentFilter = ref('all')

    const statusOptions = [
      { value: 'all', label: 'All' },
      { value: 'pending', label: 'Pending' },
      { value: 'in_progress', label: 'In Progress' },
      { value: 'completed', label: 'Completed' }
    ]

    const filteredTasks = computed(() => {
      if (currentFilter.value === 'all') {
        return tasks.value
      }
      return tasks.value.filter(task => task.status === currentFilter.value)
    })

    const fetchTasks = async () => {
      loading.value = true
      error.value = null
      
      try {
        const response = await fetch('/api/tasks/')
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        }
        
        const data = await response.json()
        tasks.value = data.results || data // Handle paginated or direct array response
        
      } catch (err) {
        console.error('Failed to fetch tasks:', err)
        error.value = `Failed to load tasks: ${err.message}`
      } finally {
        loading.value = false
      }
    }

    const markComplete = async (taskId) => {
      try {
        const response = await fetch(`/api/tasks/${taskId}/mark_complete/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        })

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        }

        // Update local task status
        const taskIndex = tasks.value.findIndex(task => task.id === taskId)
        if (taskIndex !== -1) {
          tasks.value[taskIndex].status = 'completed'
        }

      } catch (err) {
        console.error('Failed to mark task complete:', err)
        error.value = `Failed to update task: ${err.message}`
      }
    }

    const filterTasks = (status) => {
      currentFilter.value = status
    }

    const getStatusLabel = (status) => {
      const option = statusOptions.find(opt => opt.value === status)
      return option ? option.label : status
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }

    onMounted(() => {
      fetchTasks()
    })

    return {
      tasks,
      loading,
      error,
      currentFilter,
      statusOptions,
      filteredTasks,
      fetchTasks,
      markComplete,
      filterTasks,
      getStatusLabel,
      formatDate
    }
  }
}
</script>

<style scoped>
.task-list {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.loading, .error {
  text-align: center;
  padding: 20px;
}

.error {
  color: #e74c3c;
}

.retry-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.task-filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.filter-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.filter-btn.active {
  background: #3498db;
  color: white;
}

.task-items {
  list-style: none;
  padding: 0;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 10px;
}

.task-item.status-completed {
  background: #d4edda;
  border-color: #c3e6cb;
}

.task-content h3 {
  margin: 0 0 5px 0;
}

.task-status {
  display: inline-block;
  padding: 2px 8px;
  background: #e9ecef;
  border-radius: 12px;
  font-size: 12px;
  margin-right: 10px;
}

.task-date {
  color: #6c757d;
}

.complete-btn {
  background: #28a745;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.no-tasks {
  text-align: center;
  color: #6c757d;
  padding: 40px;
}
</style>
