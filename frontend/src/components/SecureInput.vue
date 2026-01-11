<template>
  <div class="form-group">
    <label v-if="label" :for="id" class="form-label">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      :maxlength="maxLength"
      @input="handleInput"
      @blur="handleBlur"
      class="form-input w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      :class="{
        'border-red-500': error,
        'border-gray-300': !error,
        'bg-gray-100': disabled
      }"
    />
    
    <p v-if="error" class="text-red-500 text-sm mt-1">
      {{ error }}
    </p>
    
    <p v-else-if="hint" class="text-gray-500 text-sm mt-1">
      {{ hint }}
    </p>
  </div>
</template>

<script>
import { InputSanitizer, InputValidator } from '@/utils/security';

export default {
  name: 'SecureInput',
  
  props: {
    modelValue: {
      type: [String, Number],
      default: ''
    },
    label: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: 'text',
      validator: (value) => ['text', 'email', 'password', 'number', 'tel', 'url', 'date'].includes(value)
    },
    placeholder: {
      type: String,
      default: ''
    },
    required: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    },
    maxLength: {
      type: Number,
      default: null
    },
    minLength: {
      type: Number,
      default: null
    },
    hint: {
      type: String,
      default: ''
    },
    validateOn: {
      type: String,
      default: 'blur', // 'input' or 'blur'
      validator: (value) => ['input', 'blur'].includes(value)
    }
  },
  
  emits: ['update:modelValue', 'validate'],
  
  data() {
    return {
      error: null,
      touched: false
    };
  },
  
  computed: {
    id() {
      return `input-${this.label?.replace(/\s+/g, '-').toLowerCase() || Math.random().toString(36).substr(2, 9)}`;
    }
  },
  
  methods: {
    handleInput(event) {
      let value = event.target.value;
      
      // Sanitize input based on type
      if (this.type === 'email' || this.type === 'text' || this.type === 'tel') {
        value = InputSanitizer.sanitizeInput(value);
      } else if (this.type === 'url') {
        value = InputSanitizer.sanitizeInput(value);
      }
      
      this.$emit('update:modelValue', value);
      
      // Validate on input if configured
      if (this.validateOn === 'input' && this.touched) {
        this.validate(value);
      }
    },
    
    handleBlur(event) {
      this.touched = true;
      const value = event.target.value;
      
      // Always validate on blur
      this.validate(value);
    },
    
    validate(value) {
      this.error = null;
      
      // Check required
      if (this.required && (!value || value.trim() === '')) {
        this.error = `${this.label || 'This field'} is required`;
        this.$emit('validate', { valid: false, error: this.error });
        return false;
      }
      
      // Skip further validation if empty and not required
      if (!value || value.trim() === '') {
        this.$emit('validate', { valid: true, error: null });
        return true;
      }
      
      // Type-specific validation
      switch (this.type) {
        case 'email':
          if (!InputValidator.isValidEmail(value)) {
            this.error = 'Please enter a valid email address';
          }
          break;
          
        case 'tel':
          if (!InputValidator.isValidPhone(value)) {
            this.error = 'Please enter a valid phone number';
          }
          break;
          
        case 'url':
          if (!InputValidator.isValidURL(value)) {
            this.error = 'Please enter a valid URL';
          }
          break;
          
        case 'number':
          if (isNaN(value)) {
            this.error = 'Please enter a valid number';
          }
          break;
      }
      
      // Length validation
      if (this.minLength && value.length < this.minLength) {
        this.error = `Must be at least ${this.minLength} characters`;
      }
      
      if (this.maxLength && value.length > this.maxLength) {
        this.error = `Must be at most ${this.maxLength} characters`;
      }
      
      const isValid = !this.error;
      this.$emit('validate', { valid: isValid, error: this.error });
      return isValid;
    },
    
    // Public method to trigger validation from parent
    validateField() {
      return this.validate(this.modelValue);
    }
  }
};
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #374151;
}

.form-input {
  transition: all 0.2s ease;
}

.form-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}
</style>