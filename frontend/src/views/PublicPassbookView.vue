<template>
  <div class="min-h-screen bg-gradient-to-br from-emerald-50 to-emerald-100">
    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center min-h-screen">
      <div class="text-center">
        <div class="animate-spin rounded-full h-16 w-16 border-b-4 border-emerald-600 mx-auto mb-4"></div>
        <p class="text-gray-600 font-semibold">Loading passbook...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="flex items-center justify-center min-h-screen p-4">
      <div class="bg-white rounded-xl shadow-lg p-8 max-w-md w-full text-center">
        <div class="text-6xl mb-4">❌</div>
        <h2 class="text-2xl font-bold text-red-700 mb-2">Invalid Link</h2>
        <p class="text-gray-600">{{ error }}</p>
      </div>
    </div>

    <!-- Expired Subscription State -->
    <div v-else-if="!passbook.is_active" class="flex items-center justify-center min-h-screen p-4">
      <div class="bg-white rounded-xl shadow-lg p-8 max-w-md w-full text-center">
        <div class="text-6xl mb-4">⏰</div>
        <h2 class="text-2xl font-bold text-orange-700 mb-2">Subscription Expired</h2>
        <p class="text-gray-700 mb-4">
          This digital passbook subscription has expired.
        </p>
        <p class="text-gray-600 text-sm">
          Please contact <span class="font-bold text-emerald-700">Sri Adithya Pet Clinic</span> to renew your subscription and regain access to your pet's medical records.
        </p>
        <div class="mt-6 p-4 bg-emerald-50 rounded-lg">
          <p class="text-sm text-emerald-800">
            📞 Contact clinic to renew<br>
            🏥 No 16,Sriram Nagar, Theni, TN - 625531
          </p>
        </div>
      </div>
    </div>

    <!-- Active Passbook Content -->
    <div v-else class="max-w-4xl mx-auto p-4 pb-20">
      <!-- Clinic Header -->
      <div class="bg-white rounded-xl shadow-lg p-6 mb-4 text-center border-t-4 border-emerald-600">
        <h1 class="text-2xl font-bold text-emerald-900">🏥 Sri Adithya Pet Clinic</h1>
        <p class="text-gray-600 text-sm">Dr. A. Balasubramanian, B.V.Sc, MBA(H A)</p>
        <p class="text-gray-500 text-xs">No 16,Sriram Nagar, Theni, Tamil Nadu - 625531</p>
      </div>

      <!-- Subscription Status Badge -->
      <div class="bg-green-500 text-white rounded-xl shadow-lg p-4 mb-4 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-2xl">✓</span>
          <div>
            <p class="font-bold">Active Subscription</p>
            <p class="text-xs text-green-100">Valid until {{ formatDate(passbook.subscription_end) }}</p>
          </div>
        </div>
        <div class="text-right">
          <p class="text-2xl font-bold">{{ passbook.days_remaining }}</p>
          <p class="text-xs text-green-100">days left</p>
        </div>
      </div>

      <!-- Pet Profile Card -->
      <div class="bg-white rounded-xl shadow-lg overflow-hidden mb-4">
        <div class="bg-gradient-to-r from-emerald-600 to-emerald-700 p-4 text-white">
          <h2 class="text-xl font-bold">🐾 Pet Profile</h2>
        </div>
        <div class="p-6">
          <div class="flex flex-col md:flex-row gap-6">
            <!-- Pet Photo -->
            <div class="flex-shrink-0">
              <img 
                v-if="passbook.photo" 
                :src="passbook.photo" 
                :alt="passbook.pet_name"
                class="w-32 h-32 rounded-full object-cover border-4 border-emerald-500 mx-auto md:mx-0"
              />
              <div v-else class="w-32 h-32 bg-emerald-100 rounded-full flex items-center justify-center text-5xl mx-auto md:mx-0">
                🐕
              </div>
            </div>

            <!-- Pet Details -->
            <div class="flex-grow grid grid-cols-2 gap-4">
              <div>
                <p class="text-xs text-gray-500 uppercase">Pet Name</p>
                <p class="font-bold text-lg text-gray-900">{{ passbook.pet_name }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500 uppercase">Species</p>
                <p class="font-semibold text-gray-900">{{ passbook.species }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500 uppercase">Breed</p>
                <p class="font-semibold text-gray-900">{{ passbook.breed }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500 uppercase">Gender</p>
                <p class="font-semibold text-gray-900">{{ passbook.gender }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500 uppercase">Date of Birth</p>
                <p class="font-semibold text-gray-900">{{ formatDate(passbook.date_of_birth) }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500 uppercase">Color</p>
                <p class="font-semibold text-gray-900">{{ passbook.color || 'N/A' }}</p>
              </div>
            </div>
          </div>

          <!-- Owner Info -->
          <div class="mt-6 pt-6 border-t border-gray-200">
            <p class="text-xs text-gray-500 uppercase mb-2">Pet Parent</p>
            <div class="flex justify-between items-center">
              <p class="font-bold text-gray-900">{{ passbook.owner_name }}</p>
              <p class="text-sm text-gray-600">📞 {{ passbook.owner_phone }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Vaccinations -->
      <div class="bg-white rounded-xl shadow-lg overflow-hidden mb-4">
        <div class="bg-gradient-to-r from-green-600 to-green-700 p-4 text-white">
          <h2 class="text-xl font-bold">💉 Vaccination History</h2>
        </div>
        <div class="p-4">
          <div v-if="passbook.vaccinations && passbook.vaccinations.length > 0" class="space-y-3">
            <div 
              v-for="(vax, index) in passbook.vaccinations" 
              :key="index"
              class="bg-green-50 border-l-4 border-green-500 p-4 rounded-r-lg"
            >
              <div class="flex justify-between items-start mb-2">
                <p class="font-bold text-gray-900">{{ vax.vaccine_name }}</p>
                <span class="text-xs bg-green-200 text-green-800 px-2 py-1 rounded">{{ formatDate(vax.date_administered) }}</span>
              </div>
              <div class="grid grid-cols-2 gap-2 text-sm text-gray-700">
                <p><span class="text-gray-500">Next Due:</span> {{ formatDate(vax.next_due_date) }}</p>
                <p><span class="text-gray-500">Cert#:</span> {{ vax.certificate_number }}</p>
              </div>
              <p class="text-xs text-gray-600 mt-2">Administered by: {{ vax.administered_by }}</p>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-500">
            <p class="text-4xl mb-2">💉</p>
            <p>No vaccination records yet</p>
          </div>
        </div>
      </div>

      <!-- Consultation History -->
      <div class="bg-white rounded-xl shadow-lg overflow-hidden mb-4">
        <div class="bg-gradient-to-r from-blue-600 to-blue-700 p-4 text-white">
          <h2 class="text-xl font-bold">🩺 Consultation History</h2>
        </div>
        <div class="p-4">
          <div v-if="passbook.consultations && passbook.consultations.length > 0" class="space-y-3">
            <div 
              v-for="(consult, index) in passbook.consultations" 
              :key="index"
              class="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-r-lg"
            >
              <div class="flex justify-between items-start mb-2">
                <p class="font-bold text-gray-900">{{ consult.visit_type }}</p>
                <span class="text-xs bg-blue-200 text-blue-800 px-2 py-1 rounded">{{ formatDate(consult.visit_date) }}</span>
              </div>
              <p class="text-sm text-gray-700 mb-2" v-if="consult.chief_complaint">
                <span class="font-semibold">Complaint:</span> {{ consult.chief_complaint }}
              </p>
              <p class="text-sm text-gray-700 mb-2" v-if="consult.diagnosis">
                <span class="font-semibold">Diagnosis:</span> {{ consult.diagnosis }}
              </p>
              <p class="text-sm text-gray-600" v-if="consult.treatment_plan">
                <span class="font-semibold">Treatment:</span> {{ consult.treatment_plan }}
              </p>
              <div class="grid grid-cols-3 gap-2 mt-3 text-xs text-gray-600">
                <p v-if="consult.temperature">Temp: {{ consult.temperature }}°F</p>
                <p v-if="consult.weight">Weight: {{ consult.weight }}kg</p>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-500">
            <p class="text-4xl mb-2">🩺</p>
            <p>No consultation records yet</p>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="bg-white rounded-xl shadow-lg p-6 text-center">
        <p class="text-sm text-gray-600 mb-2">
          This is a digital passbook provided by
        </p>
        <p class="font-bold text-emerald-700">Sri Adithya Pet Clinic</p>
        <p class="text-xs text-gray-500 mt-2">
          For support, please contact the clinic
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../services/api';

const route = useRoute();
const loading = ref(true);
const error = ref(null);
const passbook = ref({});

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-IN', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
};

const fetchPassbook = async () => {
  const token = route.params.token;
  
  console.log('=== PASSBOOK DEBUG START ===')
  console.log('Current route path:', route.path)
  console.log('Token from params:', token)
  console.log('Full route params:', route.params)
  
  if (!token) {
    console.error('No token provided!')
    error.value = 'No passbook token provided';
    loading.value = false;
    return;
  }
  
  try {
    console.log('Fetching passbook with token:', token);
    const apiUrl = `/passbooks/public/${token}/`
    console.log('API URL:', apiUrl)
    
    const response = await api.get(apiUrl);
    
    console.log('Response status:', response.status)
    console.log('Response data:', response.data);
    
    if (response.data.success) {
      passbook.value = response.data.data;
      console.log('Passbook loaded successfully:', passbook.value);
    } else {
      console.error('API returned success=false:', response.data.error)
      error.value = response.data.error || 'Invalid passbook link';
    }
  } catch (err) {
    console.error('Error fetching passbook:', err);
    console.error('Error response:', err.response?.data);
    console.error('Error status:', err.response?.status);
    error.value = 'This passbook link is invalid or has expired';
  } finally {
    loading.value = false;
    console.log('=== PASSBOOK DEBUG END ===')
  }
};

onMounted(() => {
  fetchPassbook();
});
</script>

<style scoped>
/* Mobile-optimized styles */
@media (max-width: 640px) {
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
}

/* Print styles */
@media print {
  .bg-gradient-to-br {
    background: white !important;
  }
  button {
    display: none;
  }
}

/* Tailwind CSS classes used (make sure Tailwind is configured) */
.min-h-screen { min-height: 100vh; }
.bg-gradient-to-br { background-image: linear-gradient(to bottom right, var(--tw-gradient-stops)); }
.from-emerald-50 { --tw-gradient-from: #ecfdf5; --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgba(236, 253, 245, 0)); }
.to-emerald-100 { --tw-gradient-to: #d1fae5; }
.flex { display: flex; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.text-center { text-align: center; }
.animate-spin { animation: spin 1s linear infinite; }
.rounded-full { border-radius: 9999px; }
.h-16 { height: 4rem; }
.w-16 { width: 4rem; }
.border-b-4 { border-bottom-width: 4px; }
.border-emerald-600 { border-color: #059669; }
.mx-auto { margin-left: auto; margin-right: auto; }
.mb-4 { margin-bottom: 1rem; }
.text-gray-600 { color: #4b5563; }
.font-semibold { font-weight: 600; }
.p-4 { padding: 1rem; }
.bg-white { background-color: #ffffff; }
.rounded-xl { border-radius: 0.75rem; }
.shadow-lg { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
.p-8 { padding: 2rem; }
.max-w-md { max-width: 28rem; }
.w-full { width: 100%; }
.text-6xl { font-size: 3.75rem; line-height: 1; }
.text-2xl { font-size: 1.5rem; line-height: 2rem; }
.font-bold { font-weight: 700; }
.text-red-700 { color: #b91c1c; }
.mb-2 { margin-bottom: 0.5rem; }
.max-w-4xl { max-width: 56rem; }
.pb-20 { padding-bottom: 5rem; }

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>