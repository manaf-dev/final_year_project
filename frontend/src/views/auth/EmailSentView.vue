<script setup>

defineProps( {
    email: {
      type: String,
      required: true,
    }
  }
)
</script>


<template>
    <div class="bg-gray-100 min-h-screen flex items-center justify-center px-4">
      <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-6 text-center">
        <i class="pi pi-envelope text-6xl text-[#8c003b] mb-4"></i>
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Check Your Email</h2>
        <p class="text-sm text-gray-500 mb-6">
          We’ve sent a password reset link to <span class="font-medium">{{ email }}</span>. Please check your inbox
          and follow the instructions.
        </p>
        <router-link
          :to="{name: 'login'}"
          class="inline-block mt-4 bg-[#006938] hover:bg-[#008a4a] text-white font-medium py-2 px-6 rounded-md shadow"
        >
          Back to Login
        </router-link>
      </div>
    </div>
  </template>
  
