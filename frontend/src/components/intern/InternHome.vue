<script setup>
    import apiClient from "@/services/api";
    import { useAuthStore } from "@/stores/auth";
    import { ref, computed, onMounted } from "vue";
    import Loader from "../loader.vue";

    const authStore = useAuthStore();

    const supervisor = authStore.user.supervisor;

    const submissions = ref([]);
    const completedSubmissions = ref(0);
    const totalPortfolio = ref(0);
    const loading = ref(false);

    const getSubmissions = async () => {
        try {
            const response = await apiClient.get("submissions/intern/");
            submissions.value = response.data;
        } catch (error) {
            throw new Error("Error fetching submissions");
        }
    };

    // const recentSubmissions = ref([]);

    // const getRecents = async () => {
    //     try {
    //         const response = await apiClient.get("portfolio/recents/");
    //         recentSubmissions.value = response.data;

    //         console.log("RECENTS,", recentSubmissions.value);
    //     } catch (error) {
    //         console.error("Recents error:", error);
    //     }
    // };

    onMounted(async () => {
        loading.value = true;
        try {
            await getSubmissions();
            // await getRecents();
        } catch (error) {
            throw new Error("Error fetching data");
        } finally {
            loading.value = false;
        }
    });

    // Computed
    const getGreeting = computed(() => {
        const hour = new Date().getHours();
        if (hour < 12) return "Good morning";
        if (hour < 18) return "Good afternoon";
        return "Good evening";
    });

    // const currentSubmission = computed(() => {
    //     if (completedSubmissions.value === 0) {
    //         return completedSubmissions.value + 1;
    //     } else {
    //         return submissions.graded_submissions.value;
    //     }
    // });
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
        <div class="max-w-7xl mx-auto px-6 lg:px-8 py-8">
            <!-- Enhanced Greeting Section -->
            <div class="mb-8">
                <div class="bg-gradient-to-r from-maroon via-green to-green rounded-3xl p-8 text-white relative overflow-hidden">
                    <div class="absolute inset-0 bg-black/5"></div>
                    <div class="relative z-10">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-6">
                                <!-- User Avatar -->
                                <div class="w-16 h-16 rounded-full bg-white/20 backdrop-blur-sm border border-white/30 flex items-center justify-center text-2xl font-bold">
                                    {{ authStore.user.first_name?.charAt(0)?.toUpperCase() || 'U' }}
                                </div>
                                
                                <div>
                                    <h1 class="text-3xl font-bold mb-2">
                                        {{ getGreeting }}, {{ authStore.user.first_name }}! 👋
                                    </h1>
                                    <p class="text-gray-100 text-lg">
                                        Here's your portfolio overview and progress
                                    </p>
                                    <div class="mt-3 flex items-center space-x-4">
                                        <span class="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-sm border border-white/30">
                                            Teaching Intern
                                        </span>
                                        <span class="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-sm border border-white/30">
                                            {{ new Date().getFullYear() }} Cohort
                                        </span>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Quick Progress Ring -->
                            <div class="hidden md:flex items-center space-x-4">
                                <div class="text-right">
                                    <div class="text-2xl font-bold">{{ Math.round((submissions.graded_submissions / 4) * 100) }}%</div>
                                    <div class="text-sm text-blue-100">Complete</div>
                                </div>
                                <div class="w-16 h-16 rounded-full border-4 border-white/30 flex items-center justify-center relative">
                                    <div class="absolute inset-0 rounded-full border-4 border-transparent border-t-white transform rotate-45" 
                                         :style="`transform: rotate(${(submissions.graded_submissions / 4) * 360}deg)`"></div>
                                    <span class="text-sm font-bold">{{ submissions.graded_submissions }}/4</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Decorative elements -->
                    <div class="absolute -top-8 -right-8 w-32 h-32 rounded-full bg-white/10"></div>
                    <div class="absolute -bottom-4 -left-4 w-24 h-24 rounded-full bg-white/5"></div>
                </div>
            </div>

            <!-- Enhanced Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <!-- Total Portfolio -->
                <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
                    <div class="p-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-3xl font-bold text-maroon mb-1">
                                    {{ submissions.portfolio_count }}
                                </div>
                                <div class="text-gray-600 font-medium">Total Portfolio Items</div>
                                <div class="text-sm text-gray-500 mt-1">Uploaded images/documents</div>
                            </div>
                            <div class="w-14 h-14 bg-gradient-to-br from-maroon to-red-600 rounded-2xl flex items-center justify-center">
                                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                </svg>
                            </div>
                        </div>
                        <div class="mt-4 bg-red-50 rounded-lg p-3">
                            <div class="flex items-center text-sm text-maroon">
                                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                                </svg>
                                Keep building your portfolio
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Graded Submissions -->
                <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
                    <div class="p-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-3xl font-bold text-green-600 mb-1">
                                    {{ submissions.graded_submissions }}
                                </div>
                                <div class="text-gray-600 font-medium">Graded Submissions</div>
                                <div class="text-sm text-gray-500 mt-1">Reviewed by supervisor</div>
                            </div>
                            <div class="w-14 h-14 bg-gradient-to-br from-green to-green rounded-2xl flex items-center justify-center">
                                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                            </div>
                        </div>
                        <div class="mt-4 bg-green-50 rounded-lg p-3">
                            <div class="flex items-center text-sm text-green">
                                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                                </svg>
                                {{ submissions.graded_submissions === 0 ? 'Start your first submission' : 'Great progress!' }}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Supervisor -->
                <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
                    <div class="p-6">
                        <div class="flex items-center justify-between">
                            <div class="flex-1">
                                <div class="text-lg font-bold text-yellow mb-1 capitalize truncate">
                                    {{ supervisor?.title }}. {{ supervisor?.last_name }}
                                </div>
                                <div class="text-gray-600 font-medium">Your Supervisor</div>
                                <div class="text-sm text-gray-500 mt-1 truncate">{{ supervisor?.department?.name }}</div>
                            </div>
                            <div class="w-14 h-14 bg-gradient-to-br from-yellow to-yellow rounded-2xl flex items-center justify-center">
                                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                                </svg>
                            </div>
                        </div>
                        <div class="mt-4 bg-yellow-50 rounded-lg p-3">
                            <router-link :to="{ name: 'intern-supervisor' }" class="flex items-center text-sm text-orange-500  hover:text-yellow-800 transition-colors">
                                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                                </svg>
                                View supervisor details
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Enhanced Action Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Upload Portfolio Card -->
                <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 group">
                    <div class="p-8">
                        <div class="w-16 h-16 bg-gradient-to-br from-maroon to-red-700 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                            </svg>
                        </div>
                        
                        <h3 class="text-xl font-bold text-gray-900 mb-3">Upload Portfolio</h3>
                        <p class="text-gray-600 mb-6 leading-relaxed">
                            Upload your teaching philosophy, CV, reflective documents, and monthly portfolio images.
                        </p>
                        
                        <router-link
                            :to="{ name: 'submissions-page', params: { month: 1 } }"
                            class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-maroon to-red-600 text-white font-medium rounded-xl hover:from-red-600 hover:to-red-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                        >
                            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                            </svg>
                            Upload Now
                        </router-link>
                        
                    </div>
                </div>

                <!-- View Feedback Card -->
                <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 group">
                    <div class="p-8">
                        <div class="w-16 h-16 bg-gradient-to-br from-green to-green rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                            </svg>
                        </div>
                        
                        <h3 class="text-xl font-bold text-gray-900 mb-3">View Feedback</h3>
                        <p class="text-gray-600 mb-6 leading-relaxed">
                            Check detailed comments, grades, and constructive feedback from your supervisor.
                        </p>
                        
                        <router-link
                            :to="{ name: 'submissions-page', params: { month: 1 } }"
                            class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-green to-green text-white font-medium rounded-xl hover:from-green-700 hover:to-green-800 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                        >
                            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                            </svg>
                            View Feedback
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
                            Stay updated with deadlines, feedback notifications, and important announcements.
                        </p>
                        
                        <router-link
                            :to="{ name: 'notifications' }"
                            class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-yellow to-yellow text-white font-medium rounded-xl hover:from-yellow-600 hover:to-orange-600 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
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
