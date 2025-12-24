<template>
  <div id="vaccination-print-area" class="vaccination-print-container">
    <div class="certificate-page">
      <!-- Header -->
      <div class="header">
        <h1>SRI ADITHYA PET CLINIC</h1>
        <p>Main Road, Cumbum, Tamil Nadu - 625516</p>
        <p>Phone: +91 94433 55667 | Email: sriadithyapetclinic@gmail.com</p>
        <hr>
        <h2>VACCINATION CERTIFICATE</h2>
      </div>

      <!-- Certificate Number -->
      <div class="cert-number">
        <strong>Certificate No:</strong> {{ vaccination.certificate_number }}
      </div>

      <!-- Pet & Owner Details -->
      <div class="details-section">
        <table class="details-table">
          <tbody>
            <tr>
              <td colspan="2" class="section-header">PET DETAILS</td>
            </tr>
            <tr>
              <td><strong>Pet Name:</strong></td>
              <td>{{ vaccination.patient_name }}</td>
            </tr>
            <tr>
              <td><strong>Species:</strong></td>
              <td>{{ patientDetails?.species || 'N/A' }}</td>
            </tr>
            <tr>
              <td><strong>Breed:</strong></td>
              <td>{{ patientDetails?.breed || 'N/A' }}</td>
            </tr>
            <tr>
              <td><strong>Age:</strong></td>
              <td>{{ calculateAge(patientDetails?.date_of_birth) }}</td>
            </tr>
            <tr>
              <td colspan="2" class="section-header">OWNER DETAILS</td>
            </tr>
            <tr>
              <td><strong>Owner Name:</strong></td>
              <td>{{ ownerDetails?.name || 'N/A' }}</td>
            </tr>
            <tr>
              <td><strong>Phone:</strong></td>
              <td>{{ ownerDetails?.phone || 'N/A' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Vaccination Details -->
      <div class="vaccine-section">
        <table class="vaccine-table">
          <tbody>
            <tr>
              <td colspan="2" class="section-header">VACCINATION DETAILS</td>
            </tr>
            <tr>
              <td><strong>Vaccine Name:</strong></td>
              <td>{{ vaccination.vaccine_name }}</td>
            </tr>
            <tr>
              <td><strong>Manufacturer:</strong></td>
              <td>{{ vaccination.manufacturer || 'N/A' }}</td>
            </tr>
            <tr>
              <td><strong>Batch Number:</strong></td>
              <td>{{ vaccination.batch_number || 'N/A' }}</td>
            </tr>
            <tr>
              <td><strong>Date Administered:</strong></td>
              <td>{{ formatDate(vaccination.date_administered) }}</td>
            </tr>
            <tr>
              <td><strong>Next Due Date:</strong></td>
              <td>{{ vaccination.next_due_date ? formatDate(vaccination.next_due_date) : 'N/A' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Notes -->
      <div class="notes-section" v-if="vaccination.notes">
        <strong>Notes:</strong>
        <p>{{ vaccination.notes }}</p>
      </div>

      <!-- Footer -->
      <div class="footer">
        <div class="signature">
          <p>_________________________</p>
          <p><strong>Dr. Veterinarian</strong></p>
          <p>Veterinary Surgeon</p>
          <p>Reg. No: TNVCI/12345</p>
        </div>
        <div class="date">
          <p>Date: {{ formatDate(new Date()) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  vaccination: {
    type: Object,
    required: true
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

const calculateAge = (dob) => {
  if (!dob) return 'N/A';
  const birthDate = new Date(dob);
  const today = new Date();
  const years = today.getFullYear() - birthDate.getFullYear();
  const months = today.getMonth() - birthDate.getMonth();
  
  if (years > 0) {
    return `${years} year${years > 1 ? 's' : ''}`;
  } else if (months > 0) {
    return `${months} month${months > 1 ? 's' : ''}`;
  } else {
    return 'Less than 1 month';
  }
};
</script>

<style scoped>
/* Screen: Hide completely */
.vaccination-print-container {
  display: none;
}

/* Print: Show only this component */
@media print {
  /* Step 1: Hide everything on the page */
  body * {
    visibility: hidden !important;
  }
  
  /* Step 2: Make ONLY this component and its children visible */
  #vaccination-print-area,
  #vaccination-print-area * {
    visibility: visible !important;
  }
  
  /* Step 3: Position it at top-left of page */
  #vaccination-print-area {
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

.certificate-page {
  width: 210mm;
  min-height: 297mm;
  padding: 20mm;
  margin: 0 auto;
  background: white;
  font-family: Arial, sans-serif;
  color: black;
  font-size: 12pt;
}

.header {
  text-align: center;
  margin-bottom: 30px;
  border-bottom: 2px solid black;
  padding-bottom: 10px;
}

.header h1 {
  font-size: 20pt;
  font-weight: bold;
  margin: 0;
}

.header h2 {
  font-size: 16pt;
  margin-top: 15px;
}

.header p {
  margin: 5px 0;
  font-size: 10pt;
}

.cert-number {
  text-align: right;
  margin-bottom: 20px;
  font-size: 11pt;
}

.details-table,
.vaccine-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.details-table td,
.vaccine-table td {
  padding: 8px;
  border: 1px solid #000;
}

.details-table tr td:first-child,
.vaccine-table tr td:first-child {
  width: 40%;
  background: #f0f0f0;
}

.section-header {
  background: #000 !important;
  color: white !important;
  text-align: center;
  font-weight: bold;
  padding: 10px !important;
}

.notes-section {
  margin: 20px 0;
  padding: 10px;
  border: 1px solid #000;
}

.footer {
  margin-top: 50px;
  display: flex;
  justify-content: space-between;
}

.signature {
  text-align: center;
}

.signature p {
  margin: 5px 0;
}

.date {
  text-align: right;
  align-self: flex-end;
}

@page {
  size: A4;
  margin: 0;
}
</style>