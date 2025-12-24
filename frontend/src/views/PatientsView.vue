<template>
  <div class="min-h-screen bg-gradient-to-br from-emerald-900 via-emerald-700 to-emerald-800 p-6">
    <!-- Simple White Container -->
    <div class="bg-white rounded-xl shadow-lg p-6">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-gray-900">🐕 Patients (Pets)</h1>
        <button 
          @click="openAddModal"
          class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold"
        >
          ➕ Add New Pet
        </button>
      </div>

      <!-- Search -->
      <input 
        v-model="searchQuery"
        type="text" 
        placeholder="🔍 Search pets..."
        class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg mb-6"
      />

      <!-- Loading State -->
      <div v-if="isLoading" class="text-center py-12">
        <div class="text-4xl mb-4">⏳</div>
        <p class="text-gray-600">Loading patients...</p>
      </div>

      <!-- Patients Table -->
      <div v-else-if="filteredPatients.length > 0" class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-emerald-600 text-white">
            <tr>
              <th class="px-4 py-3 text-left">Photo</th>
              <th class="px-4 py-3 text-left">Pet Name</th>
              <th class="px-4 py-3 text-left">Species</th>
              <th class="px-4 py-3 text-left">Breed</th>
              <th class="px-4 py-3 text-left">Owner</th>
              <th class="px-4 py-3 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="patient in filteredPatients" :key="patient.id" class="border-b hover:bg-gray-50">
              <td class="px-4 py-3">
                <img 
                  v-if="getPhotoUrl(patient)" 
                  :src="getPhotoUrl(patient)" 
                  class="w-12 h-12 rounded-full object-cover"
                  alt="Pet photo"
                  @error="handleImageError"
                />
                <div v-else class="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
                  🐾
                </div>
              </td>
              <td class="px-4 py-3 font-semibold">{{ patient.pet_name }}</td>
              <td class="px-4 py-3">{{ patient.species }}</td>
              <td class="px-4 py-3">{{ patient.breed }}</td>
              <td class="px-4 py-3">{{ getOwnerName(patient.owner) }}</td>
              <td class="px-4 py-3">
                <div class="flex gap-2">
                  <button 
                    @click="editPatient(patient)"
                    class="bg-amber-500 hover:bg-amber-600 text-white p-2 rounded"
                    title="Edit"
                  >
                    ✏️
                  </button>
                  <button 
                    @click="deletePatient(patient.id)"
                    class="bg-red-500 hover:bg-red-600 text-white p-2 rounded"
                    title="Delete"
                  >
                    🗑️
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="text-center py-12 text-gray-500">
        <p class="text-xl">🐾 No patients found</p>
        <p class="mt-2">Add your first patient to get started</p>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || editingPatient" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto">
      <div class="bg-white rounded-xl max-w-3xl w-full my-8">
        <!-- Modal Header -->
        <div class="bg-emerald-600 text-white p-6">
          <h2 class="text-2xl font-bold">{{ editingPatient ? 'Edit Pet' : 'Add New Pet' }}</h2>
        </div>
        
        <!-- Modal Body -->
        <div class="p-6 space-y-4 max-h-[70vh] overflow-y-auto">
          <!-- Photo Upload Section -->
          <div class="border-4 border-dashed border-gray-300 rounded-lg p-6 text-center">
            <h3 class="text-lg font-semibold mb-4">📷 Pet Photo</h3>
            
            <!-- Photo Preview -->
            <div v-if="photoPreview" class="mb-4">
              <img :src="photoPreview" class="w-32 h-32 mx-auto rounded-lg object-cover" alt="Preview" />
              <button 
                type="button"
                @click="removePhoto"
                class="mt-2 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
              >
                ✖️ Remove Photo
              </button>
            </div>

            <!-- Photo Buttons -->
            <div v-else class="space-y-3">
              <div>
                <button 
                  type="button"
                  @click="openCamera"
                  class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold w-full"
                >
                  📷 Take Photo with Camera
                </button>
              </div>
              <div>
                <label class="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-lg font-semibold cursor-pointer inline-block w-full">
                  📁 Choose from Files
                  <input 
                    type="file" 
                    @change="handleFileSelect"
                    accept="image/*"
                    class="hidden"
                    ref="fileInput"
                  />
                </label>
              </div>
            </div>
          </div>

          <!-- Owner Selection -->
          <div>
            <label class="block font-semibold mb-2">Owner *</label>
            <select v-model="form.owner" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg">
              <option value="">Select Owner</option>
              <option v-for="owner in owners" :key="owner.id" :value="owner.id">
                {{ owner.name }}
              </option>
            </select>
          </div>

          <!-- Pet Name -->
          <div>
            <label class="block font-semibold mb-2">Pet Name *</label>
            <input v-model="form.pet_name" type="text" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Species -->
            <div>
              <label class="block font-semibold mb-2">Species *</label>
              <select v-model="form.species" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg">
                <option value="">Select Species</option>
                <option value="dog">Dog</option>
                <option value="cat">Cat</option>
                <option value="bird">Bird</option>
                <option value="rabbit">Rabbit</option>
                <option value="other">Other</option>
              </select>
            </div>
            
            <!-- Breed -->
            <div>
              <label class="block font-semibold mb-2">Breed *</label>
              <input v-model="form.breed" type="text" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Gender -->
            <div>
              <label class="block font-semibold mb-2">Gender *</label>
              <select v-model="form.gender" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg">
                <option value="">Select Gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </div>
            
            <!-- Date of Birth -->
            <div>
              <label class="block font-semibold mb-2">Date of Birth</label>
              <input v-model="form.date_of_birth" type="date" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" />
            </div>
          </div>

          <!-- Color -->
          <div>
            <label class="block font-semibold mb-2">Color</label>
            <input v-model="form.color" type="text" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" placeholder="e.g. Brown, Black, White" />
          </div>

          <!-- Weight -->
          <div>
            <label class="block font-semibold mb-2">Weight (kg)</label>
            <input v-model="form.weight" type="number" step="0.1" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" />
          </div>

          <!-- Medical History -->
          <div>
            <label class="block font-semibold mb-2">Medical History</label>
            <textarea v-model="form.medical_history" rows="2" class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" placeholder="Optional"></textarea>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-3 pt-4">
            <button 
              type="button"
              @click="savePatient"
              class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white py-3 rounded-lg font-semibold"
            >
              💾 Save Pet
            </button>
            <button 
              type="button"
              @click="closeModal"
              class="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-3 rounded-lg font-semibold"
            >
              ✖️ Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Camera Modal -->
    <div v-if="showCamera" class="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 max-w-2xl w-full">
        <h3 class="text-xl font-bold mb-4">📷 Take Photo</h3>
        
        <div class="relative">
          <video ref="videoElement" autoplay playsinline class="w-full rounded-lg"></video>
          <canvas ref="canvasElement" class="hidden"></canvas>
        </div>

        <div class="flex gap-3 mt-4">
          <button 
            type="button"
            @click="capturePhoto"
            class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold"
          >
            📸 Capture Photo
          </button>
          <button 
            type="button"
            @click="closeCamera"
            class="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-3 rounded-lg font-semibold"
          >
            ✖️ Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import api from '../services/api';

// Configuration
const BACKEND_URL = 'http://localhost:8001';
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
    p.breed?.toLowerCase().includes(query)
  );
});

const getPhotoUrl = (patient) => {
  if (!patient.photo) return null;
  
  if (patient.photo.startsWith('http://') && patient.photo.includes(':')) {
    return patient.photo;
  }
  
  if (patient.photo.startsWith('http://localhost/media')) {
    return patient.photo.replace('http://localhost/media', MEDIA_URL);
  }
  
  const photoPath = patient.photo.replace(/^\/+/, '');
  return `${MEDIA_URL}${photoPath}`;
};

const handleImageError = (event) => {
  console.warn('Failed to load image:', event.target.src);
  event.target.style.display = 'none';
};

const getOwnerName = (ownerId) => {
  if (!Array.isArray(owners.value)) return 'Unknown';
  const owner = owners.value.find(o => o.id === ownerId);
  return owner ? owner.name : 'Unknown';
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
    
    console.log('Loaded patients:', patients.value.length);
    console.log('Loaded owners:', owners.value.length);
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
    
    console.log('Uploading new photo:', file.name);
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
  try {
    if (!form.value.owner) {
      alert('Please select an owner');
      return;
    }
    if (!form.value.pet_name) {
      alert('Please enter pet name');
      return;
    }
    if (!form.value.species) {
      alert('Please select species');
      return;
    }
    if (!form.value.breed) {
      alert('Please enter breed');
      return;
    }
    if (!form.value.gender) {
      alert('Please select gender');
      return;
    }
    
    const formData = new FormData();
    
    formData.append('owner', String(form.value.owner));
    formData.append('pet_name', String(form.value.pet_name));
    formData.append('species', String(form.value.species));
    formData.append('breed', String(form.value.breed));
    formData.append('gender', String(form.value.gender));
    
    if (form.value.date_of_birth) {
      formData.append('date_of_birth', String(form.value.date_of_birth));
    }
    if (form.value.color) {
      formData.append('color', String(form.value.color));
    }
    if (form.value.weight) {
      formData.append('weight', String(form.value.weight));
    }
    if (form.value.medical_history) {
      formData.append('medical_history', String(form.value.medical_history));
    }
    
    if (photoFile.value) {
      formData.append('photo', photoFile.value);
      console.log('Sending data:');
      console.log('name:', form.value.pet_name);
      console.log('species:', form.value.species);
      console.log('owner:', form.value.owner);
      console.log('breed:', form.value.breed);
      console.log('gender:', form.value.gender);
    }
    
    if (editingPatient.value) {
      await api.put(`/patients/${editingPatient.value}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      alert('Pet updated successfully! ✅');
    } else {
      await api.post('/patients/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      alert('Pet added successfully! ✅');
    }
    
    closeModal();
    fetchData();
  } catch (error) {
    console.error('Error saving patient:', error);
    console.error('Error response:', error.response?.data);
    
    if (error.response?.data) {
      const errors = error.response.data;
      let errorMsg = 'Failed to save pet:\n';
      Object.keys(errors).forEach(key => {
        errorMsg += `${key}: ${JSON.stringify(errors[key])}\n`;
      });
      alert(errorMsg);
    } else {
      alert('Failed to save pet. Please try again.');
    }
  }
};

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
  if (!confirm('Are you sure you want to delete this pet? This action cannot be undone.')) return;
  
  try {
    await api.delete(`/patients/${id}/`);
    alert('Pet deleted successfully! ✅');
    fetchData();
  } catch (error) {
    console.error('Error deleting patient:', error);
    alert('Failed to delete pet. Please try again.');
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
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

onMounted(() => {
  fetchData();
});

onBeforeUnmount(() => {
  closeCamera();
});
</script>

<style scoped>
video {
  max-height: 400px;
  object-fit: cover;
}

@media (max-width: 768px) {
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
  
  video {
    max-height: 300px;
  }
}
</style>