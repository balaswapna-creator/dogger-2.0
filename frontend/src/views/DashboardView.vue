<template>
  <div class="dashboard-wrapper">
    <!-- ✅ NO HEADER - Content starts directly -->
    <div class="dashboard-container">
      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card patients-card">
          <div class="stat-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
            </svg>
          </div>
          <div class="stat-content">
            <h3>{{ stats.totalPatients }}</h3>
            <p>Total Patients</p>
          </div>
        </div>

        <div class="stat-card owners-card">
          <div class="stat-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </div>
          <div class="stat-content">
            <h3>{{ stats.totalOwners }}</h3>
            <p>Pet Owners</p>
          </div>
        </div>

        <div class="stat-card appointments-card">
          <div class="stat-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
          </div>
          <div class="stat-content">
            <h3>{{ stats.todayAppointments }}</h3>
            <p>Today's Appointments</p>
          </div>
        </div>

        <div class="stat-card revenue-card">
          <div class="stat-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="1" x2="12" y2="23"></line>
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
            </svg>
          </div>
          <div class="stat-content">
            <h3>₹{{ stats.monthlyRevenue }}</h3>
            <p>Monthly Revenue</p>
          </div>
        </div>
      </div>

      <!-- Quick Actions & Recent Activity -->
      <div class="content-grid">
        <!-- Quick Actions -->
        <div class="card quick-actions-card">
          <div class="card-header">
            <h2>Quick Actions</h2>
          </div>
          <div class="card-body">
            <div class="action-buttons">
              <button @click="$router.push('/patients')" class="action-btn add-patient">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                <span>Add New Patient</span>
              </button>
              
              <button @click="$router.push('/owners')" class="action-btn add-owner">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="8.5" cy="7" r="4"></circle>
                  <line x1="20" y1="8" x2="20" y2="14"></line>
                  <line x1="23" y1="11" x2="17" y2="11"></line>
                </svg>
                <span>Add Owner</span>
              </button>
              
              <button @click="$router.push('/vaccinations')" class="action-btn vaccination">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path>
                  <path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"></path>
                  <path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"></path>
                  <path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"></path>
                </svg>
                <span>Record Vaccination</span>
              </button>
              
              <button @click="$router.push('/payments')" class="action-btn payment">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
                  <line x1="1" y1="10" x2="23" y2="10"></line>
                </svg>
                <span>Add Payment</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="card recent-activity-card">
          <div class="card-header">
            <h2>Recent Activity</h2>
          </div>
          <div class="card-body">
            <div v-if="recentActivity.length === 0" class="no-activity">
              <p>No recent activity</p>
            </div>
            <div v-else class="activity-list">
              <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
                <div class="activity-icon" :class="activity.type">
                  <svg v-if="activity.type === 'owner'" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                  </svg>
                  <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <circle cx="12" cy="12" r="10"/>
                  </svg>
                </div>
                <div class="activity-content">
                  <p class="activity-title">{{ activity.title }}</p>
                  <p class="activity-time">{{ activity.time }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Patients Table -->
      <div class="card recent-patients-card">
        <div class="card-header">
          <h2>Recent Patients</h2>
          <button @click="$router.push('/patients')" class="view-all-btn">View All</button>
        </div>
        <div class="card-body">
          <div v-if="recentPatients.length === 0" class="no-data">
            <p>No patients yet. Add your first patient!</p>
          </div>
          <div v-else class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Patient Name</th>
                  <th>Species</th>
                  <th>Owner</th>
                  <th>Last Visit</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="patient in recentPatients" :key="patient.id">
                  <td>
                    <div class="patient-name">
                      <div class="patient-avatar">{{ getFirstChar(patient.pet_name) }}</div>
                      <span>{{ patient.pet_name }}</span>
                    </div>
                  </td>
                  <td>{{ patient.species }}</td>
                  <td>{{ patient.owner_name || 'N/A' }}</td>
                  <td>{{ formatDate(patient.last_visit) }}</td>
                  <td>
                    <button @click="viewPatient(patient.id)" class="btn-view">View</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../services/api'

export default {
  name: 'DashboardView',
  setup() {
    const stats = ref({
      totalPatients: 0,
      totalOwners: 0,
      todayAppointments: 0,
      monthlyRevenue: '0'
    })
    const recentPatients = ref([])
    const recentActivity = ref([])

    const fetchDashboardData = async () => {
      try {
        const dashboardRes = await api.get('/dashboard/')
        
        if (dashboardRes.data) {
          stats.value = {
            totalPatients: dashboardRes.data.total_patients || 0,
            totalOwners: dashboardRes.data.total_owners || 0,
            todayAppointments: dashboardRes.data.consultations_this_week || 0,
            monthlyRevenue: (dashboardRes.data.revenue_this_month || 0).toFixed(2)
          }
        }

        const patientsRes = await api.get('/patients/')
        const patientsData = patientsRes.data || []
        const patients = Array.isArray(patientsData) 
          ? patientsData 
          : (patientsData.results || [])
        
        recentPatients.value = Array.isArray(patients) 
          ? patients.slice(0, 5) 
          : []

        const ownersRes = await api.get('/owners/')
        const ownersData = ownersRes.data || []
        const owners = Array.isArray(ownersData) 
          ? ownersData 
          : (ownersData.results || [])

        if (Array.isArray(owners) && owners.length > 0) {
          recentActivity.value = owners.slice(0, 3).map(owner => ({
            id: `owner-${owner.id}`,
            type: 'owner',
            title: `${owner.name} - ${owner.phone}`,
            time: 'Recently added'
          }))
        }

      } catch (error) {
        console.error('Error fetching dashboard data:', error)
        stats.value = {
          totalPatients: 0,
          totalOwners: 0,
          todayAppointments: 0,
          monthlyRevenue: '0'
        }
      }
    }

    const getFirstChar = (str) => {
      if (!str || typeof str !== 'string') return '?'
      return str.charAt(0).toUpperCase()
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'Never'
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })
      } catch (e) {
        return 'Invalid'
      }
    }

    const viewPatient = (id) => {
      window.location.href = `/patients/${id}`
    }

    onMounted(() => {
      fetchDashboardData()
    })

    return {
      stats,
      recentPatients,
      recentActivity,
      getFirstChar,
      formatDate,
      viewPatient
    }
  }
}
</script>

<style scoped>
.dashboard-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
}

/* Dashboard Container */
.dashboard-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #7C3AED, #06B6D4);
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.15);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.patients-card .stat-icon { background: linear-gradient(135deg, #7C3AED, #5B21B6); }
.owners-card .stat-icon { background: linear-gradient(135deg, #06B6D4, #0891B2); }
.appointments-card .stat-icon { background: linear-gradient(135deg, #8B5CF6, #7C3AED); }
.revenue-card .stat-icon { background: linear-gradient(135deg, #14B8A6, #0D9488); }

.stat-content h3 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1F2937;
}

.stat-content p {
  margin: 4px 0 0 0;
  font-size: 13px;
  color: #6B7280;
  font-weight: 500;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

/* Card Styling */
.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  overflow: hidden;
}

.card-header {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.view-all-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s;
}

.view-all-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.card-body {
  padding: 20px;
}

/* Quick Actions */
.action-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.action-btn {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  border: none;
  padding: 14px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 3px 10px rgba(124, 58, 237, 0.25);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(124, 58, 237, 0.35);
}

.action-btn.add-owner { background: linear-gradient(135deg, #06B6D4, #0891B2); }
.action-btn.vaccination { background: linear-gradient(135deg, #8B5CF6, #7C3AED); }
.action-btn.payment { background: linear-gradient(135deg, #14B8A6, #0D9488); }

/* Recent Activity */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  border-radius: 8px;
  transition: background 0.2s;
}

.activity-item:hover {
  background: #F9FAFB;
}

.activity-icon {
  width: 38px;
  height: 38px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.activity-icon.owner { background: linear-gradient(135deg, #06B6D4, #0891B2); }

.activity-content {
  flex: 1;
}

.activity-title {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #1F2937;
}

.activity-time {
  margin: 3px 0 0 0;
  font-size: 12px;
  color: #9CA3AF;
}

/* Table Styling */
.table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
}

.data-table th {
  padding: 14px;
  text-align: left;
  font-weight: 600;
  font-size: 13px;
}

.data-table td {
  padding: 14px;
  border-bottom: 1px solid #E5E7EB;
  font-size: 13px;
  color: #374151;
}

.data-table tbody tr:hover {
  background: #F9FAFB;
}

.patient-name {
  display: flex;
  align-items: center;
  gap: 10px;
}

.patient-avatar {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
}

.btn-view {
  background: linear-gradient(135deg, #7C3AED, #5B21B6);
  color: white;
  border: none;
  padding: 7px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-view:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(124, 58, 237, 0.25);
}

.no-data, .no-activity {
  text-align: center;
  padding: 30px;
  color: #9CA3AF;
}

/* Responsive */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 16px;
  }
  
  .stats-grid {
    gap: 12px;
    margin-bottom: 16px;
  }
  
  .content-grid {
    grid-template-columns: 1fr;
    gap: 16px;
    margin-bottom: 16px;
  }
  
  .action-buttons {
    grid-template-columns: 1fr;
  }
}
</style>