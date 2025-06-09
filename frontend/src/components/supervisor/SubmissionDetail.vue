<script setup>
import apiClient from "@/services/api";
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import SubmissionDisplay from "../SubmissionDisplay.vue";
import { useToast } from "vue-toastification";
import Loader from "../loader.vue";
import BackButton from "../BackButton.vue";

const route = useRoute();
const toast = useToast();

const portfolio = ref({});
const loadingSubmissions = ref(false);
const supervisorComment = ref("");
const grade = ref("");
const submittingReview = ref(false);
const month = ref(route.params.month);

const get_portfolio = async () => {
  loadingSubmissions.value = true;

  try {
    const response = await apiClient.get(
      `submissions/portfolio/${route.params.intern}/${route.params.month}/`
    );
    portfolio.value = response.data;
    
    // Pre-populate form if there's existing data
    if (portfolio.value.graded) {
      grade.value = portfolio.value.grade;
    }
    
    // console.log(portfolio.value);
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
  // console.log("submitting review...");
  // console.log(supervisorComment.value);
  // console.log(grade.value);

  submittingReview.value = true;

  try {
    const commentData = {
      submission_id: portfolio.value.id,
      content: supervisorComment.value,
      grade: grade.value,
    };

    const response = await apiClient.post(
      "submissions/comment/create/",
      commentData
    );
    toast.success(response.data.detail);
    get_portfolio();
  } catch (error) {
    toast.error(error.response?.data?.detail || "Error submitting review");
    console.error(error);
  } finally {
    submittingReview.value = false;
    // Only clear the comment if it's a new submission, not an update
    if (!portfolio.value.supervisor_comment) {
      supervisorComment.value = "";
      grade.value = "";
    }
  }
};

const grades = computed(() => {
  if (month.value === "4") {
    return [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50];
  }
  return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
});
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Enhanced Page Header -->
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
            <div class="space-y-4">
              <label
                class="text-lg font-semibold text-gray-800 flex items-center space-x-2"
              >
                <svg
                  class="w-5 h-5 text-[#006938]"
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
                <span>Grade Assignment</span>
              </label>
  
              <div class="grid grid-cols-1">
                <!-- Grade Selection -->
                <div class="space-y-3">
                  <select
                    v-model="grade"
                    class="w-full border-2 border-gray-200 rounded-xl p-4 text-gray-700 focus:ring-2 focus:ring-[#006938] focus:border-[#006938] transition-all duration-200 bg-white"
                    :class="{ 'border-red-300': !grade && supervisorComment }"
                  >
                    <option value="" disabled>Select Grade</option>
                    <option
                      v-for="gradeOption in grades"
                      :key="gradeOption"
                      :value="gradeOption"
                    >
                      {{ gradeOption }}{{ month === "4" ? "/50" : "/10" }}
                    </option>
                  </select>
  
                  <div
                    v-if="grade"
                    class="flex items-center justify-between text-sm"
                  >
                    <span class="text-gray-600">Selected Grade:</span>
                    <div class="flex items-center space-x-2">
                      <span class="font-bold text-[#006938] text-lg"
                        >{{ grade }}{{ month === "4" ? "/50" : "/10" }}</span
                      >
                      <div
                        class="w-3 h-3 rounded-full"
                        :class="{
                          'bg-red-400':
                            (month === '4' && grade < 25) ||
                            (month !== '4' && grade < 5),
                          'bg-yellow-400':
                            (month === '4' && grade >= 25 && grade < 35) ||
                            (month !== '4' && grade >= 5 && grade < 7),
                          'bg-green-400':
                            (month === '4' && grade >= 35) ||
                            (month !== '4' && grade >= 7),
                        }"
                      ></div>
                    </div>
                  </div>
                  
                  
                </div>
              </div>
            </div>
  
            <!-- Enhanced Submit Section -->
            <div
              class="flex items-center justify-between pt-6 border-t border-gray-200"
            >
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
                  Both grade and comments are required
                </span>
              </div>
  
              <button
                type="submit"
                :disabled="
                  submittingReview || !supervisorComment.trim() && !grade
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
