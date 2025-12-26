<template>
  <div class="passbooks-container">
    <h1>Digital Passbooks</h1>
    
    <div v-if="loading" class="loading">
      Loading passbooks...
    </div>
    
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>
    
    <div v-else-if="passbooks.length === 0" class="no-data">
      No passbooks found. Create a passbook from the patient details page.
    </div>
    
    <div v-else class="passbooks-grid">
      <div v-for="passbook in passbooks" :key="passbook.id" class="passbook-card">
        <h3>{{ passbook.patient_name }}</h3>
        <p><strong>Owner:</strong> {{ passbook.owner_name }}</p>
        <p><strong>QR Code ID:</strong> {{ passbook.qr_code }}</p>
        <button @click="viewPassbook(passbook.id)" class="btn-primary">
          View Passbook
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../services/api'

export default {
  name: 'PassbooksView',
  setup() {
    const passbooks = ref([])
    const loading = ref(true)
    const error = ref(null)

    const fetchPassbooks = async () => {
      try {
        loading.value = true
        error.value = null
        const response = await api.get('/passbooks/')
        passbooks.value = response.data || []
      } catch (err) {
        console.error('Error fetching passbooks:', err)
        error.value = 'Failed to load passbooks. Please try again.'
      } finally {
        loading.value = false
      }
    }

    const viewPassbook = (id) => {
      // Navigate to passbook detail view
      window.open(`/passbook/${id}`, '_blank')
    }

    onMounted(() => {
      fetchPassbooks()
    })

    return {
      passbooks,
      loading,
      error,
      viewPassbook
    }
  }
}
</script>

<style scoped>
.passbooks-container {
  padding: 20px;
}

h1 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.loading, .error-message, .no-data {
  padding: 20px;
  text-align: center;
  font-size: 16px;
}

.error-message {
  color: #e74c3c;
  background: #fadbd8;
  border-radius: 4px;
}

.no-data {
  color: #7f8c8d;
  background: #ecf0f1;
  border-radius: 4px;
}

.passbooks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.passbook-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.passbook-card h3 {
  margin-top: 0;
  color: #2c3e50;
}

.passbook-card p {
  margin: 10px 0;
  color: #555;
}

.btn-primary {
  background: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.btn-primary:hover {
  background: #2980b9;
}
</style>