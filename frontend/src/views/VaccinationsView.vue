<template>
  <div class="vaccinations-wrapper">
    <!-- Header Card -->
    <div class="header-card">
      <div class="header-content">
        <div class="header-title">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path>
            <path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"></path>
          </svg>
          <h1>Vaccinations</h1>
        </div>
        <button @click="openAddModal" class="btn-add">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          <span>Add Vaccination</span>
        </button>
      </div>
    </div>

    <!-- Vaccinations Table -->
    <div class="table-card">
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Patient</th>
              <th>Vaccine</th>
              <th>Date Given</th>
              <th>Next Due</th>
              <th>Certificate #</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="vax in vaccinations" :key="vax.id">
              <td>
                <div class="patient-info">
                  <div class="patient-avatar">{{ getPatientName(vax.patient).charAt(0) }}</div>
                  <span>{{ getPatientName(vax.patient) }}</span>
                </div>
              </td>
              <td>
                <span class="vaccine-badge">{{ vax.vaccine_name }}</span>
              </td>
              <td>{{ formatDate(vax.date_administered) }}</td>
              <td>
                <span class="due-badge" :class="getDueClass(vax.next_due_date)">
                  {{ formatDate(vax.next_due_date) }}
                </span>
              </td>
              <td>
                <span class="cert-number">{{ vax.certificate_number }}</span>
              </td>
              <td>
                <div class="action-buttons">
                  <button @click="openEditModal(vax)" class="btn-edit" title="Edit">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                  </button>
                  <button @click="printCertificate(vax)" class="btn-print" title="Print Certificate">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="6 9 6 2 18 2 18 9"></polyline>
                      <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                      <rect x="6" y="14" width="12" height="8"></rect>
                    </svg>
                  </button>
                  <button @click="deleteVaccination(vax.id)" class="btn-delete" title="Delete">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="vaccinations.length === 0">
              <td colspan="6" class="no-data">
                <div class="empty-state">
                  <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path>
                    <path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"></path>
                  </svg>
                  <p>No vaccinations recorded yet</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">
        <div class="modal-header">
          <h2>{{ isEditing ? 'Edit Vaccination' : 'New Vaccination' }}</h2>
          <button @click="closeModal" class="btn-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="form-grid">
            <div class="form-group full-width">
              <label>Patient *</label>
              <select v-model="form.patient">
                <option value="">Select Patient</option>
                <option v-for="patient in patients" :key="patient.id" :value="patient.id">
                  {{ patient.pet_name }} ({{ patient.species }})
                </option>
              </select>
            </div>

            <div class="form-group full-width">
              <label>Vaccine Name *</label>
              <input v-model="form.vaccine_name" type="text" placeholder="e.g., Rabies, DHPP"/>
            </div>

            <div class="form-group">
              <label>Manufacturer</label>
              <input v-model="form.manufacturer" type="text" placeholder="Optional"/>
            </div>

            <div class="form-group">
              <label>Batch Number</label>
              <input v-model="form.batch_number" type="text" placeholder="Optional"/>
            </div>

            <div class="form-group">
              <label>Date Administered *</label>
              <input v-model="form.date_administered" type="date"/>
            </div>

            <div class="form-group">
              <label>Next Due Date</label>
              <input v-model="form.next_due_date" type="date"/>
            </div>

            <div class="form-group full-width">
              <label>Administered By</label>
              <input v-model="form.administered_by" type="text" placeholder="Dr. A. Balasubramanan"/>
            </div>

            <div class="form-group full-width">
              <label>Notes</label>
              <textarea v-model="form.notes" rows="3" placeholder="Optional notes"></textarea>
            </div>
          </div>

          <div class="modal-actions">
            <button @click="closeModal" class="btn-cancel">Cancel</button>
            <button @click="saveVaccination" class="btn-save">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                <polyline points="17 21 17 13 7 13 7 21"></polyline>
                <polyline points="7 3 7 8 15 8"></polyline>
              </svg>
              {{ isEditing ? 'Update' : 'Save' }} Vaccination
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Print Modal -->
    <div v-if="showPrintModal && printData" class="modal-overlay">
      <div class="print-modal">
        <div class="print-header">
          <h2>Vaccination Certificate</h2>
          <button @click="closePrintModal" class="btn-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div id="printable-certificate" class="certificate-content">
          <div class="certificate-border">
            <div class="clinic-header">
              <h1>Sri Adithya Pet Clinic</h1>
              <p>Dr. A. Balasubramanan, B.V.Sc, MBA</p>
              <p>Main Road, Cumbum, Tamil Nadu - 625516</p>
            </div>

            <div class="certificate-title">
              <h2>VACCINATION CERTIFICATE</h2>
              <p>Certificate No: <strong>{{ printData.vaccination?.certificate_number }}</strong></p>
            </div>

            <div class="patient-section">
              <h3>Patient Information</h3>
              <div class="info-grid">
                <div><span>Pet Name:</span> <strong>{{ printData.patient?.pet_name }}</strong></div>
                <div><span>Owner Name:</span> <strong>{{ printData.owner?.name }}</strong></div>
                <div><span>Species:</span> <strong>{{ printData.patient?.species }}</strong></div>
                <div><span>Breed:</span> <strong>{{ printData.patient?.breed }}</strong></div>
              </div>
            </div>

            <div class="vaccination-section">
              <h3>Vaccination Details</h3>
              <table class="cert-table">
                <tr><td>Vaccine Name</td><td>{{ printData.vaccination?.vaccine_name }}</td></tr>
                <tr><td>Manufacturer</td><td>{{ printData.vaccination?.manufacturer || 'N/A' }}</td></tr>
                <tr><td>Batch Number</td><td>{{ printData.vaccination?.batch_number || 'N/A' }}</td></tr>
                <tr><td>Date Administered</td><td>{{ formatDate(printData.vaccination?.date_administered) }}</td></tr>
                <tr><td>Next Due Date</td><td>{{ formatDate(printData.vaccination?.next_due_date) }}</td></tr>
              </table>
            </div>

            <div class="signature-section">
              <div class="signature-line">
                <p>Dr. A. Balasubramanan</p>
                <p>B.V.Sc, MBA</p>
              </div>
            </div>
          </div>
        </div>

        <div class="print-actions">
          <button @click="triggerPrint" class="btn-print-action">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 6 2 18 2 18 9"></polyline>
              <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
              <rect x="6" y="14" width="12" height="8"></rect>
            </svg>
            Print Certificate
          </button>
          <button @click="closePrintModal" class="btn-cancel">Close</button>
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
  administered_by: 'Dr. A. Balasubramanan B.V.Sc,.MBA(HA)',
  notes: ''
});

const getPatientName = (id) => patients.value.find(p => p.id === id)?.pet_name || 'Unknown';

const formatDate = (d) => {
  if (!d) return 'N/A';
  return new Date(d).toLocaleDateString('en-IN');
};

const getDueClass = (date) => {
  if (!date) return '';
  const dueDate = new Date(date);
  const today = new Date();
  const diffDays = Math.floor((dueDate - today) / (1000 * 60 * 60 * 24));
  
  if (diffDays < 0) return 'overdue';
  if (diffDays <= 30) return 'upcoming';
  return '';
};

const fetchData = async () => {
  try {
    const [v, p] = await Promise.all([
      api.get('/vaccinations/'),
      api.get('/patients/')
    ]);
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
    administered_by: 'Dr. A. Balasubramanan B.V.Sc,.MBA(HA)',
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
    administered_by: vax.administered_by || 'Dr. A. Balasubramanan B.V.Sc,.MBA(HA)',
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
  if (!form.value.patient || !form.value.vaccine_name || !form.value.date_administered) {
    alert('Please fill in all required fields');
    return;
  }
  
  try {
    if (isEditing.value) {
      await api.put(`/vaccinations/${editingVaxId.value}/`, form.value);
      alert('Vaccination updated!');
    } else {
      await api.post('/vaccinations/', form.value);
      alert('Vaccination added!');
    }
    await fetchData();
    closeModal();
  } catch (error) {
    console.error('Error:', error);
    alert('Error saving vaccination');
  }
};

const deleteVaccination = async (id) => {
  if (!confirm('Delete this vaccination?')) return;
  try {
    await api.delete(`/vaccinations/${id}/`);
    alert('Vaccination deleted!');
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
.vaccinations-wrapper {
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
  color: #F59E0B;
}

.header-title h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1F2937;
}

.btn-add {
  background: linear-gradient(135deg, #F59E0B, #D97706);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
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
  background: linear-gradient(135deg, #F59E0B, #D97706);
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

.patient-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.patient-avatar {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, #F59E0B, #D97706);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
}

.vaccine-badge {
  background: #DBEAFE;
  color: #1E40AF;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
}

.due-badge {
  background: #D1FAE5;
  color: #065F46;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
}

.due-badge.upcoming {
  background: #FEF3C7;
  color: #92400E;
}

.due-badge.overdue {
  background: #FEE2E2;
  color: #991B1B;
}

.cert-number {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: #6B7280;
  font-size: 13px;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-edit, .btn-print, .btn-delete {
  background: #F3F4F6;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.btn-edit {
  color: #F59E0B;
}

.btn-edit:hover {
  background: #FEF3C7;
}

.btn-print {
  color: #14B8A6;
}

.btn-print:hover {
  background: #CCFBF1;
}

.btn-delete {
  color: #EF4444;
}

.btn-delete:hover {
  background: #FEE2E2;
}

.no-data {
  text-align: center;
  padding: 60px 20px !important;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.empty-state svg {
  color: #D1D5DB;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-container {
  background: white;
  border-radius: 20px;
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  background: linear-gradient(135deg, #F59E0B, #D97706);
  color: white;
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 20px 20px 0 0;
}

.modal-header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
}

.btn-close {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.btn-close:hover {
  background: rgba(255, 255, 255, 0.3);
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 10px;
  font-size: 15px;
  color: #1F2937;
  transition: all 0.3s;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #F59E0B;
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.1);
}

.modal-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #E5E7EB;
}

.btn-cancel {
  flex: 1;
  background: #F3F4F6;
  color: #4B5563;
  border: none;
  padding: 14px 24px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-cancel:hover {
  background: #E5E7EB;
}

.btn-save {
  flex: 2;
  background: linear-gradient(135deg, #F59E0B, #D97706);
  color: white;
  border: none;
  padding: 14px 24px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.btn-save:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
}

/* Print Modal */
.print-modal {
  background: white;
  border-radius: 20px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.print-header {
  background: linear-gradient(135deg, #14B8A6, #0D9488);
  color: white;
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 20px 20px 0 0;
}

.certificate-content {
  padding: 40px;
  overflow-y: auto;
}

.certificate-border {
  border: 8px double #F59E0B;
  padding: 40px;
}

.clinic-header {
  text-align: center;
  border-bottom: 4px solid #F59E0B;
  padding-bottom: 20px;
  margin-bottom: 30px;
}

.clinic-header h1 {
  margin: 0 0 10px 0;
  font-size: 32px;
  color: #1F2937;
}

.certificate-title {
  text-align: center;
  margin-bottom: 30px;
}

.certificate-title h2 {
  margin: 0 0 10px 0;
  font-size: 28px;
  color: #F59E0B;
}

.patient-section, .vaccination-section {
  margin-bottom: 30px;
}

.patient-section h3, .vaccination-section h3 {
  background: #FEF3C7;
  padding: 10px 20px;
  margin: 0 0 15px 0;
  border-radius: 8px;
  color: #92400E;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.info-grid div span {
  color: #6B7280;
}

.cert-table {
  width: 100%;
  border: 2px solid #E5E7EB;
}

.cert-table tr {
  border-bottom: 1px solid #E5E7EB;
}

.cert-table td {
  padding: 12px 20px;
}

.cert-table td:first-child {
  background: #FEF3C7;
  font-weight: 600;
  color: #92400E;
  width: 40%;
}

.signature-section {
  margin-top: 50px;
  display: flex;
  justify-content: flex-end;
}

.signature-line {
  border-top: 2px solid #1F2937;
  padding-top: 10px;
  min-width: 200px;
  text-align: center;
}

.signature-line p {
  margin: 5px 0;
  color: #1F2937;
}

.print-actions {
  padding: 20px;
  background: #F9FAFB;
  display: flex;
  gap: 12px;
  border-radius: 0 0 20px 20px;
}

.btn-print-action {
  flex: 2;
  background: linear-gradient(135deg, #14B8A6, #0D9488);
  color: white;
  border: none;
  padding: 14px 24px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-print-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(20, 184, 166, 0.4);
}

@media print {
  body * { visibility: hidden; }
  #printable-certificate, #printable-certificate * { visibility: visible; }
  #printable-certificate { position: absolute; left: 0; top: 0; }
}

@media (max-width: 768px) {
  .vaccinations-wrapper {
    padding: 16px;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>