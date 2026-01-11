<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container mx-auto p-8 max-w-2xl">
      <div class="bg-white rounded-lg shadow-lg p-8">
        <h1 class="text-3xl font-bold mb-2">🔒 Secure Forms Test</h1>
        <p class="text-gray-600 mb-6">Test input sanitization, validation, and file upload security</p>
        
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- XSS Test Input -->
          <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
            <p class="text-sm text-yellow-800">
              <strong>🧪 XSS Test:</strong> Try entering <code class="bg-yellow-100 px-1">&lt;script&gt;alert('XSS')&lt;/script&gt;</code> in the name field
            </p>
          </div>

          <SecureInput
            v-model="formData.name"
            label="Full Name"
            type="text"
            placeholder="Enter your name"
            required
            :minLength="3"
            :maxLength="50"
            hint="Minimum 3 characters, maximum 50"
          />
          
          <!-- Email Validation Test -->
          <div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4">
            <p class="text-sm text-blue-800">
              <strong>📧 Email Test:</strong> Try entering <code class="bg-blue-100 px-1">invalid-email</code> (should fail)
            </p>
          </div>

          <SecureInput
            v-model="formData.email"
            label="Email Address"
            type="email"
            placeholder="you@example.com"
            required
            hint="Must be a valid email format"
          />
          
          <!-- Phone Validation Test -->
          <div class="bg-purple-50 border-l-4 border-purple-400 p-4 mb-4">
            <p class="text-sm text-purple-800">
              <strong>📱 Phone Test:</strong> Try entering <code class="bg-purple-100 px-1">123</code> (should fail)
            </p>
          </div>

          <SecureInput
            v-model="formData.phone"
            label="Phone Number"
            type="tel"
            placeholder="+1234567890"
            required
            hint="Format: +[country code][number] (e.g., +1234567890)"
          />

          <!-- Password Validation Test -->
          <SecureInput
            v-model="formData.password"
            label="Password"
            type="password"
            placeholder="Enter a strong password"
            required
            :minLength="8"
            hint="Minimum 8 characters, must include uppercase, lowercase, number, and special character"
          />
          
          <!-- File Upload Test -->
          <div class="bg-green-50 border-l-4 border-green-400 p-4 mb-4">
            <p class="text-sm text-green-800">
              <strong>📎 File Test:</strong> Try uploading .exe or files larger than 5MB (should fail)
            </p>
          </div>

          <SecureFileUpload
            label="Upload Documents"
            :accept="['pdf', 'doc', 'docx', 'txt']"
            :maxSize="5"
            :multiple="true"
            @update:files="formData.files = $event"
            hint="Allowed: PDF, DOC, DOCX, TXT. Max size: 5MB per file"
          />
          
          <button
            type="submit"
            class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition font-semibold"
          >
            Submit Test Form
          </button>
        </form>
        
        <!-- Success Message -->
        <div v-if="submitted" class="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <h3 class="font-bold text-green-800 mb-2">✅ Form Submitted Successfully!</h3>
          <p class="text-sm text-green-700 mb-2">All inputs were sanitized and validated. Check console for details.</p>
          <details class="mt-2">
            <summary class="cursor-pointer text-sm font-semibold text-green-800 hover:text-green-900">
              View Sanitized Data
            </summary>
            <pre class="text-xs bg-white p-3 rounded mt-2 overflow-auto">{{ JSON.stringify(sanitizedData, null, 2) }}</pre>
          </details>
        </div>

        <!-- Back to Dashboard -->
        <div class="mt-6 text-center">
          <router-link
            to="/dashboard"
            class="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            ← Back to Dashboard
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SecureInput from '@/components/SecureInput.vue';
import SecureFileUpload from '@/components/SecureFileUpload.vue';

export default {
  name: 'TestSecureForms',
  components: { 
    SecureInput, 
    SecureFileUpload 
  },
  data() {
    return {
      formData: {
        name: '',
        email: '',
        phone: '',
        password: '',
        files: []
      },
      submitted: false,
      sanitizedData: null
    };
  },
  methods: {
    handleSubmit() {
      // Create a copy for display (excluding sensitive data)
      this.sanitizedData = {
        name: this.formData.name,
        email: this.formData.email,
        phone: this.formData.phone,
        password: '***REDACTED***',
        filesCount: this.formData.files.length,
        files: this.formData.files.map(f => ({
          name: f.name,
          size: `${(f.size / 1024).toFixed(2)} KB`,
          type: f.type
        }))
      };

      console.log('✅ Form submitted with sanitized data:', this.sanitizedData);
      console.log('🔒 Original form data:', this.formData);
      
      this.submitted = true;
      
      // Hide success message after 10 seconds
      setTimeout(() => {
        this.submitted = false;
      }, 10000);
    }
  }
};
</script>