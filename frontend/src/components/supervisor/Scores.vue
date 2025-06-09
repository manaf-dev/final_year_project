<script setup>
/*
 * Scores Component for Supervisor Dashboard
 *
 * Features:
 * - Cohort selection and management
 * - Comprehensive scores table with color-coded grades
 * - Excel export functionality
 * - Sample data for development testing
 *
 * Development Mode:
 * - Automatically loads sample data when NODE_ENV is 'development'
 * - Falls back to sample data if API calls fail
 * - Includes realistic test data with various score scenarios
 */

import { ref, computed, onMounted } from "vue";
import { useToast } from "vue-toastification";
import apiClient from "@/services/api";
import * as XLSX from "xlsx";
import ScoreCell from "./ScoreCell.vue";

const toast = useToast();

// Reactive data
const cohorts = ref([]);
const selectedCohort = ref("");
const scores = ref([]);
const loading = ref(false);

// Sample data for development testing
// const sampleCohorts = [
//   { id: 1, year: 2024 },
//   { id: 2, year: 2023 },
//   { id: 3, year: 2022 },
// ];

const sampleScores = [
  {
    id: 1,
    intern: {
      username: "INT2024001",
      title: "Mr",
      first_name: "John",
      last_name: "Doe",
      department: { name: "Computer Science" },
    },
    month_1: 85,
    month_2: 78,
    month_3: 92,
    month_4: 88,
  },
  {
    id: 2,
    intern: {
      username: "INT2024002",
      title: "Ms",
      first_name: "Jane",
      last_name: "Smith",
      department: { name: "Information Technology" },
    },
    month_1: 72,
    month_2: 85,
    month_3: 79,
    month_4: 83,
  },
  {
    id: 3,
    intern: {
      username: "INT2024003",
      title: "Mr",
      first_name: "Michael",
      last_name: "Johnson",
      department: { name: "Software Engineering" },
    },
    month_1: 95,
    month_2: 91,
    month_3: 88,
    month_4: 94,
  },
  {
    id: 4,
    intern: {
      username: "INT2024004",
      title: "Ms",
      first_name: "Sarah",
      last_name: "Williams",
      department: { name: "Data Science" },
    },
    month_1: 68,
    month_2: 73,
    month_3: 71,
    month_4: 76,
  },
  {
    id: 5,
    intern: {
      username: "INT2024005",
      title: "Mr",
      first_name: "David",
      last_name: "Brown",
      department: { name: "Cybersecurity" },
    },
    month_1: 82,
    month_2: null,
    month_3: 87,
    month_4: null,
  },
  {
    id: 6,
    intern: {
      username: "INT2024006",
      title: "Ms",
      first_name: "Emily",
      last_name: "Davis",
      department: { name: "Computer Science" },
    },
    month_1: 45,
    month_2: 58,
    month_3: 62,
    month_4: 55,
  },
  {
    id: 7,
    intern: {
      username: "INT2024007",
      title: "Mr",
      first_name: "James",
      last_name: "Wilson",
      department: { name: "Information Systems" },
    },
    month_1: null,
    month_2: null,
    month_3: null,
    month_4: null,
  },
  {
    id: 8,
    intern: {
      username: "INT2024008",
      title: "Ms",
      first_name: "Lisa",
      last_name: "Garcia",
      department: { name: "Web Development" },
    },
    month_1: 89,
    month_2: 92,
    month_3: 85,
    month_4: 90,
  },
];

// Computed properties
const selectedCohortName = computed(() => {
  const cohort = cohorts.value.find((c) => c.id === selectedCohort.value);
  return cohort ? `${cohort.year} Internship Cohort` : "";
});

// Methods
const loadCohorts = async () => {
  try {
    // For development, use sample data
    // if (process.env.NODE_ENV === "development") {
    //   cohorts.value = sampleCohorts;
    //   return;
    // }

    // Production API call
    const response = await apiClient.get("internships/cohorts/");
    cohorts.value = response.data;
  } catch (error) {
    console.error("Error loading cohorts:", error);
    toast.error("Failed to load cohorts");
    // Fallback to sample data if API fails
    cohorts.value = sampleCohorts;
  }
};

const loadScores = async () => {
  if (!selectedCohort.value) {
    scores.value = [];
    return;
  }

  loading.value = true;
  try {
    // For development, use sample data
    // if (process.env.NODE_ENV === "development") {
    //   // Simulate API delay
    //   await new Promise((resolve) => setTimeout(resolve, 500));
    //   scores.value = sampleScores;
    //   loading.value = false;
    //   return;
    // }

    // Production API call
    const response = await apiClient.get(
      `submissions/scores/cohort/${selectedCohort.value}/`
    );
    scores.value = response.data;
  } catch (error) {
    console.error("Error loading scores:", error);
    toast.error(error.response.data.detail || 'Error loading cohort scores');
    // Fallback to sample data if API fails
    scores.value = [];
  } finally {
    loading.value = false;
  }
};

const calculateTotal = (score) => {
  const scores = [score.month_1, score.month_2, score.month_3, score.month_4];
  const validScores = scores.filter((s) => s !== null && s !== undefined);

  if (validScores.length === 0) return "N/A";

  const total = validScores.reduce((sum, s) => sum + s, 0);
  return total;
};

const getInitials = (firstName, lastName) => {
  return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
};

const getTotalColor = (total) => {
  if (total === "N/A") return "text-gray-500";
  if (total >= 60) return "text-green-600";
  if (total >= 40) return "text-blue-600";
  if (total >= 20) return "text-yellow-600";
  return "text-red-600";
};

const monthScore = (score) => {
  if (score === null || score === undefined) return "Not graded";
  if (score === -1) return "Not submitted";
  return score;
};

const exportToExcel = () => {
  if (!scores.value.length) {
    toast.warning("No data to export");
    return;
  }

  try {
    // Prepare data for Excel
    const excelData = scores.value.map((score) => ({
      "Student ID": score.intern.username,
      Title: score.intern.title,
      "First Name": score.intern.first_name,
      "Last Name": score.intern.last_name,
      Department: score.intern.department?.name || "N/A",
      "Month 1": monthScore(score.month_1),
      "Month 2": monthScore(score.month_2),
      "Month 3": monthScore(score.month_3),
      "Month 4": monthScore(score.month_4),
      Total: calculateTotal(score),
    }));

    // Create workbook and worksheet
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(excelData);

    // Add some styling (column widths)
    const colWidths = [
      { width: 15 }, // Student ID
      { width: 8 }, // Title
      { width: 15 }, // First Name
      { width: 15 }, // Last Name
      { width: 25 }, // Department
      { width: 10 }, // Month 1
      { width: 10 }, // Month 2
      { width: 10 }, // Month 3
      { width: 10 }, // Month 4
      { width: 10 }, // Total
    ];
    ws["!cols"] = colWidths;

    // Add worksheet to workbook
    XLSX.utils.book_append_sheet(wb, ws, "Intern Scores");

    // Generate filename with cohort and date
    const cohortName = selectedCohortName.value.replace(/\s+/g, "_");
    const date = new Date().toISOString().split("T")[0];
    const filename = `${cohortName}_Scores_${date}.xlsx`;

    // Download file
    XLSX.writeFile(wb, filename);
    toast.success("Scores exported successfully!");
  } catch (error) {
    console.error("Error exporting to Excel:", error);
    toast.error("Failed to export scores");
  }
};

// Lifecycle
onMounted(() => {
  loadCohorts();
});
</script>


<template>
  <div class="p-6">
    <!-- Header Section -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <div
        class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4"
      >
        <div>
          <h1 class="text-2xl font-bold text-gray-800 mb-2">Intern Scores</h1>
          <p class="text-gray-600">
            View and manage intern scores across different cohorts
          </p>
        </div>
        <div class="flex flex-col sm:flex-row gap-3">
          <!-- Cohort Selector -->
          <div class="min-w-[200px]">
            <label
              for="cohort-select"
              class="block text-sm font-medium text-gray-700 mb-1"
            >
              Select Cohort
            </label>
            <select
              id="cohort-select"
              v-model="selectedCohort"
              @change="loadScores"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              <option value="">Select a cohort</option>
              <option
                v-for="cohort in cohorts"
                :key="cohort.id"
                :value="cohort.id"
              >
                {{ cohort.year }} Internship Cohort
              </option>
            </select>
          </div>
          <!-- Export Button -->
          <div class="flex items-end">
            <button
              @click="exportToExcel"
              :disabled="!selectedCohort || loading || scores.length === 0"
              class="px-4 py-2 bg-green text-white rounded-md hover:bg-[#00562e] transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <i class="pi pi-download"></i>
              Export to Excel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-white rounded-lg shadow-md p-12 text-center">
      <div class="flex items-center justify-center mb-4">
        <i class="pi pi-spin pi-spinner text-3xl text-green"></i>
      </div>
      <p class="text-gray-600">Loading scores...</p>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="!selectedCohort"
      class="bg-white rounded-lg shadow-md p-12 text-center"
    >
      <div class="mb-4">
        <i class="pi pi-chart-bar text-6xl text-gray-300"></i>
      </div>
      <h3 class="text-xl font-semibold text-gray-800 mb-2">Select a Cohort</h3>
      <p class="text-gray-600">
        Choose a cohort from the dropdown above to view intern scores
      </p>
    </div>

    <!-- No Scores State -->
    <div
      v-else-if="scores.length === 0 && !loading"
      class="bg-white rounded-lg shadow-md p-12 text-center"
    >
      <div class="mb-4">
        <i class="pi pi-exclamation-triangle text-6xl text-yellow-400"></i>
      </div>
      <h3 class="text-xl font-semibold text-gray-800 mb-2">No Scores Found</h3>
      <p class="text-gray-600">
        No intern scores available for the selected cohort
      </p>
    </div>

    <!-- Scores Table -->
    <div v-else class="bg-white rounded-lg shadow-md overflow-hidden">
      <!-- Table Header Info -->
      <div class="p-4 border-b border-gray-200 bg-gray-50">
        <div class="flex justify-between items-center">
          <h3 class="text-lg font-semibold text-gray-800">
            {{ selectedCohortName }} - {{ scores.length }} Intern{{
              scores.length !== 1 ? "s" : ""
            }}
          </h3>
          <div class="text-sm text-gray-600">
            Last updated: {{ new Date().toLocaleDateString() }}
          </div>
        </div>
      </div>

      <!-- Responsive Table -->
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Intern Details
              </th>
              <th
                class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Month 1 (10)
              </th>
              <th
                class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Month 2 (10)
              </th>
              <th
                class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Month 3 (10)
              </th>
              <th
                class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Month 4 (50)
              </th>
              <th
                class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Total (80)
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="score in scores"
              :key="score.id"
              class="hover:bg-gray-50"
            >
              <!-- Intern Details -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <div
                      class="h-10 w-10 rounded-full bg-green-100 flex items-center justify-center"
                    >
                      <span class="text-sm font-medium text-green-800">
                        {{
                          getInitials(
                            score.intern.first_name,
                            score.intern.last_name
                          )
                        }}
                      </span>
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">
                      {{ score.intern.title }}. {{ score.intern.first_name }}
                      {{ score.intern.last_name }}
                    </div>
                    <div class="text-sm text-gray-500">
                      ID: {{ score.intern.username }}
                    </div>
                    <div class="text-xs text-gray-400">
                      {{ score.intern.department?.name }}
                    </div>
                  </div>
                </div>
              </td>

              <!-- Month Scores -->
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <ScoreCell :score="score.month_1" month="1" />
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <ScoreCell :score="score.month_2" month="2" />
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <ScoreCell :score="score.month_3" month="3" />
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <ScoreCell :score="score.month_4" month="4" />
              </td>

              <!-- Total Score -->
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <div
                  class="text-sm font-semibold"
                  :class="getTotalColor(calculateTotal(score))"
                >
                  {{ calculateTotal(score) }}
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>


