<script setup>
    import apiClient from "@/services/api";
    import { useAuthStore } from "@/stores/auth";
    import { ref, computed, onMounted } from "vue";
    import Loader from "../loader.vue";
    import router from "@/router";

    const authStore = useAuthStore();
    const submissionCounts = ref({});
    const currentYear = new Date().getFullYear();
    const loading = ref(false);

    // Computed
    const getGreeting = computed(() => {
        const hour = new Date().getHours();
        if (hour < 12) return "Good morning";
        if (hour < 18) return "Good afternoon";
        return "Good evening";
    });

    const getSubmissionCounts = async () => {
        try {
            const response = await apiClient.get(
                `submissions/cohort/${currentYear}/count/`
            );
            submissionCounts.value = response.data;
            // console.log("subs", submissionCounts.value);
        } catch (error) {
            console.error("error fetching subs", error);
        }
    };

    onMounted(async () => {
        loading.value = true;
        try {
            console.log('fetching....')
            await getSubmissionCounts();
        } catch (error) {
            console.error("error fetching data", error);
        } finally {
            loading.value = false;
        }
    });
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-gray-50 via-red-50 to-yellow-50">
        <div class="max-w-7xl mx-auto px-6 lg:px-8 py-8">
            <!-- Enhanced Greeting Section -->
            <div class="mb-8">
                <div class="bg-gradient-to-r from-maroon via-green to-green rounded-3xl p-8 text-white relative overflow-hidden">
                    <div class="absolute inset-0 bg-black/5"></div>
                    <div class="relative z-10">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-6">
                                <!-- Supervisor Avatar -->
                                <div class="w-20 h-20 rounded-full bg-white/20 backdrop-blur-sm border border-white/30 flex items-center justify-center text-2xl font-bold">
                                    {{ (authStore.user.first_name?.charAt(0) + authStore.user.last_name?.charAt(0))?.toUpperCase() || 'S' }}
                                </div>
                                
                                <div>
                                    <h1 class="text-3xl font-bold mb-2 capitalize">
                                        {{ getGreeting }}, {{ authStore.user.title }}. {{ authStore.user.last_name }}! 👋
                                    </h1>
                                    <p class="text-gray-100 text-lg">
                                        Managing your {{ currentYear }} internship cohort
                                    </p>
                                    <div class="mt-3 flex items-center space-x-4">
                                        <span class="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-sm border border-white/30">
                                            Academic Supervisor
                                        </span>
                                        <span class="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-sm border border-white/30">
                                            {{ submissionCounts.interns_count || 0 }} Active Interns
                                        </span>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Quick Progress Summary -->
                            <div class="hidden md:block">
                                <div class="text-right">
                                    <div class="text-2xl font-bold">{{ submissionCounts.graded_submissions_count || 0 }}</div>
                                    <div class="text-sm text-gray-100">Graded This Month</div>
                                    <div class="text-sm text-gray-200 mt-1">
                                        {{ submissionCounts.submissions_count || 0 }} Total Submissions
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Decorative elements -->
                    <div class="absolute -top-8 -right-8 w-32 h-32 rounded-full bg-white/10"></div>
                    <div class="absolute -bottom-4 -left-4 w-24 h-24 rounded-full bg-white/5"></div>
                </div>
            </div>

            <!-- Enhanced Stats Section -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <!-- Total Interns -->
                <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
                    <div class="p-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-3xl font-bold text-maroon mb-1">
                                    {{ submissionCounts.interns_count || 0 }}
                                </div>
                                <div class="text-gray-600 font-medium">Assigned Interns</div>
                                <div class="text-sm text-gray-500 mt-1">Currently supervising</div>
                            </div>
                            <div class="w-14 h-14 bg-gradient-to-br from-maroon to-red-700 rounded-2xl flex items-center justify-center">
                                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
                                </svg>
                            </div>
                        </div>
                        
                    </div>
                </div>

                <!-- Total Submissions -->
                <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
                    <div class="p-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-3xl font-bold text-green mb-1">
                                    {{ submissionCounts.submissions_count || 0 }}
                                </div>
                                <div class="text-gray-600 font-medium">Total Submissions</div>
                                <div class="text-sm text-gray-500 mt-1">All time submissions</div>
                            </div>
                            <div class="w-14 h-14 bg-gradient-to-br from-green to-green rounded-2xl flex items-center justify-center">
                                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                                </svg>
                            </div>
                        </div>
                        
                    </div>
                </div>

                <!-- Graded Submissions -->
                <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
                    <div class="p-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-3xl font-bold text-yellow mb-1">
                                    {{ submissionCounts.graded_submissions_count || 0 }}
                                </div>
                                <div class="text-gray-600 font-medium">Graded Submissions</div>
                                <div class="text-sm text-gray-500 mt-1">Completed reviews</div>
                            </div>
                            <div class="w-14 h-14 bg-gradient-to-br from-yellow to-orange-500  rounded-2xl flex items-center justify-center">
                                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                            </div>
                        </div>
                        
                    </div>
                </div>
            </div>

            <!-- Enhanced Action Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- View Cohorts Card -->
                <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 group">
                    <div class="p-8">
                        <div class="w-16 h-16 bg-gradient-to-br from-maroon to-red-700 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
                            </svg>
                        </div>
                        
                        <h3 class="text-xl font-bold text-gray-900 mb-3">Manage Cohorts</h3>
                        <p class="text-gray-600 mb-6 leading-relaxed">
                            View and manage all cohorts assigned to you. Check current and past cohorts with assigned interns.
                        </p>
                        
                        <router-link
                            :to="{ name: 'cohorts-list' }"
                            class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-maroon to-red-600 text-white font-medium rounded-xl hover:from-red-600 hover:to-red-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                        >
                            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                            </svg>
                            View Cohorts
                        </router-link>
                        
                        
                    </div>
                </div>

                <!-- Grading Submissions Card -->
                <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 group">
                    <div class="p-8">
                        <div class="w-16 h-16 bg-gradient-to-br from-green to-green rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                            </svg>
                        </div>
                        
                        <h3 class="text-xl font-bold text-gray-900 mb-3">Grade Submissions</h3>
                        <p class="text-gray-600 mb-6 leading-relaxed">
                            Review and grade submissions from interns. Provide detailed comments and constructive feedback.
                        </p>
                        
                        <router-link
                            :to="{ name: 'submissions-list', params: { month: '1' } }"
                            class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-green to-green text-white font-medium rounded-xl hover:from-green-700 hover:to-green-800 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                        >
                            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                            </svg>
                            Start Grading
                        </router-link>
                        
                        
                    </div>
                </div>

                <!-- Notifications Card -->
                <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 group">
                    <div class="p-8">
                        <div class="w-16 h-16 bg-gradient-to-br from-yellow to-yellow rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM12 7a4 4 0 00-4 4v6h8v-6a4 4 0 00-4-4zM8 7V6a4 4 0 118 0v1"></path>
                            </svg>
                        </div>
                        
                        <h3 class="text-xl font-bold text-gray-900 mb-3">Notifications</h3>
                        <p class="text-gray-600 mb-6 leading-relaxed">
                            Stay updated with the latest notifications about submissions, grading deadlines, and system updates.
                        </p>
                        
                        <router-link
                            :to="{ name: 'notifications' }"
                            class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-yellow to-yellow  text-white font-medium rounded-xl hover:from-yellow-600 hover:to-yellow-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                        >
                            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM12 7a4 4 0 00-4 4v6h8v-6a4 4 0 00-4-4zM8 7V6a4 4 0 118 0v1"></path>
                            </svg>
                            View Notifications
                        </router-link>
                        
                        
                    </div>
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
