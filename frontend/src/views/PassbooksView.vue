<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-purple-800 p-6">
    <div class="bg-white rounded-xl shadow-lg p-6">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-gray-900">📒 Pet Passbooks</h1>
        <button 
          @click="showAddModal = true"
          class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-semibold"
        >
          ➕ Create Passbook
        </button>
      </div>

      <!-- Passbooks List -->
      <div v-if="passbooks.length > 0" class="grid gap-4">
        <div 
          v-for="passbook in passbooks" 
          :key="passbook.id"
          class="border-2 border-purple-200 rounded-lg p-6 hover:shadow-lg transition-shadow"
        >
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <h3 class="text-xl font-bold text-purple-900">
                {{ getPatientName(passbook.patient) }}
              </h3>
              <p class="text-gray-600 mt-2">
                <span class="font-semibold">Owner:</span> {{ getOwnerName(passbook.patient) }}
              </p>
              <p class="text-gray-600">
                <span class="font-semibold">Created:</span> {{ formatDate(passbook.created_at) }}
              </p>
              <p class="text-gray-600">
                <span class="font-semibold">Last Updated:</span> {{ formatDate(passbook.updated_at) }}
              </p>
            </div>
            
            <div class="flex gap-2">
              <button 
                @click="viewPassbook(passbook)"
                class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
                title="View QR Code"
              >
                📱 View
              </button>
              <button 
                @click="deletePassbook(passbook.id)"
                class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
                title="Delete"
              >
                🗑️
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-12 text-gray-500">
        <p class="text-xl">📒 No passbooks found</p>
        <p class="mt-2">Create a passbook for your pet to track their health records</p>
      </div>
    </div>

    <!-- Add Passbook Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl max-w-md w-full p-6">
        <h2 class="text-2xl font-bold text-purple-900 mb-4">Create Pet Passbook</h2>
        
        <div class="mb-4">
          <label class="block font-semibold mb-2">Select Pet *</label>
          <select 
            v-model="selectedPatient" 
            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg"
          >
            <option value="">Choose a pet...</option>
            <option 
              v-for="patient in availablePatients" 
              :key="patient.id" 
              :value="patient.id"
            >
              {{ patient.pet_name }} ({{ patient.species }})
            </option>
          </select>
        </div>

        <div class="flex gap-3">
          <button 
            @click="createPassbook"
            :disabled="!selectedPatient"
            class="flex-1 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white py-3 rounded-lg font-semibold"
          >
            ✅ Create
          </button>
          <button 
            @click="closeAddModal"
            class="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-3 rounded-lg font-semibold"
          >
            ✖️ Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- View Passbook Modal (QR Code) -->
    <div v-if="viewingPassbook" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl max-w-lg w-full p-6">
        <h2 class="text-2xl font-bold text-purple-900 mb-4">
          📱 {{ getPatientName(viewingPassbook.patient) }}'s Passbook
        </h2>
        
        <div class="text-center mb-4">
          <div class="bg-gray-100 p-6 rounded-lg inline-block">
            <div class="text-6xl mb-4">🐾</div>
            <p class="text-sm text-gray-600">QR Code will be generated here</p>
            <p class="text-xs text-gray-500 mt-2">Passbook ID: {{ viewingPassbook.id }}</p>
          </div>
        </div>

        <div class="bg-purple-50 p-4 rounded-lg mb-4">
          <p class="text-sm text-gray-700">
            <span class="font-semibold">Patient:</span> {{ getPatientName(viewingPassbook.patient) }}
          </p>
          <p class="text-sm text-gray-700">
            <span class="font-semibold">Owner:</span> {{ getOwnerName(viewingPassbook.patient) }}
          </p>
          <p class="text-sm text-gray-700">
            <span class="font-semibold">Created:</span> {{ formatDate(viewingPassbook.created_at) }}
          </p>
        </div>

        <button 
          @click="viewingPassbook = null"
          class="w-full bg-gray-500 hover:bg-gray-600 text-white py-3 rounded-lg font-semibold"
        >
          ✖️ Close
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../services/api';

const passbooks = ref([]);
const patients = ref([]);
const showAddModal = ref(false);
const selectedPatient = ref('');
const viewingPassbook = ref(null);

// Get patients that don't have passbooks yet
const availablePatients = computed(() => {
  const passbookPatientIds = passbooks.value.map(pb => pb.patient);
  return patients.value.filter(p => !passbookPatientIds.includes(p.id));
});

const fetchData = async () => {
  try {
    const [passbooksData, patientsData] = await Promise.all([
      api.get('/passbooks/'),
      api.get('/patients/')
    ]);
    
    passbooks.value = passbooksData.data.results || passbooksData.data || [];
    patients.value = patientsData.data.results || patientsData.data || [];
    
    console.log('Loaded passbooks:', passbooks.value.length);
    console.log('Loaded patients:', patients.value.length);
  } catch (error) {
    console.error('Error fetching data:', error);
    alert('Failed to load data. Please refresh the page.');
  }
};

const getPatientName = (patientId) => {
  const patient = patients.value.find(p => p.id === patientId);
  return patient ? patient.pet_name : 'Unknown Pet';
};

const getOwnerName = (patientId) => {
  const patient = patients.value.find(p => p.id === patientId);
  if (!patient) return 'Unknown Owner';
  
  // If patient has owner_name field
  if (patient.owner_name) return patient.owner_name;
  
  // Otherwise return owner ID
  return `Owner #${patient.owner}`;
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const createPassbook = async () => {
  if (!selectedPatient.value) {
    alert('Please select a pet');
    return;
  }

  try {
    await api.post('/passbooks/', {
      patient: selectedPatient.value
    });
    
    alert('Passbook created successfully! ✅');
    closeAddModal();
    fetchData();
  } catch (error) {
    console.error('Error creating passbook:', error);
    console.error('Error response:', error.response?.data);
    
    if (error.response?.data) {
      const errors = error.response.data;
      let errorMsg = 'Failed to create passbook:\n';
      Object.keys(errors).forEach(key => {
        errorMsg += `${key}: ${errors[key]}\n`;
      });
      alert(errorMsg);
    } else {
      alert('Failed to create passbook. Please try again.');
    }
  }
};

const viewPassbook = (passbook) => {
  viewingPassbook.value = passbook;
};

const deletePassbook = async (id) => {
  if (!confirm('Are you sure you want to delete this passbook?')) return;
  
  try {
    await api.delete(`/passbooks/${id}/`);
    alert('Passbook deleted successfully! ✅');
    fetchData();
  } catch (error) {
    console.error('Error deleting passbook:', error);
    alert('Failed to delete passbook. Please try again.');
  }
};

const closeAddModal = () => {
  showAddModal.value = false;
  selectedPatient.value = '';
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
/* Add any custom styles here */
</style>