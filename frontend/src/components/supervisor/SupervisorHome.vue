<script setup>
    import apiClient from "@/services/api";
    import { useAuthStore } from "@/stores/auth";
    import { ref, computed, onMounted } from "vue";
    import Loader from "../loader.vue";

    const authStore = useAuthStore();
    const submissions = ref({});
    const interns = ref({});
    const loading = ref(false);
    const currentYear = new Date().getFullYear();
    const cohort = ref(null);

    // Computed
    const getGreeting = computed(() => {
        const hour = new Date().getHours();
        if (hour < 12) return "Good morning";
        if (hour < 18) return "Good afternoon";
        return "Good evening";
    });

    const fetchCurrentCohort = async () => {
        try {
            const response = await apiClient.get(
                `internships/cohort/${currentYear}/`
            );
            cohort.value = response.data;
        } catch (error) {
            console.error("error fetching current cohort", error);
        }
    };

    const determineMonth = () => {
        if (!cohort.value) return 1;

        const startDate = new Date(cohort.value.start_date);
        const endDate = new Date(cohort.value.end_date);
        const currentDate = new Date();

        console.log(
            "start:",
            startDate,
            "end:",
            endDate,
            "currentDate:",
            currentDate,
            "cY:",
            currentDate.getFullYear(),
            "sY:",
            startDate.getFullYear(),
            "cM:",
            currentDate.getMonth(),
            "sM:",
            startDate.getMonth()
        );
        if (currentDate < startDate) return 1;

        const monthDifference =
            (currentDate.getFullYear() - startDate.getFullYear()) * 12 +
            (currentDate.getMonth() - startDate.getMonth());
        if (monthDifference < 1) return 1;
        if (monthDifference < 2) return 2;
        if (monthDifference < 3) return 3;
        return 4;
    };

    const currentMonth = computed(determineMonth);

    const fetchSubmissions = async () => {
        try {
            const response = await apiClient.get(
                `submissions/cohort/${currentYear}/${currentMonth.value}/count/`
            );
            submissions.value = response.data;
            console.log("subs", submissions.value);
        } catch (error) {
            console.error("error fetching subs", error);
        }
    };

    const fetchInterns = async () => {
        try {
            const response = await apiClient.get(
                `accounts/cohort/${currentYear}/interns/count/`
            );
            interns.value = response.data;
            console.log("interns", interns.value);
        } catch (error) {
            console.error("error fetching interns", error);
        }
    };

    onMounted(async () => {
        loading.value = true;
        try {
            await fetchCurrentCohort();
            await fetchSubmissions();
            await fetchInterns();
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
                            {{ interns.interns_count || 0 }}
                        </h2>
                        <p class="text-gray-600">Total Interns</p>
                    </div>
                </div>

                <!-- Total Submissions -->
                <div
                    class="bg-white rounded-lg shadow-lg p-6 flex items-center space-x-4 hover:shadow-xl transition-shadow"
                >
                    <i class="pi pi-folder text-5xl text-green"></i>
                    <div>
                        <h2 class="text-3xl font-bold text-green">
                            {{ submissions.submissions_count || 0 }}
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
                                interns.interns_count -
                                    submissions.submissions_count || 0
                            }}
                        </h2>
                        <p class="text-gray-600">Pending Submissions</p>
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
                            name: 'submissions-first',
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
                    <button
                        class="mt-4 bg-yellow text-black px-4 py-2 rounded-lg hover:bg-[#ffd83e] flex items-center"
                        @click="navigateTo('notifications')"
                    >
                        <i class="pi pi-bell mr-2"></i> View Notifications
                    </button>
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
