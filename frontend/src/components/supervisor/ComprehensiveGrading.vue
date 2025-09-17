<script setup>
  import apiClient from "@/services/api";
  import { ref, computed, onMounted } from "vue";
  import { useRoute, useRouter } from "vue-router";
  import { useToast } from "vue-toastification";
  import Loader from "../loader.vue";
  import BackButton from "../BackButton.vue";
  import { useNotificationStore } from "@/stores/notifications";

  // Props
  const props = defineProps({
    internId: {
      type: String,
      default: null,
    },
  });

  const route = useRoute();
  const router = useRouter();
  const toast = useToast();
  const notificationStore = useNotificationStore();

  const internGrades = ref({});
  const loading = ref(false);
  const saving = ref(false);

  // Form data for the three components
  const portfolioScores = ref({
    month_1: null,
    month_2: null,
    month_3: null,
    month_4: null,
  });
  const teachingPhilosophyScore = ref(null);
  const reflectivePracticeScore = ref(null);

  const internId = computed(() => props.internId || route.params.intern);

  const loadInternGrades = async () => {
    loading.value = true;
    try {
      const response = await apiClient.get(
        `accounts/interns/${internId.value}/`
      );
      const intern = response.data;

      // Try to get existing grades
      try {
        const gradesResponse = await apiClient.get(
          `submissions/grades/intern/${internId.value}/`
        );
        internGrades.value = gradesResponse.data;

        // Pre-populate form with existing grades
        if (internGrades.value) {
          portfolioScores.value = {
            month_1: internGrades.value.portfolio_month_1,
            month_2: internGrades.value.portfolio_month_2,
            month_3: internGrades.value.portfolio_month_3,
            month_4: internGrades.value.portfolio_month_4,
          };
          teachingPhilosophyScore.value =
            internGrades.value.teaching_philosophy_score;
          reflectivePracticeScore.value =
            internGrades.value.reflective_practice_score;
        }
      } catch (error) {
        // No existing grades found, that's okay
        internGrades.value = { intern };
      }
    } catch (error) {
      console.error("Error loading intern data:", error);
      toast.error("Error loading intern information");
    } finally {
      loading.value = false;
    }
  };

  const updatePortfolioScore = async (month, score) => {
    if (!score || score < 0) return;

    const maxScore = month === 4 ? 40 : 20;
    if (score > maxScore) {
      toast.error(`Score for month ${month} cannot exceed ${maxScore} points`);
      return;
    }

    saving.value = true;
    try {
      await apiClient.post("submissions/grades/portfolio/update/", {
        intern_id: internId.value,
        month: month,
        score: parseFloat(score),
      });

      toast.success(`Month ${month} portfolio score updated successfully`);
      await loadInternGrades(); // Refresh data
    } catch (error) {
      console.error(`Error updating month ${month} score:`, error);
      toast.error(
        error.response?.data?.detail || `Error updating month ${month} score`
      );
    } finally {
      saving.value = false;
    }
  };

  const updateTeachingPhilosophyScore = async () => {
    if (
      !teachingPhilosophyScore.value ||
      teachingPhilosophyScore.value < 0 ||
      teachingPhilosophyScore.value > 100
    ) {
      toast.error("Teaching philosophy score must be between 0 and 100");
      return;
    }

    saving.value = true;
    try {
      await apiClient.post("submissions/grades/teaching-philosophy/update/", {
        intern_id: internId.value,
        score: parseFloat(teachingPhilosophyScore.value),
      });

      toast.success("Teaching philosophy score updated successfully");
      await loadInternGrades(); // Refresh data
    } catch (error) {
      console.error("Error updating teaching philosophy score:", error);
      toast.error(
        error.response?.data?.detail ||
          "Error updating teaching philosophy score"
      );
    } finally {
      saving.value = false;
    }
  };

  const updateReflectivePracticeScore = async () => {
    if (
      !reflectivePracticeScore.value ||
      reflectivePracticeScore.value < 0 ||
      reflectivePracticeScore.value > 100
    ) {
      toast.error("Reflective practice score must be between 0 and 100");
      return;
    }

    saving.value = true;
    try {
      await apiClient.post("submissions/grades/reflective-practice/update/", {
        intern_id: internId.value,
        score: parseFloat(reflectivePracticeScore.value),
      });

      toast.success("Reflective practice score updated successfully");
      await loadInternGrades(); // Refresh data
    } catch (error) {
      console.error("Error updating reflective practice score:", error);
      toast.error(
        error.response?.data?.detail ||
          "Error updating reflective practice score"
      );
    } finally {
      saving.value = false;
    }
  };

  const portfolioTotal = computed(() => {
    const scores = [
      portfolioScores.value.month_1 || 0,
      portfolioScores.value.month_2 || 0,
      portfolioScores.value.month_3 || 0,
      portfolioScores.value.month_4 || 0,
    ];
    return scores.reduce((sum, score) => sum + (parseFloat(score) || 0), 0);
  });

  const overallTotal = computed(() => {
    const portfolio = portfolioTotal.value;
    const philosophy = parseFloat(teachingPhilosophyScore.value) || 0;
    const reflective = parseFloat(reflectivePracticeScore.value) || 0;
    return portfolio + philosophy + reflective;
  });

  const getScoreColor = (score, maxScore) => {
    if (!score) return "text-gray-500";
    const percentage = (score / maxScore) * 100;
    if (percentage >= 80) return "text-green-600";
    if (percentage >= 60) return "text-blue-600";
    if (percentage >= 40) return "text-yellow-600";
    return "text-red-600";
  };

  onMounted(loadInternGrades);
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Page Header -->
    <div class="bg-gradient-to-r bg-maroon shadow-lg">
      <div class="max-w-7xl mx-auto px-6 lg:px-8 py-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <BackButton />
            <div class="text-white">
              <h1 class="text-2xl font-bold">Comprehensive Grading</h1>
              <p class="text-white/80 text-sm">
                Evaluate intern's portfolio, teaching philosophy, and reflective
                practice
              </p>
            </div>
          </div>
          <div class="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
            <div class="flex items-center space-x-2 text-white">
              <svg
                class="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"
                ></path>
              </svg>
              <span class="font-medium">Total: {{ overallTotal }}/300</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <Loader />
    </div>

    <!-- Main Content -->
    <div v-else class="max-w-7xl mx-auto px-6 lg:px-8 py-8 space-y-8">
      <!-- Intern Information -->
      <div class="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <div class="flex items-center space-x-4">
          <div
            class="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl"
          >
            {{ internGrades.intern?.first_name?.charAt(0)
            }}{{ internGrades.intern?.last_name?.charAt(0) }}
          </div>
          <div>
            <h2 class="text-xl font-bold text-gray-900">
              {{ internGrades.intern?.first_name }}
              {{ internGrades.intern?.last_name }}
            </h2>
            <p class="text-gray-600">
              Student ID: {{ internGrades.intern?.username }}
            </p>
            <p class="text-sm text-gray-500">
              {{ internGrades.intern?.department?.name || "No Department" }}
            </p>
          </div>
        </div>
      </div>

      <!-- Portfolio Grading (Month 1-4) -->
      <div
        class="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden"
      >
        <div class="bg-gray-50 px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-800 flex items-center">
            <svg
              class="w-5 h-5 mr-2 text-[#8c003b]"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
              ></path>
            </svg>
            Portfolio Assessment (Images/Videos) - Total:
            {{ portfolioTotal }}/100
          </h3>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <!-- Month 1-3 (20 points each) -->
            <div v-for="month in [1, 2, 3]" :key="month" class="space-y-3">
              <label class="block text-sm font-medium text-gray-700">
                Month {{ month }} (/20)
              </label>
              <div class="flex space-x-2">
                <input
                  v-model="portfolioScores[`month_${month}`]"
                  type="number"
                  min="0"
                  max="20"
                  step="0.01"
                  class="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#8c003b] focus:border-[#8c003b]"
                  placeholder="0.00"
                />
                <button
                  @click="
                    updatePortfolioScore(
                      month,
                      portfolioScores[`month_${month}`]
                    )
                  "
                  :disabled="saving || !portfolioScores[`month_${month}`]"
                  class="px-3 py-2 bg-[#8c003b] text-white rounded-lg hover:bg-[#a00048] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Save
                </button>
              </div>
              <div
                class="text-sm"
                :class="getScoreColor(portfolioScores[`month_${month}`], 20)"
              >
                Current: {{ portfolioScores[`month_${month}`] || 0 }}/20
              </div>
            </div>

            <!-- Month 4 (40 points) -->
            <div class="space-y-3">
              <label class="block text-sm font-medium text-gray-700">
                Month 4 (/40)
              </label>
              <div class="flex space-x-2">
                <input
                  v-model="portfolioScores.month_4"
                  type="number"
                  min="0"
                  max="40"
                  step="0.01"
                  class="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#8c003b] focus:border-[#8c003b]"
                  placeholder="0.00"
                />
                <button
                  @click="updatePortfolioScore(4, portfolioScores.month_4)"
                  :disabled="saving || !portfolioScores.month_4"
                  class="px-3 py-2 bg-[#8c003b] text-white rounded-lg hover:bg-[#a00048] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Save
                </button>
              </div>
              <div
                class="text-sm"
                :class="getScoreColor(portfolioScores.month_4, 40)"
              >
                Current: {{ portfolioScores.month_4 || 0 }}/40
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Teaching Philosophy Grading -->
      <div
        class="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden"
      >
        <div class="bg-gray-50 px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-800 flex items-center">
            <svg
              class="w-5 h-5 mr-2 text-[#006938]"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
              ></path>
            </svg>
            Teaching Philosophy Assessment (/100)
          </h3>
        </div>
        <div class="p-6">
          <div class="max-w-md space-y-3">
            <label class="block text-sm font-medium text-gray-700">
              Teaching Philosophy Score
            </label>
            <div class="flex space-x-2">
              <input
                v-model="teachingPhilosophyScore"
                type="number"
                min="0"
                max="100"
                step="0.01"
                class="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#006938] focus:border-[#006938]"
                placeholder="0.00"
              />
              <button
                @click="updateTeachingPhilosophyScore"
                :disabled="saving || !teachingPhilosophyScore"
                class="px-3 py-2 bg-[#006938] text-white rounded-lg hover:bg-[#00562e] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Save
              </button>
            </div>
            <div
              class="text-sm"
              :class="getScoreColor(teachingPhilosophyScore, 100)"
            >
              Current: {{ teachingPhilosophyScore || 0 }}/100
            </div>
          </div>
        </div>
      </div>

      <!-- Reflective Practice Grading -->
      <div
        class="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden"
      >
        <div class="bg-gray-50 px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-800 flex items-center">
            <svg
              class="w-5 h-5 mr-2 text-[#f59e0b]"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
              ></path>
            </svg>
            Reflective Practice Assessment (/100)
          </h3>
        </div>
        <div class="p-6">
          <div class="max-w-md space-y-3">
            <label class="block text-sm font-medium text-gray-700">
              Reflective Practice Score
            </label>
            <div class="flex space-x-2">
              <input
                v-model="reflectivePracticeScore"
                type="number"
                min="0"
                max="100"
                step="0.01"
                class="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#f59e0b] focus:border-[#f59e0b]"
                placeholder="0.00"
              />
              <button
                @click="updateReflectivePracticeScore"
                :disabled="saving || !reflectivePracticeScore"
                class="px-3 py-2 bg-[#f59e0b] text-white rounded-lg hover:bg-[#d97706] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Save
              </button>
            </div>
            <div
              class="text-sm"
              :class="getScoreColor(reflectivePracticeScore, 100)"
            >
              Current: {{ reflectivePracticeScore || 0 }}/100
            </div>
          </div>
        </div>
      </div>

      <!-- Overall Summary -->
      <div
        class="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden"
      >
        <div class="bg-gray-50 px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-800">Overall Summary</h3>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div class="text-center">
              <div
                class="text-2xl font-bold"
                :class="getScoreColor(portfolioTotal, 100)"
              >
                {{ portfolioTotal }}
              </div>
              <div class="text-sm text-gray-600">Portfolio (/100)</div>
            </div>
            <div class="text-center">
              <div
                class="text-2xl font-bold"
                :class="getScoreColor(teachingPhilosophyScore, 100)"
              >
                {{ teachingPhilosophyScore || 0 }}
              </div>
              <div class="text-sm text-gray-600">
                Teaching Philosophy (/100)
              </div>
            </div>
            <div class="text-center">
              <div
                class="text-2xl font-bold"
                :class="getScoreColor(reflectivePracticeScore, 100)"
              >
                {{ reflectivePracticeScore || 0 }}
              </div>
              <div class="text-sm text-gray-600">
                Reflective Practice (/100)
              </div>
            </div>
            <div class="text-center">
              <div
                class="text-3xl font-bold"
                :class="getScoreColor(overallTotal, 300)"
              >
                {{ overallTotal }}
              </div>
              <div class="text-sm text-gray-600">Total (/300)</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
