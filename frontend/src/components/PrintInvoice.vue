<template>
  <div id="invoice-print-area" class="invoice-print-container">
    <div class="invoice-page">
      <!-- Header -->
      <div class="header">
        <h1>SRI ADITHYA PET CLINIC</h1>
        <p>Main Road, Cumbum, Tamil Nadu - 625516</p>
        <p>Phone: +91 94433 55667 | GSTIN: 33XXXXX1234X1ZX</p>
        <hr>
        <h2>INVOICE</h2>
      </div>

      <!-- Invoice Meta -->
      <div class="invoice-meta">
        <div>
          <p><strong>Invoice No:</strong> {{ payment.id ? payment.id.substring(0, 8).toUpperCase() : 'N/A' }}</p>
          <p><strong>Date:</strong> {{ formatDate(payment.payment_date) }}</p>
        </div>
        <div style="text-align: right;">
          <p><strong>Visit ID:</strong> {{ consultation?.id ? consultation.id.substring(0, 8).toUpperCase() : 'N/A' }}</p>
          <p><strong>Payment Status:</strong> {{ payment.payment_status ? payment.payment_status.toUpperCase() : 'N/A' }}</p>
        </div>
      </div>

      <!-- Client Details -->
      <div class="client-section">
        <p><strong>Bill To:</strong></p>
        <p>{{ ownerDetails?.name || 'N/A' }}</p>
        <p>Phone: {{ ownerDetails?.phone || 'N/A' }}</p>
        <p v-if="ownerDetails?.address">{{ ownerDetails.address }}</p>
      </div>

      <!-- Pet Details -->
      <div class="pet-details">
        <p><strong>Patient:</strong> {{ payment.patient_name || 'N/A' }} ({{ patientDetails?.species || 'N/A' }})</p>
      </div>

      <!-- Bill Items -->
      <table class="bill-table">
        <thead>
          <tr>
            <th>S.No</th>
            <th>Description</th>
            <th class="amount">Amount (₹)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="payment.consultation_fee > 0">
            <td>1</td>
            <td>Consultation Fee</td>
            <td class="amount">{{ payment.consultation_fee.toFixed(2) }}</td>
          </tr>
          <tr v-if="payment.medication_cost > 0">
            <td>2</td>
            <td>Medication Charges</td>
            <td class="amount">{{ payment.medication_cost.toFixed(2) }}</td>
          </tr>
          <tr v-if="payment.lab_cost > 0">
            <td>3</td>
            <td>Laboratory Tests</td>
            <td class="amount">{{ payment.lab_cost.toFixed(2) }}</td>
          </tr>
          <tr v-if="payment.other_charges > 0">
            <td>4</td>
            <td>Other Charges</td>
            <td class="amount">{{ payment.other_charges.toFixed(2) }}</td>
          </tr>
        </tbody>
        <tfoot>
          <tr class="subtotal">
            <td colspan="2"><strong>Subtotal</strong></td>
            <td class="amount"><strong>{{ subtotal.toFixed(2) }}</strong></td>
          </tr>
          <tr v-if="payment.discount > 0" class="discount">
            <td colspan="2">Discount</td>
            <td class="amount">-{{ payment.discount.toFixed(2) }}</td>
          </tr>
          <tr class="total">
            <td colspan="2"><strong>TOTAL</strong></td>
            <td class="amount"><strong>₹{{ payment.amount.toFixed(2) }}</strong></td>
          </tr>
        </tfoot>
      </table>

      <!-- Payment Info -->
      <div class="payment-info">
        <p><strong>Payment Method:</strong> {{ payment.payment_method ? payment.payment_method.toUpperCase() : 'N/A' }}</p>
        <p v-if="payment.transaction_id"><strong>Transaction ID:</strong> {{ payment.transaction_id }}</p>
      </div>

      <!-- Footer -->
      <div class="footer">
        <p><strong>Thank you for visiting Sri Adithya Pet Clinic!</strong></p>
        <p style="font-size: 9pt;">For any queries, contact us at sriadithyapetclinic@gmail.com</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  payment: {
    type: Object,
    required: true
  },
  consultation: {
    type: Object,
    default: null
  },
  patientDetails: {
    type: Object,
    required: true
  },
  ownerDetails: {
    type: Object,
    required: true
  }
});

const subtotal = computed(() => {
  return (
    parseFloat(props.payment.consultation_fee || 0) +
    parseFloat(props.payment.medication_cost || 0) +
    parseFloat(props.payment.lab_cost || 0) +
    parseFloat(props.payment.other_charges || 0)
  );
});

const formatDate = (date) => {
  if (!date) return 'N/A';
  return new Date(date).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });
};
</script>

<style scoped>
/* Screen: Hide completely */
.invoice-print-container {
  display: none;
}

/* Print: Show only this component */
@media print {
  /* Step 1: Hide everything on the page */
  body * {
    visibility: hidden !important;
  }
  
  /* Step 2: Make ONLY this component and its children visible */
  #invoice-print-area,
  #invoice-print-area * {
    visibility: visible !important;
  }
  
  /* Step 3: Position it at top-left of page */
  #invoice-print-area {
    position: absolute !important;
    left: 0 !important;
    top: 0 !important;
    width: 100% !important;
    display: block !important;
  }
  
  /* Remove any background colors from body */
  body {
    background: white !important;
  }
}

.invoice-page {
  width: 210mm;
  min-height: 297mm;
  padding: 20mm;
  margin: 0 auto;
  background: white;
  font-family: Arial, sans-serif;
  color: black;
  font-size: 11pt;
}

.header {
  text-align: center;
  border-bottom: 2px solid black;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.header h1 {
  font-size: 18pt;
  margin: 0;
}

.header h2 {
  font-size: 16pt;
  margin-top: 10px;
}

.invoice-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.client-section,
.pet-details {
  margin: 15px 0;
}

.bill-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

.bill-table th,
.bill-table td {
  border: 1px solid #000;
  padding: 10px;
  text-align: left;
}

.bill-table th {
  background: #000;
  color: white;
}

.amount {
  text-align: right !important;
  width: 150px;
}

.subtotal td {
  border-top: 2px solid #000;
}

.total td {
  background: #f0f0f0;
  border-top: 2px solid #000;
  font-size: 13pt;
}

.payment-info {
  margin: 20px 0;
  padding: 10px;
  background: #f9f9f9;
}

.footer {
  margin-top: 40px;
  text-align: center;
  border-top: 1px solid #ccc;
  padding-top: 10px;
}

@page {
  size: A4;
  margin: 0;
}
</style>