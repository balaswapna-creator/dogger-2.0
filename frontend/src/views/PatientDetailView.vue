<template>
  <div class="patient-detail-wrapper">
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading patient details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
      </svg>
      <h3>Error Loading Patient</h3>
      <p>{{ error }}</p>
      <button @click="$router.push('/patients')" class="btn-back">Back to Patients</button>
    </div>

    <!-- Patient Details -->
    <div v-else-if="patient" class="patient-detail-container">
      <!-- Header with Back Button -->
      <div class="detail-header">
        <button @click="$router.push('/patients')" class="btn-back-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          Back to Patients
        </button>
        <button @click="editPatient" class="btn-edit-header">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
          Edit
        </button>
      </div>

      <!-- Patient Profile Card -->
      <div class="profile-card">
        <div class="profile-photo">
          <img 
            v-if="getPhotoUrl(patient)" 
            :src="getPhotoUrl(patient)" 
            :alt="patient.pet_name"
            @error="handleImageError"
          />
          <div v-else class="photo-placeholder">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
            </svg>
          </div>
        </div>
        
        <div class="profile-info">
          <h1>{{ patient.pet_name }}</h1>
          <div class="profile-badges">
            <span class="badge species">{{ patient.species }}</span>
            <span class="badge">{{ patient.breed }}</span>
            <span class="badge gender" :class="patient.gender">
              <svg v-if="patient.gender === 'male'" width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                <circle cx="10" cy="14" r="6"></circle>
                <line x1="16" y1="8" x2="21" y2="3"></line>
                <line x1="21" y1="3" x2="21" y2="8"></line>
                <line x1="21" y1="3" x2="16" y2="3"></line>
              </svg>
              <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                <circle cx="12" cy="8" r="6"></circle>
                <line x1="12" y1="14" x2="12" y2="21"></line>
                <line x1="9" y1="18" x2="15" y2="18"></line>
              </svg>
              {{ patient.gender }}
            </span>
          </div>
          
          <div class="owner-info">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <div>
              <span class="owner-label">Owner</span>
              <span class="owner-name">{{ getOwnerName(patient.owner) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="stats-grid">
        <div class="stat-card">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
          <div>
            <span class="stat-label">Age</span>
            <span class="stat-value">{{ getAge(patient.date_of_birth) }}</span>
          </div>
        </div>

        <div class="stat-card">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
          </svg>
          <div>
            <span class="stat-label">Weight</span>
            <span class="stat-value">{{ patient.weight ? patient.weight + ' kg' : 'N/A' }}</span>
          </div>
        </div>

        <div class="stat-card">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
          <div>
            <span class="stat-label">Records</span>
            <span class="stat-value">{{ medicalRecords.length }}</span>
          </div>
        </div>

        <div class="stat-card">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <div>
            <span class="stat-label">Vaccinations</span>
            <span class="stat-value">{{ vaccinations.length }}</span>
          </div>
        </div>
      </div>

      <!-- Details Section -->
      <div class="details-section">
        <div class="section-card">
          <h2>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            Basic Information
          </h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">Pet Name</span>
              <span class="info-value">{{ patient.pet_name }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Species</span>
              <span class="info-value">{{ patient.species }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Breed</span>
              <span class="info-value">{{ patient.breed || 'Not specified' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Gender</span>
              <span class="info-value">{{ patient.gender }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Date of Birth</span>
              <span class="info-value">{{ formatDate(patient.date_of_birth) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Color</span>
              <span class="info-value">{{ patient.color || 'Not specified' }}</span>
            </div>
          </div>
          
          <div v-if="patient.medical_history" class="medical-history">
            <span class="info-label">Medical History</span>
            <p class="history-text">{{ patient.medical_history }}</p>
          </div>
        </div>
      </div>

      <!-- Medical Records -->
      <div class="section-card">
        <div class="section-header">
          <h2>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
            </svg>
            Medical Records
          </h2>
          <button @click="$router.push('/medical-records')" class="btn-view-all">View All</button>
        </div>
        
        <div v-if="medicalRecords.length > 0" class="records-list">
          <div v-for="record in medicalRecords" :key="record.id" class="record-item">
            <div class="record-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
              </svg>
            </div>
            <div class="record-content">
              <h4>{{ record.diagnosis }}</h4>
              <p>{{ record.treatment }}</p>
              <span class="record-date">{{ formatDate(record.visit_date) }}</span>
            </div>
          </div>
        </div>
        <div v-else class="empty-section">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
          <p>No medical records yet</p>
        </div>
      </div>

      <!-- Vaccinations -->
      <div class="section-card">
        <div class="section-header">
          <h2>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            Vaccination History
          </h2>
          <button @click="$router.push('/vaccinations')" class="btn-view-all">View All</button>
        </div>
        
        <div v-if="vaccinations.length > 0" class="vaccinations-list">
          <div v-for="vacc in vaccinations" :key="vacc.id" class="vaccination-item">
            <div class="vacc-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
            </div>
            <div class="vacc-content">
              <h4>{{ vacc.vaccine_name }}</h4>
              <span class="vacc-date">Given: {{ formatDate(vacc.vaccination_date) }}</span>
              <span v-if="vacc.next_due_date" class="vacc-next">Next: {{ formatDate(vacc.next_due_date) }}</span>
            </div>
          </div>
        </div>
        <div v-else class="empty-section">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <p>No vaccinations recorded</p>
        </div>
      </div>

      <!-- Payments -->
      <div class="section-card">
        <div class="section-header">
          <h2>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
              <line x1="1" y1="10" x2="23" y2="10"></line>
            </svg>
            Payment History
          </h2>
          <button @click="$router.push('/payments')" class="btn-view-all">View All</button>
        </div>
        
        <div v-if="payments.length > 0" class="payments-list">
          <div v-for="payment in payments" :key="payment.id" class="payment-item">
            <div class="payment-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="1" x2="12" y2="23"></line>
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
              </svg>
            </div>
            <div class="payment-content">
              <div class="payment-info">
                <h4>{{ payment.description || 'Payment' }}</h4>
                <span class="payment-amount">₹{{ payment.amount }}</span>
              </div>
              <div class="payment-meta">
                <span class="payment-date">{{ formatDate(payment.payment_date) }}</span>
                <span class="payment-status" :class="payment.payment_method">{{ payment.payment_method }}</span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="empty-section">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
            <line x1="1" y1="10" x2="23" y2="10"></line>
          </svg>
          <p>No payments recorded</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';

const route = useRoute();
const router = useRouter();

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const BACKEND_URL = API_BASE_URL.replace('/api', '');
const MEDIA_URL = `${BACKEND_URL}/media/`;

const patient = ref(null);
const medicalRecords = ref([]);
const vaccinations = ref([]);
const payments = ref([]);
const owners = ref([]);
const isLoading = ref(true);
const error = ref(null);

const getPhotoUrl = (patient) => {
  if (!patient.photo) return null;
  if (patient.photo.startsWith('http')) return patient.photo;
  const photoPath = patient.photo.replace(/^\/+/, '').replace('media/', '');
  return `${MEDIA_URL}${photoPath}`;
};

const handleImageError = (event) => {
  event.target.style.display = 'none';
};

const getOwnerName = (ownerId) => {
  const owner = owners.value.find(o => o.id === ownerId);
  return owner ? owner.name : 'Unknown Owner';
};

const getAge = (dateOfBirth) => {
  if (!dateOfBirth) return 'Unknown';
  
  const birthDate = new Date(dateOfBirth);
  const today = new Date();
  const diffTime = Math.abs(today - birthDate);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  const years = Math.floor(diffDays / 365);
  const months = Math.floor((diffDays % 365) / 30);
  
  if (years > 0) {
    return months > 0 ? `${years}y ${months}m` : `${years} year${years > 1 ? 's' : ''}`;
  } else if (months > 0) {
    return `${months} month${months > 1 ? 's' : ''}`;
  } else {
    return `${diffDays} day${diffDays > 1 ? 's' : ''}`;
  }
};

const formatDate = (date) => {
  if (!date) return 'Not specified';
  return new Date(date).toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
};

const fetchPatientData = async () => {
  isLoading.value = true;
  error.value = null;
  
  try {
    const patientId = route.params.id;
    console.log('Fetching patient data for ID:', patientId);
    
    // Fetch patient first
    const patientRes = await api.get(`/patients/${patientId}/`);
    patient.value = patientRes.data;
    console.log('Patient loaded:', patient.value);
    
    // Then fetch related data
    const [ownersRes, recordsRes, vaccRes, paymentsRes, passbooksRes] = await Promise.all([
      api.get('/owners/'),
      api.get('/medical-records/'),
      api.get('/vaccinations/'),
      api.get('/payments/'),
      api.get('/passbooks/').catch(err => {
        console.log('Passbooks endpoint not available:', err);
        return { data: [] };
      })
    ]);
    
    owners.value = Array.isArray(ownersRes.data) ? ownersRes.data : (ownersRes.data.results || []);
    
    // Filter records for this patient (compare as strings since IDs are UUIDs)
    const allRecords = Array.isArray(recordsRes.data) ? recordsRes.data : (recordsRes.data.results || []);
    medicalRecords.value = allRecords.filter(r => {
      const recordPatientId = r.patient?.id || r.patient;
      return String(recordPatientId) === String(patientId);
    });
    
    const allVacc = Array.isArray(vaccRes.data) ? vaccRes.data : (vaccRes.data.results || []);
    vaccinations.value = allVacc.filter(v => {
      const vaccPatientId = v.patient?.id || v.patient;
      return String(vaccPatientId) === String(patientId);
    });
    
    const allPayments = Array.isArray(paymentsRes.data) ? paymentsRes.data : (paymentsRes.data.results || []);
    payments.value = allPayments.filter(p => {
      const paymentPatientId = p.patient?.id || p.patient;
      return String(paymentPatientId) === String(patientId);
    });
    
    // Check if passbook exists for this patient
    const allPassbooks = Array.isArray(passbooksRes.data) ? passbooksRes.data : (passbooksRes.data.results || []);
    hasPassbook.value = allPassbooks.some(pb => {
      const pbPatientId = pb.patient?.id || pb.patient;
      return String(pbPatientId) === String(patientId);
    });
    
    console.log('Data loaded - Records:', medicalRecords.value.length, 'Vaccinations:', vaccinations.value.length, 'Payments:', payments.value.length, 'Has Passbook:', hasPassbook.value);
    
  } catch (err) {
    console.error('Error fetching patient data:', err);
    error.value = err.response?.data?.detail || err.message || 'Failed to load patient details';
  } finally {
    isLoading.value = false;
  }
};

const editPatient = () => {
  router.push(`/patients?edit=${patient.value.id}`);
};

const createPassbook = async () => {
  if (!patient.value?.id) return;
  
  creatingPassbook.value = true;
  try {
    const response = await api.post('/passbooks/', {
      patient: patient.value.id,
      is_enabled: true,
      subscription_type: 'yearly'
    });
    
    alert('Digital passbook created successfully!');
    hasPassbook.value = true;
    
    // Optionally refresh data
    await fetchPatientData();
  } catch (err) {
    console.error('Error creating passbook:', err);
    alert('Failed to create passbook: ' + (err.response?.data?.detail || err.message));
  } finally {
    creatingPassbook.value = false;
  }
};

const viewPassbook = () => {
  if (patient.value?.id) {
    router.push('/passbooks');
  }
};

onMounted(() => {
  fetchPatientData();
});
</script>

<style scoped>
.patient-detail-wrapper {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Loading & Error States */
.loading-state, .error-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #E5E7EB;
  border-top-color: #7C3AED;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state svg {
  color: #EF4444;
  margin-bottom: 16px;
}

.error-state h3 {
  margin: 0 0 8px 0;
  color: #1F2937;
}

.error-state p {
  color: #6B7280;
  margin: 0 0 24px 0;
}

/* Header */
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.btn-back-icon, .btn-back {
  background: white;
  color: #4B5563;
  border: 2px solid #E5E7EB;
  padding: 10px 20px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-back-icon:hover, .btn-back:hover {
  border-color: #7C3AED;
  color: #7C3AED;
  transform: translateX(-4px);
}

.btn-edit-header {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.btn-edit-header:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
}

/* Profile Card */
.profile-card {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  border-radius: 20px;
  padding: 40px;
  margin-bottom: 24px;
  display: flex;
  gap: 32px;
  align-items: center;
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.3);
  color: white;
}

.profile-photo {
  width: 180px;
  height: 180px;
  border-radius: 20px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 4px solid rgba(255, 255, 255, 0.3);
}

.profile-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-placeholder {
  color: white;
  opacity: 0.6;
}

.profile-info {
  flex: 1;
}

.profile-info h1 {
  margin: 0 0 16px 0;
  font-size: 36px;
  font-weight: 700;
}

.profile-badges {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.badge {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  color: white;
  padding: 6px 16px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

.badge.species {
  background: rgba(255, 255, 255, 0.3);
}

.badge.gender.male {
  background: rgba(59, 130, 246, 0.3);
}

.badge.gender.female {
  background: rgba(236, 72, 153, 0.3);
}

.owner-info {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  padding: 16px 20px;
  border-radius: 12px;
}

.owner-info > div {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.owner-label {
  font-size: 13px;
  opacity: 0.8;
}

.owner-name {
  font-size: 16px;
  font-weight: 600;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.15);
}

.stat-card svg {
  color: #7C3AED;
  flex-shrink: 0;
}

.stat-card > div {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 13px;
  color: #6B7280;
  font-weight: 500;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: #1F2937;
}

/* Section Cards */
.section-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.section-card h2 {
  margin: 0 0 20px 0;
  font-size: 20px;
  font-weight: 700;
  color: #1F2937;
  display: flex;
  align-items: center;
  gap: 12px;
}

.section-card h2 svg {
  color: #7C3AED;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.btn-view-all {
  background: #F3F4F6;
  color: #7C3AED;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-view-all:hover {
  background: #EDE9FE;
}

/* Info Grid */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.info-label {
  font-size: 13px;
  color: #6B7280;
  font-weight: 600;
}

.info-value {
  font-size: 15px;
  color: #1F2937;
  font-weight: 500;
}

.medical-history {
  padding-top: 20px;
  border-top: 1px solid #E5E7EB;
}

.history-text {
  margin: 8px 0 0 0;
  color: #4B5563;
  line-height: 1.6;
}

/* Records List */
.records-list, .vaccinations-list, .payments-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.record-item, .vaccination-item, .payment-item {
  background: #F9FAFB;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  gap: 16px;
  transition: all 0.3s;
}

.record-item:hover, .vaccination-item:hover, .payment-item:hover {
  background: #F3F4F6;
  transform: translateX(4px);
}

.record-icon, .vacc-icon, .payment-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.record-content, .vacc-content {
  flex: 1;
}

.record-content h4, .vacc-content h4 {
  margin: 0 0 6px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1F2937;
}

.record-content p {
  margin: 0 0 8px 0;
  color: #6B7280;
  font-size: 14px;
  line-height: 1.5;
}

.record-date, .vacc-date, .vacc-next {
  font-size: 13px;
  color: #9CA3AF;
  display: block;
}

.vacc-next {
  color: #7C3AED;
  font-weight: 600;
  margin-top: 4px;
}

/* Payment Items */
.payment-content {
  flex: 1;
}

.payment-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.payment-info h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1F2937;
}

.payment-amount {
  font-size: 18px;
  font-weight: 700;
  color: #10B981;
}

.payment-meta {
  display: flex;
  gap: 12px;
  align-items: center;
}

.payment-date {
  font-size: 13px;
  color: #9CA3AF;
}

.payment-status {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 6px;
  text-transform: uppercase;
  background: #DBEAFE;
  color: #1E40AF;
}

.payment-status.cash {
  background: #D1FAE5;
  color: #065F46;
}

.payment-status.card {
  background: #E0E7FF;
  color: #3730A3;
}

.payment-status.upi {
  background: #FCE7F3;
  color: #831843;
}

/* Empty Section */
.empty-section {
  text-align: center;
  padding: 40px 20px;
  color: #9CA3AF;
}

.empty-section svg {
  margin-bottom: 12px;
}

.empty-section p {
  margin: 0;
  font-size: 15px;
}

/* Responsive */
@media (max-width: 768px) {
  .patient-detail-wrapper {
    padding: 16px;
  }
  
  .profile-card {
    flex-direction: column;
    text-align: center;
    padding: 30px 20px;
  }
  
  .profile-photo {
    width: 140px;
    height: 140px;
  }
  
  .profile-info h1 {
    font-size: 28px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .detail-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .btn-back-icon, .btn-edit-header {
    justify-content: center;
  }
}

/* Passbook Section Styles */
.passbook-section {
  background: linear-gradient(135deg, #F0FDF4, #DCFCE7);
  border: 2px solid #10B981;
}

.passbook-active {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 20px;
}

.passbook-badge {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #14B8A6, #0D9488);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.passbook-info {
  flex: 1;
}

.passbook-info h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 700;
  color: #065F46;
}

.passbook-info p {
  margin: 0 0 16px 0;
  color: #047857;
  font-size: 14px;
}

.btn-view-passbook {
  background: linear-gradient(135deg, #14B8A6, #0D9488);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-view-passbook:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(20, 184, 166, 0.4);
}

.passbook-inactive {
  text-align: center;
  padding: 40px 20px;
}

.passbook-inactive svg {
  color: #10B981;
  margin-bottom: 16px;
}

.passbook-inactive h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 700;
  color: #065F46;
}

.passbook-inactive p {
  margin: 0 0 24px 0;
  color: #047857;
  font-size: 14px;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.btn-create-passbook {
  background: linear-gradient(135deg, #10B981, #059669);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-create-passbook:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

.btn-create-passbook:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.mini-spinner {
  width: 18px;
  height: 18px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
</style>