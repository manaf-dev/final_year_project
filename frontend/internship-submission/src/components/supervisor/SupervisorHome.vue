<script setup>
    import apiClient from "@/services/api";
    import { useAuthStore } from "@/stores/auth";
    import { ref, computed, onMounted } from "vue";
    import Loader from "../loader.vue";

    const authStore = useAuthStore();
    const loading = ref(false);

    // Computed
    const getGreeting = computed(() => {
        const hour = new Date().getHours();
        if (hour < 12) return "Good morning";
        if (hour < 18) return "Good afternoon";
        return "Good evening";
    });

    const formatDate = (dateStr) => {
        const date = new Date(dateStr);
        return date.toLocaleDateString("en-GB", {
            year: "numeric",
            month: "numeric",
            day: "numeric",
        });
    };
</script>

<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Top Stats Overview -->
        <div class="max-w-7xl mx-auto px-6 lg:px-8 pt-8">
            <!-- Greeting Section -->
            <div class="mb-8">
                <div class="flex items-center justify-between">
                    <div>
                        <h1
                            class="text-2xl font-semibold text-gray-900 capitalize"
                        >
                            {{ getGreeting }}, {{ authStore.user.title }}.
                            {{ authStore.user.last_name }}! 👋
                        </h1>
                        <p class="mt-1 text-sm text-gray-500">
                            Here's what's happening with your interns
                        </p>
                    </div>
                </div>
            </div>

            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div class="bg-white p-6 rounded-xl shadow-sm">
                    <div class="flex items-center justify-between">
                        <span class="text-sm font-medium text-gray-500">
                            Total submissions
                        </span>
                        <span> 4 month(s) </span>
                    </div>
                    <div class="mt-2 flex items-baseline">
                        <span class="text-2xl font-semibold text-gray-900">
                            20
                        </span>
                        <span class="ml-2 text-sm text-gray-500"> graded </span>
                    </div>
                </div>
                <div class="bg-white p-6 rounded-xl shadow-sm">
                    <div class="flex items-center justify-between">
                        <span class="text-sm font-medium text-gray-500">
                            Graded submissions
                        </span>
                        <span> 10% </span>
                    </div>
                    <div class="mt-2 flex items-baseline">
                        <span class="text-2xl font-semibold text-gray-900">
                            1/4
                        </span>
                        <span class="ml-2 text-sm text-gray-500"> graded </span>
                    </div>
                </div>
            </div>
            <div class="bg-white rounded-xl shadow-sm p-6 mb-8">
                <h2 class="text-lg font-medium text-gray-900 mb-4">
                    Quick Actions
                </h2>
                <div class="grid grid-cols-2 gap-4">
                    <router-link
                        :to="{
                            name: 'submissions-first',
                            params: { month: '1' },
                        }"
                        class="flex flex-col items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        <span class="w-6 h-6 text-gray-700 mb-2">Icon</span>
                        <span class="text-sm text-gray-700"
                            >Submit Portfolio</span
                        >
                    </router-link>
                    <router-link
                        :to="{
                            name: 'profile',
                        }"
                        class="flex flex-col items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        <span class="w-6 h-6 text-gray-700 mb-2">Icon</span>
                        <span class="text-sm text-gray-700">View Profile</span>
                    </router-link>
                </div>
            </div>
        </div>

        <div
            v-if="loading"
            class="absolute inset-0 bg-black opacity-50 flex items-center justify-center rounded-lg z-20"
        >
            <Loader />
        </div>
    </div>
</template>
