<template>
  <div style="min-height: 100vh; background: linear-gradient(135deg, #064e3b 0%, #047857 50%, #065f46 100%); padding: 24px;">
    <!-- Header -->
    <div style="background: linear-gradient(90deg, #064e3b 0%, #065f46 100%); color: white; border-radius: 24px; padding: 32px; margin-bottom: 32px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
          <h1 style="font-size: 36px; font-weight: bold; margin-bottom: 8px;">🐾 Sri Adithya Pet Clinic</h1>
          <p style="color: #a7f3d0; font-size: 16px;">Dr. A. Balasubramanian, B.V.Sc, MBA</p>
        </div>
        <div style="text-align: right;">
          <p style="font-size: 14px; margin-bottom: 4px;">{{ currentDate }}</p>
          <p style="font-size: 12px; color: #a7f3d0;">Dogger 2.0</p>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-bottom: 32px;">
      <div style="background: white; border-radius: 16px; padding: 24px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3); border: 2px solid #047857;">
        <p style="color: #6b7280; font-size: 14px; margin-bottom: 8px;">Total Patients</p>
        <p style="font-size: 40px; font-weight: bold; color: #047857;">{{ stats.totalPatients }}</p>
      </div>
      <div style="background: white; border-radius: 16px; padding: 24px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3); border: 2px solid #2563eb;">
        <p style="color: #6b7280; font-size: 14px; margin-bottom: 8px;">Today's Visits</p>
        <p style="font-size: 40px; font-weight: bold; color: #2563eb;">{{ stats.todayVisits }}</p>
      </div>
      <div style="background: white; border-radius: 16px; padding: 24px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3); border: 2px solid #9333ea;">
        <p style="color: #6b7280; font-size: 14px; margin-bottom: 8px;">Vaccinations Due</p>
        <p style="font-size: 40px; font-weight: bold; color: #9333ea;">{{ stats.vaccinationsDue }}</p>
      </div>
      <div style="background: white; border-radius: 16px; padding: 24px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3); border: 2px solid #ea580c;">
        <p style="color: #6b7280; font-size: 14px; margin-bottom: 8px;">Pending Payments</p>
        <p style="font-size: 40px; font-weight: bold; color: #ea580c;">₹{{ stats.pendingAmount }}</p>
      </div>
    </div>

    <!-- Action Buttons -->
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px;">
      <button @click="$router.push('/patients')" 
        style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 32px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4); border: none; cursor: pointer; transition: all 0.3s;">
        <div style="font-size: 48px; margin-bottom: 12px;">➕</div>
        <div style="font-weight: bold; font-size: 18px; margin-bottom: 4px;">Add Patient</div>
        <div style="font-size: 14px; opacity: 0.9;">Register new pet</div>
      </button>

      <button @click="$router.push('/patients')" 
        style="background: linear-gradient(135deg, #a855f7 0%, #9333ea 100%); color: white; padding: 32px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(168, 85, 247, 0.4); border: none; cursor: pointer; transition: all 0.3s;">
        <div style="font-size: 48px; margin-bottom: 12px;">👥</div>
        <div style="font-weight: bold; font-size: 18px; margin-bottom: 4px;">View Patients</div>
        <div style="font-size: 14px; opacity: 0.9;">Browse all records</div>
      </button>

      <button @click="showSearch = true" 
        style="background: linear-gradient(135deg, #ec4899 0%, #db2777 100%); color: white; padding: 32px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(236, 72, 153, 0.4); border: none; cursor: pointer; transition: all 0.3s;">
        <div style="font-size: 48px; margin-bottom: 12px;">🔍</div>
        <div style="font-weight: bold; font-size: 18px; margin-bottom: 4px;">Search</div>
        <div style="font-size: 14px; opacity: 0.9;">Find patient records</div>
      </button>

      <button @click="$router.push('/vaccinations')" 
        style="background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); color: white; padding: 32px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(249, 115, 22, 0.4); border: none; cursor: pointer; transition: all 0.3s;">
        <div style="font-size: 48px; margin-bottom: 12px;">💉</div>
        <div style="font-weight: bold; font-size: 18px; margin-bottom: 4px;">Vaccinations</div>
        <div style="font-size: 14px; opacity: 0.9;">Track immunizations</div>
      </button>
    </div>

    <!-- Recent Activity -->
    <div style="background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-radius: 24px; padding: 32px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3); border: 2px solid #047857;">
      <h2 style="font-size: 24px; font-weight: bold; color: #1f2937; margin-bottom: 24px; display: flex; align-items: center;">
        <span style="margin-right: 12px;">🕐</span> Recent Activity
      </h2>
      
      <!-- Patient List -->
      <div v-if="loading" style="text-align: center; padding: 40px; color: #6b7280;">
        Loading patients...
      </div>
      
      <div v-else-if="recentPatients.length === 0" style="text-align: center; padding: 40px; color: #6b7280;">
        No patients yet. Add your first patient!
      </div>

      <div v-else style="display: flex; flex-direction: column; gap: 16px;">
        <div v-for="patient in recentPatients" :key="patient.id"
          @click="$router.push('/patients')"
          style="display: flex; align-items: center; justify-content: space-between; padding: 16px; background: linear-gradient(90deg, #a7f3d0 0%, #6ee7b7 100%); border-radius: 12px; cursor: pointer; transition: all 0.3s;">
          <div style="display: flex; align-items: center; gap: 16px;">
            <div style="background: #047857; width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px;">
              {{ patient.species === 'dog' ? '🐕' : patient.species === 'cat' ? '🐱' : '🐾' }}
            </div>
            <div>
              <p style="font-weight: bold; color: #1f2937; margin-bottom: 4px;">{{ patient.pet_name }}</p>
              <p style="font-size: 14px; color: #4b5563;">{{ patient.breed || patient.species.toUpperCase() }} • Owner: {{ patient.owner_name }}</p>
            </div>
          </div>
          <div style="text-align: right;">
            <p style="font-size: 12px; color: #6b7280;">{{ formatDate(patient.created_at) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Search Dialog -->
    <div v-if="showSearch" @click="showSearch = false"
      style="position: fixed; inset: 0; background: rgba(0, 0, 0, 0.7); display: flex; align-items: center; justify-content: center; z-index: 50;">
      <div @click.stop style="background: white; border-radius: 16px; padding: 32px; max-width: 448px; width: 100%; margin: 16px;">
        <h2 style="font-size: 24px; font-weight: bold; margin-bottom: 16px;">Search Patients</h2>
        <input v-model="searchQuery" type="text"
          style="width: 100%; padding: 12px 16px; border: 2px solid #e5e7eb; border-radius: 12px; margin-bottom: 16px; font-size: 16px;"
          placeholder="Enter patient name"
          @keyup.enter="doSearch">
        <div style="display: flex; gap: 12px;">
          <button @click="doSearch" 
            style="flex: 1; background: #047857; color: white; padding: 12px; border-radius: 12px; font-weight: 600; border: none; cursor: pointer;">
            Search
          </button>
          <button @click="showSearch = false" 
            style="padding: 12px 24px; border: 2px solid #d1d5db; border-radius: 12px; background: white; cursor: pointer;">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../services/api';

const patients = ref([]);
const consultations = ref([]);
const payments = ref([]);
const vaccinations = ref([]);
const loading = ref(false);
const showSearch = ref(false);
const searchQuery = ref('');

const currentDate = computed(() => {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const now = new Date();
  return `${days[now.getDay()]}, ${months[now.getMonth()]} ${now.getDate()}, ${now.getFullYear()}`;
});

const stats = computed(() => {
  const patientsData = patients.value.results || patients.value;
  const consultationsData = consultations.value.results || consultations.value;
  const paymentsData = payments.value.results || payments.value;
  const vaccinationsData = vaccinations.value.results || vaccinations.value;
  
  const patientsArray = Array.isArray(patientsData) ? patientsData : [];
  const consultationsArray = Array.isArray(consultationsData) ? consultationsData : [];
  const paymentsArray = Array.isArray(paymentsData) ? paymentsData : [];
  const vaccinationsArray = Array.isArray(vaccinationsData) ? vaccinationsData : [];

  const today = new Date().toISOString().split('T')[0];
  const now = new Date();
  const oneWeek = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);

  return {
    totalPatients: patientsArray.length,
    todayVisits: consultationsArray.filter(c => c.visit_date.split('T')[0] === today).length,
    vaccinationsDue: vaccinationsArray.filter(v => {
      if (!v.next_due_date) return false;
      const due = new Date(v.next_due_date);
      return due >= now && due <= oneWeek;
    }).length,
    pendingAmount: paymentsArray.filter(p => p.payment_status === 'pending').reduce((sum, p) => sum + parseFloat(p.amount || 0), 0).toFixed(0)
  };
});

const recentPatients = computed(() => {
  const patientsData = patients.value.results || patients.value;
  const patientsArray = Array.isArray(patientsData) ? patientsData : [];
  return patientsArray.slice(0, 5);
});

const fetchAllData = async () => {
  loading.value = true;
  try {
    const [patientsRes, consultationsRes, paymentsRes, vaccinationsRes] = await Promise.all([
      api.get('/patients/'),
      api.get('/medical-records/'),
      api.get('/payments/'),
      api.get('/vaccinations/')
    ]);

    patients.value = patientsRes.data;
    consultations.value = consultationsRes.data;
    payments.value = paymentsRes.data;
    vaccinations.value = vaccinationsRes.data;
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  return `${months[date.getMonth()]} ${date.getDate()}`;
};

const doSearch = () => {
  if (searchQuery.value.trim()) {
    // Simple search - just navigate to patients page
    // You can enhance this to filter by search query
    showSearch.value = false;
    searchQuery.value = '';
  }
};

onMounted(() => {
  fetchAllData();
});
</script>