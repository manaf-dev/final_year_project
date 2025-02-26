 
  <script>
  import { ref } from 'vue'
  import apiClient from '@/services/api'


    const newPassword = ref("")
    const confirmPassword = ref("")
    const handlePasswordReset = async () => {
        try {
            const response = apiClient.post('accounts/auth/password/reset/confirm/')
        } catch (error) {
            
        }
    }
  </script>




<template>
    <div class="bg-gray-100 min-h-screen flex items-center justify-center px-4">
      <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-6">
        <h2 class="text-2xl font-semibold text-gray-800 text-center mb-4">Set New Password</h2>
        <p class="text-sm text-gray-500 text-center mb-6">
          Enter a new password for your account.
        </p>
        <form @submit.prevent="handlePasswordReset" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">New Password</label>
            <input
              type="password"
              v-model="newPassword"
              required
              class="mt-1 py-2 px-4 w-full border rounded-md shadow-sm text-gray-700 focus:ring-[#006938] focus:border-[#006938]"
              placeholder="Enter new password"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Confirm New Password</label>
            <input
              type="password"
              v-model="confirmPassword"
              required
              class="mt-1 py-2 px-4 w-full border rounded-md shadow-sm text-gray-700 focus:ring-[#006938] focus:border-[#006938]"
              placeholder="Confirm new password"
            />
          </div>
          <button
            type="submit"
            class="w-full bg-[#8c003b] hover:bg-[#a00449] text-white font-medium py-2 px-4 rounded-md shadow"
          >
            Reset Password
          </button>
        </form>
      </div>
    </div>
  </template>
   