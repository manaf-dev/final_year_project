<script setup>
import apiClient from "@/services/api";
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import SubmissionDisplay from "../SubmissionDisplay.vue";
import { useToast } from "vue-toastification";
import Loader from "../loader.vue";
import BackButton from "../BackButton.vue";
import { useNotificationStore } from "@/stores/notifications";

const route = useRoute();
const toast = useToast();
const notificationStore = useNotificationStore();

const portfolio = ref({});
const loadingSubmissions = ref(false);
const supervisorComment = ref("");
const grade = ref("");
const teachingPhilosophyScore = ref("");
const reflectivePracticeScore = ref("");
const submittingReview = ref(false);
const month = ref(route.params.month);

const hasNewGrades = computed(() => {
  if (month.value === "1") return grade.value !== "";
  if (month.value === "2") return grade.value !== "";
  if (month.value === "3") return grade.value !== "";
  if (month.value === "4") return grade.value !== "" || teachingPhilosophyScore.value !== "" || reflectivePracticeScore.value !== "";
  return false;
});

// Computed property to show the actual saved grade (not just form value)
const currentPortfolioGrade = computed(() => {
  // First check if we have a saved grade from the new system
  if (portfolio.value.new_grade !== null && portfolio.value.new_grade !== undefined) {
    return portfolio.value.new_grade;
  }
  // Fallback to old system grade
  if (portfolio.value.grade) {
    return portfolio.value.grade;
  }
  return null;
});

const currentTeachingPhilosophyGrade = computed(() => {
  return portfolio.value.teaching_philosophy_score || null;
});

const currentReflectivePracticeGrade = computed(() => {
  return portfolio.value.reflective_practice_score || null;
});

const get_portfolio = async () => {
  loadingSubmissions.value = true;

  try {
    const response = await apiClient.get(
      `submissions/portfolio/${route.params.intern}/${route.params.month}/`
    );
    portfolio.value = response.data;
    
    // Clear previous values
    grade.value = "";
    teachingPhilosophyScore.value = "";
    reflectivePracticeScore.value = "";
    
    // Load existing grades from the new grading system (from portfolio response)
    if (portfolio.value.new_grade !== null && portfolio.value.new_grade !== undefined) {
      grade.value = portfolio.value.new_grade;
    }
    
    // For month 4, also load teaching philosophy and reflective practice scores
    if (month.value === "4") {
      if (portfolio.value.teaching_philosophy_score !== null && portfolio.value.teaching_philosophy_score !== undefined) {
        teachingPhilosophyScore.value = portfolio.value.teaching_philosophy_score;
      }
      if (portfolio.value.reflective_practice_score !== null && portfolio.value.reflective_practice_score !== undefined) {
        reflectivePracticeScore.value = portfolio.value.reflective_practice_score;
      }
    }
    
    // Pre-populate form if there's existing data from old system (fallback)
    if (!grade.value && portfolio.value.graded) {
      grade.value = portfolio.value.grade;
    }
    
    console.log("Portfolio data loaded:", portfolio.value);
  } catch (error) {
    console.error(error);
  } finally {
    loadingSubmissions.value = false;
  }
};

onMounted(get_portfolio);

// Watch for portfolio changes to pre-populate existing grades and comments
watch(portfolio, (newPortfolio) => {
  if (newPortfolio && newPortfolio.graded) {
    grade.value = newPortfolio.grade;
  }
}, { deep: true });

const submitReview = async () => {
  submittingReview.value = true;

  try {
    // For months 1-4, update the portfolio score
    if (grade.value) {
      await apiClient.post('submissions/grades/portfolio/update/', {
        intern_id: route.params.intern,
        month: parseInt(month.value),
        score: parseFloat(grade.value)
      });
    }

    // For month 4, also update teaching philosophy and reflective practice scores
    if (month.value === "4") {
      if (teachingPhilosophyScore.value) {
        await apiClient.post('submissions/grades/teaching-philosophy/update/', {
          intern_id: route.params.intern,
          score: parseFloat(teachingPhilosophyScore.value)
        });
      }

      if (reflectivePracticeScore.value) {
        await apiClient.post('submissions/grades/reflective-practice/update/', {
          intern_id: route.params.intern,
          score: parseFloat(reflectivePracticeScore.value)
        });
      }
    }

    // Submit the traditional comment if provided
    if (supervisorComment.value) {
      const commentData = {
        submission_id: portfolio.value.id,
        content: supervisorComment.value,
        // Don't pass grade to comment API since we're using new grading system
      };

      await apiClient.post("submissions/comment/create/", commentData);
    }
    
    toast.success("Grades and review submitted successfully!");
    
    // Clear only the comment after successful submission
    supervisorComment.value = "";
    
    // Reload the data to reflect changes
    await get_portfolio();
    // Refresh notification count since a new notification was likely created
    notificationStore.fetchUnreadCount();
  } catch (error) {
    toast.error(error.response?.data?.detail || "Error submitting review");
    console.error(error);
  } finally {
    submittingReview.value = false;
    // Only clear the comment if it's a new submission, not an update
    if (!portfolio.value.supervisor_comment) {
      supervisorComment.value = "";
      grade.value = "";
      if (month.value === "4") {
        teachingPhilosophyScore.value = "";
        reflectivePracticeScore.value = "";
      }
    }
  }
};

const grades = computed(() => {
  if (month.value === "4") {
    return [1, 5, 10, 15, 20, 25, 30, 35, 40]; // Portfolio scoring for month 4 (out of 40)
  }
  return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]; // Portfolio scoring for months 1-3 (out of 20)
});

const teachingPhilosophyGrades = computed(() => {
  return Array.from({length: 21}, (_, i) => i * 5); // 0, 5, 10, 15, ... 100
});

const reflectivePracticeGrades = computed(() => {
  return Array.from({length: 21}, (_, i) => i * 5); // 0, 5, 10, 15, ... 100
});
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div
      class="bg-gradient-to-r bg-maroon shadow-lg"
    >
      <div class="max-w-7xl mx-auto px-6 lg:px-8 py-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <BackButton />
            <div class="text-white">
              <h1 class="text-2xl font-bold">Submission Review</h1>
              <p class="text-white/80 text-sm">
                Evaluate intern submission for Month {{ month }}
              </p>
            </div>
          </div>
          <div class="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
            <div class="flex items-center space-x-2">
              <svg
                class="w-5 h-5 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8 7V3a2 2 0 012-2h4a2 2 0 012 2v4m-6 4h6m-2 4h2a2 2 0 002-2V7a2 2 0 00-2-2H8a2 2 0 00-2 2v8a2 2 0 002 2z"
                ></path>
              </svg>
              <span class="text-white font-medium">Month {{ month }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Container -->
    <div class="max-w-7xl mx-auto px-6 lg:px-8 py-8 space-y-8">
      <!-- Submission Display Section -->
      <div
        class="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden"
      >
        <div class="bg-gray-50 px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-800 flex items-center">
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
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              ></path>
            </svg>
            Submission Details
          </h2>
          <!-- Debug info -->
          <div v-if="portfolio.new_grade !== undefined" class="mt-2 text-sm text-blue-600">
            Current Grade: {{ portfolio.new_grade }}
          </div>
          <!-- Current Grades Summary -->
          <div v-if="currentPortfolioGrade || currentTeachingPhilosophyGrade || currentReflectivePracticeGrade" class="mt-3 p-3 bg-green-50 rounded-lg border border-green-200">
            <h3 class="text-sm font-semibold text-green-800 mb-2">Current Grades</h3>
            <div class="space-y-1 text-sm">
              <div v-if="currentPortfolioGrade" class="flex justify-between">
                <span class="text-green-700">Portfolio (Month {{ month }}):</span>
                <span class="font-semibold text-green-800">{{ currentPortfolioGrade }}/{{ month === "4" ? "40" : "20" }}</span>
              </div>
              <div v-if="month === '4' && currentTeachingPhilosophyGrade" class="flex justify-between">
                <span class="text-green-700">Teaching Philosophy:</span>
                <span class="font-semibold text-green-800">{{ currentTeachingPhilosophyGrade }}/100</span>
              </div>
              <div v-if="month === '4' && currentReflectivePracticeGrade" class="flex justify-between">
                <span class="text-green-700">Reflective Practice:</span>
                <span class="font-semibold text-green-800">{{ currentReflectivePracticeGrade }}/100</span>
              </div>
              <div v-if="month === '4' && (currentPortfolioGrade || currentTeachingPhilosophyGrade || currentReflectivePracticeGrade)" class="flex justify-between border-t border-green-300 pt-1 mt-2">
                <span class="text-green-700 font-semibold">Total:</span>
                <span class="font-bold text-green-800">{{ (parseFloat(currentPortfolioGrade) || 0) + (parseFloat(currentTeachingPhilosophyGrade) || 0) + (parseFloat(currentReflectivePracticeGrade) || 0) }}/240</span>
              </div>
            </div>
          </div>
        </div>
        <div class="p-6">
          <SubmissionDisplay :submissions="portfolio" :month="month" />
        </div>
      </div>

        <!-- Supervisor Review Section -->
      <div
        v-if="portfolio"
        class="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden"
      >
        <div class="p-8">
          <form @submit.prevent="submitReview" class="space-y-8">
            <!-- Supervisor Comments Section -->
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <label
                  class="text-lg font-semibold text-gray-800 flex items-center space-x-2"
                >
                  <svg
                    class="w-5 h-5 text-[#8c003b]"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-3.582 8-8 8a8.955 8.955 0 01-2.624-.374c-.297.061-.526.374-.924.374-1.5 0-2-.5-2-1 0-.75.5-1.5.75-2.5C7.343 17.5 7 16.5 7 15c0-4.418 3.582-8 8-8s8 3.582 8 8z"
                    ></path>
                  </svg>
                  <span>Grade & Reviews</span>
                </label>
                <span
                  class="text-sm text-gray-500"
                  :class="{ 'text-red-500': supervisorComment.length > 500 }"
                >
                  {{ supervisorComment.length }}/500
                </span>
              </div>
  
              <div class="relative">
                <textarea
                  v-model="supervisorComment"
                  placeholder="Provide detailed feedback on the intern's performance, areas of improvement, and recognition of achievements..."
                  class="w-full border-2 border-gray-200 rounded-xl p-4 text-gray-700 placeholder-gray-400 focus:ring-2 focus:ring-[#8c003b] focus:border-[#8c003b] transition-all duration-200 resize-none"
                  rows="6"
                  maxlength="500"
                ></textarea>
                <div class="absolute bottom-3 right-3 text-xs text-gray-400">
                  Press Shift + Enter for new line
                </div>
              </div>
            </div>
  
            <!-- Enhanced Grade Selection Section -->
            <div class="space-y-6">
              <!-- Portfolio Grading -->
              <div class="space-y-4">
                <label class="text-lg font-semibold text-gray-800 flex items-center space-x-2">
                  <svg class="w-5 h-5 text-[#006938]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
                  </svg>
                  <span>Portfolio Grade ({{ month === "4" ? "40" : "20" }} points)</span>
                </label>

                <div class="space-y-3">
                  <select
                    v-model="grade"
                    class="w-full border-2 border-gray-200 rounded-xl p-4 text-gray-700 focus:ring-2 focus:ring-[#006938] focus:border-[#006938] transition-all duration-200 bg-white"
                  >
                    <option value="" disabled>Select Portfolio Grade</option>
                    <option v-for="gradeOption in grades" :key="gradeOption" :value="gradeOption">
                      {{ gradeOption }}/{{ month === "4" ? "40" : "20" }}
                    </option>
                  </select>

                  <div v-if="currentPortfolioGrade" class="flex items-center justify-between text-sm">
                    <span class="text-gray-600">Current Portfolio Score:</span>
                    <div class="flex items-center space-x-2">
                      <span class="font-bold text-[#006938] text-lg">{{ currentPortfolioGrade }}/{{ month === "4" ? "40" : "20" }}</span>
                      <div class="w-3 h-3 rounded-full" :class="{
                        'bg-red-400': (month === '4' && currentPortfolioGrade < 20) || (month !== '4' && currentPortfolioGrade < 10),
                        'bg-yellow-400': (month === '4' && currentPortfolioGrade >= 20 && currentPortfolioGrade < 32) || (month !== '4' && currentPortfolioGrade >= 10 && currentPortfolioGrade < 16),
                        'bg-green-400': (month === '4' && currentPortfolioGrade >= 32) || (month !== '4' && currentPortfolioGrade >= 16)
                      }"></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Month 4 Additional Grading -->
              <div v-if="month === '4'" class="space-y-6 border-t pt-6">
                <!-- Teaching Philosophy Grading -->
                <div class="space-y-4">
                  <label class="text-lg font-semibold text-gray-800 flex items-center space-x-2">
                    <svg class="w-5 h-5 text-[#8c003b]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                    </svg>
                    <span>Teaching Philosophy Grade (100 points)</span>
                  </label>

                  <div class="space-y-3">
                    <select
                      v-model="teachingPhilosophyScore"
                      class="w-full border-2 border-gray-200 rounded-xl p-4 text-gray-700 focus:ring-2 focus:ring-[#8c003b] focus:border-[#8c003b] transition-all duration-200 bg-white"
                    >
                      <option value="" disabled>Select Teaching Philosophy Grade</option>
                      <option v-for="score in teachingPhilosophyGrades" :key="score" :value="score">
                        {{ score }}/100
                      </option>
                    </select>

                    <div v-if="currentTeachingPhilosophyGrade" class="flex items-center justify-between text-sm">
                      <span class="text-gray-600">Current Teaching Philosophy Score:</span>
                      <div class="flex items-center space-x-2">
                        <span class="font-bold text-[#8c003b] text-lg">{{ currentTeachingPhilosophyGrade }}/100</span>
                        <div class="w-3 h-3 rounded-full" :class="{
                          'bg-red-400': currentTeachingPhilosophyGrade < 50,
                          'bg-yellow-400': currentTeachingPhilosophyGrade >= 50 && currentTeachingPhilosophyGrade < 70,
                          'bg-green-400': currentTeachingPhilosophyGrade >= 70
                        }"></div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Reflective Practice Grading -->
                <div class="space-y-4">
                  <label class="text-lg font-semibold text-gray-800 flex items-center space-x-2">
                    <svg class="w-5 h-5 text-[#006938]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                    </svg>
                    <span>Reflective Practice Grade (100 points)</span>
                  </label>

                  <div class="space-y-3">
                    <select
                      v-model="reflectivePracticeScore"
                      class="w-full border-2 border-gray-200 rounded-xl p-4 text-gray-700 focus:ring-2 focus:ring-[#006938] focus:border-[#006938] transition-all duration-200 bg-white"
                    >
                      <option value="" disabled>Select Reflective Practice Grade</option>
                      <option v-for="score in reflectivePracticeGrades" :key="score" :value="score">
                        {{ score }}/100
                      </option>
                    </select>

                    <div v-if="currentReflectivePracticeGrade" class="flex items-center justify-between text-sm">
                      <span class="text-gray-600">Current Reflective Practice Score:</span>
                      <div class="flex items-center space-x-2">
                        <span class="font-bold text-[#006938] text-lg">{{ currentReflectivePracticeGrade }}/100</span>
                        <div class="w-3 h-3 rounded-full" :class="{
                          'bg-red-400': currentReflectivePracticeGrade < 50,
                          'bg-yellow-400': currentReflectivePracticeGrade >= 50 && currentReflectivePracticeGrade < 70,
                          'bg-green-400': currentReflectivePracticeGrade >= 70
                        }"></div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Month 4 Total Summary -->
                <div v-if="currentPortfolioGrade || currentTeachingPhilosophyGrade || currentReflectivePracticeGrade" class="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-xl border border-blue-200">
                  <div class="flex items-center justify-between">
                    <span class="text-lg font-semibold text-gray-800">Month 4 Current Total:</span>
                    <span class="text-xl font-bold text-indigo-600">
                      {{ (parseFloat(currentPortfolioGrade) || 0) + (parseFloat(currentTeachingPhilosophyGrade) || 0) + (parseFloat(currentReflectivePracticeGrade) || 0) }}/240
                    </span>
                  </div>
                  <div class="text-sm text-gray-600 mt-1">
                    Portfolio: {{ currentPortfolioGrade || 0 }}/40 • Teaching Philosophy: {{ currentTeachingPhilosophyGrade || 0 }}/100 • Reflective Practice: {{ currentReflectivePracticeGrade || 0 }}/100
                  </div>
                </div>
              </div>
            </div>

            <!-- Enhanced Submit Section -->
            <div class="flex items-center justify-between pt-6 border-t border-gray-200">
              <div class="text-sm text-gray-600">
                <span class="flex items-center">
                  <svg
                    class="w-4 h-4 mr-1"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                  Either grade or comment is required
                </span>
              </div>
  
              <button
                type="submit"
                :disabled="
                  submittingReview || (!supervisorComment.trim() && !grade && !teachingPhilosophyScore && !reflectivePracticeScore)
                "
                class="group relative bg-gradient-to-r bg-maroon text-white px-8 py-3 rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                <div class="flex items-center space-x-2">
                  <svg
                    v-if="!submittingReview"
                    class="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                    ></path>
                  </svg>
                  <svg
                    v-else
                    class="w-5 h-5 animate-spin"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      class="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      stroke-width="4"
                    ></circle>
                    <path
                      class="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  <span>{{
                    submittingReview ? "Submitting Review..." : "Submit Review"
                  }}</span>
                </div>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>


    <div
      v-if="loadingSubmissions"
      class="absolute inset-0 bg-black opacity-50 flex items-center justify-center rounded-lg z-20"
    >
      <Loader />
    </div>
  </div>
</template>
