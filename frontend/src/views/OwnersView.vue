<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const API_BASE_URL = 'https://dogger2-backend.onrender.com'

// Get token from localStorage
const getAuthHeader = () => {
  const token = localStorage.getItem('token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

// State
const owners = ref([])
const searchQuery = ref('')
const isLoading = ref(false)
const error = ref(null)
const showModal = ref(false)
const editingOwner = ref(null)

// Form data
const formData = ref({
  name: '',
  phone: '',
  email: '',
  whatsapp: '',
  city: '',
  address: ''
})

// Computed
const filteredOwners = computed(() => {
  if (!searchQuery.value) return owners.value
  const query = searchQuery.value.toLowerCase()
  return owners.value.filter(owner => 
    owner.name?.toLowerCase().includes(query) ||
    owner.phone?.includes(query) ||
    owner.email?.toLowerCase().includes(query) ||
    owner.city?.toLowerCase().includes(query)
  )
})

// Methods
const fetchOwners = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    console.log('Fetching owners from:', `${API_BASE_URL}/api/owners/`)
    const response = await axios.get(`${API_BASE_URL}/api/owners/`, {
      headers: getAuthHeader()
    })
    console.log('Owners fetched:', response.data)
    owners.value = response.data
  } catch (err) {
    console.error('Error fetching owners:', err)
    error.value = err.response?.data?.detail || 'Failed to fetch owners'
    
    // If unauthorized, redirect to login
    if (err.response?.status === 401) {
      localStorage.clear()
      window.location.href = '/login'
    }
  } finally {
    isLoading.value = false
  }
}

const openModal = (owner = null) => {
  editingOwner.value = owner
  if (owner) {
    formData.value = { ...owner }
  } else {
    resetForm()
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingOwner.value = null
  resetForm()
}

const resetForm = () => {
  formData.value = {
    name: '',
    phone: '',
    email: '',
    whatsapp: '',
    city: '',
    address: ''
  }
}

const saveOwner = async () => {
  error.value = null
  isLoading.value = true

  try {
    if (editingOwner.value) {
      // Update existing owner
      console.log('Updating owner:', editingOwner.value.id)
      await axios.put(
        `${API_BASE_URL}/api/owners/${editingOwner.value.id}/`,
        formData.value,
        { headers: getAuthHeader() }
      )
    } else {
      // Create new owner
      console.log('Creating new owner')
      await axios.post(
        `${API_BASE_URL}/api/owners/`,
        formData.value,
        { headers: getAuthHeader() }
      )
    }
    
    closeModal()
    await fetchOwners()
  } catch (err) {
    console.error('Error saving owner:', err)
    error.value = err.response?.data?.detail || 'Failed to save owner'
    
    if (err.response?.status === 401) {
      localStorage.clear()
      window.location.href = '/login'
    }
  } finally {
    isLoading.value = false
  }
}

const deleteOwner = async (id) => {
  if (!confirm('Are you sure you want to delete this owner?')) return

  isLoading.value = true
  error.value = null

  try {
    console.log('Deleting owner:', id)
    await axios.delete(`${API_BASE_URL}/api/owners/${id}/`, {
      headers: getAuthHeader()
    })
    await fetchOwners()
  } catch (err) {
    console.error('Error deleting owner:', err)
    error.value = err.response?.data?.detail || 'Failed to delete owner'
    
    if (err.response?.status === 401) {
      localStorage.clear()
      window.location.href = '/login'
    }
  } finally {
    isLoading.value = false
  }
}

// Load owners on mount
onMounted(() => {
  fetchOwners()
})
</script>

<template>
  <div class="p-6">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">Owners</h1>
      <button 
        @click="openModal()"
        class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
      >
        + Add Owner
      </button>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
      {{ error }}
    </div>

    <!-- Search Bar -->
    <div class="mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search owners by name, phone, email, or city..."
        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      />
    </div>

    <!-- Loading -->
    <div v-if="isLoading && owners.length === 0" class="text-center py-12">
      <div class="text-gray-500">Loading owners...</div>
    </div>

    <!-- No Owners -->
    <div v-else-if="!isLoading && filteredOwners.length === 0" class="text-center py-12">
      <div class="text-gray-500">
        {{ searchQuery ? 'No owners found matching your search' : 'No owners yet. Click "Add Owner" to get started.' }}
      </div>
    </div>

    <!-- Owners Table -->
    <div v-else class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Phone</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">City</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="owner in filteredOwners" :key="owner.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{{ owner.name }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ owner.phone }}</div>
              <div v-if="owner.whatsapp" class="text-xs text-gray-500">WhatsApp: {{ owner.whatsapp }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ owner.email || 'N/A' }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ owner.city || 'N/A' }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <button 
                @click="openModal(owner)" 
                class="text-blue-600 hover:text-blue-900 mr-4"
              >
                Edit
              </button>
              <button 
                @click="deleteOwner(owner.id)" 
                class="text-red-600 hover:text-red-900"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div 
      v-if="showModal" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-bold text-gray-800">
            {{ editingOwner ? 'Edit Owner' : 'Add New Owner' }}
          </h2>
          <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveOwner" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Full Name *</label>
            <input
              v-model="formData.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="Enter full name"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Phone Number *</label>
            <input
              v-model="formData.phone"
              type="tel"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="10-digit mobile number"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
            <input
              v-model="formData.email"
              type="email"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="email@example.com"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">WhatsApp Number</label>
            <input
              v-model="formData.whatsapp"
              type="tel"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="WhatsApp number"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">City</label>
            <input
              v-model="formData.city"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="Curnburn"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Address</label>
            <textarea
              v-model="formData.address"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="Full address"
            ></textarea>
          </div>

          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="isLoading"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {{ isLoading ? 'Saving...' : (editingOwner ? 'Update Owner' : 'Create Owner') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>