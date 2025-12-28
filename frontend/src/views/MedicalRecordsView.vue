<template>
  <div class="records-wrapper">
    <!-- Header Card -->
    <div class="header-card">
      <div class="header-content">
        <div class="header-title">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
          <h1>Medical Records</h1>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading medical records...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-card">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
      </svg>
      <h3>Failed to Load Records</h3>
      <p>{{ error }}</p>
      <button @click="fetchRecords" class="btn-retry">Try Again</button>
    </div>

    <!-- Empty State -->
    <div v-else-if="records.length === 0" class="empty-state-card">
      <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
      </svg>
      <h3>No Medical Records Found</h3>
      <p>Medical records will appear here when you add them from patient details.</p>
    </div>

    <!-- Records Table -->
    <div v-else class="table-card">
      <div class="table-wrapper">
        <table class="data-table">
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
              <td>
                <div class="date-badge">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                  {{ formatDate(record.visit_date) }}
                </div>
              </td>
              <td>
                <div class="patient-info">
                  <div class="patient-avatar">{{ getInitial(getPatientName(record)) }}</div>
                  <span>{{ getPatientName(record) }}</span>
                </div>
              </td>
              <td>{{ getOwnerName(record) }}</td>
              <td>
                <span class="diagnosis-badge">{{ record.diagnosis || 'Not specified' }}</span>
              </td>
              <td class="treatment-cell">{{ record.treatment_plan || '-' }}</td>
              <td>
                <button @click="viewRecord(record.id)" class="btn-view">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  View
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
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
      loading.value = true
      error.value = null
      try {
        // ✅ FIXED: Use api service with correct endpoint
        const response = await api.get('/medical-records/')
        
        // ✅ FIXED: Handle both array and paginated responses
        const data = response.data || []
        records.value = Array.isArray(data) ? data : (data.results || [])
          
      } catch (err) {
        console.error('Error fetching records:', err)
        error.value = 'Failed to load medical records. Please try again.'
        records.value = []
      } finally {
        loading.value = false
      }
    }

    // ✅ FIXED: Safe helper functions to prevent null errors
    const getPatientName = (record) => {
      if (!record) return 'Unknown'
      if (record.patient_name) return record.patient_name
      if (record.patient?.pet_name) return record.patient.pet_name
      return 'Unknown Patient'
    }

    const getOwnerName = (record) => {
      if (!record) return 'Unknown'
      if (record.owner_name) return record.owner_name
      if (record.patient?.owner_name) return record.patient.owner_name
      if (record.patient?.owner?.name) return record.patient.owner.name
      return 'Unknown Owner'
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('en-IN', {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        })
      } catch (e) {
        return 'Invalid Date'
      }
    }

    const getInitial = (name) => {
      if (!name || typeof name !== 'string') return '?'
      return name.charAt(0).toUpperCase()
    }

    const viewRecord = (id) => {
      if (!id) {
        console.error('No record ID provided')
        return
      }
      window.location.href = `/records`
    }

    onMounted(() => {
      fetchRecords()
    })

    return {
      records,
      loading,
      error,
      getPatientName,
      getOwnerName,
      formatDate,
      getInitial,
      viewRecord,
      fetchRecords
    }
  }
}
</script>

<style scoped>
.records-wrapper {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.header-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-title svg {
  color: #8B5CF6;
}

.header-title h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1F2937;
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #E5E7EB;
  border-top-color: #8B5CF6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-card {
  background: white;
  border-radius: 16px;
  padding: 48px 24px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.error-card svg {
  color: #EF4444;
  margin-bottom: 16px;
}

.error-card h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
  color: #1F2937;
}

.error-card p {
  color: #6B7280;
  margin: 0 0 24px 0;
}

.btn-retry {
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-retry:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

.empty-state-card {
  background: white;
  border-radius: 16px;
  padding: 80px 24px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.empty-state-card svg {
  color: #D1D5DB;
  margin-bottom: 20px;
}

.empty-state-card h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
  color: #1F2937;
}

.empty-state-card p {
  color: #6B7280;
  margin: 0;
  max-width: 400px;
  margin: 0 auto;
}

.table-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
  color: white;
}

.data-table th {
  padding: 16px;
  text-align: left;
  font-weight: 600;
  font-size: 14px;
  white-space: nowrap;
}

.data-table td {
  padding: 16px;
  border-bottom: 1px solid #E5E7EB;
  font-size: 14px;
  color: #374151;
}

.data-table tbody tr:hover {
  background: #F9FAFB;
}

.data-table tbody tr:last-child td {
  border-bottom: none;
}

.date-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #EDE9FE;
  color: #6B21A8;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
}

.patient-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.patient-avatar {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  flex-shrink: 0;
}

.diagnosis-badge {
  background: #DBEAFE;
  color: #1E40AF;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
}

.treatment-cell {
  max-width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-view {
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s;
}

.btn-view:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

@media (max-width: 768px) {
  .records-wrapper {
    padding: 16px;
  }
}
</style>