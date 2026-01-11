<template>
  <div class="file-upload-container">
    <label v-if="label" class="block font-medium mb-2">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    
    <div
      class="border-2 border-dashed rounded-lg p-6 text-center transition-colors"
      :class="{
        'border-blue-500 bg-blue-50': isDragging,
        'border-gray-300 hover:border-gray-400': !isDragging && !error,
        'border-red-500 bg-red-50': error
      }"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave"
      @drop.prevent="handleDrop"
    >
      <input
        ref="fileInput"
        type="file"
        :accept="acceptString"
        :multiple="multiple"
        @change="handleFileSelect"
        class="hidden"
      />
      
      <div v-if="!selectedFiles.length" class="cursor-pointer" @click="$refs.fileInput.click()">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        <p class="mt-2 text-sm text-gray-600">
          Drag and drop files here, or click to select
        </p>
        <p class="text-xs text-gray-500 mt-1">
          {{ acceptHint }}
        </p>
      </div>
      
      <div v-else class="space-y-2">
        <div
          v-for="(file, index) in selectedFiles"
          :key="index"
          class="flex items-center justify-between bg-white p-3 rounded border"
          :class="{ 'border-red-300': file.error, 'border-gray-200': !file.error }"
        >
          <div class="flex items-center space-x-3 flex-1">
            <svg class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">
                {{ file.sanitizedName || file.name }}
              </p>
              <p class="text-xs text-gray-500">
                {{ formatFileSize(file.size) }}
              </p>
              <p v-if="file.error" class="text-xs text-red-500 mt-1">
                {{ file.error }}
              </p>
            </div>
          </div>
          
          <button
            @click="removeFile(index)"
            class="text-red-500 hover:text-red-700 p-1"
            type="button"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <button
          v-if="multiple"
          @click="$refs.fileInput.click()"
          class="text-blue-600 hover:text-blue-700 text-sm font-medium"
          type="button"
        >
          + Add more files
        </button>
      </div>
    </div>
    
    <p v-if="error && !selectedFiles.length" class="text-red-500 text-sm mt-2">
      {{ error }}
    </p>
    
    <p v-if="hint" class="text-gray-500 text-sm mt-2">
      {{ hint }}
    </p>
  </div>
</template>

<script>
import { FileUploadValidator } from '@/utils/security';

export default {
  name: 'SecureFileUpload',
  
  props: {
    label: {
      type: String,
      default: ''
    },
    accept: {
      type: Array,
      default: () => FileUploadValidator.ALLOWED_ALL_TYPES
    },
    maxSize: {
      type: Number,
      default: 10 // MB
    },
    multiple: {
      type: Boolean,
      default: false
    },
    required: {
      type: Boolean,
      default: false
    },
    hint: {
      type: String,
      default: ''
    }
  },
  
  emits: ['update:files', 'validate'],
  
  data() {
    return {
      selectedFiles: [],
      isDragging: false,
      error: null
    };
  },
  
  computed: {
    acceptString() {
      return this.accept.map(ext => `.${ext}`).join(',');
    },
    
    acceptHint() {
      return `Accepted: ${this.accept.join(', ')} (max ${this.maxSize}MB)`;
    }
  },
  
  methods: {
    handleDragOver() {
      this.isDragging = true;
    },
    
    handleDragLeave() {
      this.isDragging = false;
    },
    
    handleDrop(event) {
      this.isDragging = false;
      const files = Array.from(event.dataTransfer.files);
      this.processFiles(files);
    },
    
    handleFileSelect(event) {
      const files = Array.from(event.target.files);
      this.processFiles(files);
    },
    
    processFiles(files) {
      this.error = null;
      
      // If not multiple, replace existing files
      if (!this.multiple && files.length > 0) {
        this.selectedFiles = [];
      }
      
      // Validate each file
      for (const file of files) {
        const validation = FileUploadValidator.validateFile(file, {
          allowedTypes: this.accept,
          maxSize: this.maxSize
        });
        
        if (validation.valid) {
          this.selectedFiles.push({
            ...file,
            sanitizedName: validation.sanitizedName,
            error: null
          });
        } else {
          this.selectedFiles.push({
            ...file,
            sanitizedName: validation.sanitizedName,
            error: validation.error
          });
        }
      }
      
      // Check if required and no valid files
      if (this.required && this.selectedFiles.length === 0) {
        this.error = 'At least one file is required';
      }
      
      this.emitFiles();
    },
    
    removeFile(index) {
      this.selectedFiles.splice(index, 1);
      this.error = null;
      
      // Check required validation
      if (this.required && this.selectedFiles.length === 0) {
        this.error = 'At least one file is required';
      }
      
      this.emitFiles();
    },
    
    emitFiles() {
      const validFiles = this.selectedFiles.filter(f => !f.error);
      const hasErrors = this.selectedFiles.some(f => f.error);
      
      this.$emit('update:files', validFiles);
      this.$emit('validate', {
        valid: !hasErrors && (!this.required || validFiles.length > 0),
        files: validFiles,
        error: this.error
      });
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    },
    
    // Public method for parent validation
    validateField() {
      if (this.required && this.selectedFiles.length === 0) {
        this.error = 'At least one file is required';
        return false;
      }
      
      const hasErrors = this.selectedFiles.some(f => f.error);
      return !hasErrors;
    }
  }
};
</script>

<style scoped>
.file-upload-container {
  margin-bottom: 1rem;
}
</style>