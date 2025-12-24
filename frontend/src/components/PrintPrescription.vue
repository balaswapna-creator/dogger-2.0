<template>
  <div id="prescription-print-area" class="prescription-print-container">
    <div class="prescription-page">
      <!-- Header -->
      <div class="header">
        <h1>SRI ADITHYA PET CLINIC</h1>
        <p>Main Road, Cumbum, Tamil Nadu - 625516</p>
        <p>Phone: +91 94433 55667</p>
        <hr>
        <h2>℞ PRESCRIPTION</h2>
      </div>

      <!-- Date & Visit ID -->
      <div class="meta">
        <p><strong>Date:</strong> {{ formatDate(consultation.visit_date) }}</p>
        <p><strong>Visit ID:</strong> {{ consultation.id ? consultation.id.substring(0, 8).toUpperCase() : 'N/A' }}</p>
      </div>

      <!-- Patient Details -->
      <div class="patient-section">
        <table class="info-table">
          <tbody>
            <tr>
              <td><strong>Pet Name:</strong></td>
              <td>{{ consultation.patient_name }}</td>
              <td><strong>Species:</strong></td>
              <td>{{ patientDetails?.species || 'N/A' }}</td>
            </tr>
            <tr>
              <td><strong>Owner:</strong></td>
              <td>{{ ownerDetails?.name || 'N/A' }}</td>
              <td><strong>Phone:</strong></td>
              <td>{{ ownerDetails?.phone || 'N/A' }}</td>
            </tr>
            <tr>
              <td><strong>Weight:</strong></td>
              <td>{{ consultation.weight ? consultation.weight + ' kg' : 'N/A' }}</td>
              <td><strong>Temperature:</strong></td>
              <td>{{ consultation.temperature ? consultation.temperature + '°F' : 'N/A' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Diagnosis -->
      <div class="diagnosis-section">
        <p><strong>Diagnosis:</strong> {{ consultation.diagnosis || 'N/A' }}</p>
      </div>

      <!-- Prescriptions -->
      <div class="rx-section">
        <table class="rx-table">
          <thead>
            <tr>
              <th>S.No</th>
              <th>Medicine</th>
              <th>Dosage</th>
              <th>Frequency</th>
              <th>Duration</th>
              <th>Instructions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(rx, index) in prescriptions" :key="rx.id || index">
              <td>{{ index + 1 }}</td>
              <td>{{ rx.medication_name }}</td>
              <td>{{ rx.dosage }}</td>
              <td>{{ rx.frequency }}</td>
              <td>{{ rx.duration }}</td>
              <td>{{ rx.instructions || '-' }}</td>
            </tr>
            <tr v-if="!prescriptions || prescriptions.length === 0">
              <td colspan="6" style="text-align: center;">No prescriptions available</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Additional Notes -->
      <div class="notes" v-if="consultation.treatment_plan">
        <p><strong>Treatment Plan:</strong></p>
        <p>{{ consultation.treatment_plan }}</p>
      </div>

      <!-- Footer -->
      <div class="footer">
        <div class="doctor-signature">
          <p>_________________________</p>
          <p><strong>Dr. Veterinarian</strong></p>
          <p>Veterinary Surgeon</p>
          <p>Reg. No: TNVCI/12345</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  consultation: {
    type: Object,
    required: true
  },
  prescriptions: {
    type: Array,
    default: () => []
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
.prescription-print-container {
  display: none;
}

/* Print: Show only this component */
@media print {
  /* Step 1: Hide everything on the page */
  body * {
    visibility: hidden !important;
  }
  
  /* Step 2: Make ONLY this component and its children visible */
  #prescription-print-area,
  #prescription-print-area * {
    visibility: visible !important;
  }
  
  /* Step 3: Position it at top-left of page */
  #prescription-print-area {
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

.prescription-page {
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

.meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.info-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 15px;
}

.info-table td {
  padding: 5px;
  border: 1px solid #ccc;
}

.info-table td:nth-child(odd) {
  background: #f0f0f0;
  width: 25%;
}

.diagnosis-section {
  margin: 15px 0;
  padding: 10px;
  background: #f9f9f9;
  border-left: 4px solid #000;
}

.rx-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

.rx-table th,
.rx-table td {
  border: 1px solid #000;
  padding: 8px;
  text-align: left;
}

.rx-table th {
  background: #000;
  color: white;
  font-weight: bold;
}

.notes {
  margin: 20px 0;
  padding: 10px;
  border: 1px dashed #000;
}

.footer {
  margin-top: 60px;
}

.doctor-signature {
  float: right;
  text-align: center;
}

.doctor-signature p {
  margin: 5px 0;
}

@page {
  size: A4;
  margin: 0;
}
</style>