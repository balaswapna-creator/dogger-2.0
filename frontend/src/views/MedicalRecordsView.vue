<template>
  <div class="records-container">
    <h1>Medical Records</h1>
    
    <div v-if="loading" class="loading">
      Loading medical records...
    </div>
    
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>
    
    <div v-else-if="records.length === 0" class="no-data">
      No medical records found. Add records from the patient details page.
    </div>
    
    <div v-else class="records-table">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Patient</th>
            <th>Owner</th>
            <th>Diagnosis</th>
            <th>Treatment</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in records" :key="record.id">
            <td>{{ formatDate(record.date) }}</td>
            <td>{{ record.patient_name }}</td>
            <td>{{ record.owner_name }}</td>
            <td>{{ record.diagnosis || '-' }}</td>
            <td>{{ record.treatment || '-' }}</td>
            <td>
              <button @click="viewRecord(record.id)" class="btn-small">
                View
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../services/api'

export default {
  name: 'MedicalRecordsView',
  setup() {
    const records = ref([])
    const loading = ref(true)
    const error = ref(null)

    const fetchRecords = async () => {
      try {
        loading.value = true
        error.value = null
        const response = await api.get('/medical-records/')
        records.value = response.data || []
      } catch (err) {
        console.error('Error fetching records:', err)
        error.value = 'Failed to load medical records. Please try again.'
      } finally {
        loading.value = false
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return '-'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }

    const viewRecord = (id) => {
      // Navigate to record detail view
      window.location.href = `/record/${id}`
    }

    onMounted(() => {
      fetchRecords()
    })

    return {
      records,
      loading,
      error,
      formatDate,
      viewRecord
    }
  }
}
</script>

<style scoped>
.records-container {
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

.records-table {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #3498db;
  color: white;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

tbody tr:hover {
  background: #f8f9fa;
}

.btn-small {
  background: #3498db;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-small:hover {
  background: #2980b9;
}
</style>