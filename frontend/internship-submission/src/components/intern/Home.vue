<script setup>
    import apiClient from "@/services/api";
    import { useAuthStore } from "@/stores/auth";
    import { ref, computed, onMounted } from "vue";

    const authStore = useAuthStore();

    const supervisor = authStore.user.supervisor;

    const lastUpdated = ref(new Date());
    const isRefreshing = ref(false);
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

    const stats = ref([
        { label: "Total Submissions", value: 48, unit: "files", trend: 12 },
        { label: "Completed Submissions", value: "1/4", unit: "GB", trend: -5 },
    ]);

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
    const quickActions = ref([
        {
            label: "Upload Files",
            icon: "UploadIcon",
            handler: () => {
                /* Handle upload */
            },
        },
        {
            label: "View Notifications",
            icon: "FolderPlusIcon",
            handler: () => {
                /* notifications project */
            },
        },
    ]);

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

    // Methods
    const refreshData = async () => {
        isRefreshing.value = true;
        try {
            // Implement your refresh logic here
            await new Promise((resolve) => setTimeout(resolve, 1000));
            lastUpdated.value = new Date();
        } finally {
            isRefreshing.value = false;
        }
    };

    const formatDate = (dateStr) => {
        const date = new Date(dateStr);
        return date.toLocaleDateString("en-GB", {
            year: "numeric",
            month: "numeric",
            day: "numeric",
        });
    };

    const viewSubmission = (submission) => {
        // Implement view logic
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
                    <button
                        v-for="action in quickActions"
                        :key="action.label"
                        @click="action.handler"
                        class="flex flex-col items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        <component
                            :is="action.icon"
                            class="w-6 h-6 text-gray-700 mb-2"
                        />
                        <span class="text-sm text-gray-700">{{
                            action.label
                        }}</span>
                    </button>
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
                                <svg
                                    v-if="submission.image"
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="24"
                                    height="24"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    class="text-gray-500"
                                >
                                    <rect
                                        width="18"
                                        height="18"
                                        x="3"
                                        y="3"
                                        rx="2"
                                        ry="2"
                                    />
                                    <circle cx="9" cy="9" r="2" />
                                    <path
                                        d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"
                                    />
                                </svg>
                                <svg
                                    v-if="submission.file"
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="24"
                                    height="24"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    class="text-gray-500"
                                >
                                    <path
                                        d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"
                                    />
                                    <polyline points="14 2 14 8 20 8" />
                                </svg>
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
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="18"
                                        height="18"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        stroke-width="2"
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                    >
                                        <path
                                            d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"
                                        />
                                        <polyline points="15 3 21 3 21 9" />
                                        <line x1="10" x2="21" y1="14" y2="3" />
                                    </svg>
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
                    <!-- Quick Actions -->

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
                                    {{ supervisor.title }}.
                                    {{ supervisor.last_name }}
                                    {{ supervisor.first_name }}
                                </h3>
                                <p class="text-sm text-gray-500">
                                    {{ supervisor.phone }}
                                </p>
                                <p class="text-sm text-gray-500">
                                    {{ supervisor.email }}
                                </p>
                                <p class="text-sm text-gray-500">
                                    {{ supervisor.department.name }}
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
