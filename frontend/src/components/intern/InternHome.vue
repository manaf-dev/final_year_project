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
            // console.log("getting submissions...");
            submissions.value.forEach((submission) => {
                if (submission.graded) {
                    completedSubmissions.value += 1;
                }
            });
        } catch (error) {
            throw new Error("Error fetching submissions");
        }
    };

    const getPortfolioCount = async () => {
        try {
            const response = await apiClient.get("portfolio/count-all/");
            totalPortfolio.value += response.data.portfolio_count;
        } catch (error) {
            throw new Error("Error fetching portfolio count");
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
            await getPortfolioCount();
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

    const currentSubmission = computed(() => {
        if (completedSubmissions.value === 0) {
            return completedSubmissions.value + 1;
        } else {
            return completedSubmissions.value;
        }
    });
</script>

<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Top Stats Overview -->
        <div class="max-w-7xl mx-auto px-6 lg:px-8 py-8">
            <!-- Greeting Section -->
            <div class="mb-8">
                <div class="flex items-center justify-between">
                    <div>
                        <h1 class="text-2xl font-semibold text-gray-900">
                            {{ getGreeting }}, {{ authStore.user.first_name }}!
                            👋
                        </h1>
                        <p class="mt-1 text-sm text-gray-500">
                            Here's what's happening with your portfolio
                        </p>
                    </div>
                </div>
            </div>

            <!-- Stats Cards -->

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
                <!-- Total Submissions -->
                <div
                    class="bg-white rounded-lg shadow-lg p-6 flex items-center space-x-4 hover:shadow-xl transition-shadow"
                >
                    <i class="pi pi-file text-5xl text-maroon"></i>
                    <div>
                        <h2 class="text-3xl font-bold text-maroon">
                            {{ totalPortfolio }}
                        </h2>
                        <p class="text-gray-600">Total Portfolio</p>
                    </div>
                </div>

                <!-- Pending Submissions -->
                <div
                    class="bg-white rounded-lg shadow-lg p-6 flex items-center space-x-4 hover:shadow-xl transition-shadow"
                >
                    <i class="pi pi-check text-5xl text-green"></i>
                    <div>
                        <h2 class="text-3xl font-bold text-green">
                            {{ completedSubmissions }}
                        </h2>
                        <p class="text-gray-600">Graded Submissions</p>
                    </div>
                </div>

                <!-- Supervisor -->
                <div
                    class="bg-white rounded-lg shadow-lg p-6 flex items-center space-x-4 hover:shadow-xl transition-shadow"
                >
                    <i class="pi pi-user text-5xl text-yellow"></i>
                    <div>
                        <h2 class="text-3xl font-bold text-yellow capitalize">
                            {{ supervisor.title }}.
                            {{ supervisor.last_name }}
                            {{ supervisor.first_name }}
                        </h2>
                        <p class="text-gray-600">Supervisor</p>
                    </div>
                </div>
            </div>

            <!-- Main Content -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
                <!-- Card: Upload Portfolio -->
                <div
                    class="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow"
                >
                    <i class="pi pi-upload text-maroon text-4xl mb-4"></i>
                    <h2 class="text-xl font-semibold text-maroon">
                        Upload Portfolio
                    </h2>
                    <p class="text-gray-600 mt-2">
                        Upload your teaching philosophy, CV, and monthly reports
                        here.
                    </p>
                    <router-link
                        :to="{
                            name: 'submissions-page',
                            params: { month: 1 },
                        }"
                        class="mt-4 bg-maroon text-white px-4 py-2 w-fit rounded-lg hover:bg-[#a00048] flex items-center"
                    >
                        <i class="pi pi-upload mr-2"></i> Upload Now
                    </router-link>
                </div>

                <!-- Card: View Feedback -->
                <div
                    class="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow"
                >
                    <i class="pi pi-comment text-green text-4xl mb-4"></i>
                    <h2 class="text-xl font-semibold text-green">
                        View Feedback
                    </h2>
                    <p class="text-gray-600 mt-2">
                        Check comments and grades from your supervisor on your
                        submissions.
                    </p>
                    <router-link
                        :to="{
                            name: 'submissions-page',
                            params: { month: currentSubmission },
                        }"
                        class="mt-4 bg-green text-white px-4 py-2 w-fit rounded-lg hover:bg-[#008f4f] flex items-center"
                    >
                        <i class="pi pi-eye mr-2"></i> View Feedback
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
                        Stay updated with deadlines, feedback, and important
                        announcements.
                    </p>
                    <router-link
                        :to="{ name: 'notifications' }"
                        class="mt-4 bg-yellow text-black px-4 py-2 rounded-lg hover:bg-[#ffd83e] flex items-center"
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
