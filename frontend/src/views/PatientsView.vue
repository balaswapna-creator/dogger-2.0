<template>
  <div class="patients-wrapper">
    <!-- Header Card -->
    <div class="header-card">
      <div class="header-content">
        <div class="header-title">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <circle cx="12" cy="10" r="3"></circle>
            <path d="M7 20.662V19a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v1.662"></path>
          </svg>
          <h1>Patients (Pets)</h1>
        </div>
        <button @click="openAddModal" class="btn-add">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          <span>Add New Pet</span>
        </button>
      </div>
    </div>

    <!-- Search Card -->
    <div class="search-card">
      <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"></circle>
        <path d="m21 21-4.35-4.35"></path>
      </svg>
      <input 
        v-model="searchQuery"
        type="text" 
        placeholder="Search pets by name, species, breed, or owner..."
        class="search-input"
      />
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading patients...</p>
    </div>

    <!-- Patients Grid -->
    <div v-else-if="filteredPatients.length > 0" class="patients-grid">
      <div v-for="patient in filteredPatients" :key="patient.id" class="patient-card">
        <div class="patient-photo">
          <img 
            v-if="getPhotoUrl(patient)" 
            :src="getPhotoUrl(patient)" 
            :alt="patient.pet_name"
            @error="handleImageError"
          />
          <div v-else class="photo-placeholder">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
            </svg>
          </div>
        </div>
        
        <div class="patient-info">
          <h3>{{ patient.pet_name }}</h3>
          <div class="patient-details">
            <span class="detail-badge species">{{ patient.species }}</span>
            <span class="detail-badge">{{ patient.breed }}</span>
          </div>
          <p class="owner-name">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            {{ getOwnerName(patient.owner) }}
          </p>
        </div>
        
        <div class="patient-actions">
          <!-- ✅ NEW: View Details Button -->
          <button @click="viewPatientDetails(patient.id)" class="btn-view" title="View Details">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>
          </button>
          <button @click="editPatient(patient)" class="btn-edit" title="Edit">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
            </svg>
          </button>
          <button @click="deletePatient(patient.id)" class="btn-delete" title="Delete">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="12" cy="12" r="10"></circle>
        <circle cx="12" cy="10" r="3"></circle>
        <path d="M7 20.662V19a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v1.662"></path>
      </svg>
      <h3>No Patients Found</h3>
      <p>Add your first patient to get started</p>
      <button @click="openAddModal" class="btn-empty-action">Add First Pet</button>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || editingPatient" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">
        <div class="modal-header">
          <h2>{{ editingPatient ? 'Edit Pet' : 'Add New Pet' }}</h2>
          <button @click="closeModal" class="btn-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <!-- Photo Upload -->
          <div class="photo-upload-section">
            <div v-if="photoPreview" class="photo-preview">
              <img :src="photoPreview" alt="Preview" />
              <button @click="removePhoto" class="btn-remove-photo">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
            <div v-else class="photo-buttons">
              <button @click="openCamera" class="btn-camera">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
                Take Photo
              </button>
              <label class="btn-file">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="17 8 12 3 7 8"></polyline>
                  <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
                Choose File
                <input type="file" @change="handleFileSelect" accept="image/*" ref="fileInput" class="file-input"/>
              </label>
            </div>
          </div>

          <!-- Form Fields -->
          <div class="form-grid">
            <div class="form-group full-width">
              <label>Owner *</label>
              <select v-model="form.owner">
                <option value="">Select Owner</option>
                <option v-for="owner in owners" :key="owner.id" :value="owner.id">
                  {{ owner.name }}
                </option>
              </select>
            </div>

            <div class="form-group full-width">
              <label>Pet Name *</label>
              <input v-model="form.pet_name" type="text" placeholder="e.g., Max, Bella"/>
            </div>

            <div class="form-group">
              <label>Species *</label>
              <select v-model="form.species">
                <option value="">Select Species</option>
                <option value="dog">Dog</option>
                <option value="cat">Cat</option>
                <option value="bird">Bird</option>
                <option value="rabbit">Rabbit</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div class="form-group">
              <label>Breed *</label>
              <input v-model="form.breed" type="text" placeholder="e.g., Labrador"/>
            </div>

            <div class="form-group">
              <label>Gender *</label>
              <select v-model="form.gender">
                <option value="">Select Gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </div>

            <div class="form-group">
              <label>Date of Birth</label>
              <input v-model="form.date_of_birth" type="date"/>
            </div>

            <div class="form-group">
              <label>Color</label>
              <input v-model="form.color" type="text" placeholder="e.g., Brown, Black"/>
            </div>

            <div class="form-group">
              <label>Weight (kg)</label>
              <input v-model="form.weight" type="number" step="0.1" placeholder="0.0"/>
            </div>

            <div class="form-group full-width">
              <label>Medical History</label>
              <textarea v-model="form.medical_history" rows="3" placeholder="Optional medical notes..."></textarea>
            </div>
          </div>

          <div class="modal-actions">
            <button @click="closeModal" class="btn-cancel">Cancel</button>
            <button @click="savePatient" class="btn-save">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                <polyline points="17 21 17 13 7 13 7 21"></polyline>
                <polyline points="7 3 7 8 15 8"></polyline>
              </svg>
              Save Pet
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Camera Modal -->
    <div v-if="showCamera" class="modal-overlay">
      <div class="camera-modal">
        <div class="camera-header">
          <h3>Take Photo</h3>
          <button @click="closeCamera" class="btn-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <video ref="videoElement" autoplay playsinline class="camera-video"></video>
        <canvas ref="canvasElement" class="camera-canvas"></canvas>
        <div class="camera-actions">
          <button @click="capturePhoto" class="btn-capture">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <circle cx="12" cy="12" r="10"></circle>
            </svg>
            Capture
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

const router = useRouter();

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const BACKEND_URL = API_BASE_URL.replace('/api', '');
const MEDIA_URL = `${BACKEND_URL}/media/`;

const patients = ref([]);
const owners = ref([]);
const searchQuery = ref('');
const showAddModal = ref(false);
const editingPatient = ref(null);
const showCamera = ref(false);
const photoPreview = ref('');
const photoFile = ref(null);
const videoElement = ref(null);
const canvasElement = ref(null);
const fileInput = ref(null);
const isLoading = ref(true);
let videoStream = null;

const form = ref({
  owner: '',
  pet_name: '',
  species: '',
  breed: '',
  gender: '',
  date_of_birth: '',
  color: '',
  weight: '',
  medical_history: ''
});

const filteredPatients = computed(() => {
  if (!Array.isArray(patients.value) || patients.value.length === 0) {
    return [];
  }
  
  if (!searchQuery.value) return patients.value;
  
  const query = searchQuery.value.toLowerCase();
  return patients.value.filter(p => 
    p.pet_name?.toLowerCase().includes(query) ||
    p.species?.toLowerCase().includes(query) ||
    p.breed?.toLowerCase().includes(query) ||
    getOwnerName(p.owner).toLowerCase().includes(query)
  );
});

const getPhotoUrl = (patient) => {
  if (!patient.photo) return null;
  if (patient.photo.startsWith('http')) return patient.photo;
  const photoPath = patient.photo.replace(/^\/+/, '').replace('media/', '');
  return `${MEDIA_URL}${photoPath}`;
};

const handleImageError = (event) => {
  event.target.style.display = 'none';
};

const getOwnerName = (ownerId) => {
  if (!Array.isArray(owners.value)) return 'Unknown';
  const owner = owners.value.find(o => o.id === ownerId);
  return owner ? owner.name : 'Unknown';
};

// ✅ NEW: View Patient Details Function
const viewPatientDetails = (patientId) => {
  router.push(`/patients/${patientId}`);
};

const fetchData = async () => {
  isLoading.value = true;
  try {
    const [patientsData, ownersData] = await Promise.all([
      api.get('/patients/'),
      api.get('/owners/')
    ]);
    
    patients.value = Array.isArray(patientsData.data) 
      ? patientsData.data 
      : (patientsData.data.results || []);
      
    owners.value = Array.isArray(ownersData.data) 
      ? ownersData.data 
      : (ownersData.data.results || []);
  } catch (error) {
    console.error('Error fetching data:', error);
    patients.value = [];
    owners.value = [];
  } finally {
    isLoading.value = false;
  }
};

const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (file) {
    if (file.size > 5 * 1024 * 1024) {
      alert('File too large! Maximum size is 5MB');
      return;
    }
    
    photoFile.value = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      photoPreview.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const openCamera = async () => {
  try {
    showCamera.value = true;
    await new Promise(resolve => setTimeout(resolve, 100));
    
    videoStream = await navigator.mediaDevices.getUserMedia({ 
      video: { 
        facingMode: 'environment',
        width: { ideal: 1280 },
        height: { ideal: 720 }
      } 
    });
    
    if (videoElement.value) {
      videoElement.value.srcObject = videoStream;
    }
  } catch (error) {
    console.error('Camera error:', error);
    alert('Could not access camera. Please use file upload instead.');
    showCamera.value = false;
  }
};

const capturePhoto = () => {
  const video = videoElement.value;
  const canvas = canvasElement.value;
  
  if (video && canvas) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
    
    canvas.toBlob((blob) => {
      const timestamp = new Date().getTime();
      photoFile.value = new File([blob], `pet_photo_${timestamp}.jpg`, { type: 'image/jpeg' });
      photoPreview.value = canvas.toDataURL('image/jpeg');
      closeCamera();
    }, 'image/jpeg', 0.85);
  }
};

const closeCamera = () => {
  if (videoStream) {
    videoStream.getTracks().forEach(track => track.stop());
    videoStream = null;
  }
  showCamera.value = false;
};

const removePhoto = () => {
  photoPreview.value = '';
  photoFile.value = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

const openAddModal = () => {
  showAddModal.value = true;
  editingPatient.value = null;
  form.value = {
    owner: '',
    pet_name: '',
    species: '',
    breed: '',
    gender: '',
    date_of_birth: '',
    color: '',
    weight: '',
    medical_history: ''
  };
  photoPreview.value = '';
  photoFile.value = null;
};

const savePatient = async () => {
  if (!form.value.pet_name || !form.value.species || !form.value.owner) {
    alert('Please fill in all required fields (Pet Name, Species, Owner)')
    return
  }
  
  try {
    const formData = new FormData()
    formData.append('pet_name', form.value.pet_name)
    formData.append('species', form.value.species)
    formData.append('breed', form.value.breed || '')
    formData.append('gender', form.value.gender)
    formData.append('owner', form.value.owner)
    
    if (form.value.date_of_birth) formData.append('date_of_birth', form.value.date_of_birth)
    if (form.value.color) formData.append('color', form.value.color)
    if (form.value.weight) formData.append('weight', form.value.weight)
    if (form.value.medical_history) formData.append('medical_history', form.value.medical_history)
    if (photoFile.value) formData.append('photo', photoFile.value)
    
    let response
    if (editingPatient.value) {
      response = await api.put(`/patients/${editingPatient.value}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    } else {
      response = await api.post('/patients/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    }
    
    alert(editingPatient.value ? 'Pet updated successfully!' : 'Pet saved successfully!')
    closeModal()
    await fetchData()
  } catch (error) {
    console.error('Error saving patient:', error)
    alert('Failed to save pet: ' + (error.response?.data?.detail || error.message))
  }
}

const editPatient = (patient) => {
  editingPatient.value = patient.id;
  form.value = {
    owner: patient.owner,
    pet_name: patient.pet_name,
    species: patient.species,
    breed: patient.breed,
    gender: patient.gender,
    date_of_birth: patient.date_of_birth || '',
    color: patient.color || '',
    weight: patient.weight || '',
    medical_history: patient.medical_history || ''
  };
  
  if (patient.photo) {
    photoPreview.value = getPhotoUrl(patient);
  }
  showAddModal.value = true;
};

const deletePatient = async (id) => {
  if (!confirm('Are you sure you want to delete this pet?')) return;
  
  try {
    await api.delete(`/patients/${id}/`);
    alert('Pet deleted successfully!');
    fetchData();
  } catch (error) {
    console.error('Error deleting patient:', error);
    alert('Failed to delete pet.');
  }
};

const closeModal = () => {
  showAddModal.value = false;
  editingPatient.value = null;
  photoPreview.value = '';
  photoFile.value = null;
  form.value = {
    owner: '',
    pet_name: '',
    species: '',
    breed: '',
    gender: '',
    date_of_birth: '',
    color: '',
    weight: '',
    medical_history: ''
  };
  closeCamera();
  if (fileInput.value) fileInput.value.value = '';
};

onMounted(() => {
  fetchData();
});

onBeforeUnmount(() => {
  closeCamera();
});
</script>

<style scoped>
.patients-wrapper {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

/* Header Card */
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
  color: #7C3AED;
}

.header-title h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1F2937;
}

.btn-add {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
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
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
}

/* Search Card */
.search-card {
  background: white;
  border-radius: 16px;
  padding: 16px 20px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.search-icon {
  color: #9CA3AF;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 15px;
  color: #1F2937;
}

.search-input::placeholder {
  color: #9CA3AF;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #E5E7EB;
  border-top-color: #7C3AED;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Patients Grid */
.patients-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.patient-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: all 0.3s;
  position: relative;
}

.patient-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.15);
}

.patient-photo {
  width: 100%;
  height: 200px;
  background: linear-gradient(135deg, #7C3AED, #06B6D4);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.patient-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-placeholder {
  color: white;
}

.patient-info {
  padding: 20px;
}

.patient-info h3 {
  margin: 0 0 12px 0;
  font-size: 20px;
  font-weight: 700;
  color: #1F2937;
}

.patient-details {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.detail-badge {
  background: #F3F4F6;
  color: #4B5563;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
}

.detail-badge.species {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
}

.owner-name {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6B7280;
  font-size: 14px;
  margin: 0;
}

.owner-name svg {
  color: #06B6D4;
}

/* ✅ Updated Patient Actions - 3 Buttons */
.patient-actions {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
  padding: 12px 20px;
  border-top: 1px solid #E5E7EB;
}

.btn-view, .btn-edit, .btn-delete {
  color: #EF4444;
}

.btn-delete:hover {
  background: #FEE2E2;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.empty-state svg {
  color: #D1D5DB;
  margin-bottom: 20px;
}

.empty-state h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
  color: #1F2937;
}

.empty-state p {
  color: #6B7280;
  margin: 0 0 24px 0;
}

.btn-empty-action {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
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
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
}

/* Modal Overlay */
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
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
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

.modal-header {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
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
  flex: 1;
}

/* Photo Upload Section */
.photo-upload-section {
  margin-bottom: 24px;
  padding: 24px;
  border: 2px dashed #D1D5DB;
  border-radius: 12px;
  background: #F9FAFB;
}

.photo-preview {
  text-align: center;
  position: relative;
}

.photo-preview img {
  width: 200px;
  height: 200px;
  border-radius: 12px;
  object-fit: cover;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.btn-remove-photo {
  position: absolute;
  top: -8px;
  right: calc(50% - 108px);
  background: #EF4444;
  color: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
  transition: all 0.3s;
}

.btn-remove-photo:hover {
  transform: scale(1.1);
}

.photo-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.btn-camera, .btn-file {
  background: linear-gradient(135deg, #06B6D4, #0891B2);
  color: white;
  border: none;
  padding: 14px 20px;
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

.btn-camera:hover, .btn-file:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(6, 182, 212, 0.3);
}

.file-input {
  display: none;
}

/* Form Grid */
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
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

/* Modal Actions */
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
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
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
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.btn-save:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
}

/* Camera Modal */
.camera-modal {
  background: white;
  border-radius: 20px;
  max-width: 600px;
  width: 100%;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.camera-header {
  background: linear-gradient(135deg, #06B6D4, #0891B2);
  color: white;
  padding: 20px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.camera-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
}

.camera-video {
  width: 100%;
  height: 400px;
  object-fit: cover;
  background: #000;
}

.camera-canvas {
  display: none;
}

.camera-actions {
  padding: 20px;
  background: #F9FAFB;
  display: flex;
  justify-content: center;
}

.btn-capture {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  border: none;
  padding: 14px 32px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.btn-capture:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
}

/* Responsive Design */
@media (max-width: 768px) {
  .patients-wrapper {
    padding: 16px;
  }
  
  .patients-grid {
    grid-template-columns: 1fr;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-group {
    grid-column: 1 / -1;
  }
  
  .photo-buttons {
    grid-template-columns: 1fr;
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
  
  .patient-actions {
    grid-template-columns: 1fr 1fr 1fr;
  }
}
</style>
  background: #F3F4F6;
  border: none;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-view {
  color: #06B6D4;
}

.btn-view:hover {
  background: #CFFAFE;
}

.btn-edit {
  color: #7C3AED;
}

.btn-edit:hover {
  background: #EDE9FE;
}

.btn-delete {