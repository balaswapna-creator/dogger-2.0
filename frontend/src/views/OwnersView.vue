<template>
  <div class="p-6">
    <!-- Header with White Background -->
    <div class="bg-white rounded-xl shadow-md px-6 py-4 mb-6">
      <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold text-emerald-700">Pet Owners</h1>
        <button
          @click="showAddModal = true"
          class="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
        >
          + Add Owner
        </button>
      </div>
    </div>

    <!-- Search Bar -->
    <div class="bg-white rounded-xl shadow-md p-4 mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search by name, phone, email..."
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
      />
    </div>

    <!-- Owners Table -->
    <div class="bg-white rounded-xl shadow-md overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-emerald-50 border-b border-emerald-100">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-semibold text-emerald-700 uppercase tracking-wider">Name</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-emerald-700 uppercase tracking-wider">Phone</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-emerald-700 uppercase tracking-wider">Email</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-emerald-700 uppercase tracking-wider">Address</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-emerald-700 uppercase tracking-wider">City</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-emerald-700 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="owner in filteredOwners" :key="owner.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ owner.name }}</td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ owner.phone }}</td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ owner.email || '-' }}</td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ owner.address || '-' }}</td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ owner.city || 'Cumbum' }}</td>
              <td class="px-6 py-4 text-sm">
                <button
                  @click="editOwner(owner)"
                  class="text-emerald-600 hover:text-emerald-800 font-medium mr-3"
                >
                  Edit
                </button>
                <button
                  @click="deleteOwner(owner.id)"
                  class="text-red-600 hover:text-red-800 font-medium"
                >
                  Delete
                </button>
              </td>
            </tr>
            <tr v-if="filteredOwners.length === 0">
              <td colspan="6" class="px-6 py-8 text-center text-gray-500">
                No owners found
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div
      v-if="showAddModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="bg-emerald-600 text-white px-6 py-4 rounded-t-xl">
          <h2 class="text-xl font-bold">{{ editingOwner ? 'Edit Owner' : 'Add New Owner' }}</h2>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Full Name *</label>
                <input
                  v-model="form.name"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Phone *</label>
                <input
                  v-model="form.phone"
                  type="tel"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  v-model="form.email"
                  type="email"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">WhatsApp Number</label>
                <input
                  v-model="form.whatsapp_number"
                  type="tel"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">City</label>
                <input
                  v-model="form.city"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                />
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">Address</label>
                <textarea
                  v-model="form.address"
                  rows="3"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                ></textarea>
              </div>
            </div>
            <div class="flex justify-end gap-3 mt-6">
              <button
                @click="closeModal"
                type="button"
                class="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                @click="submitForm"
                type="button"
                class="px-6 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg"
              >
                {{ editingOwner ? 'Update' : 'Create' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../services/api';

const owners = ref([]);
const searchQuery = ref('');
const showAddModal = ref(false);
const editingOwner = ref(null);

const form = ref({
  name: '',
  phone: '',
  email: '',
  address: '',
  city: 'Cumbum',
  whatsapp_number: ''
});

const filteredOwners = computed(() => {
  if (!searchQuery.value) return owners.value;
  const query = searchQuery.value.toLowerCase();
  return owners.value.filter(o =>
    o.name?.toLowerCase().includes(query) ||
    o.phone?.includes(query) ||
    o.email?.toLowerCase().includes(query)
  );
});

async function fetchOwners() {
  try {
    const response = await api.get('/owners/');
    owners.value = response.data.results || response.data;
  } catch (error) {
    console.error('Error fetching owners:', error);
  }
}

function editOwner(owner) {
  editingOwner.value = owner;
  form.value = { ...owner };
  showAddModal.value = true;
}

async function deleteOwner(id) {
  if (!confirm('Are you sure you want to delete this owner? This will also delete all their pets!')) return;
  try {
    await api.delete(`/owners/${id}/`);
    await fetchOwners();
  } catch (error) {
    console.error('Error deleting owner:', error);
    alert('Failed to delete owner. They may have existing patients.');
  }
}

async function submitForm() {
  if (!form.value.name || !form.value.phone) {
    alert('Please fill in all required fields (Name, Phone)');
    return;
  }
  
  try {
    if (editingOwner.value) {
      await api.put(`/owners/${editingOwner.value.id}/`, form.value);
    } else {
      await api.post('/owners/', form.value);
    }
    closeModal();
    await fetchOwners();
  } catch (error) {
    console.error('Error saving owner:', error);
    alert('Failed to save owner: ' + (error.response?.data?.detail || error.message));
  }
}

function closeModal() {
  showAddModal.value = false;
  editingOwner.value = null;
  form.value = {
    name: '',
    phone: '',
    email: '',
    address: '',
    city: 'Cumbum',
    whatsapp_number: ''
  };
}

onMounted(() => {
  fetchOwners();
});
</script>