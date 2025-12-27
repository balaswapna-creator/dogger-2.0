<template>
  <div class="payments-wrapper">
    <!-- Header Card -->
    <div class="header-card">
      <div class="header-content">
        <div class="header-title">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
            <line x1="1" y1="10" x2="23" y2="10"></line>
          </svg>
          <h1>Payments</h1>
        </div>
        <button @click="openAddModal" class="btn-add">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          <span>New Payment</span>
        </button>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="stat-card paid">
        <div class="stat-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Total Paid</p>
          <h3>₹{{ stats.totalPaid }}</h3>
        </div>
      </div>

      <div class="stat-card pending">
        <div class="stat-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Pending</p>
          <h3>₹{{ stats.pending }}</h3>
        </div>
      </div>

      <div class="stat-card failed">
        <div class="stat-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Failed</p>
          <h3>₹{{ stats.failed }}</h3>
        </div>
      </div>

      <div class="stat-card total">
        <div class="stat-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="1" x2="12" y2="23"></line>
            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">Total</p>
          <h3>₹{{ stats.total }}</h3>
        </div>
      </div>
    </div>

    <!-- Payments Table -->
    <div class="table-card">
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Patient</th>
              <th>Amount</th>
              <th>Method</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="payment in payments" :key="payment.id">
              <td>{{ formatDate(payment.created_at) }}</td>
              <td>
                <div class="patient-info">
                  <div class="patient-avatar">{{ getPatientName(payment.patient).charAt(0) }}</div>
                  <span>{{ getPatientName(payment.patient) }}</span>
                </div>
              </td>
              <td>
                <span class="amount">₹{{ payment.amount }}</span>
              </td>
              <td>
                <span class="method-badge" :class="'method-' + payment.payment_method">
                  {{ formatMethod(payment.payment_method) }}
                </span>
              </td>
              <td>
                <span class="status-badge" :class="'status-' + payment.payment_status">
                  {{ formatStatus(payment.payment_status) }}
                </span>
              </td>
              <td>
                <div class="action-buttons">
                  <button @click="openEditModal(payment)" class="btn-edit" title="Edit">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                  </button>
                  <button @click="printInvoice(payment)" class="btn-print" title="Print Invoice">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="6 9 6 2 18 2 18 9"></polyline>
                      <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                      <rect x="6" y="14" width="12" height="8"></rect>
                    </svg>
                  </button>
                  <button @click="deletePayment(payment.id)" class="btn-delete" title="Delete">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="payments.length === 0">
              <td colspan="6" class="no-data">
                <div class="empty-state">
                  <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
                    <line x1="1" y1="10" x2="23" y2="10"></line>
                  </svg>
                  <p>No payments recorded yet</p>
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
          <h2>{{ isEditing ? 'Edit Payment' : 'New Payment' }}</h2>
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

            <div class="form-group">
              <label>Consultation Fee (₹)</label>
              <input v-model.number="form.consultation_fee" type="number" placeholder="0"/>
            </div>

            <div class="form-group">
              <label>Medication Cost (₹)</label>
              <input v-model.number="form.medication_cost" type="number" placeholder="0"/>
            </div>

            <div class="form-group">
              <label>Lab Cost (₹)</label>
              <input v-model.number="form.lab_cost" type="number" placeholder="0"/>
            </div>

            <div class="form-group">
              <label>Other Charges (₹)</label>
              <input v-model.number="form.other_charges" type="number" placeholder="0"/>
            </div>

            <div class="form-group">
              <label>Discount (₹)</label>
              <input v-model.number="form.discount" type="number" placeholder="0"/>
            </div>

            <div class="form-group full-width">
              <div class="total-display">
                <span>Total Amount:</span>
                <h3>₹{{ calculateTotal() }}</h3>
              </div>
            </div>

            <div class="form-group">
              <label>Payment Method *</label>
              <select v-model="form.payment_method">
                <option value="cash">Cash</option>
                <option value="card">Card</option>
                <option value="upi">UPI</option>
                <option value="bank_transfer">Bank Transfer</option>
              </select>
            </div>

            <div class="form-group">
              <label>Payment Status *</label>
              <select v-model="form.payment_status">
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
                <option value="failed">Failed</option>
                <option value="refunded">Refunded</option>
              </select>
            </div>

            <div class="form-group full-width">
              <label>Transaction ID</label>
              <input v-model="form.transaction_id" type="text" placeholder="Optional"/>
            </div>
          </div>

          <div class="modal-actions">
            <button @click="closeModal" class="btn-cancel">Cancel</button>
            <button @click="savePayment" class="btn-save">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                <polyline points="17 21 17 13 7 13 7 21"></polyline>
                <polyline points="7 3 7 8 15 8"></polyline>
              </svg>
              {{ isEditing ? 'Update' : 'Save' }} Payment
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Print Invoice Modal -->
    <div v-if="showPrintModal && printData" class="modal-overlay">
      <div class="print-modal">
        <div class="print-header">
          <h2>Invoice</h2>
          <button @click="closePrintModal" class="btn-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div id="printable-invoice" class="invoice-content">
          <div class="clinic-header">
            <h1>Sri Adithya Pet Clinic</h1>
            <p>Dr. A. Balasubramanan, B.V.Sc, MBA</p>
            <p>Main Road, Cumbum, Tamil Nadu - 625516</p>
          </div>

          <div class="invoice-details">
            <div class="bill-to">
              <h3>Bill To:</h3>
              <p><strong>{{ printData.owner?.name }}</strong></p>
              <p>{{ printData.owner?.phone }}</p>
              <p>{{ printData.owner?.address }}</p>
            </div>
            <div class="invoice-info">
              <h3>Invoice Details:</h3>
              <p><strong>Patient:</strong> {{ printData.patient?.pet_name }}</p>
              <p><strong>Species:</strong> {{ printData.patient?.species }}</p>
              <p><strong>Date:</strong> {{ formatDate(printData.payment?.created_at) }}</p>
            </div>
          </div>

          <table class="invoice-table">
            <thead>
              <tr>
                <th>Description</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="printData.payment?.consultation_fee > 0">
                <td>Consultation Fee</td>
                <td>₹{{ printData.payment.consultation_fee }}</td>
              </tr>
              <tr v-if="printData.payment?.medication_cost > 0">
                <td>Medication</td>
                <td>₹{{ printData.payment.medication_cost }}</td>
              </tr>
              <tr v-if="printData.payment?.lab_cost > 0">
                <td>Lab Tests</td>
                <td>₹{{ printData.payment.lab_cost }}</td>
              </tr>
              <tr v-if="printData.payment?.other_charges > 0">
                <td>Other Charges</td>
                <td>₹{{ printData.payment.other_charges }}</td>
              </tr>
              <tr v-if="printData.payment?.discount > 0" class="discount-row">
                <td>Discount</td>
                <td>-₹{{ printData.payment.discount }}</td>
              </tr>
              <tr class="total-row">
                <td><strong>TOTAL</strong></td>
                <td><strong>₹{{ printData.payment?.amount }}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="print-actions">
          <button @click="triggerPrint" class="btn-print-action">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 6 2 18 2 18 9"></polyline>
              <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
              <rect x="6" y="14" width="12" height="8"></rect>
            </svg>
            Print Invoice
          </button>
          <button @click="closePrintModal" class="btn-cancel">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../services/api';

const payments = ref([]);
const patients = ref([]);
const showModal = ref(false);
const isEditing = ref(false);
const editingPaymentId = ref(null);
const showPrintModal = ref(false);
const printData = ref(null);

const form = ref({
  patient: '',
  consultation_fee: 0,
  medication_cost: 0,
  lab_cost: 0,
  other_charges: 0,
  discount: 0,
  payment_method: 'cash',
  payment_status: 'completed',
  transaction_id: ''
});

const stats = computed(() => {
  const totalPaid = payments.value.filter(p => p.payment_status === 'completed').reduce((sum, p) => sum + (p.amount || 0), 0);
  const pending = payments.value.filter(p => p.payment_status === 'pending').reduce((sum, p) => sum + (p.amount || 0), 0);
  const failed = payments.value.filter(p => p.payment_status === 'failed').reduce((sum, p) => sum + (p.amount || 0), 0);
  const total = payments.value.reduce((sum, p) => sum + (p.amount || 0), 0);
  return { totalPaid, pending, failed, total };
});

const getPatientName = (id) => patients.value.find(p => p.id === id)?.pet_name || 'Unknown';

const formatDate = (d) => {
  if (!d) return 'N/A';
  return new Date(d).toLocaleDateString('en-IN');
};

const formatMethod = (method) => {
  const methods = { cash: 'Cash', card: 'Card', upi: 'UPI', bank_transfer: 'Bank Transfer' };
  return methods[method] || method;
};

const formatStatus = (status) => {
  const statuses = { completed: 'Completed', pending: 'Pending', failed: 'Failed', refunded: 'Refunded' };
  return statuses[status] || status;
};

const calculateTotal = () => {
  return Math.max(0, (form.value.consultation_fee || 0) + (form.value.medication_cost || 0) + 
    (form.value.lab_cost || 0) + (form.value.other_charges || 0) - (form.value.discount || 0));
};

const fetchData = async () => {
  try {
    const [p, pt] = await Promise.all([api.get('/payments/'), api.get('/patients/')]);
    payments.value = p.data.results || p.data;
    patients.value = pt.data.results || pt.data;
  } catch (error) {
    console.error('Error:', error);
  }
};

const openAddModal = () => {
  isEditing.value = false;
  editingPaymentId.value = null;
  form.value = {
    patient: '',
    consultation_fee: 0,
    medication_cost: 0,
    lab_cost: 0,
    other_charges: 0,
    discount: 0,
    payment_method: 'cash',
    payment_status: 'completed',
    transaction_id: ''
  };
  showModal.value = true;
};

const openEditModal = (payment) => {
  isEditing.value = true;
  editingPaymentId.value = payment.id;
  form.value = {
    patient: payment.patient,
    consultation_fee: payment.consultation_fee || 0,
    medication_cost: payment.medication_cost || 0,
    lab_cost: payment.lab_cost || 0,
    other_charges: payment.other_charges || 0,
    discount: payment.discount || 0,
    payment_method: payment.payment_method,
    payment_status: payment.payment_status,
    transaction_id: payment.transaction_id || ''
  };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  isEditing.value = false;
  editingPaymentId.value = null;
};

const savePayment = async () => {
  if (!form.value.patient) {
    alert('Please select a patient');
    return;
  }
  
  try {
    const amount = calculateTotal();
    const data = { ...form.value, amount };
    
    if (isEditing.value) {
      await api.put(`/payments/${editingPaymentId.value}/`, data);
      alert('Payment updated!');
    } else {
      await api.post('/payments/', data);
      alert('Payment created!');
    }
    
    closeModal();
    await fetchData();
  } catch (error) {
    console.error('Error:', error);
    alert('Failed to save payment');
  }
};

const deletePayment = async (id) => {
  if (!confirm('Delete this payment?')) return;
  try {
    await api.delete(`/payments/${id}/`);
    alert('Payment deleted!');
    fetchData();
  } catch (error) {
    console.error('Error:', error);
  }
};

const printInvoice = async (payment) => {
  try {
    const pt = await api.get(`/patients/${payment.patient}/`);
    const ow = await api.get(`/owners/${pt.data.owner}/`);
    printData.value = { payment, patient: pt.data, owner: ow.data };
    showPrintModal.value = true;
  } catch (error) {
    alert('Failed to load invoice data');
  }
};

const triggerPrint = () => window.print();
const closePrintModal = () => { showPrintModal.value = false; printData.value = null; };

onMounted(() => fetchData());
</script>

<style scoped>
.payments-wrapper {
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
  color: #10B981;
}

.header-title h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1F2937;
}

.btn-add {
  background: linear-gradient(135deg, #10B981, #059669);
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
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
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
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-card.paid .stat-icon {
  background: linear-gradient(135deg, #10B981, #059669);
}

.stat-card.pending .stat-icon {
  background: linear-gradient(135deg, #F59E0B, #D97706);
}

.stat-card.failed .stat-icon {
  background: linear-gradient(135deg, #EF4444, #DC2626);
}

.stat-card.total .stat-icon {
  background: linear-gradient(135deg, #3B82F6, #2563EB);
}

.stat-content {
  flex: 1;
}

.stat-label {
  margin: 0 0 4px 0;
  color: #6B7280;
  font-size: 14px;
  font-weight: 500;
}

.stat-content h3 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #1F2937;
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
  background: linear-gradient(135deg, #10B981, #059669);
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
  background: linear-gradient(135deg, #10B981, #059669);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
}

.amount {
  font-size: 18px;
  font-weight: 700;
  color: #10B981;
}

.method-badge {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
}

.method-cash {
  background: #D1FAE5;
  color: #065F46;
}

.method-card {
  background: #DBEAFE;
  color: #1E40AF;
}

.method-upi {
  background: #E9D5FF;
  color: #6B21A8;
}

.method-bank_transfer {
  background: #FEF3C7;
  color: #92400E;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
}

.status-completed {
  background: #D1FAE5;
  color: #065F46;
}

.status-pending {
  background: #FED7AA;
  color: #92400E;
}

.status-failed {
  background: #FEE2E2;
  color: #991B1B;
}

.status-refunded {
  background: #E0E7FF;
  color: #3730A3;
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
  color: #10B981;
}

.btn-edit:hover {
  background: #D1FAE5;
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
overflow-y: auto;
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
background: linear-gradient(135deg, #10B981, #059669);
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
.form-group select {
padding: 12px 16px;
border: 2px solid #E5E7EB;
border-radius: 10px;
font-size: 15px;
color: #1F2937;
transition: all 0.3s;
font-family: inherit;
}
.form-group input:focus,
.form-group select:focus {
outline: none;
border-color: #10B981;
box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}
.total-display {
background: #ECFDF5;
border: 2px solid #10B981;
border-radius: 12px;
padding: 16px 20px;
display: flex;
justify-content: space-between;
align-items: center;
}
.total-display span {
font-size: 16px;
color: #065F46;
font-weight: 600;
}
.total-display h3 {
margin: 0;
font-size: 28px;
color: #10B981;
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
background: linear-gradient(135deg, #10B981, #059669);
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
box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}
.btn-save:hover {
transform: translateY(-2px);
box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
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
.invoice-content {
padding: 40px;
overflow-y: auto;
}
.clinic-header {
text-align: center;
border-bottom: 4px solid #10B981;
padding-bottom: 20px;
margin-bottom: 30px;
}
.clinic-header h1 {
margin: 0 0 10px 0;
font-size: 32px;
color: #1F2937;
}
.invoice-details {
display: grid;
grid-template-columns: 1fr 1fr;
gap: 30px;
margin-bottom: 30px;
}
.invoice-details h3 {
margin: 0 0 10px 0;
color: #10B981;
}
.invoice-details p {
margin: 5px 0;
color: #374151;
}
.invoice-table {
width: 100%;
border: 2px solid #E5E7EB;
margin-bottom: 30px;
}
.invoice-table thead {
background: #10B981;
color: white;
}
.invoice-table th, .invoice-table td {
padding: 12px 20px;
text-align: left;
}
.invoice-table tbody tr {
border-bottom: 1px solid #E5E7EB;
}
.invoice-table td:last-child {
text-align: right;
}
.discount-row {
color: #EF4444;
}
.total-row {
background: #ECFDF5;
font-size: 18px;
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
#printable-invoice, #printable-invoice * { visibility: visible; }
#printable-invoice { position: absolute; left: 0; top: 0; }
}
@media (max-width: 768px) {
.payments-wrapper {
padding: 16px;
}
.stats-grid {
grid-template-columns: 1fr;
}
.form-grid {
grid-template-columns: 1fr;
}
.invoice-details {
grid-template-columns: 1fr;

}

}
</style>