<script setup>
    import BackButton from "@/components/BackButton.vue";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import MonthSubmissionsList from "@/components/supervisor/MonthSubmissionsList.vue";
    import { useRoute } from "vue-router";

    const route = useRoute();
</script>

<template>
    <DashboardLayout :title="'Past Submissions'">
        <template #content>
            <div class="bg-gray-50 min-h-screen">
                <div class="bg-white shadow-sm border-b border-gray-200">
                    <div class="max-w-7xl mx-auto px-6 py-4">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-4">
                                <BackButton />
                                <div>
                                    <h1 class="text-2xl font-bold text-gray-900">
                                        Month {{ route.params.month }} Submissions
                                    </h1>
                                    <p class="text-gray-600 mt-1">
                                        {{ route.params.year }} Cohort • Internship Period {{ route.params.month }}
                                    </p>
                                </div>
                            </div>
                            <div class="flex items-center space-x-2 text-sm text-gray-500">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3a2 2 0 012-2h4a2 2 0 012 2v4m-6 0V3a2 2 0 012-2h4a2 2 0 012 2v4m-6 0a2 2 0 00-2 2v6a2 2 0 002 2h8a2 2 0 002-2V9a2 2 0 00-2-2H8z"></path>
                                </svg>
                                <span>Academic Year {{ route.params.year }}</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <MonthSubmissionsList
                    :month="route.params.month"
                    :year="route.params.year"
                />
            </div>
        </template>
    </DashboardLayout>
</template>
