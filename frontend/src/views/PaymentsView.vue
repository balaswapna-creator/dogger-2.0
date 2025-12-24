<template>
  <div class="min-h-screen bg-gradient-to-br from-emerald-900 via-emerald-700 to-emerald-800 p-6">
    <div class="bg-white rounded-xl shadow-lg p-6">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-emerald-700">💰 Payments</h1>
        <button @click="openAddModal" class="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-lg font-semibold">
          ➕ New Payment
        </button>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-4 gap-4 mb-6">
        <div class="bg-green-100 p-4 rounded-lg border-2 border-green-300">
          <p class="text-sm text-green-700">Total Paid</p>
          <p class="text-2xl font-bold text-green-800">₹{{ stats.totalPaid }}</p>
        </div>
        <div class="bg-orange-100 p-4 rounded-lg border-2 border-orange-300">
          <p class="text-sm text-orange-700">Pending</p>
          <p class="text-2xl font-bold text-orange-800">₹{{ stats.pending }}</p>
        </div>
        <div class="bg-red-100 p-4 rounded-lg border-2 border-red-300">
          <p class="text-sm text-red-700">Failed</p>
          <p class="text-2xl font-bold text-red-800">₹{{ stats.failed }}</p>
        </div>
        <div class="bg-blue-100 p-4 rounded-lg border-2 border-blue-300">
          <p class="text-sm text-blue-700">Total</p>
          <p class="text-2xl font-bold text-blue-800">₹{{ stats.total }}</p>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-emerald-100">
            <tr>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Date</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Patient</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Amount</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Method</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Status</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-emerald-800">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="payment in payments" :key="payment.id" class="hover:bg-gray-50">
              <td class="px-4 py-3">{{ formatDate(payment.created_at) }}</td>
              <td class="px-4 py-3 font-semibold">{{ getPatientName(payment.patient) }}</td>
              <td class="px-4 py-3 font-bold text-lg">₹{{ payment.amount }}</td>
              <td class="px-4 py-3">
                <span :class="getMethodBadge(payment.payment_method)" class="px-2 py-1 rounded text-xs">
                  {{ payment.payment_method }}
                </span>
              </td>
              <td class="px-4 py-3">
                <span :class="getStatusBadge(payment.payment_status)" class="px-2 py-1 rounded text-xs">
                  {{ payment.payment_status }}
                </span>
              </td>
              <td class="px-4 py-3">
                <div class="flex gap-2">
                  <button @click="openEditModal(payment)" class="bg-amber-500 hover:bg-amber-600 text-white px-2 py-1 rounded text-sm">✏️</button>
                  <button @click="printInvoice(payment)" class="bg-teal-500 hover:bg-teal-600 text-white px-2 py-1 rounded text-sm">🖨️</button>
                  <button @click="deletePayment(payment.id)" class="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-sm">🗑️</button>
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
          <h2 class="text-2xl font-bold">{{ isEditing ? 'Edit Payment' : 'New Payment' }}</h2>
        </div>
        
        <div class="p-6 space-y-4">
          <!-- Patient Selection -->
          <div>
            <label class="block font-semibold text-gray-700 mb-2">Patient * (Required)</label>
            <select v-model="form.patient" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg">
              <option value="">-- Select Patient --</option>
              <option v-for="patient in patients" :key="patient.id" :value="patient.id">
                {{ patient.pet_name }} ({{ patient.species }})
              </option>
            </select>
          </div>

          <!-- Charges -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block font-semibold text-gray-700 mb-2">Consultation Fee (₹)</label>
              <input v-model.number="form.consultation_fee" type="number" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" placeholder="0" />
            </div>
            <div>
              <label class="block font-semibold text-gray-700 mb-2">Medication Cost (₹)</label>
              <input v-model.number="form.medication_cost" type="number" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" placeholder="0" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block font-semibold text-gray-700 mb-2">Lab Cost (₹)</label>
              <input v-model.number="form.lab_cost" type="number" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" placeholder="0" />
            </div>
            <div>
              <label class="block font-semibold text-gray-700 mb-2">Other Charges (₹)</label>
              <input v-model.number="form.other_charges" type="number" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" placeholder="0" />
            </div>
          </div>

          <div>
            <label class="block font-semibold text-gray-700 mb-2">Discount (₹)</label>
            <input v-model.number="form.discount" type="number" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" placeholder="0" />
          </div>

          <!-- Total -->
          <div class="bg-emerald-50 p-4 rounded-lg border-2 border-emerald-300">
            <p class="text-emerald-900 font-semibold">Total Amount: <span class="text-2xl">₹{{ calculateTotal() }}</span></p>
          </div>

          <!-- Payment Details -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block font-semibold text-gray-700 mb-2">Payment Method * (Required)</label>
              <select v-model="form.payment_method" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg">
                <option value="cash">Cash</option>
                <option value="card">Card</option>
                <option value="upi">UPI</option>
                <option value="bank_transfer">Bank Transfer</option>
              </select>
            </div>
            <div>
              <label class="block font-semibold text-gray-700 mb-2">Payment Status * (Required)</label>
              <select v-model="form.payment_status" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg">
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
                <option value="failed">Failed</option>
                <option value="refunded">Refunded</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block font-semibold text-gray-700 mb-2">Transaction ID</label>
            <input v-model="form.transaction_id" type="text" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" placeholder="Optional" />
          </div>

          <!-- Actions -->
          <div class="flex gap-3 pt-4">
            <button @click="savePayment" class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white py-3 rounded-lg font-semibold">
              💾 {{ isEditing ? 'Update' : 'Save' }} Payment
            </button>
            <button @click="closeModal" class="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-3 rounded-lg font-semibold">
              ✖️ Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Print Invoice Modal -->
    <div v-if="showPrintModal && printData" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="bg-teal-600 text-white p-6 flex justify-between items-center">
          <h2 class="text-2xl font-bold">Invoice</h2>
          <button @click="closePrintModal" class="text-white hover:bg-white/20 p-2 rounded">✖️</button>
        </div>
        
        <div id="printable-invoice" class="p-8">
          <div class="text-center mb-6 border-b-4 border-emerald-600 pb-4">
            <h1 class="text-3xl font-bold text-emerald-900">Sri Adithya Pet Clinic</h1>
            <p class="text-gray-700">Dr. A. Balasubramanian, B.V.Sc, MBA</p>
            <p class="text-gray-600">Main Road, Cumbum, Tamil Nadu - 625516</p>
          </div>

          <div class="grid grid-cols-2 gap-4 mb-6">
            <div>
              <h3 class="font-bold text-gray-900 mb-2">Bill To:</h3>
              <p class="font-bold">{{ printData.owner?.name }}</p>
              <p>{{ printData.owner?.phone }}</p>
              <p>{{ printData.owner?.address }}</p>
            </div>
            <div>
              <h3 class="font-bold text-gray-900 mb-2">Patient:</h3>
              <p class="font-bold">{{ printData.patient?.pet_name }}</p>
              <p>{{ printData.patient?.species }} / {{ printData.patient?.breed }}</p>
              <p>{{ formatDate(printData.payment?.created_at) }}</p>
            </div>
          </div>

          <table class="w-full border-2 border-gray-300 mb-6">
            <thead>
              <tr class="bg-emerald-600 text-white">
                <th class="border px-4 py-2 text-left">Description</th>
                <th class="border px-4 py-2 text-right">Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="printData.payment?.consultation_fee > 0">
                <td class="border px-4 py-2">Consultation Fee</td>
                <td class="border px-4 py-2 text-right">₹{{ printData.payment.consultation_fee }}</td>
              </tr>
              <tr v-if="printData.payment?.medication_cost > 0">
                <td class="border px-4 py-2">Medication</td>
                <td class="border px-4 py-2 text-right">₹{{ printData.payment.medication_cost }}</td>
              </tr>
              <tr v-if="printData.payment?.lab_cost > 0">
                <td class="border px-4 py-2">Lab Tests</td>
                <td class="border px-4 py-2 text-right">₹{{ printData.payment.lab_cost }}</td>
              </tr>
              <tr v-if="printData.payment?.other_charges > 0">
                <td class="border px-4 py-2">Other Charges</td>
                <td class="border px-4 py-2 text-right">₹{{ printData.payment.other_charges }}</td>
              </tr>
              <tr v-if="printData.payment?.discount > 0">
                <td class="border px-4 py-2 text-red-600">Discount</td>
                <td class="border px-4 py-2 text-right text-red-600">-₹{{ printData.payment.discount }}</td>
              </tr>
              <tr class="bg-emerald-100">
                <td class="border px-4 py-2 font-bold">TOTAL</td>
                <td class="border px-4 py-2 text-right font-bold text-lg">₹{{ printData.payment?.amount }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="p-6 bg-gray-50 flex gap-3">
          <button @click="triggerPrint" class="flex-1 bg-teal-600 hover:bg-teal-700 text-white py-3 rounded-lg font-semibold">
            🖨️ Print Invoice
          </button>
          <button @click="closePrintModal" class="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-3 rounded-lg font-semibold">
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
const getMethodBadge = (m) => ({'cash':'bg-green-100 text-green-800','card':'bg-blue-100 text-blue-800','upi':'bg-purple-100 text-purple-800'}[m] || 'bg-gray-100');
const getStatusBadge = (s) => ({'completed':'bg-green-100 text-green-800','pending':'bg-orange-100 text-orange-800','failed':'bg-red-100 text-red-800'}[s] || 'bg-gray-100');
const formatDate = (d) => d ? new Date(d).toLocaleDateString('en-IN') : 'N/A';

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
    alert('❌ Please select a patient');
    return;
  }
  
  try {
    const amount = calculateTotal();
    const data = { ...form.value, amount };
    
    if (isEditing.value) {
      await api.put(`/payments/${editingPaymentId.value}/`, data);
      alert('✅ Payment updated!');
    } else {
      await api.post('/payments/', data);
      alert('✅ Payment created!');
    }
    
    closeModal();
    await fetchData();
  } catch (error) {
    console.error('❌ Error:', error);
    alert('❌ Failed to save payment');
  }
};

const deletePayment = async (id) => {
  if (!confirm('Delete this payment?')) return;
  try {
    await api.delete(`/payments/${id}/`);
    alert('✅ Payment deleted!');
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
@media print {
  body * { visibility: hidden; }
  #printable-invoice, #printable-invoice * { visibility: visible; }
  #printable-invoice { position: absolute; left: 0; top: 0; }
}
</style>