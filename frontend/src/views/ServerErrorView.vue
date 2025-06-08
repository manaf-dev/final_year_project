<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";

const router = useRouter();

// Animation states
const isVisible = ref(false);
const showDetails = ref(false);

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true;
  }, 100);
});

const goHome = () => {
  router.push("/");
};

const goBack = () => {
  router.go(-1);
};

const refreshPage = () => {
  window.location.reload();
};

const toggleDetails = () => {
  showDetails.value = !showDetails.value;
};
</script>

<template>
  <div
    class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 flex items-center justify-center p-4"
  >
    <!-- Background Decorative Elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div
        class="absolute -top-40 -right-40 w-80 h-80 bg-[#8c003b]/5 rounded-full"
      ></div>
      <div
        class="absolute -bottom-40 -left-40 w-80 h-80 bg-[#006938]/5 rounded-full"
      ></div>
      <div
        class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-[#ffc712]/3 rounded-full"
      ></div>
    </div>

    <!-- Main Error Container -->
    <div
      :class="[
        'relative z-10 max-w-2xl mx-auto text-center',
        'transition-all duration-1000 transform',
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8',
      ]"
    >
      <!-- Error Icon -->
      <div class="mb-8">
        <div
          class="inline-flex items-center justify-center w-32 h-32 bg-gradient-to-r from-[#8c003b] to-[#a00449] rounded-full shadow-2xl relative"
        >
          <!-- Animated pulse rings -->
          <div
            class="absolute inset-0 rounded-full bg-gradient-to-r from-[#8c003b] to-[#a00449] animate-ping opacity-20"
          ></div>
          <div
            class="absolute inset-2 rounded-full bg-gradient-to-r from-[#8c003b] to-[#a00449] animate-ping opacity-30"
            style="animation-delay: 0.5s"
          ></div>

          <!-- Error Icon -->
          <i
            class="pi pi-exclamation-triangle text-5xl text-white relative z-10"
          ></i>
        </div>
      </div>

      <!-- Error Code -->
      <div class="mb-6">
        <h1
          class="text-8xl font-black text-transparent bg-clip-text bg-gradient-to-r from-[#8c003b] via-[#006938] to-[#ffc712] mb-2"
        >
          500
        </h1>
        <h2 class="text-3xl font-bold text-gray-800 mb-2">
          Internal Server Error
        </h2>
        <p class="text-lg text-gray-600 max-w-md mx-auto">
          Oops! Something went wrong on our end. Our team has been notified and
          is working to fix this issue.
        </p>
      </div>

      <!-- Status Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <!-- Server Status -->
        <div class="bg-white rounded-xl p-4 shadow-lg border border-red-100">
          <div class="flex items-center justify-center mb-2">
            <div
              class="w-10 h-10 bg-red-500 rounded-lg flex items-center justify-center"
            >
              <i class="pi pi-server text-white"></i>
            </div>
          </div>
          <h3 class="font-semibold text-gray-800 text-sm">Server Status</h3>
          <p class="text-red-600 text-xs font-medium">Unavailable</p>
        </div>

        <!-- Error Type -->
        <div class="bg-white rounded-xl p-4 shadow-lg border border-orange-100">
          <div class="flex items-center justify-center mb-2">
            <div
              class="w-10 h-10 bg-orange-500 rounded-lg flex items-center justify-center"
            >
              <i class="pi pi-bug text-white"></i>
            </div>
          </div>
          <h3 class="font-semibold text-gray-800 text-sm">Error Type</h3>
          <p class="text-orange-600 text-xs font-medium">Internal</p>
        </div>

        <!-- Support Status -->
        <div class="bg-white rounded-xl p-4 shadow-lg border border-green-100">
          <div class="flex items-center justify-center mb-2">
            <div
              class="w-10 h-10 bg-[#006938] rounded-lg flex items-center justify-center"
            >
              <i class="pi pi-headphones text-white"></i>
            </div>
          </div>
          <h3 class="font-semibold text-gray-800 text-sm">Support</h3>
          <p class="text-[#006938] text-xs font-medium">Available 24/7</p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center mb-8">
        <!-- Refresh Button -->
        <button
          @click="refreshPage"
          class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-[#8c003b] to-[#a00449] hover:from-[#a00449] hover:to-[#8c003b] text-white font-semibold rounded-lg shadow-lg transition-all duration-200 transform hover:scale-105"
        >
          <i class="pi pi-refresh mr-2"></i>
          Try Again
        </button>

        <!-- Go Back Button -->
        <button
          @click="goBack"
          class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-[#006938] to-[#007d42] hover:from-[#007d42] hover:to-[#006938] text-white font-semibold rounded-lg shadow-lg transition-all duration-200 transform hover:scale-105"
        >
          <i class="pi pi-arrow-left mr-2"></i>
          Go Back
        </button>

        <!-- Home Button -->
        <button
          @click="goHome"
          class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-[#ffc712] to-[#ffb700] hover:from-[#ffb700] hover:to-[#ffc712] text-white font-semibold rounded-lg shadow-lg transition-all duration-200 transform hover:scale-105"
        >
          <i class="pi pi-home mr-2"></i>
          Home
        </button>
      </div>

      <!-- Additional Information Toggle -->
      <div
        class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden"
      >
        <!-- Toggle Header -->
        <button
          @click="toggleDetails"
          class="w-full px-6 py-4 bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200 flex items-center justify-between hover:from-gray-100 hover:to-gray-150 transition-all duration-200"
        >
          <span class="flex items-center font-medium text-gray-800">
            <i class="pi pi-info-circle text-[#8c003b] mr-2"></i>
            What happened?
          </span>
          <i
            :class="[
              'pi transition-transform duration-200',
              showDetails ? 'pi-chevron-up' : 'pi-chevron-down',
            ]"
          ></i>
        </button>

        <!-- Details Content -->
        <div v-show="showDetails" class="p-6 text-left">
          <div class="space-y-4">
            <div>
              <h4 class="font-semibold text-gray-800 mb-2 flex items-center">
                <i class="pi pi-clock text-[#ffc712] mr-2"></i>
                When did this occur?
              </h4>
              <p class="text-gray-600 text-sm">
                {{ new Date().toLocaleString() }}
              </p>
            </div>

            <div>
              <h4 class="font-semibold text-gray-800 mb-2 flex items-center">
                <i class="pi pi-cog text-[#006938] mr-2"></i>
                What can you do?
              </h4>
              <ul class="text-gray-600 text-sm space-y-1">
                <li class="flex items-center">
                  <i class="pi pi-check text-green-500 mr-2"></i>
                  Wait a few moments and try refreshing the page
                </li>
                <li class="flex items-center">
                  <i class="pi pi-check text-green-500 mr-2"></i>
                  Clear your browser cache and cookies
                </li>
                <li class="flex items-center">
                  <i class="pi pi-check text-green-500 mr-2"></i>
                  Try accessing the page from a different browser
                </li>
                <li class="flex items-center">
                  <i class="pi pi-check text-green-500 mr-2"></i>
                  Contact support if the issue persists
                </li>
              </ul>
            </div>

            <div>
              <h4 class="font-semibold text-gray-800 mb-2 flex items-center">
                <i class="pi pi-shield text-[#8c003b] mr-2"></i>
                Is my data safe?
              </h4>
              <p class="text-gray-600 text-sm">
                Yes, your data is secure. This is a temporary server issue and
                no user data has been compromised.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="mt-8 text-center">
        <p class="text-gray-500 text-sm">
          Error ID:
          <span class="font-mono bg-gray-100 px-2 py-1 rounded"
            >#{{ Math.random().toString(36).substr(2, 9).toUpperCase() }}</span
          >
        </p>
        <p class="text-gray-400 text-xs mt-2">
          If this error persists, please contact our support team with the error
          ID above.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Additional animations for enhanced visual appeal */
@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

/* Hover effects for buttons */
button:hover {
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

/* Smooth transitions for all interactive elements */
* {
  transition: all 0.2s ease-in-out;
}
</style>
