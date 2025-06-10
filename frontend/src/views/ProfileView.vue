<script setup>
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import { useAuthStore } from "@/stores/auth";
    import { useToast } from "vue-toastification";
    import { ref, reactive } from "vue";
    import apiClient from "@/services/api";

    const authStore = useAuthStore();
    const toast = useToast();
    const profile = authStore.user;
    const passwordData = reactive({
        old_password: "",
        new_password1: "",
        new_password2: "",
    });
    const loading = ref(false);

    const validatePasswordData = () => {
        if (
            !passwordData.old_password ||
            !passwordData.new_password1 ||
            !passwordData.new_password2
        ) {
            toast.error("All fields are required");
            return false;
        }
        if (passwordData.new_password1 !== passwordData.new_password2) {
            toast.error("New passwords do not match");
            return false;
        }
        if (passwordData.new_password1.length < 8) {
            toast.error("Password must be at least 8 characters");
            return false;
        }
        return true;
    };

    const handleChangePassword = async () => {
        if (validatePasswordData() === false) return;
        loading.value = true;
        try {
            const response = await apiClient.put(
                "accounts/auth/password/change/",
                {current_password: passwordData.old_password, password: passwordData.new_password1}
            );
            toast.success(response.data.detail);
            authStore.logout();
        } catch (error) {
            // console.log("error", error);
            const errorMessage =
                error.response?.data?.old_password?.[0] ||
                error.response?.data?.new_password2?.[0] ||
                error.response?.data?.detail ||
                "An error occurred";
            toast.error(errorMessage);
        } finally {
            passwordData.old_password = "";
            passwordData.new_password1 = "";
            passwordData.new_password2 = "";
            loading.value = false;
        }
    };
</script>

<template>
    <DashboardLayout :title="'Profile'">
        <template #content>
            <div class="bg-gray-50 min-h-screen p-4">
                <div class="max-w-4xl mx-auto">
                    <!-- Main Content Container -->
                    <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                        <!-- Enhanced Header -->
                        <div class="bg-gradient-to-r from-maroon via-green to-green text-white px-6 py-8">
                            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                                <div class="flex items-center space-x-6">
                                    <!-- User Avatar with Initials -->
                                    <div class="w-20 h-20 rounded-full bg-white/20 backdrop-blur-sm border-2 border-white/30 flex items-center justify-center">
                                        <span class="text-2xl font-bold text-white uppercase">
                                            {{ profile.first_name?.charAt(0) || '' }}{{ profile.last_name?.charAt(0) || '' }}
                                        </span>
                                    </div>
                                    
                                    <div>
                                        <h1 class="text-3xl font-bold mb-2 capitalize">
                                            {{ profile.last_name }} {{ profile.first_name }} {{ profile.other_names }}
                                        </h1>
                                        <div class="flex items-center space-x-4">
                                            <span class="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-sm border border-white/30 capitalize">
                                                {{ profile.account_type }}
                                            </span>
                                            <span class="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-sm border border-white/30">
                                                <i class="pi pi-shield-check mr-1.5"></i>
                                                Active User
                                            </span>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Profile Stats -->
                                <div class="hidden md:block text-right mt-4 sm:mt-0">
                                    <div class="text-2xl font-bold">{{ profile.username }}</div>
                                    <div class="text-sm text-white/80">{{ authStore.isIntern ? "Student" : "Staff" }} ID</div>
                                </div>
                            </div>
                            
                            
                        </div>

                        <!-- Profile Details Section -->
                        <div class="p-6">
                            <h2 class="text-xl font-bold text-gray-900 mb-6 flex items-center">
                                <i class="pi pi-info-circle text-[#8c003b] mr-2"></i>
                                Profile Information
                            </h2>
                            
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <!-- Email Card -->
                                <div class="bg-gradient-to-r from-blue-50 to-blue-100 p-4 rounded-xl border border-blue-200">
                                    <div class="flex items-center space-x-3">
                                        <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
                                            <i class="pi pi-envelope text-white"></i>
                                        </div>
                                        <div>
                                            <h3 class="text-sm font-medium text-gray-700">Email Address</h3>
                                            <p class="text-lg font-semibold text-gray-900">{{ profile.email }}</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- ID Card -->
                                <div class="bg-gradient-to-r from-[#8c003b]/10 to-[#8c003b]/20 p-4 rounded-xl border border-[#8c003b]/30">
                                    <div class="flex items-center space-x-3">
                                        <div class="w-10 h-10 bg-[#8c003b] rounded-lg flex items-center justify-center">
                                            <i class="pi pi-id-card text-white"></i>
                                        </div>
                                        <div>
                                            <h3 class="text-sm font-medium text-gray-700">{{ authStore.isIntern ? "Student" : "Staff" }} ID</h3>
                                            <p class="text-lg font-semibold text-gray-900">{{ profile.username }}</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Cohort Card (for interns) -->
                                <div v-if="authStore.isIntern" class="bg-gradient-to-r from-[#006938]/10 to-[#006938]/20 p-4 rounded-xl border border-[#006938]/30">
                                    <div class="flex items-center space-x-3">
                                        <div class="w-10 h-10 bg-[#006938] rounded-lg flex items-center justify-center">
                                            <i class="pi pi-users text-white"></i>
                                        </div>
                                        <div>
                                            <h3 class="text-sm font-medium text-gray-700">Cohort</h3>
                                            <p class="text-lg font-semibold text-gray-900">{{ profile.cohort.year }} Internship Cohort</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Phone Card -->
                                <div class="bg-gradient-to-r from-[#ffc712]/10 to-[#ffc712]/20 p-4 rounded-xl border border-[#ffc712]/30">
                                    <div class="flex items-center space-x-3">
                                        <div class="w-10 h-10 bg-[#ffc712] rounded-lg flex items-center justify-center">
                                            <i class="pi pi-phone text-white"></i>
                                        </div>
                                        <div>
                                            <h3 class="text-sm font-medium text-gray-700">Phone Number</h3>
                                            <p class="text-lg font-semibold text-gray-900">{{ profile.phone }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Divider -->
                        <div class="border-b border-gray-200"></div>

                        <!-- Change Password Section -->
                        <div class="p-6">
                            <h2 class="text-xl font-bold text-gray-900 mb-6 flex items-center">
                                <i class="pi pi-key text-[#8c003b] mr-2"></i>
                                Change Password
                            </h2>
                            
                            <div class="bg-gradient-to-r from-gray-50 to-gray-100 p-6 rounded-xl border border-gray-200">
                                <form @submit.prevent="handleChangePassword" class="space-y-6">
                                    <!-- Current Password -->
                                    <div>
                                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                                            <i class="pi pi-lock mr-1.5"></i>
                                            Current Password
                                        </label>
                                        <input
                                            type="password"
                                            v-model="passwordData.old_password"
                                            class="w-full py-3 px-4 border border-gray-300 rounded-lg shadow-sm text-gray-700 focus:ring-2 focus:ring-[#006938] focus:border-[#006938] transition-all duration-200"
                                            placeholder="Enter your current password"
                                        />
                                    </div>

                                    <!-- New Password -->
                                    <div>
                                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                                            <i class="pi pi-shield mr-1.5"></i>
                                            New Password
                                        </label>
                                        <input
                                            type="password"
                                            v-model="passwordData.new_password1"
                                            class="w-full py-3 px-4 border border-gray-300 rounded-lg shadow-sm text-gray-700 focus:ring-2 focus:ring-[#006938] focus:border-[#006938] transition-all duration-200"
                                            placeholder="Enter your new password"
                                        />
                                    </div>

                                    <!-- Confirm New Password -->
                                    <div>
                                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                                            <i class="pi pi-check-circle mr-1.5"></i>
                                            Confirm New Password
                                        </label>
                                        <input
                                            type="password"
                                            v-model="passwordData.new_password2"
                                            class="w-full py-3 px-4 border border-gray-300 rounded-lg shadow-sm text-gray-700 focus:ring-2 focus:ring-[#006938] focus:border-[#006938] transition-all duration-200"
                                            placeholder="Confirm your new password"
                                        />
                                    </div>

                                    <!-- Submit Button -->
                                    <button
                                        type="submit"
                                        :disabled="loading"
                                        class="w-full bg-gradient-to-r from-[#8c003b] to-[#a00449] hover:from-[#a00449] hover:to-[#8c003b] text-white font-semibold py-3 px-6 rounded-lg shadow-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                                    >
                                        <i v-if="loading" class="pi pi-spin pi-spinner mr-2"></i>
                                        <i v-else class="pi pi-refresh mr-2"></i>
                                        {{ loading ? 'Updating Password...' : 'Update Password' }}
                                    </button>
                                </form>

                                <!-- Password Requirements -->
                                <div class="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                                    <h4 class="text-sm font-semibold text-blue-800 mb-2">
                                        <i class="pi pi-info-circle mr-1.5"></i>
                                        Password Requirements
                                    </h4>
                                    <ul class="text-sm text-blue-700 space-y-1">
                                        <li class="flex items-center">
                                            <i class="pi pi-check text-green-600 mr-2"></i>
                                            At least 8 characters long
                                        </li>
                                        <li class="flex items-center">
                                            <i class="pi pi-check text-green-600 mr-2"></i>
                                            Must match confirmation password
                                        </li>
                                        <li class="flex items-center">
                                            <i class="pi pi-check text-green-600 mr-2"></i>
                                            Different from current password
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </DashboardLayout>
</template>
