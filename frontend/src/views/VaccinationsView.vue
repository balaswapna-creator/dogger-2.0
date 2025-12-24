<template>
  <div class="min-h-screen bg-gradient-to-br from-emerald-900 via-emerald-700 to-emerald-800 p-6">
    <div class="bg-white rounded-xl shadow-lg p-6">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-emerald-700">💉 Vaccinations</h1>
        <button @click="openAddModal" class="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-lg font-semibold">
          ➕ Add Vaccination
        </button>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-emerald-100">
            <tr>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Patient</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Vaccine</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Date</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Next Due</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Certificate#</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="vax in vaccinations" :key="vax.id" class="hover:bg-gray-50">
              <td class="px-4 py-3 font-semibold">{{ getPatientName(vax.patient) }}</td>
              <td class="px-4 py-3">{{ vax.vaccine_name }}</td>
              <td class="px-4 py-3">{{ formatDate(vax.date_administered) }}</td>
              <td class="px-4 py-3">{{ formatDate(vax.next_due_date) }}</td>
              <td class="px-4 py-3 font-mono text-sm">{{ vax.certificate_number }}</td>
              <td class="px-4 py-3">
                <div class="flex gap-2">
                  <button @click="openEditModal(vax)" class="bg-amber-500 hover:bg-amber-600 text-white px-2 py-1 rounded text-sm">✏️</button>
                  <button @click="printCertificate(vax)" class="bg-teal-500 hover:bg-teal-600 text-white px-2 py-1 rounded text-sm">🖨️</button>
                  <button @click="deleteVaccination(vax.id)" class="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-sm">🗑️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="bg-emerald-600 text-white p-6">
          <h2 class="text-2xl font-bold">{{ isEditing ? 'Edit Vaccination' : 'New Vaccination' }}</h2>
        </div>
        
        <div class="p-6 space-y-4">
          <div>
            <label class="block font-semibold text-gray-700 mb-2">Patient * (Required)</label>
            <select v-model="form.patient" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg">
              <option value="">-- Select Patient --</option>
              <option v-for="patient in patients" :key="patient.id" :value="patient.id">
                {{ patient.pet_name }} ({{ patient.species }})
              </option>
            </select>
          </div>

          <div>
            <label class="block font-semibold text-gray-700 mb-2">Vaccine Name * (Required)</label>
            <input v-model="form.vaccine_name" type="text" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" placeholder="e.g. Rabies, DHPP" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block font-semibold text-gray-700 mb-2">Manufacturer</label>
              <input v-model="form.manufacturer" type="text" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" placeholder="Optional" />
            </div>
            <div>
              <label class="block font-semibold text-gray-700 mb-2">Batch Number</label>
              <input v-model="form.batch_number" type="text" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" placeholder="Optional" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block font-semibold text-gray-700 mb-2">Date Administered * (Required)</label>
              <input v-model="form.date_administered" type="date" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" />
            </div>
            <div>
              <label class="block font-semibold text-gray-700 mb-2">Next Due Date</label>
              <input v-model="form.next_due_date" type="date" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" />
            </div>
          </div>

          <div>
            <label class="block font-semibold text-gray-700 mb-2">Administered By</label>
            <input v-model="form.administered_by" type="text" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" placeholder="Dr. A. Balasubramanan" />
          </div>

          <div>
            <label class="block font-semibold text-gray-700 mb-2">Notes</label>
            <textarea v-model="form.notes" rows="3" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" placeholder="Optional notes"></textarea>
          </div>

          <div class="flex gap-3 pt-4">
            <button @click="saveVaccination" class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white py-3 rounded-lg font-semibold">
              💾 {{ isEditing ? 'Update' : 'Save' }} Vaccination
            </button>
            <button @click="closeModal" class="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-3 rounded-lg font-semibold">
              ✖️ Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Print Modal -->
    <div v-if="showPrintModal && printData" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="bg-teal-600 text-white p-6 flex justify-between items-center">
          <h2 class="text-2xl font-bold">Vaccination Certificate</h2>
          <button @click="closePrintModal" class="text-white hover:bg-white/20 p-2 rounded">✖️</button>
        </div>
        
        <div id="printable-certificate" class="p-8">
          <div class="border-8 border-double border-emerald-600 p-8">
            <div class="text-center mb-6 border-b-4 border-emerald-600 pb-4">
              <h1 class="text-4xl font-bold text-emerald-900 mb-2">Sri Adithya Pet Clinic</h1>
              <p class="text-lg text-gray-700">Dr. A. Balasubramanan, B.V.Sc, MBA</p>
              <p class="text-gray-600">Main Road, Cumbum, Tamil Nadu - 625516</p>
            </div>

            <div class="text-center mb-6">
              <h2 class="text-3xl font-bold text-emerald-800 mb-2">VACCINATION CERTIFICATE</h2>
              <p class="text-gray-600">Certificate No: <span class="font-bold text-gray-900">{{ printData.vaccination?.certificate_number }}</span></p>
            </div>

            <div class="bg-emerald-50 p-6 rounded-lg mb-6">
              <h3 class="text-xl font-bold text-emerald-900 mb-4">Patient Information</h3>
              <div class="grid grid-cols-2 gap-4">
                <div><p class="text-sm text-gray-600">Pet Name</p><p class="font-bold text-lg">{{ printData.patient?.pet_name }}</p></div>
                <div><p class="text-sm text-gray-600">Owner Name</p><p class="font-bold text-lg">{{ printData.owner?.name }}</p></div>
                <div><p class="text-sm text-gray-600">Species</p><p class="font-bold">{{ printData.patient?.species }}</p></div>
                <div><p class="text-sm text-gray-600">Breed</p><p class="font-bold">{{ printData.patient?.breed }}</p></div>
              </div>
            </div>

            <div class="mb-6">
              <h3 class="text-xl font-bold text-emerald-900 mb-4">Vaccination Details</h3>
              <table class="w-full border-2 border-gray-300">
                <tbody>
                  <tr class="border-b"><td class="px-4 py-3 bg-emerald-100 font-bold">Vaccine Name</td><td class="px-4 py-3">{{ printData.vaccination?.vaccine_name }}</td></tr>
                  <tr class="border-b"><td class="px-4 py-3 bg-emerald-100 font-bold">Manufacturer</td><td class="px-4 py-3">{{ printData.vaccination?.manufacturer || 'N/A' }}</td></tr>
                  <tr class="border-b"><td class="px-4 py-3 bg-emerald-100 font-bold">Batch Number</td><td class="px-4 py-3">{{ printData.vaccination?.batch_number || 'N/A' }}</td></tr>
                  <tr class="border-b"><td class="px-4 py-3 bg-emerald-100 font-bold">Date Administered</td><td class="px-4 py-3">{{ formatDate(printData.vaccination?.date_administered) }}</td></tr>
                  <tr><td class="px-4 py-3 bg-emerald-100 font-bold">Next Due Date</td><td class="px-4 py-3">{{ formatDate(printData.vaccination?.next_due_date) }}</td></tr>
                </tbody>
              </table>
            </div>

            <div class="flex justify-between items-end mt-12">
              <div><p class="text-gray-600 text-sm">Date: {{ formatDate(printData.vaccination?.date_administered) }}</p></div>
              <div class="text-right">
                <div class="border-t-2 border-gray-400 pt-2 min-w-[200px]">
                  <p class="font-bold text-gray-900">Dr. A. Balasubramanan</p>
                  <p class="text-gray-600 text-sm">B.V.Sc, MBA</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="p-6 bg-gray-50 flex gap-3">
          <button @click="triggerPrint" class="flex-1 bg-teal-600 hover:bg-teal-700 text-white py-3 rounded-lg font-semibold">🖨️ Print</button>
          <button @click="closePrintModal" class="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-3 rounded-lg font-semibold">✖️ Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';

const vaccinations = ref([]);
const patients = ref([]);
const showModal = ref(false);
const isEditing = ref(false);
const editingVaxId = ref(null);
const showPrintModal = ref(false);
const printData = ref(null);

const form = ref({
  patient: '',
  vaccine_name: '',
  manufacturer: '',
  batch_number: '',
  date_administered: new Date().toISOString().split('T')[0],
  next_due_date: '',
  administered_by: 'Dr. A. Balasubramanian B.V.Sc,.MBA(HA)',
  notes: ''
});

const getPatientName = (id) => patients.value.find(p => p.id === id)?.pet_name || 'Unknown';
const formatDate = (d) => d ? new Date(d).toLocaleDateString('en-IN') : 'N/A';

const fetchData = async () => {
  try {
    const [v, p] = await Promise.all([api.get('/vaccinations/'), api.get('/patients/')]);
    vaccinations.value = v.data.results || v.data;
    patients.value = p.data.results || p.data;
  } catch (error) {
    console.error('Error:', error);
  }
};

const openAddModal = () => {
  isEditing.value = false;
  editingVaxId.value = null;
  form.value = {
    patient: '',
    vaccine_name: '',
    manufacturer: '',
    batch_number: '',
    date_administered: new Date().toISOString().split('T')[0],
    next_due_date: '',
    administered_by: 'Dr. A. Balasubramanian B.V.Sc,.MBA(HA)',
    notes: ''
  };
  showModal.value = true;
};

const openEditModal = (vax) => {
  isEditing.value = true;
  editingVaxId.value = vax.id;
  form.value = {
    patient: vax.patient,
    vaccine_name: vax.vaccine_name,
    manufacturer: vax.manufacturer || '',
    batch_number: vax.batch_number || '',
    date_administered: vax.date_administered,
    next_due_date: vax.next_due_date || '',
    administered_by: vax.administered_by || 'Dr. A. Balasubramanian B.V.Sc,.MBA(HA)',
    notes: vax.notes || ''
  };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  isEditing.value = false;
  editingVaxId.value = null;
};

const saveVaccination = async () => {
  try {
    console.log('📤 Sending vaccination data:', form.value);
    
    if (isEditing.value) {
      await api.put(`/vaccinations/${editingVaxId.value}/`, form.value);
    } else {
      await api.post('/vaccinations/', form.value);
    }
    await fetchData();
    closeModal();
    alert(isEditing.value ? 'Vaccination updated!' : 'Vaccination added!');
  } catch (error) {
    console.error('❌ Full error:', error);
    console.error('❌ Error response:', error.response?.data);
    
    const errorMsg = error.response?.data 
      ? JSON.stringify(error.response.data, null, 2)
      : error.message;
    
    alert('Error saving vaccination:\n\n' + errorMsg);
  }
};

const deleteVaccination = async (id) => {
  if (!confirm('Delete this vaccination?')) return;
  try {
    await api.delete(`/vaccinations/${id}/`);
    alert('✅ Vaccination deleted!');
    fetchData();
  } catch (error) {
    console.error('Error:', error);
  }
};

const printCertificate = async (vaccination) => {
  try {
    const pt = await api.get(`/patients/${vaccination.patient}/`);
    const ow = await api.get(`/owners/${pt.data.owner}/`);
    printData.value = { vaccination, patient: pt.data, owner: ow.data };
    showPrintModal.value = true;
  } catch (error) {
    alert('Failed to load certificate data');
  }
};

const triggerPrint = () => window.print();

const closePrintModal = () => { 
  showPrintModal.value = false; 
  printData.value = null; 
};

onMounted(() => fetchData());
</script>

<style scoped>
@media print {
  body * { visibility: hidden; }
  #printable-certificate, #printable-certificate * { visibility: visible; }
  #printable-certificate { position: absolute; left: 0; top: 0; width: 100%; }
}
</style>