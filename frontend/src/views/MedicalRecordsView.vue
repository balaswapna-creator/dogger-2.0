<template>
  <div class="records-wrapper">
    <!-- Header Card -->
    <div class="header-card">
      <div class="header-content">
        <div class="header-title">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
          <h1>Medical Records</h1>
        </div>
        <button @click="openNewRecordForm" class="btn-add">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          New Clinical Exam
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading medical records...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-card">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
      </svg>
      <h3>Failed to Load Records</h3>
      <p>{{ error }}</p>
      <button @click="fetchRecords" class="btn-retry">Try Again</button>
    </div>

    <!-- Empty State -->
    <div v-else-if="records.length === 0" class="empty-state-card">
      <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
      </svg>
      <h3>No Medical Records Found</h3>
      <p>Start by creating a new clinical examination record</p>
      <button @click="openNewRecordForm" class="btn-empty-action">Create First Record</button>
    </div>

    <!-- Records Table -->
    <div v-else class="table-card">
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Patient</th>
              <th>Owner</th>
              <th>Diagnosis</th>
              <th>Treatment</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in records" :key="record.id">
              <td>
                <div class="date-badge">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                  {{ formatDate(record.visit_date) }}
                </div>
              </td>
              <td>
                <div class="patient-info">
                  <div class="patient-avatar">{{ getInitial(getPatientName(record)) }}</div>
                  <span>{{ getPatientName(record) }}</span>
                </div>
              </td>
              <td>{{ getOwnerName(record) }}</td>
              <td>
                <span class="diagnosis-badge">{{ record.diagnosis || 'Not specified' }}</span>
              </td>
              <td class="treatment-cell">{{ record.treatment_plan || '-' }}</td>
              <td>
                <button @click="viewRecord(record.id)" class="btn-view">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  View
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

   <!-- Styled Medical Record View Modal -->
<div v-if="viewingRecord" class="modal-overlay" @click.self="closeViewModal">
  <div class="record-view-modal">
    <!-- Header -->
    <div class="record-header">
      <div class="clinic-info">
        <h1>🏥 Sri Adithya Pet Clinic</h1>
        <p>Dr. A. Balasubramanian, B.V.Sc, MBA(H A)</p>
        <p class="clinic-address">No:16,Sriram Nagar,Theni, Tamil Nadu - 625531</p>
      </div>
      <button @click="closeViewModal" class="btn-close-modal">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>

    <div class="record-body">
      <!-- Patient & Visit Info Card -->
      <div class="info-card">
        <h2 class="card-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <circle cx="12" cy="10" r="3"></circle>
            <path d="M7 20.662V19a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v1.662"></path>
          </svg>
          Patient Information
        </h2>
        <div class="info-grid-2">
          <div class="info-item">
            <span class="label">Patient Name</span>
            <span class="value">{{ getPatientName(viewingRecord) }}</span>
          </div>
          <div class="info-item">
            <span class="label">Owner</span>
            <span class="value">{{ getOwnerName(viewingRecord) }}</span>
          </div>
          <div class="info-item">
            <span class="label">Visit Date</span>
            <span class="value">{{ formatDate(viewingRecord.visit_date) }}</span>
          </div>
          <div class="info-item">
            <span class="label">Visit Type</span>
            <span class="value visit-type">{{ viewingRecord.visit_type }}</span>
          </div>
        </div>
      </div>

      <!-- Chief Complaint -->
      <div class="info-card complaint-card" v-if="viewingRecord.chief_complaint">
        <h2 class="card-title red">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          Chief Complaint
        </h2>
        <p class="content-text">{{ viewingRecord.chief_complaint }}</p>
      </div>

      <!-- History -->
      <div class="info-card" v-if="viewingRecord.history">
        <h2 class="card-title amber">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
          Medical History
        </h2>
        <p class="content-text">{{ viewingRecord.history }}</p>
      </div>

      <!-- Vitals -->
      <div class="info-card vitals-card" v-if="viewingRecord.temperature || viewingRecord.weight || viewingRecord.heart_rate">
        <h2 class="card-title green">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
          </svg>
          Vital Signs
        </h2>
        <div class="vitals-grid-view">
          <div class="vital-box" v-if="viewingRecord.temperature">
            <div class="vital-icon temp">🌡️</div>
            <div class="vital-info">
              <span class="vital-label">Temperature</span>
              <span class="vital-value">{{ viewingRecord.temperature }}°F</span>
            </div>
          </div>
          <div class="vital-box" v-if="viewingRecord.weight">
            <div class="vital-icon weight">⚖️</div>
            <div class="vital-info">
              <span class="vital-label">Weight</span>
              <span class="vital-value">{{ viewingRecord.weight }} kg</span>
            </div>
          </div>
          <div class="vital-box" v-if="viewingRecord.heart_rate">
            <div class="vital-icon heart">💓</div>
            <div class="vital-info">
              <span class="vital-label">Heart Rate</span>
              <span class="vital-value">{{ viewingRecord.heart_rate }} bpm</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Clinical Notes -->
      <div class="info-card" v-if="viewingRecord.clinical_notes">
        <h2 class="card-title green">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 3v18h18"></path>
            <path d="M7 12v5"></path>
            <path d="M12 8v9"></path>
            <path d="M17 4v13"></path>
          </svg>
          Clinical Examination
        </h2>
        <div class="clinical-notes-box">{{ viewingRecord.clinical_notes }}</div>
      </div>

      <!-- Diagnosis -->
      <div class="info-card diagnosis-card">
        <h2 class="card-title purple">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          Diagnosis
        </h2>
        <p class="content-text diagnosis">{{ viewingRecord.diagnosis || 'Not specified' }}</p>
      </div>

      <!-- Treatment Plan -->
      <div class="info-card treatment-card">
        <h2 class="card-title blue">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
          Treatment Plan
        </h2>
        <p class="content-text">{{ viewingRecord.treatment_plan || 'Not specified' }}</p>
      </div>

      <!-- Follow-up -->
      <div class="info-card" v-if="viewingRecord.follow_up_notes || viewingRecord.next_visit_date">
        <h2 class="card-title cyan">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
          Follow-up Information
        </h2>
        <div class="info-grid-2" v-if="viewingRecord.next_visit_date">
          <div class="info-item">
            <span class="label">Next Visit</span>
            <span class="value next-visit">{{ formatDate(viewingRecord.next_visit_date) }}</span>
          </div>
        </div>
        <p class="content-text" v-if="viewingRecord.follow_up_notes">{{ viewingRecord.follow_up_notes }}</p>
      </div>

      <!-- Fee -->
      <div class="info-card fee-card" v-if="viewingRecord.consultation_fee">
        <h2 class="card-title green">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="1" x2="12" y2="23"></line>
            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
          </svg>
          Consultation Fee
        </h2>
        <div class="fee-amount">₹{{ viewingRecord.consultation_fee }}</div>
      </div>
    </div>

    <!-- Footer Actions -->
    <div class="record-footer">
      <button @click="closeViewModal" class="btn-close-record">Close</button>
      <button @click="printRecord" class="btn-print-record">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="6 9 6 2 18 2 18 9"></polyline>
          <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
          <rect x="6" y="14" width="12" height="8"></rect>
        </svg>
        Print Record
      </button>
    </div>
  </div>
</div>

    <!-- Patient Selection Modal -->
    <div v-if="showForm && !selectedPatient" class="modal-overlay" @click.self="closeForm">
      <div class="modal-container patient-select">
        <div class="modal-header-select">
          <h2>Select Patient for Clinical Exam</h2>
          <button @click="closeForm" class="btn-close-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <!-- Search Patients -->
        <div class="search-box">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.35-4.35"></path>
          </svg>
          <input 
            v-model="patientSearch" 
            type="text" 
            placeholder="Search patients by name or owner..."
            class="search-input"
          />
        </div>

        <div class="patients-grid-modal">
          <div 
            v-for="patient in filteredPatients" 
            :key="patient.id" 
            @click="selectPatient(patient)" 
            class="patient-card-select"
          >
            <h3>{{ patient.pet_name }}</h3>
            <p>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              {{ getPatientOwnerName(patient.owner) }}
            </p>
            <div class="badges">
              <span class="badge species">{{ patient.species }}</span>
              <span class="badge">{{ patient.breed }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Clinical Examination Form -->
    <div v-if="showForm && selectedPatient" class="modal-overlay" @click.self="closeForm">
      <div class="form-container">
        <div class="form-header">
          <div>
            <h2>Clinical Examination Record</h2>
            <p>Patient: <strong>{{ selectedPatient.pet_name }}</strong> | Owner: <strong>{{ getPatientOwnerName(selectedPatient.owner) }}</strong></p>
          </div>
          <button @click="closeForm" class="btn-close-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div class="form-scroll">
          <!-- Visit Date -->
          <div class="form-section">
            <label class="section-label">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              Visit Date *
            </label>
            <input v-model="form.visit_date" type="date" class="input-field" />
          </div>

          <div class="form-section">
            <label class="section-label">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 11l3 3L22 4"></path>
                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
              </svg>
              Visit Type *
            </label>
            <select v-model="form.visit_type" class="input-field">
              <option value="consultation">General Consultation</option>
              <option value="vaccination">Vaccination</option>
              <option value="surgery">Surgery</option>
              <option value="emergency">Emergency</option>
              <option value="followup">Follow-up</option>
              <option value="grooming">Grooming</option>
              <option value="lab">Lab Test</option>
            </select>
          </div>

          <!-- Chief Complaint -->
          <div class="form-section section-red">
            <h3 class="section-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              Chief Complaint
            </h3>
            <textarea v-model="form.chief_complaint" rows="3" placeholder="What is the primary reason for today's visit? (e.g., vomiting, lethargy, loss of appetite)" class="textarea-field"></textarea>
          </div>

          <!-- History -->
          <div class="form-section section-amber">
            <h3 class="section-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
              </svg>
              History
            </h3>
            <textarea v-model="form.history" rows="4" placeholder="Duration of symptoms, previous treatments, diet changes, vaccination history, etc." class="textarea-field"></textarea>
          </div>

          <!-- Physical Examination -->
          <div class="form-section section-green">
            <h3 class="section-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 3v18h18"></path>
                <path d="M7 12v5"></path>
                <path d="M12 8v9"></path>
                <path d="M17 4v13"></path>
              </svg>
              Physical Examination
            </h3>
            
            <!-- Vitals -->
            <div class="vitals-grid">
              <div class="input-group">
                <label>Temperature (°F)</label>
                <input v-model="form.physical.temperature" type="text" placeholder="101.5" />
              </div>
              <div class="input-group">
                <label>Pulse (bpm)</label>
                <input v-model="form.physical.pulse" type="text" placeholder="120" />
              </div>
              <div class="input-group">
                <label>Respiration (rpm)</label>
                <input v-model="form.physical.respiration" type="text" placeholder="30" />
              </div>
              <div class="input-group">
                <label>Weight (kg)</label>
                <input v-model="form.physical.weight" type="text" placeholder="25.5" />
              </div>
            </div>

            <!-- System Examination -->
            <div class="systems-grid">
              <div class="input-group">
                <label>General Appearance</label>
                <textarea v-model="form.physical.general_appearance" rows="2" placeholder="Alert, responsive, body condition..."></textarea>
              </div>
              <div class="input-group">
                <label>Skin & Coat</label>
                <textarea v-model="form.physical.skin_coat" rows="2" placeholder="Condition, lesions, parasites..."></textarea>
              </div>
              <div class="input-group">
                <label>Eyes</label>
                <textarea v-model="form.physical.eyes" rows="2" placeholder="Discharge, redness, clarity..."></textarea>
              </div>
              <div class="input-group">
                <label>Ears</label>
                <textarea v-model="form.physical.ears" rows="2" placeholder="Condition, odor, inflammation..."></textarea>
              </div>
              <div class="input-group">
                <label>Mouth & Teeth</label>
                <textarea v-model="form.physical.mouth" rows="2" placeholder="Dental condition, gum color..."></textarea>
              </div>
              <div class="input-group">
                <label>Cardiovascular</label>
                <textarea v-model="form.physical.cardiovascular" rows="2" placeholder="Heart sounds, murmurs..."></textarea>
              </div>
              <div class="input-group">
                <label>Respiratory</label>
                <textarea v-model="form.physical.respiratory" rows="2" placeholder="Lung sounds, breathing effort..."></textarea>
              </div>
              <div class="input-group">
                <label>Abdomen</label>
                <textarea v-model="form.physical.abdomen" rows="2" placeholder="Palpation findings, pain..."></textarea>
              </div>
              <div class="input-group">
                <label>Musculoskeletal</label>
                <textarea v-model="form.physical.musculoskeletal" rows="2" placeholder="Gait, lameness, swelling..."></textarea>
              </div>
              <div class="input-group">
                <label>Nervous System</label>
                <textarea v-model="form.physical.nervous_system" rows="2" placeholder="Reflexes, coordination..."></textarea>
              </div>
            </div>
          </div>

          <!-- Tentative Diagnosis -->
          <div class="form-section section-purple">
            <h3 class="section-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              Tentative Diagnosis *
            </h3>
            <textarea v-model="form.diagnosis" rows="2" placeholder="Primary diagnosis based on examination findings" class="textarea-field"></textarea>
          </div>

          <!-- Differential Diagnosis -->
          <div class="form-section section-cyan">
            <h3 class="section-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
              </svg>
              Differential Diagnosis
            </h3>
            <textarea v-model="form.differential_diagnosis" rows="2" placeholder="Other possible diagnoses to consider" class="textarea-field"></textarea>
          </div>

          <!-- Treatment Plan -->
          <div class="form-section section-amber">
            <h3 class="section-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
              </svg>
              Treatment Plan *
            </h3>
            <textarea v-model="form.treatment_plan" rows="3" placeholder="Treatment approach, procedures planned, medications, etc." class="textarea-field"></textarea>
          </div>

          <!-- Medicine Prescription -->
          <div class="form-section section-pink">
            <h3 class="section-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="9" y1="9" x2="15" y2="15"></line>
                <line x1="15" y1="9" x2="9" y2="15"></line>
              </svg>
              Medicine Prescription
            </h3>
            
            <div v-for="(med, index) in form.medications" :key="index" class="medicine-card">
              <div class="medicine-header">
                <h4>Medicine {{ index + 1 }}</h4>
                <button v-if="form.medications.length > 1" @click="removeMedicine(index)" class="btn-remove-med">Remove</button>
              </div>
              <div class="medicine-grid">
                <div class="input-group">
                  <label>Medicine Name</label>
                  <input v-model="med.name" type="text" placeholder="e.g., Amoxicillin" />
                </div>
                <div class="input-group">
                  <label>Dosage</label>
                  <input v-model="med.dosage" type="text" placeholder="e.g., 500mg" />
                </div>
                <div class="input-group">
                  <label>Frequency</label>
                  <input v-model="med.frequency" type="text" placeholder="e.g., Twice daily" />
                </div>
                <div class="input-group">
                  <label>Duration</label>
                  <input v-model="med.duration" type="text" placeholder="e.g., 7 days" />
                </div>
                <div class="input-group">
                  <label>Route</label>
                  <input v-model="med.route" type="text" placeholder="e.g., Oral, IV" />
                </div>
              </div>
            </div>
            
            <button @click="addMedicine" class="btn-add-med">+ Add Another Medicine</button>
          </div>

          <!-- Lab Tests -->
          <div class="form-section section-cyan">
            <h3 class="section-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
              </svg>
              Lab Tests Ordered
            </h3>
            <textarea v-model="form.lab_tests" rows="2" placeholder="CBC, biochemistry, X-ray, ultrasound, urinalysis, fecal exam..." class="textarea-field"></textarea>
          </div>

          <!-- Next Review -->
          <div class="form-section section-green">
            <label class="section-label">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              Next Review Date
            </label>
            <input v-model="form.next_review_date" type="date" class="input-field" />
          </div>

          <!-- Special Instructions -->
          <div class="form-section section-amber">
            <h3 class="section-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              Special Instructions for Owner
            </h3>
            <textarea v-model="form.special_instructions" rows="3" placeholder="Diet restrictions, activity level, warning signs to watch for, follow-up care..." class="textarea-field"></textarea>
          </div>

          <!-- Notes -->
          <div class="form-section">
            <label class="section-label">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
              </svg>
              Additional Notes
            </label>
            <textarea v-model="form.notes" rows="3" placeholder="Any additional observations or comments..." class="textarea-field"></textarea>
          </div>
        </div>

        <div class="form-section section-green">
          <label class="section-label">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="1" x2="12" y2="23"></line>
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
            </svg>
            Consultation Fee (₹)
          </label>
          <input 
            v-model="form.consultation_fee" 
            type="number" 
            step="0.01" 
            min="0"
            placeholder="Enter consultation fee (e.g., 500)" 
            class="input-field"
          />
          <p class="field-hint">Enter the consultation fee for this visit</p>
        </div>
      </div> <!-- End of form-scroll -->

        <!-- Action Buttons -->
        <div class="form-actions">
          <button @click="closeForm" class="btn-cancel">Cancel</button>
          <button @click="handleSaveRecord" class="btn-save">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
              <polyline points="17 21 17 13 7 13 7 21"></polyline>
              <polyline points="7 3 7 8 15 8"></polyline>
            </svg>
            Save Clinical Record
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

export default {
  name: 'MedicalRecordsView',
  setup() {
    const records = ref([])
    const patients = ref([])
    const owners = ref([])
    const loading = ref(true)
    const error = ref(null)
    const showForm = ref(false)
    const selectedPatient = ref(null)
    const patientSearch = ref('')

    const form = ref({
      visit_date: new Date().toISOString().split('T')[0],
      visit_type: 'consultation', // ✅ ADD THIS LINE
      chief_complaint: '',
      history: '',
      physical: {
        temperature: '',
        pulse: '',
        respiration: '',
        weight: '',
        general_appearance: '',
        skin_coat: '',
        eyes: '',
        ears: '',
        mouth: '',
        cardiovascular: '',
        respiratory: '',
        abdomen: '',
        musculoskeletal: '',
        nervous_system: ''
      },
      diagnosis: '',
      differential_diagnosis: '',
      treatment_plan: '',
      medications: [
        { name: '', dosage: '', frequency: '', duration: '', route: '' }
      ],
      lab_tests: '',
      next_review_date: '',
      special_instructions: '',
      notes: '',
      consultation_fee: '' // ✅ ADD THIS LINE
    })

    const filteredPatients = computed(() => {
      if (!patientSearch.value) return patients.value
      const query = patientSearch.value.toLowerCase()
      return patients.value.filter(p => 
        p.pet_name?.toLowerCase().includes(query) ||
        getPatientOwnerName(p.owner).toLowerCase().includes(query)
      )
    })

    const fetchRecords = async () => {
      loading.value = true
      error.value = null
      try {
        const [recordsRes, patientsRes, ownersRes] = await Promise.all([
          api.get('/medical-records/'),
          api.get('/patients/'),
          api.get('/owners/')
        ])
        
        const recordsData = recordsRes.data || []
        records.value = Array.isArray(recordsData) ? recordsData : (recordsData.results || [])
        
        const patientsData = patientsRes.data || []
        patients.value = Array.isArray(patientsData) ? patientsData : (patientsData.results || [])
        
        const ownersData = ownersRes.data || []
        owners.value = Array.isArray(ownersData) ? ownersData : (ownersData.results || [])
          
      } catch (err) {
        console.error('Error fetching data:', err)
        error.value = 'Failed to load medical records. Please try again.'
        records.value = []
      } finally {
        loading.value = false
      }
    }

    const getPatientName = (record) => {
      if (!record) return 'Unknown'
      if (record.patient_name) return record.patient_name
      if (record.patient?.pet_name) return record.patient.pet_name
      return 'Unknown Patient'
    }

    const getOwnerName = (record) => {
      if (!record) return 'Unknown'
      if (record.owner_name) return record.owner_name
      if (record.patient?.owner_name) return record.patient.owner_name
      if (record.patient?.owner?.name) return record.patient.owner.name
      return 'Unknown Owner'
    }

    const getPatientOwnerName = (ownerId) => {
      const owner = owners.value.find(o => o.id === ownerId)
      return owner ? owner.name : 'Unknown Owner'
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('en-IN', {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        })
      } catch (e) {
        return 'Invalid Date'
      }
    }

    const getInitial = (name) => {
      if (!name || typeof name !== 'string') return '?'
      return name.charAt(0).toUpperCase()
    }

    const openNewRecordForm = () => {
      showForm.value = true
      selectedPatient.value = null
    }

    const selectPatient = (patient) => {
      selectedPatient.value = patient
      patientSearch.value = ''
    }

    const addMedicine = () => {
      form.value.medications.push({ name: '', dosage: '', frequency: '', duration: '', route: '' })
    }

    const removeMedicine = (index) => {
      if (form.value.medications.length > 1) {
        form.value.medications.splice(index, 1)
      }
    }

    const handleSaveRecord = async () => {
      if (!selectedPatient.value) {
        alert('Please select a patient')
        return
      }

      if (!form.value.diagnosis || !form.value.treatment_plan || !form.value.chief_complaint) {
        alert('Please fill in required fields: Chief Complaint, Diagnosis, and Treatment Plan')
        return
      }

      try {
        const medicationsText = form.value.medications
          .filter(med => med.name)
          .map((med, i) => 
            `${i + 1}. ${med.name}${med.dosage ? ` - ${med.dosage}` : ''}${med.frequency ? `, ${med.frequency}` : ''}${med.duration ? `, ${med.duration}` : ''}${med.route ? `, Route: ${med.route}` : ''}`
          ).join('\n') || 'No medications prescribed'

        const clinicalNotes = `
PHYSICAL EXAMINATION:
Vitals: Temp: ${form.value.physical.temperature || 'N/A'}°F, Pulse: ${form.value.physical.pulse || 'N/A'} bpm, Resp: ${form.value.physical.respiration || 'N/A'} rpm, Weight: ${form.value.physical.weight || 'N/A'} kg
General Appearance: ${form.value.physical.general_appearance || 'N/A'}
Skin & Coat: ${form.value.physical.skin_coat || 'N/A'}
Eyes: ${form.value.physical.eyes || 'N/A'}
Ears: ${form.value.physical.ears || 'N/A'}
Mouth & Teeth: ${form.value.physical.mouth || 'N/A'}
Cardiovascular: ${form.value.physical.cardiovascular || 'N/A'}
Respiratory: ${form.value.physical.respiratory || 'N/A'}
Abdomen: ${form.value.physical.abdomen || 'N/A'}
Musculoskeletal: ${form.value.physical.musculoskeletal || 'N/A'}
Nervous System: ${form.value.physical.nervous_system || 'N/A'}

DIFFERENTIAL DIAGNOSIS:
${form.value.differential_diagnosis || 'Not provided'}

MEDICATIONS PRESCRIBED:
${medicationsText}

LAB TESTS ORDERED:
${form.value.lab_tests || 'None'}

SPECIAL INSTRUCTIONS FOR OWNER:
${form.value.special_instructions || 'None'}
        `.trim()

        const followUpNotes = `
Next Review Date: ${form.value.next_review_date || 'Not scheduled'}
Additional Notes: ${form.value.notes || 'None'}
        `.trim()

        const recordData = {
          patient: selectedPatient.value.id,
          visit_date: form.value.visit_date,
          visit_type: form.value.visit_type || 'consultation', // ✅ NOW FROM FORM
          chief_complaint: form.value.chief_complaint || 'Not specified',
          history: form.value.history || '',
          clinical_notes: clinicalNotes,
          diagnosis: form.value.diagnosis,
          treatment_plan: form.value.treatment_plan,
          temperature: form.value.physical.temperature ? parseFloat(form.value.physical.temperature) : null,
          weight: form.value.physical.weight ? parseFloat(form.value.physical.weight) : null,
          heart_rate: form.value.physical.pulse ? parseInt(form.value.physical.pulse) : null,
          next_visit_date: form.value.next_review_date || null,
          follow_up_notes: followUpNotes,
          consultation_fee: form.value.consultation_fee ? parseFloat(form.value.consultation_fee) : 0 // ✅ NOW FROM FORM
        }

        console.log('Sending record data:', recordData)
        
        const response = await api.post('/medical-records/', recordData)
        
        console.log('Record saved successfully:', response.data)
        alert('Clinical record saved successfully!')
        closeForm()
        await fetchRecords()
      } catch (err) {
        console.error('Error saving record:', err)
        console.error('Error response:', err.response?.data)
        
        let errorMsg = 'Failed to save record'
        
        if (err.response?.data) {
          const errorData = err.response.data
          if (typeof errorData === 'object') {
            const errors = Object.entries(errorData)
              .map(([field, messages]) => {
                const msgArray = Array.isArray(messages) ? messages : [messages]
                return `${field}: ${msgArray.join(', ')}`
              })
              .join('\n')
            errorMsg = errors || errorMsg
          } else {
            errorMsg = errorData
          }
        } else if (err.message) {
          errorMsg = err.message
        }
        
        alert(errorMsg)
      }
    }

    const closeForm = () => {
      showForm.value = false
      selectedPatient.value = null
      patientSearch.value = ''
      
      form.value = {
        visit_date: new Date().toISOString().split('T')[0],
        visit_type: 'consultation', // ✅ ADD THIS
        chief_complaint: '',
        history: '',
        physical: {
          temperature: '', pulse: '', respiration: '', weight: '',
          general_appearance: '', skin_coat: '', eyes: '', ears: '', mouth: '',
          cardiovascular: '', respiratory: '', abdomen: '', musculoskeletal: '', nervous_system: ''
        },
        diagnosis: '',
        differential_diagnosis: '',
        treatment_plan: '',
        medications: [{ name: '', dosage: '', frequency: '', duration: '', route: '' }],
        lab_tests: '',
        next_review_date: '',
        special_instructions: '',
        notes: '',
        consultation_fee: '' // ✅ ADD THIS
      }
    }

    const viewingRecord = ref(null)
    
    const viewRecord = async (id) => {
      if (!id) {
        console.error('No record ID provided')
        return
      }
      
      try {
        console.log('Fetching record:', id)
        const response = await api.get(`/medical-records/${id}/`)
        viewingRecord.value = response.data
        console.log('Record loaded:', response.data)
      } catch (err) {
        console.error('Error loading record:', err)
        alert('Failed to load record details')
      }
    }
    
    const closeViewModal = () => {
      viewingRecord.value = null
    }

// Add this function in your MedicalRecordsView.vue script setup
     const printRecord = () => {
       window.print();
    };

    onMounted(() => {
      fetchRecords()
    })

    return {
      records,
      patients,
      loading,
      error,
      showForm,
      selectedPatient,
      patientSearch,
      form,
      filteredPatients,
      viewingRecord,
      getPatientName,
      getOwnerName,
      getPatientOwnerName,
      formatDate,
      getInitial,
      openNewRecordForm,
      selectPatient,
      addMedicine,
      removeMedicine,
      handleSaveRecord,
      closeForm,
      viewRecord,
      closeViewModal,
      fetchRecords
    }
  }
}
</script>

<style scoped>
.records-wrapper {
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
  color: #8B5CF6;
}

.header-title h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1F2937;
}

.btn-add {
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
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
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
  transition: all 0.3s;
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #E5E7EB;
  border-top-color: #8B5CF6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-card {
  background: white;
  border-radius: 16px;
  padding: 48px 24px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.error-card svg {
  color: #EF4444;
  margin-bottom: 16px;
}

.error-card h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
  color: #1F2937;
}

.error-card p {
  color: #6B7280;
  margin: 0 0 24px 0;
}

.btn-retry {
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-retry:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

.empty-state-card {
  background: white;
  border-radius: 16px;
  padding: 80px 24px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.empty-state-card svg {
  color: #D1D5DB;
  margin-bottom: 20px;
}

.empty-state-card h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
  color: #1F2937;
}

.empty-state-card p {
  color: #6B7280;
  margin: 0 0 24px 0;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.btn-empty-action {
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
  color: white;
  border: none;
  padding: 12px 32px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-empty-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
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
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
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

.data-table tbody tr:last-child td {
  border-bottom: none;
}

.date-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #EDE9FE;
  color: #6B21A8;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
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
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  flex-shrink: 0;
}

.diagnosis-badge {
  background: #DBEAFE;
  color: #1E40AF;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
}

.treatment-cell {
  max-width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-view {
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s;
}

.btn-view:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
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
  padding: 32px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header-select {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 2px solid #E5E7EB;
}

.modal-header-select h2 {
  margin: 0;
  color: #1F2937;
  font-size: 24px;
}

.btn-close-icon {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #9CA3AF;
  padding: 8px;
  transition: all 0.3s;
}

.btn-close-icon:hover {
  color: #4B5563;
}

.search-box {
  background: #F9FAFB;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.search-box svg {
  color: #9CA3AF;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 15px;
  color: #1F2937;
}

.patients-grid-modal {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
  max-height: 400px;
  overflow-y: auto;
}

.patient-card-select {
  background: #F9FAFB;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.patient-card-select:hover {
  border-color: #8B5CF6;
  background: #F3F4F6;
  transform: translateY(-2px);
}

.patient-card-select h3 {
  margin: 0 0 8px 0;
  color: #1F2937;
  font-size: 18px;
}

.patient-card-select p {
  margin: 0 0 12px 0;
  color: #6B7280;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.badge {
  background: #E0E7FF;
  color: #4338CA;
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
}

.badge.species {
  background: #EDE9FE;
  color: #7C3AED;
}

/* Form Container */
.form-container {
  background: white;
  border-radius: 20px;
  max-width: 1000px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  animation: modalSlideIn 0.3s ease-out;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 24px 32px;
  border-bottom: 2px solid #E5E7EB;
}

.form-header h2 {
  margin: 0 0 8px 0;
  color: #1F2937;
  font-size: 24px;
}

.form-header p {
  margin: 0;
  color: #6B7280;
  font-size: 15px;
}

.form-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

.form-section {
  margin-bottom: 32px;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 12px;
  font-size: 15px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 16px 0;
}

.section-red .section-title { color: #EF4444; }
.section-amber .section-title { color: #F59E0B; }
.section-green .section-title { color: #10B981; }
.section-purple .section-title { color: #8B5CF6; }
.section-cyan .section-title { color: #06B6D4; }
.section-pink .section-title { color: #EC4899; }

.input-field, .textarea-field {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 10px;
  font-size: 15px;
  color: #1F2937;
  font-family: inherit;
  transition: all 0.3s;
}

.input-field:focus, .textarea-field:focus {
  outline: none;
  border-color: #8B5CF6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.textarea-field {
  resize: vertical;
}

.vitals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.systems-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-group label {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 6px;
}

.input-group input,
.input-group textarea {
  padding: 10px 14px;
  border: 2px solid #E5E7EB;
  border-radius: 8px;
  font-size: 14px;
  color: #1F2937;
  font-family: inherit;
  transition: all 0.3s;
}

.input-group input:focus,
.input-group textarea:focus {
  outline: none;
  border-color: #8B5CF6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.medicine-card {
  background: #F9FAFB;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 16px;
  border: 2px solid #E5E7EB;
}

.medicine-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.medicine-header h4 {
  margin: 0;
  color: #374151;
  font-size: 16px;
}

.btn-remove-med {
  background: #FEE2E2;
  color: #DC2626;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-remove-med:hover {
  background: #FCA5A5;
}

.medicine-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
}

.btn-add-med {
  background: #E0E7FF;
  color: #4338CA;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-add-med:hover {
  background: #C7D2FE;
}

.form-actions {
  display: flex;
  gap: 12px;
  padding: 24px 32px;
  border-top: 2px solid #E5E7EB;
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
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
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
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
  transition: all 0.3s;
}

.btn-save:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

/* Medical Record View Modal Styles */
.record-view-modal {
  background: white;
  border-radius: 20px;
  max-width: 900px;
  width: 100%;
  max-height: 95vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease-out;
}

.record-header {
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
  color: white;
  padding: 24px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.clinic-info h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 700;
}

.clinic-info p {
  margin: 4px 0;
  font-size: 14px;
  opacity: 0.9;
}

.clinic-address {
  font-size: 13px !important;
  opacity: 0.8 !important;
}

.btn-close-modal {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.btn-close-modal:hover {
  background: rgba(255, 255, 255, 0.3);
}

.record-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: #F9FAFB;
}

.info-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border-left: 4px solid #8B5CF6;
}

.complaint-card { border-left-color: #EF4444; }
.diagnosis-card { border-left-color: #8B5CF6; }
.treatment-card { border-left-color: #3B82F6; }
.vitals-card { border-left-color: #10B981; }
.fee-card { border-left-color: #10B981; }

.card-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 700;
  color: #8B5CF6;
  margin: 0 0 16px 0;
}

.card-title.red { color: #EF4444; }
.card-title.amber { color: #F59E0B; }
.card-title.green { color: #10B981; }
.card-title.purple { color: #8B5CF6; }
.card-title.blue { color: #3B82F6; }
.card-title.cyan { color: #06B6D4; }

.info-grid-2 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label {
  font-size: 12px;
  font-weight: 600;
  color: #6B7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.value {
  font-size: 16px;
  font-weight: 600;
  color: #1F2937;
}

.visit-type {
  background: #EDE9FE;
  color: #7C3AED;
  padding: 6px 12px;
  border-radius: 8px;
  display: inline-block;
  text-transform: capitalize;
}

.next-visit {
  background: #DBEAFE;
  color: #1E40AF;
  padding: 6px 12px;
  border-radius: 8px;
  display: inline-block;
}

.content-text {
  margin: 0;
  color: #374151;
  line-height: 1.7;
  font-size: 15px;
}

.diagnosis {
  font-weight: 600;
  color: #7C3AED;
  font-size: 16px;
}

.vitals-grid-view {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}

.vital-box {
  background: linear-gradient(135deg, #F0FDF4, #DCFCE7);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border: 2px solid #10B981;
}

.vital-icon {
  font-size: 32px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 10px;
  flex-shrink: 0;
}

.vital-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.vital-label {
  font-size: 12px;
  font-weight: 600;
  color: #065F46;
  text-transform: uppercase;
}

.vital-value {
  font-size: 20px;
  font-weight: 700;
  color: #047857;
}

.clinical-notes-box {
  background: #F9FAFB;
  border: 2px solid #E5E7EB;
  border-radius: 10px;
  padding: 16px;
  white-space: pre-wrap;
  font-family: inherit;
  font-size: 14px;
  color: #374151;
  line-height: 1.7;
  max-height: 300px;
  overflow-y: auto;
}

.fee-amount {
  font-size: 36px;
  font-weight: 700;
  color: #10B981;
  text-align: center;
  padding: 16px;
  background: linear-gradient(135deg, #F0FDF4, #DCFCE7);
  border-radius: 12px;
  border: 2px solid #10B981;
}

.record-footer {
  padding: 20px 24px;
  border-top: 2px solid #E5E7EB;
  display: flex;
  gap: 12px;
  background: white;
}

.btn-close-record {
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

.btn-close-record:hover {
  background: #E5E7EB;
}

.btn-print-record {
  flex: 2;
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
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
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
  transition: all 0.3s;
}

.btn-print-record:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

.field-hint {
  margin: 8px 0 0 0;
  font-size: 13px;
  color: #6B7280;
  font-style: italic;
}

select.input-field {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg width='12' height='12' viewBox='0 0 12 12' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M2.5 4.5L6 8L9.5 4.5' stroke='%236B7280' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 16px center;
  padding-right: 40px;
  cursor: pointer;
}

select.input-field:focus {
  outline: none;
  border-color: #8B5CF6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

input[type="number"].input-field {
  appearance: textfield;
}

input[type="number"].input-field::-webkit-inner-spin-button,
input[type="number"].input-field::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

@media print {
  .record-header {
    background: white !important;
    color: black !important;
    border-bottom: 3px solid #8B5CF6;
  }
  
  .btn-close-modal, .record-footer {
    display: none !important;
  }
  
  .record-body {
    background: white !important;
  }
}

@media (max-width: 768px) {
  .records-wrapper {
    padding: 16px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .btn-add {
    width: 100%;
    justify-content: center;
  }
  
  .vitals-grid, .systems-grid, .medicine-grid {
    grid-template-columns: 1fr;
  }
  
  .form-scroll {
    padding: 20px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn-cancel, .btn-save {
    flex: 1;
  }
}

/* View Modal Styles */
.view-modal {
  background: white;
  border-radius: 20px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  animation: modalSlideIn 0.3s ease-out;
}

.view-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px 32px;
}

.view-section {
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #E5E7EB;
}

.view-section:last-child {
  border-bottom: none;
}

.view-section h3 {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 700;
  color: #8B5CF6;
}

.view-section p {
  margin: 0;
  color: #374151;
  line-height: 1.6;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.info-grid div {
  color: #374151;
}

.clinical-notes {
  background: #F9FAFB;
  padding: 16px;
  border-radius: 8px;
  white-space: pre-wrap;
  font-family: inherit;
  font-size: 14px;
  color: #374151;
  line-height: 1.6;
  border: 1px solid #E5E7EB;
  max-height: 300px;
  overflow-y: auto;
}

.fee-amount {
  font-size: 24px;
  font-weight: 700;
  color: #10B981;
}
</style>


