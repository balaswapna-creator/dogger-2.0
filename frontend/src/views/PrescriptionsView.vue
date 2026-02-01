<template>
  <div class="prescriptions-view">
    <div class="page-header">
      <h1>Prescriptions</h1>
      <button @click="openNewPrescriptionModal" class="btn-primary">
        <i class="fas fa-plus"></i> New Prescription
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <i class="fas fa-spinner fa-spin"></i> Loading prescriptions...
    </div>

    <!-- Prescriptions Table -->
    <div v-else-if="prescriptions.length > 0" class="prescriptions-table">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Patient</th>
            <th>Medicines</th>
            <th>First Medicine</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="prescription in (Array.isArray(prescriptions) ? prescriptions : []).filter(p => p && p.id)" :key="prescription.id">
            <td>{{ formatDate(prescription.created_at) }}</td>
            <td>{{ prescription.patient_name || 'Unknown' }}</td>
            <td>
              <span class="medicine-count">
                {{ prescription.medicine_count || prescription.medicines?.length || 1 }} Medicine(s)
              </span>
            </td>
            <td>
              <span v-if="prescription.medicines && prescription.medicines.length > 0">
                {{ prescription.medicines[0].medication_name }}
                <span v-if="prescription.medicines.length > 1" class="more-medicines">
                  + {{ prescription.medicines.length - 1 }} more
                </span>
              </span>
              <span v-else>{{ prescription.medication_name || 'N/A' }}</span>
            </td>
            <td class="actions">
              <button @click="viewPrescription(prescription)" class="btn-view" title="View">
                <i class="fas fa-eye"></i>
              </button>
              <button @click="printPrescription(prescription)" class="btn-print" title="Print">
                <i class="fas fa-print"></i>
              </button>
              <button @click="deletePrescription(prescription.id)" class="btn-delete" title="Delete">
                <i class="fas fa-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <i class="fas fa-prescription"></i>
      <p>No prescriptions found</p>
      <button @click="openNewPrescriptionModal" class="btn-primary">
        Create First Prescription
      </button>
    </div>

    <!-- New/Edit Prescription Modal -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ isEditMode ? 'Edit Prescription' : 'New Prescription' }}</h2>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="savePrescription">
            <!-- Medical Record Selection -->
            <div class="form-group">
              <label>Patient/Consultation *</label>
              <select v-model="form.medical_record" required :disabled="isEditMode">
                <option value="">Select consultation</option>
                <option 
                  v-for="record in (Array.isArray(medicalRecords) ? medicalRecords : []).filter(r => r && r.id)" 
                  :key="record.id" 
                  :value="record.id"
                >
                  {{ record.patient_name || 'Unknown' }} - {{ formatDate(record.visit_date) }}
                </option>
              </select>
            </div>

            <!-- Medicines Section -->
            <div class="medicines-section">
              <div class="section-header">
                <h3>Medicines</h3>
                <button type="button" @click="addMedicine" class="btn-add-medicine">
                  <i class="fas fa-plus"></i> Add Medicine
                </button>
              </div>

              <div v-for="(medicine, index) in form.medicines" :key="index" class="medicine-card">
                <div class="medicine-header">
                  <span class="medicine-number">Medicine #{{ index + 1 }}</span>
                  <button 
                    v-if="form.medicines.length > 1" 
                    type="button" 
                    @click="removeMedicine(index)" 
                    class="btn-remove-medicine"
                  >
                    <i class="fas fa-times"></i>
                  </button>
                </div>

                <div class="medicine-fields">
                  <div class="form-group">
                    <label>Medication Name *</label>
                    <input 
                      v-model="medicine.medication_name" 
                      type="text" 
                      placeholder="e.g., Syrup Soft coat"
                      required
                    />
                  </div>

                  <div class="form-row">
                    <div class="form-group">
                      <label>Dosage *</label>
                      <input 
                        v-model="medicine.dosage" 
                        type="text" 
                        placeholder="e.g., 10ml, 2 tablets"
                        required
                      />
                    </div>

                    <div class="form-group">
                      <label>Frequency *</label>
                      <input 
                        v-model="medicine.frequency" 
                        type="text" 
                        placeholder="e.g., Twice daily"
                        required
                      />
                    </div>

                    <div class="form-group">
                      <label>Duration *</label>
                      <input 
                        v-model="medicine.duration" 
                        type="text" 
                        placeholder="e.g., 7 days"
                        required
                      />
                    </div>
                  </div>

                  <div class="form-group">
                    <label>Instructions</label>
                    <textarea 
                      v-model="medicine.instructions" 
                      rows="2"
                      placeholder="e.g., After meals, Before bedtime"
                    ></textarea>
                  </div>
                </div>
              </div>
            </div>

            <!-- Form Actions -->
            <div class="form-actions">
              <button type="button" @click="closeModal" class="btn-secondary">Cancel</button>
              <button type="submit" class="btn-primary">
                {{ isEditMode ? 'Update' : 'Create' }} Prescription
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- View Prescription Modal -->
    <div v-if="showViewModal" class="modal-overlay" @click="closeViewModal">
      <div class="modal-content view-modal" @click.stop>
        <div class="modal-header">
          <h2>Prescription Details</h2>
          <button @click="closeViewModal" class="close-btn">&times;</button>
        </div>

        <div class="modal-body" v-if="selectedPrescription">
          <div class="prescription-info">
            <div class="info-row">
              <strong>Patient:</strong> {{ selectedPrescription.patient_name }}
            </div>
            <div class="info-row">
              <strong>Date:</strong> {{ formatDate(selectedPrescription.created_at) }}
            </div>
          </div>

          <div class="medicines-list">
            <h3>Medicines ({{ selectedPrescription.medicines?.length || 1 }})</h3>
            
            <!-- Multiple Medicines (New Format) -->
            <div v-if="selectedPrescription.medicines && selectedPrescription.medicines.length > 0">
              <div v-for="(med, index) in selectedPrescription.medicines" :key="index" class="medicine-detail-card">
                <div class="medicine-number-badge">{{ index + 1 }}</div>
                <div class="medicine-details">
                  <h4>{{ med.medication_name }}</h4>
                  <div class="detail-grid">
                    <div class="detail-item">
                      <span class="label">Dosage:</span>
                      <span class="value">{{ med.dosage }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="label">Frequency:</span>
                      <span class="value">{{ med.frequency }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="label">Duration:</span>
                      <span class="value">{{ med.duration }}</span>
                    </div>
                    <div v-if="med.instructions" class="detail-item full-width">
                      <span class="label">Instructions:</span>
                      <span class="value">{{ med.instructions }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Single Medicine (Old Format) -->
            <div v-else class="medicine-detail-card">
              <div class="medicine-number-badge">1</div>
              <div class="medicine-details">
                <h4>{{ selectedPrescription.medication_name }}</h4>
                <div class="detail-grid">
                  <div class="detail-item">
                    <span class="label">Dosage:</span>
                    <span class="value">{{ selectedPrescription.dosage }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="label">Frequency:</span>
                    <span class="value">{{ selectedPrescription.frequency }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="label">Duration:</span>
                    <span class="value">{{ selectedPrescription.duration }}</span>
                  </div>
                  <div v-if="selectedPrescription.instructions" class="detail-item full-width">
                    <span class="label">Instructions:</span>
                    <span class="value">{{ selectedPrescription.instructions }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { apiRequest } from '../utils/api';

export default {
  name: 'PrescriptionsView',
  setup() {
    // State
    const loading = ref(false);
    const prescriptions = ref([]);
    const medicalRecords = ref([]);
    const showModal = ref(false);
    const showViewModal = ref(false);
    const isEditMode = ref(false);
    const selectedPrescription = ref(null);

    // Form data
    const form = ref({
      medical_record: '',
      medicines: [
        {
          medication_name: '',
          dosage: '',
          frequency: '',
          duration: '',
          instructions: ''
        }
      ]
    });

    // Fetch prescriptions
    const fetchPrescriptions = async () => {
      loading.value = true;
      try {
        const data = await apiRequest('GET', '/prescriptions/');
        // Handle paginated response
        prescriptions.value = Array.isArray(data) ? data : (data.results || []);
      } catch (error) {
        console.error('Error fetching prescriptions:', error);
        alert('Failed to load prescriptions');
      } finally {
        loading.value = false;
      }
    };

    // Fetch medical records for dropdown
    const fetchMedicalRecords = async () => {
      try {
        const data = await apiRequest('GET', '/medical-records/');
        // Handle paginated response
        medicalRecords.value = Array.isArray(data) ? data : (data.results || []);
      } catch (error) {
        console.error('Error fetching medical records:', error);
      }
    };

    // Open new prescription modal
    const openNewPrescriptionModal = async () => {
      isEditMode.value = false;
      resetForm();
      await fetchMedicalRecords();
      showModal.value = true;
    };

    // Add medicine to form
    const addMedicine = () => {
      form.value.medicines.push({
        medication_name: '',
        dosage: '',
        frequency: '',
        duration: '',
        instructions: ''
      });
    };

    // Remove medicine from form
    const removeMedicine = (index) => {
      if (form.value.medicines.length > 1) {
        form.value.medicines.splice(index, 1);
      }
    };

    // Save prescription
    const savePrescription = async () => {
      try {
        const payload = {
          medical_record_id: form.value.medical_record,  // Send medical_record_id
          medicines: form.value.medicines
        };

        console.log('Saving prescription with payload:', payload);

        if (isEditMode.value) {
          await apiRequest('PUT', `/prescriptions/${selectedPrescription.value.id}/`, payload);
          alert('Prescription updated successfully');
        } else {
          await apiRequest('POST', '/prescriptions/', payload);
          alert('Prescription created successfully');
        }

        closeModal();
        fetchPrescriptions();
      } catch (error) {
        console.error('Error saving prescription:', error);
        alert('Failed to save prescription: ' + (error.message || 'Unknown error'));
      }
    };

    // View prescription
    const viewPrescription = (prescription) => {
      selectedPrescription.value = prescription;
      showViewModal.value = true;
    };

    // Print prescription
    const printPrescription = (prescription) => {
      console.log('Printing prescription:', prescription);
      console.log('Medicines array:', prescription.medicines);
      console.log('Old format fields:', {
        medication_name: prescription.medication_name,
        dosage: prescription.dosage,
        frequency: prescription.frequency,
        duration: prescription.duration
      });
      
      const printWindow = window.open('', '_blank');
      
      let medicinesHtml = '';
      
      // Check if medicines array exists and has data
      if (prescription.medicines && Array.isArray(prescription.medicines) && prescription.medicines.length > 0) {
        console.log('Using medicines array format');
        medicinesHtml = prescription.medicines.map((med, index) => `
          <div style="margin-bottom: 15px; padding: 10px; background: #f9f9f9; border-left: 3px solid #4CAF50;">
            <div style="font-weight: bold; margin-bottom: 5px;">${index + 1}. ${med.medication_name || 'Not specified'}</div>
            <div style="margin-left: 20px;">
              <div>Dosage: ${med.dosage || 'Not specified'}</div>
              <div>Frequency: ${med.frequency || 'Not specified'}</div>
              <div>Duration: ${med.duration || 'Not specified'}</div>
              ${med.instructions ? `<div>Instructions: ${med.instructions}</div>` : ''}
            </div>
          </div>
        `).join('');
      } 
      // Check if old format fields exist
      else if (prescription.medication_name || prescription.dosage || prescription.frequency) {
        console.log('Using old single-medicine format');
        medicinesHtml = `
          <div style="margin-bottom: 15px; padding: 10px; background: #f9f9f9; border-left: 3px solid #4CAF50;">
            <div style="font-weight: bold; margin-bottom: 5px;">1. ${prescription.medication_name || 'Not specified'}</div>
            <div style="margin-left: 20px;">
              <div>Dosage: ${prescription.dosage || 'Not specified'}</div>
              <div>Frequency: ${prescription.frequency || 'Not specified'}</div>
              <div>Duration: ${prescription.duration || 'Not specified'}</div>
              ${prescription.instructions ? `<div>Instructions: ${prescription.instructions}</div>` : ''}
            </div>
          </div>
        `;
      } 
      // No medicine data found
      else {
        console.error('No medicine data found in prescription!');
        medicinesHtml = `
          <div style="margin-bottom: 15px; padding: 10px; background: #fff3cd; border-left: 3px solid #ffc107;">
            <div style="font-weight: bold; color: #856404;">No medicine information available</div>
            <div style="margin-top: 10px; font-size: 12px; color: #856404;">
              This prescription may have been created with incomplete data.
            </div>
          </div>
        `;
      }

      printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
          <title>Prescription - ${prescription.patient_name || 'Unknown Patient'}</title>
          <style>
            body {
              font-family: Arial, sans-serif;
              padding: 40px;
              max-width: 800px;
              margin: 0 auto;
            }
            .header {
              text-align: center;
              border-bottom: 2px solid #333;
              padding-bottom: 20px;
              margin-bottom: 30px;
            }
            .clinic-name {
              font-size: 24px;
              font-weight: bold;
              color: #2c3e50;
            }
            .rx-symbol {
              font-size: 36px;
              color: #4CAF50;
              margin: 20px 0;
            }
            .patient-info {
              margin-bottom: 30px;
            }
            .patient-info div {
              margin: 5px 0;
            }
            .signature {
              margin-top: 60px;
              text-align: right;
            }
            @media print {
              body { padding: 20px; }
            }
          </style>
        </head>
        <body>
          <div class="header">
            <div class="clinic-name">Sri Adithya Pet Clinic</div>
            <div>Veterinary Care & Services</div>
          </div>
          
          <div class="patient-info">
            <div><strong>Patient:</strong> ${prescription.patient_name || 'Unknown'}</div>
            <div><strong>Date:</strong> ${formatDate(prescription.created_at)}</div>
          </div>
          
          <div class="rx-symbol">℞</div>
          
          <div class="medicines">
            ${medicinesHtml}
          </div>
          
          <div class="signature">
            <div style="margin-top: 40px; border-top: 1px solid #333; display: inline-block; padding-top: 5px;">
              Doctor's Signature
            </div>
          </div>
        </body>
        </html>
      `);
      
      printWindow.document.close();
      printWindow.print();
    };

    // Delete prescription
    const deletePrescription = async (id) => {
      if (!confirm('Are you sure you want to delete this prescription?')) {
        return;
      }

      try {
        await apiRequest('DELETE', `/prescriptions/${id}/`);
        alert('Prescription deleted successfully');
        fetchPrescriptions();
      } catch (error) {
        console.error('Error deleting prescription:', error);
        alert('Failed to delete prescription');
      }
    };

    // Close modals
    const closeModal = () => {
      showModal.value = false;
      resetForm();
    };

    const closeViewModal = () => {
      showViewModal.value = false;
      selectedPrescription.value = null;
    };

    // Reset form
    const resetForm = () => {
      form.value = {
        medical_record: '',
        medicines: [
          {
            medication_name: '',
            dosage: '',
            frequency: '',
            duration: '',
            instructions: ''
          }
        ]
      };
    };

    // Format date
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    };

    // Load data on mount
    onMounted(() => {
      fetchPrescriptions();
    });

    return {
      loading,
      prescriptions,
      medicalRecords,
      showModal,
      showViewModal,
      isEditMode,
      selectedPrescription,
      form,
      fetchPrescriptions,
      openNewPrescriptionModal,
      addMedicine,
      removeMedicine,
      savePrescription,
      viewPrescription,
      printPrescription,
      deletePrescription,
      closeModal,
      closeViewModal,
      formatDate
    };
  }
};
</script>

<style scoped>
.prescriptions-view {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  font-size: 24px;
  color: #2c3e50;
}

.btn-primary {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary:hover {
  background: #45a049;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.loading-state i {
  font-size: 36px;
  margin-bottom: 10px;
}

.empty-state i {
  font-size: 64px;
  margin-bottom: 20px;
  color: #bdc3c7;
}

.prescriptions-table {
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
  background: #f8f9fa;
}

th {
  padding: 12px;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #dee2e6;
}

td {
  padding: 12px;
  border-bottom: 1px solid #dee2e6;
}

.medicine-count {
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.more-medicines {
  color: #7f8c8d;
  font-size: 12px;
  margin-left: 5px;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-view,
.btn-print,
.btn-delete {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-view {
  background: #2196F3;
  color: white;
}

.btn-print {
  background: #FF9800;
  color: white;
}

.btn-delete {
  background: #f44336;
  color: white;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #dee2e6;
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #7f8c8d;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #2c3e50;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.medicines-section {
  margin-top: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-header h3 {
  margin: 0;
  font-size: 18px;
  color: #2c3e50;
}

.btn-add-medicine {
  background: #2196F3;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.medicine-card {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  background: #fafafa;
}

.medicine-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.medicine-number {
  font-weight: 600;
  color: #4CAF50;
  font-size: 16px;
}

.btn-remove-medicine {
  background: #f44336;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #dee2e6;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.prescription-info {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.info-row {
  margin-bottom: 8px;
}

.medicines-list h3 {
  margin-bottom: 15px;
  color: #2c3e50;
}

.medicine-detail-card {
  display: flex;
  gap: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
  margin-bottom: 15px;
  border-left: 4px solid #4CAF50;
}

.medicine-number-badge {
  background: #4CAF50;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.medicine-details {
  flex: 1;
}

.medicine-details h4 {
  margin: 0 0 10px 0;
  color: #2c3e50;
  font-size: 16px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-item .label {
  font-size: 12px;
  color: #7f8c8d;
  margin-bottom: 2px;
}

.detail-item .value {
  font-size: 14px;
  color: #2c3e50;
  font-weight: 500;
}
</style>
