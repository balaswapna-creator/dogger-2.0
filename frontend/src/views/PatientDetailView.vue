<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      <p class="mt-4 text-gray-600">Loading patient details...</p>
    </div>

    <div v-else-if="error" class="max-w-4xl mx-auto px-4">
      <div class="bg-red-50 border border-red-200 text-red-800 rounded-lg p-4">
        <p class="font-semibold">Error loading patient</p>
        <p class="text-sm mt-1">{{ error }}</p>
        <button @click="$router.push('/patients')" class="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
          Back to Patients
        </button>
      </div>
    </div>

    <div v-else-if="patient" class="max-w-6xl mx-auto px-4">
      <!-- Header -->
      <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <button @click="$router.push('/patients')" class="p-2 hover:bg-gray-200 rounded-lg">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <h1 class="text-3xl font-bold text-gray-800">Patient Details</h1>
        </div>
        <button @click="$router.push(`/patients/edit/${patient.id}`)" class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
          Edit Patient
        </button>
      </div>

      <!-- Patient Info Card -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <div class="flex items-start gap-6">
          <!-- Photo -->
          <div class="flex-shrink-0">
            <img v-if="patient.photo" :src="patient.photo" :alt="patient.name" class="w-32 h-32 rounded-lg object-cover border-2 border-gray-200">
            <div v-else class="w-32 h-32 rounded-lg bg-gray-200 flex items-center justify-center">
              <svg class="w-16 h-16 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" />
              </svg>
            </div>
          </div>

          <!-- Info Grid -->
          <div class="flex-1 grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-600">Patient Name</p>
              <p class="text-lg font-semibold text-gray-800">{{ patient.name }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Species</p>
              <p class="text-lg font-semibold text-gray-800 capitalize">{{ patient.species }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Breed</p>
              <p class="text-lg font-semibold text-gray-800">{{ patient.breed || 'N/A' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Gender</p>
              <p class="text-lg font-semibold text-gray-800 capitalize">{{ patient.gender }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Age</p>
              <p class="text-lg font-semibold text-gray-800">{{ calculateAge(patient.date_of_birth) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Date of Birth</p>
              <p class="text-lg font-semibold text-gray-800">{{ formatDate(patient.date_of_birth) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Registration Date</p>
              <p class="text-lg font-semibold text-gray-800">{{ formatDate(patient.created_at) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Microchip ID</p>
              <p class="text-lg font-semibold text-gray-800">{{ patient.microchip_id || 'N/A' }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Owner Info Card -->
      <div v-if="patient.owner" class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" />
          </svg>
          Owner Information
        </h2>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-sm text-gray-600">Name</p>
            <p class="text-lg font-semibold text-gray-800">{{ patient.owner.name }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-600">Phone</p>
            <p class="text-lg font-semibold text-gray-800">{{ patient.owner.phone }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-600">Email</p>
            <p class="text-lg font-semibold text-gray-800">{{ patient.owner.email || 'N/A' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-600">Address</p>
            <p class="text-lg font-semibold text-gray-800">{{ patient.owner.address || 'N/A' }}</p>
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-cols-3 gap-4 mb-6">
        <div class="bg-white rounded-lg shadow-md p-4">
          <p class="text-sm text-gray-600">Latest Vaccination</p>
          <p class="text-lg font-semibold text-blue-600">{{ getLatestVaccination() }}</p>
        </div>
        <div class="bg-white rounded-lg shadow-md p-4">
          <p class="text-sm text-gray-600">Total Visits</p>
          <p class="text-lg font-semibold text-green-600">{{ patient.medical_records?.length || 0 }}</p>
        </div>
        <div class="bg-white rounded-lg shadow-md p-4">
          <p class="text-sm text-gray-600">Total Payments</p>
          <p class="text-lg font-semibold text-purple-600">{{ getTotalPayments() }}</p>
        </div>
      </div>

      <!-- Digital Passbook Section -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
            <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd" />
          </svg>
          Digital Passbook
        </h2>
        <p class="text-gray-600 mb-4">Create a digital passbook for {{ patient.name }} to share medical records with the owner via QR code.</p>
        <button @click="createPassbook" :disabled="creatingPassbook" class="px-6 py-3 bg-teal-600 text-white rounded-lg hover:bg-teal-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2">
          <svg v-if="creatingPassbook" class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ creatingPassbook ? 'Creating...' : 'Create Digital Passbook' }}</span>
        </button>
      </div>

      <!-- Tabs for different sections -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="border-b border-gray-200">
          <nav class="flex -mb-px">
            <button @click="activeTab = 'medical'" :class="tabClass('medical')" class="px-6 py-4 text-sm font-medium border-b-2">
              Medical Records
            </button>
            <button @click="activeTab = 'vaccinations'" :class="tabClass('vaccinations')" class="px-6 py-4 text-sm font-medium border-b-2">
              Vaccinations
            </button>
            <button @click="activeTab = 'payments'" :class="tabClass('payments')" class="px-6 py-4 text-sm font-medium border-b-2">
              Payments
            </button>
          </nav>
        </div>

        <div class="p-6">
          <!-- Medical Records Tab -->
          <div v-if="activeTab === 'medical'">
            <div v-if="patient.medical_records && patient.medical_records.length > 0" class="space-y-4">
              <div v-for="record in patient.medical_records" :key="record.id" class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <p class="font-semibold text-gray-800">{{ formatDate(record.visit_date) }}</p>
                    <p class="text-sm text-gray-600">Dr. {{ record.veterinarian || 'N/A' }}</p>
                  </div>
                  <span class="px-3 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">{{ record.visit_type || 'Checkup' }}</span>
                </div>
                <div class="mt-3">
                  <p class="text-sm text-gray-600">Diagnosis:</p>
                  <p class="text-gray-800">{{ record.diagnosis || 'N/A' }}</p>
                </div>
                <div class="mt-2">
                  <p class="text-sm text-gray-600">Treatment:</p>
                  <p class="text-gray-800">{{ record.treatment || 'N/A' }}</p>
                </div>
                <div v-if="record.notes" class="mt-2">
                  <p class="text-sm text-gray-600">Notes:</p>
                  <p class="text-gray-800">{{ record.notes }}</p>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-12 text-gray-500">
              <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p class="text-lg">No medical records found</p>
            </div>
          </div>

          <!-- Vaccinations Tab -->
          <div v-if="activeTab === 'vaccinations'">
            <div v-if="patient.vaccinations && patient.vaccinations.length > 0" class="space-y-4">
              <div v-for="vaccination in patient.vaccinations" :key="vaccination.id" class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                <div class="flex justify-between items-start">
                  <div class="flex-1">
                    <p class="font-semibold text-gray-800">{{ vaccination.vaccine_name }}</p>
                    <p class="text-sm text-gray-600 mt-1">Administered: {{ formatDate(vaccination.date_administered) }}</p>
                    <p class="text-sm text-gray-600">Next Due: {{ formatDate(vaccination.next_due_date) || 'N/A' }}</p>
                    <p v-if="vaccination.certificate_number" class="text-sm text-gray-600 mt-2">Certificate: {{ vaccination.certificate_number }}</p>
                  </div>
                  <span :class="vaccination.next_due_date && new Date(vaccination.next_due_date) < new Date() ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'" class="px-3 py-1 text-xs rounded-full">
                    {{ vaccination.next_due_date && new Date(vaccination.next_due_date) < new Date() ? 'Overdue' : 'Current' }}
                  </span>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-12 text-gray-500">
              <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
              </svg>
              <p class="text-lg">No vaccination records found</p>
            </div>
          </div>

          <!-- Payments Tab -->
          <div v-if="activeTab === 'payments'">
            <div v-if="patient.payments && patient.payments.length > 0" class="space-y-4">
              <div v-for="payment in patient.payments" :key="payment.id" class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                <div class="flex justify-between items-start">
                  <div class="flex-1">
                    <p class="font-semibold text-gray-800">₹{{ parseFloat(payment.amount).toFixed(2) }}</p>
                    <p class="text-sm text-gray-600 mt-1">{{ formatDate(payment.payment_date) }}</p>
                    <p class="text-sm text-gray-600">Method: {{ payment.payment_method || 'Cash' }}</p>
                    <p v-if="payment.notes" class="text-sm text-gray-600 mt-2">{{ payment.notes }}</p>
                  </div>
                  <span :class="payment.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'" class="px-3 py-1 text-xs rounded-full capitalize">
                    {{ payment.status || 'Pending' }}
                  </span>
                </div>
              </div>
              <div class="border-t pt-4 mt-4">
                <div class="flex justify-between items-center">
                  <span class="text-lg font-semibold text-gray-800">Total Payments:</span>
                  <span class="text-2xl font-bold text-green-600">{{ getTotalPayments() }}</span>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-12 text-gray-500">
              <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <p class="text-lg">No payment records found</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Passbook Modal -->
    <div v-if="showPassbookModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-xl font-bold mb-4">Create Digital Passbook</h3>
        <p class="text-gray-600 mb-6">Are you sure you want to create a digital passbook for {{ patient?.name }}?</p>
        <p class="text-sm text-gray-500 mb-6">This will generate a QR code that the owner can use to access medical records.</p>
        <div class="flex gap-3 justify-end">
          <button @click="showPassbookModal = false" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
            Cancel
          </button>
          <button @click="confirmCreatePassbook" :disabled="creatingPassbook" class="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 disabled:bg-gray-400">
            {{ creatingPassbook ? 'Creating...' : 'Create' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';

const route = useRoute();
const router = useRouter();

const patient = ref(null);
const loading = ref(true);
const error = ref(null);
const activeTab = ref('medical');
const showPassbookModal = ref(false);
const creatingPassbook = ref(false);

const calculateAge = (dateOfBirth) => {
  if (!dateOfBirth) return 'Unknown';
  
  const birthDate = new Date(dateOfBirth);
  const today = new Date();
  
  let years = today.getFullYear() - birthDate.getFullYear();
  let months = today.getMonth() - birthDate.getMonth();
  
  if (months < 0) {
    years--;
    months += 12;
  }
  
  if (years === 0) {
    return `${months} month${months !== 1 ? 's' : ''}`;
  } else if (months === 0) {
    return `${years} year${years !== 1 ? 's' : ''}`;
  } else {
    return `${years} year${years !== 1 ? 's' : ''}, ${months} month${months !== 1 ? 's' : ''}`;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-IN', { 
    day: '2-digit', 
    month: 'short', 
    year: 'numeric' 
  });
};

const getLatestVaccination = () => {
  if (!patient.value?.vaccinations || patient.value.vaccinations.length === 0) {
    return 'No vaccinations';
  }
  
  const latest = patient.value.vaccinations.sort((a, b) => 
    new Date(b.date_administered) - new Date(a.date_administered)
  )[0];
  
  return `${latest.vaccine_name} - ${formatDate(latest.date_administered)}`;
};

const getTotalPayments = () => {
  if (!patient.value?.payments || patient.value.payments.length === 0) {
    return '₹0.00';
  }
  
  const total = patient.value.payments.reduce((sum, payment) => 
    sum + parseFloat(payment.amount || 0), 0
  );
  
  return `₹${total.toFixed(2)}`;
};

const tabClass = (tab) => {
  return activeTab.value === tab
    ? 'border-purple-600 text-purple-600'
    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300';
};

const fetchPatient = async () => {
  try {
    loading.value = true;
    const response = await api.get(`/patients/${route.params.id}/`);
    patient.value = response.data;
    error.value = null;
  } catch (err) {
    console.error('Error fetching patient:', err);
    error.value = err.response?.data?.detail || 'Failed to load patient details';
  } finally {
    loading.value = false;
  }
};

const createPassbook = () => {
  showPassbookModal.value = true;
};

const confirmCreatePassbook = async () => {
  try {
    creatingPassbook.value = true;
    const response = await api.post('/passbooks/', {
      patient_id: patient.value.id
    });
    
    alert('Passbook created successfully!');
    showPassbookModal.value = false;
    
    // Refresh patient data to get passbook info
    await fetchPatient();
  } catch (err) {
    console.error('Error creating passbook:', err);
    alert(err.response?.data?.error || 'Failed to create passbook');
  } finally {
    creatingPassbook.value = false;
  }
};

onMounted(() => {
  fetchPatient();
});
</script>

<style scoped>
.patient-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading-state, .error-state {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #7C3AED;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon {
  font-size: 60px;
  margin-bottom: 20px;
}

.detail-header {
  margin-bottom: 30px;
}

.detail-header h1 {
  font-size: 32px;
  color: #1a1a1a;
  margin: 10px 0;
}

.btn-back {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-back:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
}

.info-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f3f4f6;
}

.card-header h2 {
  font-size: 20px;
  color: #1a1a1a;
  margin: 0;
}

.record-count {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.info-grid {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.photo-section {
  text-align: center;
}

.patient-photo {
  width: 180px;
  height: 180px;
  object-fit: cover;
  border-radius: 16px;
  border: 4px solid #7C3AED;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.no-photo {
  width: 180px;
  height: 180px;
  background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  border-radius: 16px;
  margin: 0 auto;
}

.info-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.detail-row .label {
  font-weight: 600;
  color: #6b7280;
  min-width: 150px;
}

.detail-row .value {
  color: #1a1a1a;
  font-weight: 500;
}

.owner-section {
  padding-top: 24px;
  border-top: 2px solid #f3f4f6;
}

.owner-section h3 {
  font-size: 18px;
  margin-bottom: 16px;
  color: #1a1a1a;
}

/* Passbook Section */
.passbook-section {
  background: linear-gradient(135deg, #F0F9FF, #E0F2FE);
  border: 2px solid #06B6D4;
}

.passbook-create, .passbook-exists {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.passbook-info {
  color: #0c4a6e;
  line-height: 1.6;
  flex: 1;
}

.btn-create-passbook {
  background: linear-gradient(135deg, #06B6D4, #0891B2);
  color: white;
  border: none;
  padding: 14px 28px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  white-space: nowrap;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
}

.btn-create-passbook:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(6, 182, 212, 0.4);
}

.passbook-success {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #047857;
  font-weight: 600;
  font-size: 16px;
}

.success-icon {
  font-size: 24px;
}

.btn-view-passbook {
  background: linear-gradient(135deg, #10B981, #059669);
  color: white;
  border: none;
  padding: 14px 28px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-view-passbook:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

/* Records Lists */
.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #9ca3af;
  font-style: italic;
}

.records-list, .vaccination-list, .payment-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.record-item, .vaccination-item, .payment-item {
  background: #f9fafb;
  padding: 16px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s;
}

.record-item:hover, .vaccination-item:hover, .payment-item:hover {
  background: #f3f4f6;
  transform: translateX(4px);
}

.record-date, .vacc-date, .payment-date {
  font-weight: 600;
  color: #7C3AED;
  min-width: 100px;
}

.record-details {
  flex: 1;
}

.record-type {
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.record-complaint {
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.record-diagnosis {
  font-size: 14px;
  color: #6b7280;
}

.record-fee, .payment-amount {
  font-weight: 700;
  color: #10B981;
  font-size: 18px;
}

.payment-method {
  background: #e0f2fe;
  color: #0369a1;
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.payment-status {
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

.payment-status.completed {
  background: #d1fae5;
  color: #047857;
}

.payment-status.pending {
  background: #fef3c7;
  color: #92400e;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 0;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 2px solid #f3f4f6;
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
  color: #1a1a1a;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  color: #9ca3af;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.3s;
}

.btn-close:hover {
  background: #f3f4f6;
  color: #1a1a1a;
}

.modal-body {
  padding: 24px;
}

.modal-body p {
  margin: 0 0 12px 0;
  color: #374151;
  line-height: 1.6;
}

.modal-info {
  color: #6b7280;
  font-size: 14px;
}

.modal-footer {
  padding: 24px;
  border-top: 2px solid #f3f4f6;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-cancel {
  background: #f3f4f6;
  color: #374151;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-cancel:hover {
  background: #e5e7eb;
}

.btn-confirm {
  background: linear-gradient(135deg, #06B6D4, #0891B2);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
}

.btn-confirm:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(6, 182, 212, 0.4);
}

.btn-confirm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .passbook-create, .passbook-exists {
    flex-direction: column;
    text-align: center;
  }
  
  .record-item, .payment-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>