<template>
  <div class="owners-wrapper">
    <!-- Header Card -->
    <div class="header-card">
      <div class="header-content">
        <div class="header-title">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          <h1>Pet Owners</h1>
        </div>
        <button @click="openAddModal" class="btn-add">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          <span>Add Owner</span>
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
        placeholder="Search by name, phone, email, or city..."
        class="search-input"
      />
    </div>

    <!-- Owners Table -->
    <div class="table-card">
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Phone</th>
              <th>Email</th>
              <th>City</th>
              <th>Address</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="owner in filteredOwners" :key="owner.id">
              <td>
                <div class="owner-name">
                  <div class="owner-avatar">{{ owner.name.charAt(0) }}</div>
                  <span>{{ owner.name }}</span>
                </div>
              </td>
              <td>
                <span class="phone-badge">{{ owner.phone }}</span>
              </td>
              <td>{{ owner.email || '-' }}</td>
              <td>
                <span class="city-badge">{{ owner.city || 'Cumbum' }}</span>
              </td>
              <td class="address-cell">{{ owner.address || '-' }}</td>
              <td>
                <div class="action-buttons">
                  <button @click="editOwner(owner)" class="btn-edit" title="Edit">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                  </button>
                  <button @click="deleteOwner(owner.id)" class="btn-delete" title="Delete">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredOwners.length === 0">
              <td colspan="6" class="no-data">
                <div class="empty-state">
                  <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                  </svg>
                  <p>No owners found</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">
        <div class="modal-header">
          <h2>{{ editingOwner ? 'Edit Owner' : 'Add New Owner' }}</h2>
          <button @click="closeModal" class="btn-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="form-grid">
            <div class="form-group">
              <label>Full Name *</label>
              <input v-model="form.name" type="text" placeholder="Enter full name"/>
            </div>

            <div class="form-group">
              <label>Phone Number *</label>
              <input v-model="form.phone" type="tel" placeholder="10-digit mobile number"/>
            </div>

            <div class="form-group">
              <label>Email Address</label>
              <input v-model="form.email" type="email" placeholder="email@example.com"/>
            </div>

            <div class="form-group">
              <label>WhatsApp Number</label>
              <input v-model="form.whatsapp_number" type="tel" placeholder="WhatsApp number"/>
            </div>

            <div class="form-group">
              <label>City</label>
              <input v-model="form.city" type="text" placeholder="City name"/>
            </div>

            <div class="form-group full-width">
              <label>Address</label>
              <textarea v-model="form.address" rows="3" placeholder="Complete address"></textarea>
            </div>
          </div>

          <div class="modal-actions">
            <button @click="closeModal" class="btn-cancel">Cancel</button>
            <button @click="submitForm" class="btn-save">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                <polyline points="17 21 17 13 7 13 7 21"></polyline>
                <polyline points="7 3 7 8 15 8"></polyline>
              </svg>
              {{ editingOwner ? 'Update' : 'Create' }} Owner
            </button>
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
    o.email?.toLowerCase().includes(query) ||
    o.city?.toLowerCase().includes(query)
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

function openAddModal() {
  editingOwner.value = null;
  form.value = {
    name: '',
    phone: '',
    email: '',
    address: '',
    city: 'Cumbum',
    whatsapp_number: ''
  };
  showAddModal.value = true;
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
    alert('Owner deleted successfully!');
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
      alert('Owner updated successfully!');
    } else {
      await api.post('/owners/', form.value);
      alert('Owner created successfully!');
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

<style scoped>
.owners-wrapper {
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
  color: #06B6D4;
}

.header-title h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1F2937;
}

.btn-add {
  background: linear-gradient(135deg, #06B6D4, #0891B2);
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
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(6, 182, 212, 0.4);
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

/* Table Card */
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
  background: linear-gradient(135deg, #06B6D4, #0891B2);
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

.owner-name {
  display: flex;
  align-items: center;
  gap: 12px;
}

.owner-avatar {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #06B6D4, #0891B2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18px;
  flex-shrink: 0;
}

.phone-badge {
  background: #DBEAFE;
  color: #1E40AF;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
}

.city-badge {
  background: #D1FAE5;
  color: #065F46;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
}

.address-cell {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-edit, .btn-delete {
  background: #F3F4F6;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.btn-edit {
  color: #7C3AED;
}

.btn-edit:hover {
  background: #EDE9FE;
}

.btn-delete {
  color: #EF4444;
}

.btn-delete:hover {
  background: #FEE2E2;
}

.no-data {
  text-align: center;
  padding: 60px 20px !important;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.empty-state svg {
  color: #D1D5DB;
}

.empty-state p {
  margin: 0;
  color: #6B7280;
  font-size: 16px;
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
}

.modal-container {
  background: white;
  border-radius: 20px;
  max-width: 700px;
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
  background: linear-gradient(135deg, #06B6D4, #0891B2);
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
}

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
.form-group textarea:focus {
  outline: none;
  border-color: #06B6D4;
  box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1);
}

.form-group textarea {
  resize: vertical;
}

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
  background: linear-gradient(135deg, #06B6D4, #0891B2);
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
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
}

.btn-save:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(6, 182, 212, 0.4);
}

/* Responsive */
@media (max-width: 768px) {
  .form-grid {
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
}
</style>