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
                        <p class="mt-2 text-sm text-gray-500">
                            This is the internship stats for this month
                        </p>
                    </div>
                </div>
            </div>

            <!-- Stats Section -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
                <!-- Total Interns -->
                <div
                    class="bg-white rounded-lg shadow-lg p-6 flex items-center space-x-4 hover:shadow-xl transition-shadow"
                >
                    <i class="pi pi-users text-5xl text-maroon"></i>
                    <div>
                        <h2 class="text-3xl font-bold text-maroon">
                            {{ submissionCounts.interns_count }}
                        </h2>
                        <p class="text-gray-600">Total Assigned Interns</p>
                    </div>
                </div>

                <!-- Total Submissions -->
                <div
                    class="bg-white rounded-lg shadow-lg p-6 flex items-center space-x-4 hover:shadow-xl transition-shadow"
                >
                    <i class="pi pi-folder text-5xl text-green"></i>
                    <div>
                        <h2 class="text-3xl font-bold text-green">
                            {{ submissionCounts.submissions_count }}
                        </h2>
                        <p class="text-gray-600">Total Submissions</p>
                    </div>
                </div>

                <!-- Pending Submissions -->
                <div
                    class="bg-white rounded-lg shadow-lg p-6 flex items-center space-x-4 hover:shadow-xl transition-shadow"
                >
                    <i class="pi pi-clock text-5xl text-yellow"></i>
                    <div>
                        <h2 class="text-3xl font-bold text-yellow">
                            {{
                                submissionCounts.graded_submissions_count
                            }}
                        </h2>
                        <p class="text-gray-600">Graded Submissions</p>
                    </div>
                </div>
            </div>

            <!-- Main Content -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
                <!-- Card: View Cohorts -->
                <div
                    class="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow"
                >
                    <i class="pi pi-users text-maroon text-4xl mb-4"></i>
                    <h2 class="text-xl font-semibold text-maroon">
                        View Cohorts
                    </h2>
                    <p class="text-gray-600 mt-2">
                        View and manage all cohorts assigned to you. Check
                        current and past cohorts with assigned interns.
                    </p>
                    <router-link
                        class="mt-4 bg-maroon text-white px-4 py-2 rounded-lg hover:bg-[#a00048] flex items-center"
                        :to="{ name: 'cohorts-list' }"
                    >
                        <i class="pi pi-eye mr-2"></i> View Cohorts
                    </router-link>
                </div>

                <!-- Card: Grading Submissions -->
                <div
                    class="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow"
                >
                    <i class="pi pi-file-edit text-green text-4xl mb-4"></i>
                    <h2 class="text-xl font-semibold text-green">
                        Grading Submissions
                    </h2>
                    <p class="text-gray-600 mt-2">
                        Review and grade submissions from interns. Provide
                        comments and feedback on portfolios.
                    </p>
                    <router-link
                        class="mt-4 bg-green text-white px-4 py-2 rounded-lg hover:bg-[#008f4f] flex items-center"
                        :to="{
                            name: 'submissions-list',
                            params: { month: '1' },
                        }"
                    >
                        <i class="pi pi-pencil mr-2"></i> Grade Submissions
                    </router-link>
                </div>

                <!-- Card: Notifications -->
                <div
                    class="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow"
                >
                    <i class="pi pi-bell text-yellow text-4xl mb-4"></i>
                    <h2 class="text-xl font-semibold text-yellow">
                        Notifications
                    </h2>
                    <p class="text-gray-600 mt-2">
                        Stay updated with the latest notifications about
                        submissions, grading, and system updates.
                    </p>
                    <router-link
                        class="mt-4 bg-yellow text-black px-4 py-2 rounded-lg hover:bg-[#ffd83e] flex items-center"
                        :to="{ name: 'notifications' }"
                    >
                        <i class="pi pi-bell mr-2"></i> View Notifications
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
