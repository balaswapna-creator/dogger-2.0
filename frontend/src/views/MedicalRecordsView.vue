<template>
  <div class="min-h-screen bg-gradient-to-br from-emerald-900 via-emerald-700 to-emerald-800 p-6">
    <!-- White Container -->
    <div class="bg-white rounded-xl shadow-lg p-6">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-emerald-700">📋 Medical Records</h1>
        <button 
          @click="openAddModal"
          class="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-lg font-semibold"
        >
          ➕ New Consultation
        </button>
      </div>

      <!-- Search -->
      <input 
        v-model="searchQuery"
        type="text" 
        placeholder="🔍 Search by patient name, complaint, diagnosis..."
        class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg mb-6 focus:border-emerald-500 focus:outline-none"
      />

      <!-- Records Table -->
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-emerald-100">
            <tr>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Date</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Patient</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Type</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Chief Complaint</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Diagnosis</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Fee (₹)</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="record in filteredRecords" :key="record.id" class="hover:bg-gray-50">
              <td class="px-4 py-3 text-gray-700">{{ formatDate(record.visit_date) }}</td>
              <td class="px-4 py-3 font-semibold text-gray-900">{{ getPatientName(record.patient) }}</td>
              <td class="px-4 py-3">
                <span :class="getVisitTypeBadge(record.visit_type)" class="px-2 py-1 rounded text-xs font-semibold">
                  {{ record.visit_type }}
                </span>
              </td>
              <td class="px-4 py-3 text-gray-700">{{ record.chief_complaint || 'N/A' }}</td>
              <td class="px-4 py-3 text-gray-700">{{ record.diagnosis || 'N/A' }}</td>
              <td class="px-4 py-3 font-bold text-gray-900">₹{{ record.consultation_fee || 0 }}</td>
              <td class="px-4 py-3">
                <div class="flex gap-2">
                  <button 
                    @click="openEditModal(record)"
                    class="bg-amber-500 hover:bg-amber-600 text-white px-2 py-1 rounded text-sm"
                    title="Edit"
                  >
                    ✏️
                  </button>
                  <button 
                    @click="viewPrescription(record)"
                    class="bg-violet-500 hover:bg-violet-600 text-white px-2 py-1 rounded text-sm"
                    title="Prescription"
                  >
                    💊
                  </button>
                  <button 
                    @click="deleteRecord(record.id)"
                    class="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-sm"
                    title="Delete"
                  >
                    🗑️
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredRecords.length === 0">
              <td colspan="7" class="px-4 py-8 text-center text-gray-500">No records found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="bg-emerald-600 text-white p-6">
          <h2 class="text-2xl font-bold">{{ isEditing ? 'Edit Consultation' : 'New Consultation' }}</h2>
        </div>
        
        <div class="p-6 space-y-4">
          <!-- Patient Selection -->
          <div>
            <label class="block font-semibold text-gray-700 mb-2">Patient * (Required)</label>
            <select v-model="form.patient" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-emerald-500 focus:outline-none">
              <option value="">-- Select Patient --</option>
              <option v-for="patient in patients" :key="patient.id" :value="patient.id">
                {{ patient.pet_name }} ({{ patient.species }}) - Owner: {{ getOwnerName(patient.owner) }}
              </option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block font-semibold text-gray-700 mb-2">Visit Date * (Required)</label>
              <input v-model="form.visit_date" type="date" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-emerald-500 focus:outline-none" />
            </div>
            
            <div>
              <label class="block font-semibold text-gray-700 mb-2">Visit Type * (Required)</label>
              <select v-model="form.visit_type" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-emerald-500 focus:outline-none">
                <option value="consultation">Consultation</option>
                <option value="vaccination">Vaccination</option>
                <option value="surgery">Surgery</option>
                <option value="emergency">Emergency</option>
                <option value="follow_up">Follow Up</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block font-semibold text-gray-700 mb-2">Chief Complaint</label>
            <input v-model="form.chief_complaint" type="text" placeholder="e.g. Vomiting, Lethargy" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-emerald-500 focus:outline-none" />
          </div>

          <div>
            <label class="block font-semibold text-gray-700 mb-2">History</label>
            <textarea v-model="form.history" rows="3" placeholder="Patient history and symptoms" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-emerald-500 focus:outline-none"></textarea>
          </div>

          <div>
            <label class="block font-semibold text-gray-700 mb-2">Clinical Notes</label>
            <textarea v-model="form.clinical_notes" rows="3" placeholder="Examination findings and clinical observations" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-emerald-500 focus:outline-none"></textarea>
          </div>

          <div>
            <label class="block font-semibold text-gray-700 mb-2">Diagnosis</label>
            <textarea v-model="form.diagnosis" rows="2" placeholder="Diagnosis and condition" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-emerald-500 focus:outline-none"></textarea>
          </div>

          <div>
            <label class="block font-semibold text-gray-700 mb-2">Treatment Plan</label>
            <textarea v-model="form.treatment_plan" rows="3" placeholder="Recommended treatment and medications" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-emerald-500 focus:outline-none"></textarea>
          </div>

          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="block font-semibold text-gray-700 mb-2">Temperature (°F)</label>
              <input v-model="form.temperature" type="number" step="0.1" placeholder="e.g. 101.5" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-emerald-500 focus:outline-none" />
            </div>
            
            <div>
              <label class="block font-semibold text-gray-700 mb-2">Weight (kg)</label>
              <input v-model="form.weight" type="number" step="0.1" placeholder="e.g. 25.5" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-emerald-500 focus:outline-none" />
            </div>
            
            <div>
              <label class="block font-semibold text-gray-700 mb-2">Heart Rate (bpm)</label>
              <input v-model="form.heart_rate" type="number" placeholder="e.g. 80" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-emerald-500 focus:outline-none" />
            </div>
          </div>

          <div>
            <label class="block font-semibold text-gray-700 mb-2">Consultation Fee (₹)</label>
            <input v-model="form.consultation_fee" type="number" placeholder="e.g. 500" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-emerald-500 focus:outline-none" />
          </div>

          <div class="flex gap-3 pt-4">
            <button 
              @click="saveRecord"
              class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white py-3 rounded-lg font-semibold text-lg"
            >
              💾 {{ isEditing ? 'Update' : 'Save' }} Consultation
            </button>
            <button 
              @click="closeModal"
              class="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-3 rounded-lg font-semibold text-lg"
            >
              ✖️ Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Print Prescription Modal -->
    <div v-if="showPrintModal && printData" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="bg-violet-600 text-white p-6 flex justify-between items-center">
          <h2 class="text-2xl font-bold">Prescription</h2>
          <button @click="closePrintModal" class="text-white hover:bg-white/20 p-2 rounded">✖️</button>
        </div>
        
        <div id="printable-prescription" class="p-8">
          <!-- Clinic Header -->
          <div class="text-center mb-6 border-b-4 border-emerald-600 pb-4">
            <h1 class="text-3xl font-bold text-emerald-900">Sri Adithya Pet Clinic</h1>
            <p class="text-gray-700">Dr. A. Balasubramanian, B.V.Sc, MBA</p>
            <p class="text-gray-600">Main Road, Cumbum, Tamil Nadu - 625516</p>
          </div>

          <!-- Patient & Owner Info -->
          <div class="grid grid-cols-2 gap-4 mb-6 bg-emerald-50 p-4 rounded-lg">
            <div>
              <p class="text-sm text-gray-600">Patient Name</p>
              <p class="font-bold text-gray-900">{{ printData.patient?.pet_name }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Owner Name</p>
              <p class="font-bold text-gray-900">{{ printData.owner?.name }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Species/Breed</p>
              <p class="font-bold text-gray-900">{{ printData.patient?.species }} / {{ printData.patient?.breed }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Date</p>
              <p class="font-bold text-gray-900">{{ formatDate(printData.record?.visit_date) }}</p>
            </div>
          </div>

          <!-- Diagnosis -->
          <div class="mb-6">
            <h3 class="font-bold text-lg text-emerald-900 mb-2">Diagnosis:</h3>
            <p class="text-gray-800 bg-gray-50 p-3 rounded">{{ printData.record?.diagnosis || 'N/A' }}</p>
          </div>

          <!-- Prescriptions -->
          <div class="mb-6">
            <h3 class="font-bold text-lg text-emerald-900 mb-3">Prescribed Medications:</h3>
            <table class="w-full border-2 border-gray-300">
              <thead>
                <tr class="bg-emerald-600 text-white">
                  <th class="border border-gray-300 px-3 py-2 text-left">Medication</th>
                  <th class="border border-gray-300 px-3 py-2 text-left">Dosage</th>
                  <th class="border border-gray-300 px-3 py-2 text-left">Frequency</th>
                  <th class="border border-gray-300 px-3 py-2 text-left">Duration</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="med in printData.prescriptions" :key="med.id">
                  <td class="border border-gray-300 px-3 py-2">{{ med.medication_name }}</td>
                  <td class="border border-gray-300 px-3 py-2">{{ med.dosage }}</td>
                  <td class="border border-gray-300 px-3 py-2">{{ med.frequency }}</td>
                  <td class="border border-gray-300 px-3 py-2">{{ med.duration }}</td>
                </tr>
                <tr v-if="!printData.prescriptions || printData.prescriptions.length === 0">
                  <td colspan="4" class="border border-gray-300 px-3 py-2 text-center text-gray-500">No prescriptions</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Doctor Signature -->
          <div class="mt-8 text-right">
            <p class="font-bold text-gray-900">Dr. A. Balasubramanian</p>
            <p class="text-gray-600">B.V.Sc, MBA</p>
          </div>
        </div>

        <div class="p-6 bg-gray-50 flex gap-3">
          <button 
            @click="triggerPrint"
            class="flex-1 bg-violet-600 hover:bg-violet-700 text-white py-3 rounded-lg font-semibold"
          >
            🖨️ Print Prescription
          </button>
          <button 
            @click="closePrintModal"
            class="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-3 rounded-lg font-semibold"
          >
            ✖️ Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../services/api';

const records = ref([]);
const patients = ref([]);
const owners = ref([]);
const searchQuery = ref('');
const showModal = ref(false);
const isEditing = ref(false);
const editingRecordId = ref(null);
const showPrintModal = ref(false);
const printData = ref(null);

const form = ref({
  patient: '',
  visit_date: new Date().toISOString().split('T')[0],
  visit_type: 'consultation',
  chief_complaint: '',
  history: '',
  clinical_notes: '',
  diagnosis: '',
  treatment_plan: '',
  temperature: null,
  weight: null,
  heart_rate: null,
  consultation_fee: 0
});

const filteredRecords = computed(() => {
  if (!searchQuery.value) return records.value;
  const query = searchQuery.value.toLowerCase();
  return records.value.filter(r => 
    getPatientName(r.patient).toLowerCase().includes(query) ||
    r.chief_complaint?.toLowerCase().includes(query) ||
    r.diagnosis?.toLowerCase().includes(query)
  );
});

const getPatientName = (patientId) => {
  const patient = patients.value.find(p => p.id === patientId);
  return patient ? patient.pet_name : 'Unknown';
};

const getOwnerName = (ownerId) => {
  const owner = owners.value.find(o => o.id === ownerId);
  return owner ? owner.name : 'Unknown';
};

const getVisitTypeBadge = (type) => {
  const badges = {
    consultation: 'bg-blue-100 text-blue-800',
    vaccination: 'bg-green-100 text-green-800',
    surgery: 'bg-red-100 text-red-800',
    emergency: 'bg-orange-100 text-orange-800',
    follow_up: 'bg-purple-100 text-purple-800'
  };
  return badges[type] || 'bg-gray-100 text-gray-800';
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-IN');
};

const fetchData = async () => {
  try {
    const [recordsRes, patientsRes, ownersRes] = await Promise.all([
      api.get('/medical-records/'),
      api.get('/patients/'),
      api.get('/owners/')
    ]);
    
    records.value = recordsRes.data.results || recordsRes.data;
    patients.value = patientsRes.data.results || patientsRes.data;
    owners.value = ownersRes.data.results || ownersRes.data;
    
    console.log('✅ Loaded records:', records.value.length);
    console.log('✅ Loaded patients:', patients.value.length);
  } catch (error) {
    console.error('❌ Error fetching data:', error);
  }
};

const openAddModal = () => {
  isEditing.value = false;
  editingRecordId.value = null;
  resetForm();
  showModal.value = true;
};

const openEditModal = (record) => {
  isEditing.value = true;
  editingRecordId.value = record.id;
  form.value = {
    patient: record.patient,
    visit_date: record.visit_date,
    visit_type: record.visit_type,
    chief_complaint: record.chief_complaint || '',
    history: record.history || '',
    clinical_notes: record.clinical_notes || '',
    diagnosis: record.diagnosis || '',
    treatment_plan: record.treatment_plan || '',
    temperature: record.temperature,
    weight: record.weight,
    heart_rate: record.heart_rate,
    consultation_fee: record.consultation_fee || 0
  };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  isEditing.value = false;
  editingRecordId.value = null;
  resetForm();
};

const resetForm = () => {
  form.value = {
    patient: '',
    visit_date: new Date().toISOString().split('T')[0],
    visit_type: 'consultation',
    chief_complaint: '',
    history: '',
    clinical_notes: '',
    diagnosis: '',
    treatment_plan: '',
    temperature: null,
    weight: null,
    heart_rate: null,
    consultation_fee: 0
  };
};

const saveRecord = async () => {
  // Validation
  if (!form.value.patient) {
    alert('❌ Please select a patient');
    return;
  }
  if (!form.value.visit_date) {
    alert('❌ Please select visit date');
    return;
  }
  
  try {
    console.log('📤 Submitting record:', form.value);
    
    let response;
    if (isEditing.value) {
      response = await api.put(`/medical-records/${editingRecordId.value}/`, form.value);
      alert('✅ Record updated successfully!');
    } else {
      response = await api.post('/medical-records/', form.value);
      alert('✅ Record created successfully!');
    }
    
    console.log('✅ Response:', response.data);
    closeModal();
    await fetchData();
    
  } catch (error) {
    console.error('❌ Save error:', error);
    console.error('❌ Error response:', error.response?.data);
    
    if (error.response?.data) {
      const errors = error.response.data;
      let errorMsg = '❌ Failed to save record:\n\n';
      Object.keys(errors).forEach(key => {
        errorMsg += `${key}: ${Array.isArray(errors[key]) ? errors[key].join(', ') : errors[key]}\n`;
      });
      alert(errorMsg);
    } else {
      alert('❌ Failed to save record. Please try again.');
    }
  }
};

const deleteRecord = async (id) => {
  if (!confirm('⚠️ Are you sure you want to delete this record?')) return;
  
  try {
    await api.delete(`/medical-records/${id}/`);
    alert('✅ Record deleted successfully!');
    await fetchData();
  } catch (error) {
    console.error('❌ Delete error:', error);
    alert('❌ Failed to delete record');
  }
};

const viewPrescription = async (record) => {
  try {
    console.log('📤 Fetching prescription for record:', record.id);
    
    const [prescriptionsRes, patientRes] = await Promise.all([
      api.get(`/prescriptions/?medical_record=${record.id}`),
      api.get(`/patients/${record.patient}/`)
    ]);
    
    const patient = patientRes.data;
    const ownerRes = await api.get(`/owners/${patient.owner}/`);
    
    printData.value = {
      record,
      patient,
      owner: ownerRes.data,
      prescriptions: prescriptionsRes.data.results || prescriptionsRes.data || []
    };
    
    console.log('✅ Print data loaded:', printData.value);
    showPrintModal.value = true;
    
  } catch (error) {
    console.error('❌ Error loading prescription:', error);
    alert('❌ Failed to load prescription data');
  }
};

const triggerPrint = () => {
  window.print();
};

const closePrintModal = () => {
  showPrintModal.value = false;
  printData.value = null;
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
@media print {
  body * {
    visibility: hidden;
  }
  #printable-prescription, #printable-prescription * {
    visibility: visible;
  }
  #printable-prescription {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
  }
}
</style>