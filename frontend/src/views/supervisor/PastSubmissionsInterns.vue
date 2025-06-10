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
            <div class="p-4 bg-gray-50 flex align-center justify-between">
                <BackButton />
                <h1 class="text-2xl font-bold mb-4">
                    Submissions for month {{ route.params.month }} - year {{ route.params.year }}
                </h1>
            </div>
            <MonthSubmissionsList
                :month="route.params.month"
                :year="route.params.year"
            />
        </template>
    </DashboardLayout>
</template>
