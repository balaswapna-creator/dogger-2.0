<template>
  <div class="p-6">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Reports & Analytics</h1>
      <p class="text-gray-600 mt-1">View clinic statistics and generate reports</p>
    </div>

    <!-- Date Range Selector -->
    <div class="bg-white rounded-lg shadow-sm p-4 mb-6">
      <div class="flex items-center gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">From Date</label>
          <input
            v-model="dateRange.from"
            type="date"
            class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">To Date</label>
          <input
            v-model="dateRange.to"
            type="date"
            class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <button
          @click="loadReports"
          class="mt-6 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          Generate Report
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-gray-600">Loading reports...</p>
    </div>

    <!-- Reports Dashboard -->
    <div v-else class="space-y-6">
      <!-- Key Metrics -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Total Patients</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.totalPatients }}</p>
            </div>
            <div class="text-4xl">🐾</div>
          </div>
          <p class="text-sm text-green-600 mt-2">+{{ stats.newPatients }} this period</p>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Total Visits</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.totalVisits }}</p>
            </div>
            <div class="text-4xl">📋</div>
          </div>
          <p class="text-sm text-blue-600 mt-2">{{ stats.avgVisitsPerDay }} avg/day</p>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Revenue</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">${{ stats.totalRevenue.toFixed(2) }}</p>
            </div>
            <div class="text-4xl">💰</div>
          </div>
          <p class="text-sm text-green-600 mt-2">${{ stats.avgRevenuePerVisit.toFixed(2) }} avg/visit</p>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Pending Payments</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">${{ stats.pendingPayments.toFixed(2) }}</p>
            </div>
            <div class="text-4xl">⏳</div>
          </div>
          <p class="text-sm text-yellow-600 mt-2">{{ stats.pendingCount }} invoices</p>
        </div>
      </div>

      <!-- Species Distribution -->
      <div class="bg-white rounded-lg shadow-sm p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Patient Species Distribution</h2>
        <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div v-for="(count, species) in stats.speciesDistribution" :key="species" class="text-center p-4 bg-gray-50 rounded-lg">
            <div class="text-3xl mb-2">{{ getSpeciesEmoji(species) }}</div>
            <div class="text-lg font-bold text-gray-900">{{ count }}</div>
            <div class="text-sm text-gray-600 capitalize">{{ species }}s</div>
          </div>
        </div>
      </div>

      <!-- Visit Types -->
      <div class="bg-white rounded-lg shadow-sm p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Visit Types Breakdown</h2>
        <div class="space-y-3">
          <div v-for="(data, type) in stats.visitTypes" :key="type" class="flex items-center justify-between">
            <div class="flex items-center gap-3 flex-1">
              <div class="text-sm font-medium text-gray-700 w-32 capitalize">{{ type.replace('-', ' ') }}</div>
              <div class="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
                <div
                  class="h-full rounded-full"
                  :class="getVisitTypeColor(type)"
                  :style="{ width: data.percentage + '%' }"
                ></div>
              </div>
            </div>
            <div class="text-sm font-bold text-gray-900 ml-4 w-20 text-right">
              {{ data.count }} ({{ data.percentage.toFixed(1) }}%)
            </div>
          </div>
        </div>
      </div>

      <!-- Top Patients -->
      <div class="bg-white rounded-lg shadow-sm p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Most Frequent Patients</h2>
        <div class="space-y-3">
          <div v-for="patient in stats.topPatients" :key="patient.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-2xl">
                {{ getSpeciesEmoji(patient.species) }}
              </div>
              <div>
                <div class="font-bold text-gray-900">{{ patient.name }}</div>
                <div class="text-sm text-gray-600">{{ patient.ownerName }}</div>
              </div>
            </div>
            <div class="text-right">
              <div class="text-lg font-bold text-gray-900">{{ patient.visitCount }}</div>
              <div class="text-sm text-gray-600">visits</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Monthly Trend -->
      <div class="bg-white rounded-lg shadow-sm p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Monthly Revenue Trend</h2>
        <div class="h-64 flex items-end gap-2">
          <div
            v-for="(month, index) in stats.monthlyTrend"
            :key="index"
            class="flex-1 bg-blue-500 rounded-t-lg hover:bg-blue-600 transition cursor-pointer relative group"
            :style="{ height: (month.revenue / stats.maxMonthlyRevenue * 100) + '%' }"
          >
            <div class="absolute -top-8 left-1/2 transform -translate-x-1/2 opacity-0 group-hover:opacity-100 transition bg-gray-900 text-white text-xs px-2 py-1 rounded whitespace-nowrap">
              ${{ month.revenue.toFixed(2) }}
            </div>
            <div class="absolute -bottom-6 left-1/2 transform -translate-x-1/2 text-xs text-gray-600">
              {{ month.month }}
            </div>
          </div>
        </div>
        <div class="mt-8 text-center text-sm text-gray-500">Monthly revenue over the past 6 months</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const loading = ref(false)
const dateRange = ref({
  from: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
  to: new Date().toISOString().split('T')[0]
})

const stats = ref({
  totalPatients: 0,
  newPatients: 0,
  totalVisits: 0,
  avgVisitsPerDay: 0,
  totalRevenue: 0,
  avgRevenuePerVisit: 0,
  pendingPayments: 0,
  pendingCount: 0,
  speciesDistribution: {},
  visitTypes: {},
  topPatients: [],
  monthlyTrend: [],
  maxMonthlyRevenue: 0
})

function getSpeciesEmoji(species) {
  const emojis = {
    dog: '🐕',
    cat: '🐈',
    bird: '🐦',
    reptile: '🦎',
    other: '🐾'
  }
  return emojis[species] || '🐾'
}

function getVisitTypeColor(type) {
  const colors = {
    checkup: 'bg-blue-500',
    vaccination: 'bg-green-500',
    surgery: 'bg-red-500',
    emergency: 'bg-orange-500',
    'follow-up': 'bg-purple-500'
  }
  return colors[type] || 'bg-gray-500'
}

async function loadReports() {
  loading.value = true
  try {
    const [patients, records, payments, owners] = await Promise.all([
      api.get('/patients/'),
      api.get('/medical-records/'),
      api.get('/payments/'),
      api.get('/owners/')
    ])

    const patientsData = patients.data
    const recordsData = records.data
    const paymentsData = payments.data
    const ownersData = owners.data

    // Calculate stats
    stats.value.totalPatients = patientsData.length
    stats.value.newPatients = patientsData.filter(p => {
      const created = new Date(p.created_at || p.date_of_birth)
      return created >= new Date(dateRange.value.from) && created <= new Date(dateRange.value.to)
    }).length

    const filteredRecords = recordsData.filter(r => {
      const date = new Date(r.visit_date)
      return date >= new Date(dateRange.value.from) && date <= new Date(dateRange.value.to)
    })

    stats.value.totalVisits = filteredRecords.length
    const days = Math.max(1, Math.ceil((new Date(dateRange.value.to) - new Date(dateRange.value.from)) / (1000 * 60 * 60 * 24)))
    stats.value.avgVisitsPerDay = (filteredRecords.length / days).toFixed(1)

    const filteredPayments = paymentsData.filter(p => {
      const date = new Date(p.payment_date)
      return date >= new Date(dateRange.value.from) && date <= new Date(dateRange.value.to)
    })

    stats.value.totalRevenue = filteredPayments
      .filter(p => p.status === 'paid')
      .reduce((sum, p) => sum + parseFloat(p.amount), 0)

    stats.value.avgRevenuePerVisit = stats.value.totalVisits > 0
      ? stats.value.totalRevenue / stats.value.totalVisits
      : 0

    stats.value.pendingPayments = paymentsData
      .filter(p => p.status === 'pending' || p.status === 'overdue')
      .reduce((sum, p) => sum + parseFloat(p.amount), 0)

    stats.value.pendingCount = paymentsData.filter(p => p.status === 'pending' || p.status === 'overdue').length

    // Species distribution
    const speciesCount = {}
    patientsData.forEach(p => {
      speciesCount[p.species] = (speciesCount[p.species] || 0) + 1
    })
    stats.value.speciesDistribution = speciesCount

    // Visit types
    const visitCount = {}
    filteredRecords.forEach(r => {
      visitCount[r.visit_type] = (visitCount[r.visit_type] || 0) + 1
    })
    const totalVisitsForPercentage = filteredRecords.length || 1
    stats.value.visitTypes = Object.entries(visitCount).reduce((acc, [type, count]) => {
      acc[type] = {
        count,
        percentage: (count / totalVisitsForPercentage) * 100
      }
      return acc
    }, {})

    // Top patients
    const patientVisits = {}
    filteredRecords.forEach(r => {
      patientVisits[r.patient] = (patientVisits[r.patient] || 0) + 1
    })

    stats.value.topPatients = Object.entries(patientVisits)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 5)
      .map(([patientId, count]) => {
        const patient = patientsData.find(p => p.id === parseInt(patientId))
        const owner = ownersData.find(o => o.id === patient?.owner)
        return {
          id: patientId,
          name: patient?.name || 'Unknown',
          species: patient?.species || 'other',
          ownerName: owner ? `${owner.first_name} ${owner.last_name}` : 'Unknown',
          visitCount: count
        }
      })

    // Monthly trend (last 6 months)
    const months = []
    for (let i = 5; i >= 0; i--) {
      const date = new Date()
      date.setMonth(date.getMonth() - i)
      const monthStart = new Date(date.getFullYear(), date.getMonth(), 1)
      const monthEnd = new Date(date.getFullYear(), date.getMonth() + 1, 0)

      const monthPayments = paymentsData.filter(p => {
        const payDate = new Date(p.payment_date)
        return payDate >= monthStart && payDate <= monthEnd && p.status === 'paid'
      })

      const revenue = monthPayments.reduce((sum, p) => sum + parseFloat(p.amount), 0)

      months.push({
        month: date.toLocaleString('default', { month: 'short' }),
        revenue
      })
    }

    stats.value.monthlyTrend = months
    stats.value.maxMonthlyRevenue = Math.max(...months.map(m => m.revenue), 1)

  } catch (err) {
    console.error('Error loading reports:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadReports()
})
</script>