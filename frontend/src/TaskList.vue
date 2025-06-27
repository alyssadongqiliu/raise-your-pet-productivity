<template>
  <ul>
    <li v-for="task in tasks" :key="task.id">
      {{ task.title }} — {{ task.status }}
    </li>
  </ul>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  setup() {
    const tasks = ref([])
    onMounted(async () => {
      const res = await fetch('/api/tasks/')
      tasks.value = await res.json()
    })
    return { tasks }
  }
}
</script>
