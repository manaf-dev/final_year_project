<script setup>

import { ref, computed, onMounted } from "vue";
import { useToast } from "vue-toastification";
import apiClient from "@/services/api";
import * as XLSX from "xlsx";

const toast = useToast();

const cohorts = ref([]);
const selectedCohort = ref("");
const scores = ref([]);
const loading = ref(false);
const searchQuery = ref("");

const selectedCohortName = computed(() => {
  const cohort = cohorts.value.find((c) => c.id === selectedCohort.value);
  return cohort ? `${cohort.year} Internship Cohort` : "";
});

const filteredScores = computed(() => {
  if (!searchQuery.value.trim()) return scores.value;
  const q = searchQuery.value.trim().toLowerCase();
  return scores.value.filter((score) => {
    const intern = score.intern;
    const fullName = `${intern.first_name} ${intern.last_name}`.toLowerCase();
    const regNumber = (intern.username || '').toLowerCase();
    const department = (intern.department?.name || '').toLowerCase();
    const phone = (intern.phone || '').toLowerCase();
    return (
      fullName.includes(q) ||
      regNumber.includes(q) ||
      department.includes(q) ||
      phone.includes(q)
    );
  });
});

const loadCohorts = async () => {
  try {
    
    const response = await apiClient.get("internships/cohorts/");
    cohorts.value = response.data;
  } catch (error) {
    console.error("Error loading cohorts:", error);
    toast.error("Failed to load cohorts");
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
    // Use the new grading endpoint
    const response = await apiClient.get(
      `submissions/grades/cohort/${selectedCohort.value}/`
    );
    scores.value = response.data;
  } catch (error) {
    console.error("Error loading scores:", error);
    toast.error(error.response?.data?.detail || 'Error loading cohort scores');
   
    scores.value = [];
  } finally {
    loading.value = false;
  }
};

const calculateTotal = (grade) => {
  // New calculation based on the three components
  const portfolio = grade.portfolio_total || 0;
  const philosophy = grade.teaching_philosophy_score || 0;
  const reflective = grade.reflective_practice_score || 0;
  
  if (portfolio === 0 && philosophy === 0 && reflective === 0) return "N/A";
  
  return portfolio + philosophy + reflective;
};


const getTotalColor = (total) => {
  if (total === "N/A") return "text-gray-500";
  if (total >= 240) return "text-green-600"; // 80% of 300
  if (total >= 180) return "text-blue-600";  // 60% of 300
  if (total >= 120) return "text-yellow-600"; // 40% of 300
  return "text-red-600";
};

const formatScore = (score) => {
  if (score === null || score === undefined) return "Not graded";
  return score;
};

const exportToExcel = () => {
  if (!scores.value.length) {
    toast.warning("No data to export");
    return;
  }

  try {
    // Prepare data for Excel with new structure
    const excelData = scores.value.map((grade) => ({
      "Student ID": grade.intern.username,
      "First Name": grade.intern.first_name,
      "Last Name": grade.intern.last_name,
      Department: grade.intern.department?.name || "N/A",
      "Portfolio (/100)": grade.portfolio_total || 0,
      "Teaching Philosophy (/100)": grade.teaching_philosophy_score || "Not graded",
      "Reflective Practice (/100)": grade.reflective_practice_score || "Not graded",
      "Total (/300)": calculateTotal(grade),
    }));

    // Create workbook and worksheet
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(excelData);

    // Add some styling (column widths) for new structure
    const colWidths = [
      { width: 15 }, // Student ID
      { width: 15 }, // First Name
      { width: 15 }, // Last Name
      { width: 25 }, // Department
      { width: 18 }, // Portfolio (/100)
      { width: 22 }, // Teaching Philosophy (/100)
      { width: 22 }, // Reflective Practice (/100)
      { width: 15 }, // Total (/300)
    ];
    ws["!cols"] = colWidths;

    // Add worksheet to workbook
    XLSX.utils.book_append_sheet(wb, ws, "Intern Grades");

    // Generate filename with cohort and date
    const cohortName = selectedCohortName.value.replace(/\s+/g, "_");
    const date = new Date().toISOString().split("T")[0];
    const filename = `${cohortName}_Grades_${date}.xlsx`;

    // Download file
    XLSX.writeFile(wb, filename);
    toast.success("Grades exported successfully!");
  } catch (error) {
    console.error("Error exporting to Excel:", error);
    toast.error("Failed to export grades");
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
      <!-- Search Input -->
      <div class="mt-6 flex justify-end">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by name, student ID, department, or contact..."
          class="w-full sm:w-80 px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none transition"
        />
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
            {{ selectedCohortName }} - {{ filteredScores.length }} Intern{{
              filteredScores.length !== 1 ? "s" : ""
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
                Portfolio (/100)
              </th>
              <th
                class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Teaching Philosophy (/100)
              </th>
              <th
                class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Reflective Practice (/100)
              </th>
              <th
                class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Total (/300)
              </th>
              <th
                class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
                        <tr
              v-for="intern in scores"
              :key="intern.id"
              class="bg-white border-b hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">
                  {{ intern.intern?.first_name }} {{ intern.intern?.last_name }}
                </div>
                <div class="text-sm text-gray-500">
                  {{ intern.intern?.username }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                {{ intern.portfolio_total || "-" }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                {{ intern.teaching_philosophy_score || "-" }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                {{ intern.reflective_practice_score || "-" }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-medium text-gray-900">
                {{ intern.overall_total || "0" }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
                <router-link
                  :to="{ name: 'comprehensive-grading', params: { intern: intern.intern?.id } }"
                  class="text-indigo-600 hover:text-indigo-900 bg-indigo-100 hover:bg-indigo-200 px-3 py-1 rounded-md text-xs font-medium transition-colors duration-200"
                >
                  Grade
                </router-link>
              </td>
            </tr>
            <tr v-if="filteredScores.length === 0">
              <td colspan="5" class="px-6 py-12 text-center text-gray-500">
                No results match your search.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>


