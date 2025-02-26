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
            const response = await apiClient.post(
                "accounts/auth/password/change/",
                passwordData
            );
            toast.success(response.data.detail);
            authStore.logout();
        } catch (error) {
            console.log("error", error);
            toast.error(
                error.response?.data?.old_password?.[0] ||
                    error.response?.data?.new_password2?.[0] ||
                    "An error occurred"
            );
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
            <div class="bg-gray-100 min-h-screen py-8 px-6">
                <!-- Profile Header -->
                <div class="max-w-4xl mx-auto bg-white rounded-lg shadow p-6">
                    <!-- Header Section -->
                    <div class="flex items-center space-x-4 mb-6">
                        <div
                            class="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center"
                        >
                            <i class="pi pi-user text-4xl text-gray-500"></i>
                        </div>
                        <div>
                            <h1
                                class="text-2xl font-semibold text-gray-800 capitalize"
                            >
                                {{ profile.last_name }} {{ profile.first_name }}
                            </h1>
                            <p class="text-sm text-gray-500 capitalize">
                                {{ profile.account_type }}
                            </p>
                        </div>
                    </div>

                    <!-- Profile Details -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <div>
                            <h2 class="text-sm font-medium text-gray-700 mb-2">
                                Email
                            </h2>
                            <p class="text-gray-800">{{ profile.email }}</p>
                        </div>
                        <div>
                            <h2 class="text-sm font-medium text-gray-700 mb-2">
                                {{ authStore.isIntern ? "Student" : "Staff" }}
                                ID
                            </h2>
                            <p class="text-gray-800">{{ profile.username }}</p>
                        </div>
                        <div v-if="authStore.isIntern">
                            <h2 class="text-sm font-medium text-gray-700 mb-2">
                                Cohort
                            </h2>
                            <p class="text-gray-800">
                                {{ profile.cohort.year }} Internship Cohort
                            </p>
                        </div>
                        <div>
                            <h2 class="text-sm font-medium text-gray-700 mb-2">
                                Phone
                            </h2>
                            <p class="text-gray-800">{{ profile.phone }}</p>
                        </div>
                    </div>

                    <!-- Divider -->
                    <hr class="my-6 border-gray-300" />

                    <!-- Change Password Section -->
                    <div>
                        <h2 class="text-xl font-semibold text-gray-800 mb-4">
                            Change Password
                        </h2>
                        <form
                            @submit.prevent="handleChangePassword"
                            class="space-y-4"
                        >
                            <div>
                                <label
                                    class="block text-sm font-medium text-gray-700"
                                    >Current Password</label
                                >
                                <input
                                    type="password"
                                    v-model="passwordData.old_password"
                                    class="mt-1 py-2 px-4 w-full border rounded-md shadow-sm text-gray-700 focus:ring-[#006938] focus:border-[#006938]"
                                />
                            </div>
                            <div>
                                <label
                                    class="block text-sm font-medium text-gray-700"
                                    >New Password</label
                                >
                                <input
                                    type="password"
                                    v-model="passwordData.new_password1"
                                    class="mt-1 py-2 px-4 w-full border rounded-md shadow-sm text-gray-700 focus:ring-[#006938] focus:border-[#006938]"
                                />
                            </div>
                            <div>
                                <label
                                    class="block text-sm font-medium text-gray-700"
                                    >Confirm New Password</label
                                >
                                <input
                                    type="password"
                                    v-model="passwordData.new_password2"
                                    class="mt-1 py-2 px-4 w-full border rounded-md shadow-sm text-gray-700 focus:ring-[#006938] focus:border-[#006938]"
                                />
                            </div>
                            <button
                                type="submit"
                                :disabled="loading"
                                class="w-full bg-maroon hover:bg-[#a00449] text-white font-medium py-2 px-4 rounded-md shadow transition disabled:opacity-50"
                            >
                                Update Password
                                <i
                                    v-if="loading"
                                    class="pi pi-spin pi-spinner-dotted text-xl ml-4"
                                ></i>
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </template>
    </DashboardLayout>
</template>
