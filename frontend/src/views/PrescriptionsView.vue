<template>
  <div class="prescription-form">
    <h2>Create Prescription</h2>
    
    <form @submit.prevent="handleSubmit">
      <!-- Patient Selection -->
      <div class="form-group">
        <label for="patient">Patient *</label>
        <select v-model="form.patient_id" id="patient" required>
          <option value="">Select Patient</option>
          <option v-for="patient in patients" :key="patient.id" :value="patient.id">
            {{ patient.pet_name }} - {{ patient.owner?.name }}
          </option>
        </select>
      </div>

      <!-- Date -->
      <div class="form-group">
        <label for="date">Date *</label>
        <input 
          type="date" 
          id="date" 
          v-model="form.date" 
          required
        />
      </div>

      <!-- Diagnosis -->
      <div class="form-group">
        <label for="diagnosis">Diagnosis *</label>
        <textarea 
          id="diagnosis" 
          v-model="form.diagnosis" 
          rows="3"
          placeholder="Enter diagnosis details..."
          required
        ></textarea>
      </div>

      <!-- MEDICINES SECTION - Dynamic List -->
      <div class="medicines-section">
        <div class="section-header">
          <h3>💊 Medicines</h3>
          <button 
            type="button" 
            class="btn-add-medicine"
            @click="addMedicine"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="16"></line>
              <line x1="8" y1="12" x2="16" y2="12"></line>
            </svg>
            Add Another Medicine
          </button>
        </div>

        <!-- List of Medicines -->
        <div v-if="form.medicines.length === 0" class="empty-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path>
          </svg>
          <p>No medicines added yet</p>
          <button type="button" class="btn-add-first" @click="addMedicine">
            Add First Medicine
          </button>
        </div>

        <div v-else class="medicines-list">
          <div 
            v-for="(medicine, index) in form.medicines" 
            :key="index"
            class="medicine-card"
          >
            <div class="card-header">
              <span class="medicine-number">Medicine #{{ index + 1 }}</span>
              <button 
                v-if="form.medicines.length > 1"
                type="button" 
                class="btn-remove"
                @click="removeMedicine(index)"
                title="Remove this medicine"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </button>
            </div>

            <div class="medicine-fields">
              <!-- Medicine Name -->
              <div class="form-group">
                <label :for="`medicine-name-${index}`">Medicine Name *</label>
                <input 
                  :id="`medicine-name-${index}`"
                  type="text" 
                  v-model="medicine.name"
                  placeholder="e.g., Amoxicillin"
                  required
                />
              </div>

              <!-- Dosage -->
              <div class="form-group">
                <label :for="`dosage-${index}`">Dosage *</label>
                <input 
                  :id="`dosage-${index}`"
                  type="text" 
                  v-model="medicine.dosage"
                  placeholder="e.g., 500mg"
                  required
                />
              </div>

              <!-- Frequency -->
              <div class="form-group">
                <label :for="`frequency-${index}`">Frequency *</label>
                <select :id="`frequency-${index}`" v-model="medicine.frequency" required>
                  <option value="">Select frequency</option>
                  <option value="Once daily">Once daily</option>
                  <option value="Twice daily">Twice daily (BID)</option>
                  <option value="Three times daily">Three times daily (TID)</option>
                  <option value="Four times daily">Four times daily (QID)</option>
                  <option value="Every 6 hours">Every 6 hours</option>
                  <option value="Every 8 hours">Every 8 hours</option>
                  <option value="Every 12 hours">Every 12 hours</option>
                  <option value="As needed">As needed (PRN)</option>
                </select>
              </div>

              <!-- Duration -->
              <div class="form-group">
                <label :for="`duration-${index}`">Duration *</label>
                <div class="duration-input">
                  <input 
                    :id="`duration-${index}`"
                    type="number" 
                    v-model="medicine.duration_value"
                    min="1"
                    placeholder="7"
                    required
                  />
                  <select v-model="medicine.duration_unit" required>
                    <option value="days">Days</option>
                    <option value="weeks">Weeks</option>
                    <option value="months">Months</option>
                  </select>
                </div>
              </div>

              <!-- Instructions -->
              <div class="form-group full-width">
                <label :for="`instructions-${index}`">Instructions</label>
                <textarea 
                  :id="`instructions-${index}`"
                  v-model="medicine.instructions"
                  rows="2"
                  placeholder="e.g., Take with food, avoid dairy products..."
                ></textarea>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Notes -->
      <div class="form-group">
        <label for="notes">Additional Notes</label>
        <textarea 
          id="notes" 
          v-model="form.notes" 
          rows="3"
          placeholder="Any additional instructions or notes..."
        ></textarea>
      </div>

      <!-- Form Actions -->
      <div class="form-actions">
        <button type="button" class="btn-cancel" @click="handleCancel">
          Cancel
        </button>
        <button type="submit" class="btn-submit" :disabled="form.medicines.length === 0">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
            <polyline points="17 21 17 13 7 13 7 21"></polyline>
            <polyline points="7 3 7 8 15 8"></polyline>
          </svg>
          Create Prescription
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()
const patients = ref([])

// Form data
const form = ref({
  patient_id: '',
  date: new Date().toISOString().split('T')[0],
  diagnosis: '',
  medicines: [],
  notes: ''
})

// Medicine template
const createEmptyMedicine = () => ({
  name: '',
  dosage: '',
  frequency: '',
  duration_value: 7,
  duration_unit: 'days',
  instructions: ''
})

// Add first medicine on mount
onMounted(async () => {
  await loadPatients()
  // Start with one empty medicine
  if (form.value.medicines.length === 0) {
    addMedicine()
  }
})

const loadPatients = async () => {
  try {
    const response = await api.get('/patients/')
    patients.value = response.data
  } catch (error) {
    console.error('Error loading patients:', error)
    alert('Failed to load patients')
  }
}

const addMedicine = () => {
  form.value.medicines.push(createEmptyMedicine())
}

const removeMedicine = (index) => {
  if (confirm('Remove this medicine?')) {
    form.value.medicines.splice(index, 1)
  }
}

const handleSubmit = async () => {
  if (form.value.medicines.length === 0) {
    alert('Please add at least one medicine')
    return
  }

  try {
    // Format medicines for API
    const medicinesFormatted = form.value.medicines.map(m => ({
      name: m.name,
      dosage: m.dosage,
      frequency: m.frequency,
      duration: `${m.duration_value} ${m.duration_unit}`,
      instructions: m.instructions || ''
    }))

    const prescriptionData = {
      patient: form.value.patient_id,
      date: form.value.date,
      diagnosis: form.value.diagnosis,
      medicines: medicinesFormatted,
      notes: form.value.notes
    }

    await api.post('/prescriptions/', prescriptionData)
    alert('Prescription created successfully!')
    router.push('/prescriptions')
  } catch (error) {
    console.error('Error creating prescription:', error)
    alert('Failed to create prescription')
  }
}

const handleCancel = () => {
  if (confirm('Discard this prescription?')) {
    router.push('/prescriptions')
  }
}
</script>

<style scoped>
.prescription-form {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

h2 {
  margin: 0 0 24px 0;
  color: #1e293b;
  font-size: 24px;
  font-weight: 700;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #475569;
  font-weight: 600;
  font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px 14px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

/* Medicines Section */
.medicines-section {
  margin: 32px 0;
  padding: 24px;
  background: #f8fafc;
  border-radius: 12px;
  border: 2px dashed #cbd5e1;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 18px;
  font-weight: 700;
}

.btn-add-medicine {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: #7C3AED;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-add-medicine:hover {
  background: #6D28D9;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 48px 24px;
  color: #64748b;
}

.empty-state svg {
  margin-bottom: 16px;
  opacity: 0.3;
}

.empty-state p {
  margin: 0 0 16px 0;
  font-size: 16px;
}

.btn-add-first {
  padding: 12px 24px;
  background: #7C3AED;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-add-first:hover {
  background: #6D28D9;
}

/* Medicine Cards */
.medicines-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.medicine-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  padding: 20px;
  transition: all 0.2s;
}

.medicine-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
}

.medicine-number {
  font-weight: 700;
  color: #7C3AED;
  font-size: 14px;
}

.btn-remove {
  padding: 6px;
  background: #fee2e2;
  color: #ef4444;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-remove:hover {
  background: #fecaca;
  transform: scale(1.1);
}

.medicine-fields {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.medicine-fields .full-width {
  grid-column: 1 / -1;
}

.duration-input {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 8px;
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e2e8f0;
}

.btn-cancel,
.btn-submit {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-cancel {
  background: #f1f5f9;
  color: #475569;
}

.btn-cancel:hover {
  background: #e2e8f0;
}

.btn-submit {
  background: #10b981;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  background: #059669;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-submit:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
  opacity: 0.6;
}

/* Responsive */
@media (max-width: 768px) {
  .prescription-form {
    padding: 20px;
  }

  .section-header {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .btn-add-medicine {
    justify-content: center;
  }

  .medicine-fields {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-cancel,
  .btn-submit {
    width: 100%;
    justify-content: center;
  }
}
</style>