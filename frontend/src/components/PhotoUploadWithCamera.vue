<template>
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-2">Pet Photo</label>
    
    <!-- Photo Preview -->
    <div v-if="photoPreview" class="mb-4">
      <img :src="photoPreview" class="w-40 h-40 object-cover rounded-lg border-2 border-green-500 shadow-lg" alt="Pet photo" />
      <button type="button" @click="removePhoto" class="mt-2 text-sm text-red-600 hover:text-red-800 font-medium">
        🗑️ Remove Photo
      </button>
    </div>

    <!-- Upload Options -->
    <div class="grid grid-cols-2 gap-3 mb-2">
      <!-- Camera Button -->
      <button type="button" @click="openCamera" class="flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors">
        <span class="text-xl">📷</span>
        Take Photo
      </button>

      <!-- File Upload Button -->
      <label class="flex items-center justify-center gap-2 px-4 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium cursor-pointer transition-colors">
        <span class="text-xl">📁</span>
        Choose File
        <input type="file" accept="image/jpeg,image/jpg,image/png" @change="handleFileUpload" class="hidden" ref="fileInput" />
      </label>
    </div>

    <p class="text-xs text-gray-500">JPG or PNG, max 5MB. Auto-resized to 300×300px</p>

    <!-- Camera Modal -->
    <div v-if="showCamera" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4" @click.self="closeCamera">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-2xl" @click.stop>
        <div class="p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-bold text-gray-800">📷 Take Photo</h3>
            <button @click="closeCamera" class="text-gray-500 hover:text-gray-700 text-2xl">×</button>
          </div>

          <!-- Camera View -->
          <div class="relative bg-black rounded-lg overflow-hidden" style="aspect-ratio: 4/3;">
            <video ref="videoElement" autoplay playsinline class="w-full h-full object-cover"></video>
            
            <!-- Camera not available message -->
            <div v-if="cameraError" class="absolute inset-0 flex items-center justify-center bg-gray-900 text-white text-center p-4">
              <div>
                <p class="text-xl mb-2">📷</p>
                <p class="font-medium">Camera not available</p>
                <p class="text-sm mt-2">{{ cameraError }}</p>
              </div>
            </div>
          </div>

          <!-- Capture Button -->
          <div class="mt-4 flex justify-center">
            <button @click="capturePhoto" :disabled="cameraError" class="px-8 py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white rounded-full font-semibold text-lg transition-colors">
              📸 Capture
            </button>
          </div>

          <!-- Hidden canvas for capture -->
          <canvas ref="canvasElement" style="display: none;"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits, onUnmounted } from 'vue';

const emit = defineEmits(['photo-selected']);

const photoPreview = ref(null);
const photoFile = ref(null);
const showCamera = ref(false);
const cameraError = ref(null);
const videoElement = ref(null);
const canvasElement = ref(null);
const fileInput = ref(null);
let mediaStream = null;

// Open Camera
const openCamera = async () => {
  showCamera.value = true;
  cameraError.value = null;

  try {
    // Request camera access
    mediaStream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: 'environment', // Use back camera on mobile
        width: { ideal: 1280 },
        height: { ideal: 720 }
      }
    });

    // Attach stream to video element
    if (videoElement.value) {
      videoElement.value.srcObject = mediaStream;
    }
  } catch (error) {
    console.error('Camera access error:', error);
    cameraError.value = 'Please allow camera access or use file upload instead.';
  }
};

// Close Camera
const closeCamera = () => {
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop());
    mediaStream = null;
  }
  showCamera.value = false;
  cameraError.value = null;
};

// Capture Photo from Camera
const capturePhoto = () => {
  if (!videoElement.value || !canvasElement.value) return;

  const video = videoElement.value;
  const canvas = canvasElement.value;

  // Set canvas size to video size
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  // Draw video frame to canvas
  const context = canvas.getContext('2d');
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  // Convert canvas to blob
  canvas.toBlob((blob) => {
    if (blob) {
      // Create file from blob
      const file = new File([blob], `pet_photo_${Date.now()}.jpg`, { type: 'image/jpeg' });
      processPhoto(file);
      closeCamera();
    }
  }, 'image/jpeg', 0.9);
};

// Handle File Upload
const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    // Validate file size (5MB max)
    if (file.size > 5 * 1024 * 1024) {
      alert('File size must be less than 5MB');
      return;
    }

    // Validate file type
    if (!['image/jpeg', 'image/jpg', 'image/png'].includes(file.type)) {
      alert('Only JPG and PNG files are allowed');
      return;
    }

    processPhoto(file);
  }
};

// Process Photo (resize and preview)
const processPhoto = (file) => {
  photoFile.value = file;

  // Create preview
  const reader = new FileReader();
  reader.onload = (e) => {
    photoPreview.value = e.target.result;
  };
  reader.readAsDataURL(file);

  // Emit photo to parent component
  emit('photo-selected', file);
};

// Remove Photo
const removePhoto = () => {
  photoPreview.value = null;
  photoFile.value = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
  emit('photo-selected', null);
};

// Cleanup on unmount
onUnmounted(() => {
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop());
  }
});

// Expose methods for parent component
defineExpose({
  removePhoto,
  photoFile
});
</script>