<script setup>
    import apiClient from "@/services/api";
    import { useAuthStore } from "@/stores/auth";
    import { ref, computed, onMounted } from "vue";

    const authStore = useAuthStore();

    const supervisor = authStore.user.supervisor;

    const submissions = ref([]);
    const completedSubmissions = ref(0);
    const totalPortfolio = ref(0);

    const getSubmissions = async () => {
        try {
            const response = await apiClient.get("submissions/intern/");
            submissions.value = response.data;
            console.log("getting submissions...");
            submissions.value.forEach((submission) => {
                if (submission.graded) {
                    completedSubmissions.value += 1;
                }
            });
        } catch (error) {
            console.log("submissions error:", error);
        }
    };

    const getPortfolio = async () => {
        try {
            const response = await apiClient.get("portfolio/all/");
            if (response.data.images) {
                totalPortfolio.value += response.data.images.length;
            }
            if (response.data.files) {
                totalPortfolio.value += response.data.files.length;
            }
        } catch (error) {
            console.log("portfolio error:", error);
        }
    };

    const recentSubmissions = ref([]);

    const getRecents = async () => {
        try {
            const response = await apiClient.get("portfolio/recents/");
            recentSubmissions.value = response.data;

            console.log("RECENTS,", recentSubmissions.value);
        } catch (error) {
            console.error("Recents error:", error);
        }
    };

    onMounted(async () => {
        await getSubmissions();
        await getPortfolio();
        await getRecents();
    });

    const upcomingDeadlines = ref([
        {
            id: 2,
            title: "Month Submission",
            daysLeft: 5,
        },
    ]);

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
                    <div class="flex items-center gap-3">
                        <span
                            v-if="recentSubmissions.length"
                            class="text-sm text-gray-500"
                            >Last updated:
                            {{
                                formatDate(recentSubmissions[0].uploaded_at)
                            }}</span
                        >
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
                        <span> {{ submissions.length }} month(s) </span>
                    </div>
                    <div class="mt-2 flex items-baseline">
                        <span class="text-2xl font-semibold text-gray-900">
                            {{ totalPortfolio }}
                        </span>
                        <span class="ml-2 text-sm text-gray-500"> files </span>
                    </div>
                </div>
                <div class="bg-white p-6 rounded-xl shadow-sm">
                    <div class="flex items-center justify-between">
                        <span class="text-sm font-medium text-gray-500">
                            Completed submissions
                        </span>
                        <span> {{ (completedSubmissions / 4) * 100 }}% </span>
                    </div>
                    <div class="mt-2 flex items-baseline">
                        <span class="text-2xl font-semibold text-gray-900">
                            {{ completedSubmissions + "/4" }}
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
                            name: 'first-submission',
                            params: { month: completedSubmissions + 1 },
                        }"
                        class="flex flex-col items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        <span class="w-6 h-6 text-gray-700 mb-2"
                            ><i class="pi pi-save" style="font-size: 1rem"></i
                        ></span>
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
                        <span class="w-6 h-6 text-gray-700 mb-2"
                            ><i class="pi pi-user" style="font-size: 1rem"></i
                        ></span>
                        <span class="text-sm text-gray-700">View Profile</span>
                    </router-link>
                </div>
            </div>

            <!-- Main Content Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Recent Submissions -->
                <div class="lg:col-span-2 bg-white rounded-xl shadow-sm p-6">
                    <div class="flex items-center justify-between mb-6">
                        <h2 class="text-lg font-medium text-gray-900">
                            Recent Submissions
                        </h2>
                        <router-link
                            :to="{ name: 'intern-portfolio' }"
                            class="text-sm text-blue-600 hover:text-blue-700"
                        >
                            View all
                        </router-link>
                    </div>

                    <div class="space-y-4">
                        <div
                            v-for="submission in recentSubmissions"
                            :key="submission.id"
                            class="flex items-center gap-4 p-4 hover:bg-gray-50 rounded-lg transition-colors"
                        >
                            <div
                                class="w-12 h-12 rounded-lg bg-gray-100 flex items-center justify-center"
                            >
                                <i
                                    v-if="submission.image"
                                    class="pi pi-image"
                                    style="font-size: 1rem"
                                ></i>
                                <i
                                    v-if="submission.file"
                                    class="pi pi-file-check"
                                    style="font-size: 1rem"
                                ></i>
                            </div>

                            <div class="flex-1 min-w-0">
                                <h3
                                    class="text-sm font-medium text-gray-900 truncate"
                                >
                                    {{
                                        submission.image
                                            ? "Portfolio image"
                                            : "Portfolio file"
                                    }}
                                </h3>
                                <p class="text-sm text-gray-500">
                                    {{ formatDate(submission.uploaded_at) }}
                                </p>
                            </div>

                            <div class="flex items-center gap-2">
                                <a
                                    :href="
                                        submission.image
                                            ? submission.image
                                            : submission.file
                                    "
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                                >
                                    <i
                                        class="pi pi-external-link"
                                        style="font-size: 1rem"
                                    ></i>
                                </a>
                            </div>
                        </div>

                        <div
                            v-if="!recentSubmissions.length"
                            class="text-center py-8 text-gray-500"
                        >
                            No recent submissions
                        </div>
                    </div>
                </div>

                <!-- Side Panel -->
                <div class="space-y-6">
                    <!-- Upcoming Deadlines -->
                    <div class="bg-white rounded-xl shadow-sm p-6">
                        <h2 class="text-lg font-medium text-gray-900 mb-4">
                            Supervisor
                        </h2>
                        <div class="space-y-4">
                            <div class="flex-1">
                                <h3
                                    class="text-sm font-medium text-gray-900 capitalize"
                                >
                                    {{ supervisor?.title }}.
                                    {{ supervisor?.last_name }}
                                    {{ supervisor?.first_name }}
                                </h3>
                                <p class="text-sm text-gray-500">
                                    {{ supervisor?.phone }}
                                </p>
                                <p class="text-sm text-gray-500">
                                    {{ supervisor?.email }}
                                </p>
                                <p class="text-sm text-gray-500">
                                    {{ supervisor?.department.name }}
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="bg-white rounded-xl shadow-sm p-6">
                        <h2 class="text-lg font-medium text-gray-900 mb-4">
                            Upcoming Deadlines
                        </h2>
                        <div class="space-y-4">
                            <div
                                v-for="deadline in upcomingDeadlines"
                                :key="deadline.id"
                                class="flex items-center gap-3"
                            >
                                <div
                                    class="w-2 h-2 rounded-full"
                                    :class="{
                                        'bg-red-500': deadline.daysLeft <= 3,
                                        'bg-yellow-500':
                                            deadline.daysLeft <= 7 &&
                                            deadline.daysLeft > 3,
                                        'bg-green-500': deadline.daysLeft > 7,
                                    }"
                                ></div>
                                <div class="flex-1">
                                    <h3
                                        class="text-sm font-medium text-gray-900"
                                    >
                                        {{ deadline.title }}
                                    </h3>
                                    <p class="text-sm text-gray-500">
                                        Due in {{ deadline.daysLeft }} days
                                    </p>
                                </div>
                            </div>

                            <div
                                v-if="!upcomingDeadlines.length"
                                class="text-center py-4 text-gray-500"
                            >
                                No upcoming deadlines
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
