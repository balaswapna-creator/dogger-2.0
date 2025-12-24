<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">💊 Prescriptions</h1>
      <button
        @click="openModal()"
        class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg flex items-center gap-2"
      >
        <span class="text-xl">➕</span> New Prescription
      </button>
    </div>

    <!-- Search Bar -->
    <div class="mb-6">
      <input
        v-model="searchQuery"
        @input="searchPrescriptions"
        type="text"
        placeholder="🔍 Search by medication, patient name, or instructions..."
        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Prescriptions Table -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div v-if="loading" class="text-center py-12">
        <div class="text-gray-500">Loading prescriptions...</div>
      </div>

      <div v-else-if="prescriptions.length === 0" class="text-center py-12">
        <div class="text-gray-500 text-lg">No prescriptions found</div>
        <button
          @click="openModal()"
          class="mt-4 text-blue-600 hover:text-blue-800 font-medium"
        >
          Create your first prescription
        </button>
      </div>

      <table v-else class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Patient</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Medication</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Dosage</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Frequency</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Duration</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Doctor</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="prescription in prescriptions" :key="prescription.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ formatDate(prescription.created_at) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{{ prescription.patient_name }}</div>
            </td>
            <td class="px-6 py-4">
              <div class="text-sm font-medium text-gray-900">{{ prescription.medication_name }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
              {{ prescription.dosage }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
              {{ prescription.frequency }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
              {{ prescription.duration }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
              {{ prescription.doctor_name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm space-x-2">
              <button
                @click="viewPrescription(prescription)"
                class="text-blue-600 hover:text-blue-800"
                title="View"
              >
                👁️
              </button>
              <button
                @click="openModal(prescription)"
                class="text-green-600 hover:text-green-800"
                title="Edit"
              >
                ✏️
              </button>
              <button
                @click="printPrescription(prescription)"
                class="text-purple-600 hover:text-purple-800"
                title="Print"
              >
                🖨️
              </button>
              <button
                @click="deletePrescription(prescription.id)"
                class="text-red-600 hover:text-red-800"
                title="Delete"
              >
                🗑️
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <h2 class="text-2xl font-bold mb-6 text-gray-800">
            {{ editMode ? '✏️ Edit Prescription' : '➕ New Prescription' }}
          </h2>
          
          <form @submit.prevent="savePrescription" class="space-y-4">
            <!-- Medical Record (Consultation) Selection -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Select Consultation *</label>
              <select
                v-model="form.medical_record"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Choose Consultation</option>
                <option v-for="consultation in consultations" :key="consultation.id" :value="consultation.id">
                  {{ consultation.patient_name }} - {{ formatDate(consultation.visit_date) }} - {{ consultation.diagnosis || consultation.chief_complaint }}
                </option>
              </select>
              <p class="text-xs text-gray-500 mt-1">Prescription will be linked to this consultation</p>
            </div>

            <!-- Medication Name -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Medication Name *</label>
              <input
                v-model="form.medication_name"
                type="text"
                required
                placeholder="e.g., Amoxicillin"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <!-- Dosage -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Dosage *</label>
              <input
                v-model="form.dosage"
                type="text"
                required
                placeholder="e.g., 250mg, 1 tablet"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <!-- Frequency -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Frequency *</label>
              <select
                v-model="form.frequency"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select Frequency</option>
                <option value="Once daily">Once daily</option>
                <option value="Twice daily">Twice daily</option>
                <option value="Three times daily">Three times daily</option>
                <option value="Four times daily">Four times daily</option>
                <option value="Every 8 hours">Every 8 hours</option>
                <option value="Every 12 hours">Every 12 hours</option>
                <option value="As needed">As needed</option>
                <option value="Before meals">Before meals</option>
                <option value="After meals">After meals</option>
              </select>
            </div>

            <!-- Duration -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Duration *</label>
              <input
                v-model="form.duration"
                type="text"
                required
                placeholder="e.g., 7 days, 2 weeks"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <!-- Instructions -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Instructions</label>
              <textarea
                v-model="form.instructions"
                rows="3"
                placeholder="Additional instructions for pet owner..."
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              ></textarea>
            </div>

            <!-- Action Buttons -->
            <div class="flex justify-end gap-3 mt-6">
              <button
                type="button"
                @click="closeModal"
                class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
              >
                {{ editMode ? 'Update' : 'Create' }} Prescription
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- View Modal -->
    <div
      v-if="showViewModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="closeViewModal"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full">
        <div class="p-8">
          <div class="flex justify-between items-start mb-6">
            <h2 class="text-2xl font-bold text-gray-800">💊 Prescription Details</h2>
            <button @click="closeViewModal" class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
          </div>
          
          <div v-if="selectedPrescription" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-500">Patient</p>
                <p class="font-medium">{{ selectedPrescription.patient_name }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Date</p>
                <p class="font-medium">{{ formatDate(selectedPrescription.created_at) }}</p>
              </div>
            </div>
            
            <div class="border-t pt-4">
              <p class="text-sm text-gray-500">Medication</p>
              <p class="text-lg font-bold text-blue-600">{{ selectedPrescription.medication_name }}</p>
            </div>
            
            <div class="grid grid-cols-3 gap-4">
              <div>
                <p class="text-sm text-gray-500">Dosage</p>
                <p class="font-medium">{{ selectedPrescription.dosage }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Frequency</p>
                <p class="font-medium">{{ selectedPrescription.frequency }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Duration</p>
                <p class="font-medium">{{ selectedPrescription.duration }}</p>
              </div>
            </div>
            
            <div v-if="selectedPrescription.instructions" class="border-t pt-4">
              <p class="text-sm text-gray-500">Instructions</p>
              <p class="text-gray-700">{{ selectedPrescription.instructions }}</p>
            </div>
            
            <div class="border-t pt-4">
              <p class="text-sm text-gray-500">Prescribed by</p>
              <p class="font-medium">Dr. {{ selectedPrescription.doctor_name }}</p>
            </div>

            <div class="flex justify-end gap-3 mt-6">
              <button
                @click="printPrescription(selectedPrescription)"
                class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg flex items-center gap-2"
              >
                🖨️ Print
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const prescriptions = ref([])
const consultations = ref([])
const loading = ref(true)
const showModal = ref(false)
const showViewModal = ref(false)
const editMode = ref(false)
const searchQuery = ref('')
const selectedPrescription = ref(null)

const form = ref({
  medical_record: '',
  medication_name: '',
  dosage: '',
  frequency: '',
  duration: '',
  instructions: ''
})

const fetchPrescriptions = async () => {
  try {
    loading.value = true
    const response = await api.get('/prescriptions/')
    prescriptions.value = response.data?.results || response.data || []
  } catch (error) {
    console.error('Error fetching prescriptions:', error)
    alert('Failed to load prescriptions')
  } finally {
    loading.value = false
  }
}

const fetchConsultations = async () => {
  try {
    const response = await api.get('/medical-records/')
    consultations.value = response.data?.results || response.data || []
  } catch (error) {
    console.error('Error fetching consultations:', error)
  }
}

const openModal = (prescription = null) => {
  if (prescription) {
    editMode.value = true
    form.value = {
      id: prescription.id,
      medical_record: prescription.medical_record,
      medication_name: prescription.medication_name,
      dosage: prescription.dosage,
      frequency: prescription.frequency,
      duration: prescription.duration,
      instructions: prescription.instructions || ''
    }
  } else {
    editMode.value = false
    form.value = {
      medical_record: '',
      medication_name: '',
      dosage: '',
      frequency: '',
      duration: '',
      instructions: ''
    }
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const savePrescription = async () => {
  try {
    const payload = {
      ...form.value,
      medical_record: form.value.medical_record || null
    }
    
    if (editMode.value) {
      await api.put(`/prescriptions/${form.value.id}/`, payload)
      alert('Prescription updated successfully!')
    } else {
      await api.post('/prescriptions/', payload)
      alert('Prescription created successfully!')
    }
    
    closeModal()
    fetchPrescriptions()
  } catch (error) {
    console.error('Error saving prescription:', error)
    alert('Failed to save prescription')
  }
}

const deletePrescription = async (id) => {
  if (!confirm('Are you sure you want to delete this prescription?')) return
  
  try {
    await api.delete(`/prescriptions/${id}/`)
    alert('Prescription deleted successfully!')
    fetchPrescriptions()
  } catch (error) {
    console.error('Error deleting prescription:', error)
    alert('Failed to delete prescription')
  }
}

const viewPrescription = (prescription) => {
  selectedPrescription.value = prescription
  showViewModal.value = true
}

const closeViewModal = () => {
  showViewModal.value = false
  selectedPrescription.value = null
}

const printPrescription = (prescription) => {
  const printWindow = window.open('', '_blank')
  printWindow.document.write(`
    <html>
      <head>
        <title>Prescription - ${prescription.patient_name}</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 40px; }
          .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
          .clinic-name { font-size: 24px; font-weight: bold; color: #2563eb; }
          .details { margin: 20px 0; }
          .label { font-weight: bold; color: #666; }
          .rx { font-size: 36px; font-weight: bold; color: #2563eb; margin: 20px 0; }
          .medication { background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0; }
          .footer { margin-top: 50px; border-top: 1px solid #ccc; padding-top: 20px; }
        </style>
      </head>
      <body>
        <div class="header">
          <div class="clinic-name">Dogger Pet Clinic</div>
          <div>Veterinary Care Center</div>
        </div>
        
        <div class="details">
          <div><span class="label">Date:</span> ${formatDate(prescription.created_at)}</div>
          <div><span class="label">Patient:</span> ${prescription.patient_name}</div>
          <div><span class="label">Doctor:</span> Dr. ${prescription.doctor_name}</div>
        </div>
        
        <div class="rx">℞</div>
        
        <div class="medication">
          <h3>${prescription.medication_name}</h3>
          <p><span class="label">Dosage:</span> ${prescription.dosage}</p>
          <p><span class="label">Frequency:</span> ${prescription.frequency}</p>
          <p><span class="label">Duration:</span> ${prescription.duration}</p>
          ${prescription.instructions ? `<p><span class="label">Instructions:</span> ${prescription.instructions}</p>` : ''}
        </div>
        
        <div class="footer">
          <p>_________________________</p>
          <p>Dr. ${prescription.doctor_name}</p>
          <p>Veterinary Surgeon</p>
        </div>
      </body>
    </html>
  `)
  printWindow.document.close()
  printWindow.print()
}

const searchPrescriptions = async () => {
  if (!searchQuery.value.trim()) {
    fetchPrescriptions()
    return
  }
  
  try {
    loading.value = true
    const response = await api.get(`/prescriptions/?search=${searchQuery.value}`)
    prescriptions.value = response.data?.results || response.data || []
  } catch (error) {
    console.error('Error searching prescriptions:', error)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-IN', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}

onMounted(() => {
  fetchPrescriptions()
  fetchConsultations()
})
</script>