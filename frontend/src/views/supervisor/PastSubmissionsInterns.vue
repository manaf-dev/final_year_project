<script setup>
    import BackButton from "@/components/BackButton.vue";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import FirstMonthList from "@/components/supervisor/MonthSubmissionsList.vue";
    import { useRoute } from "vue-router";

    const route = useRoute();
</script>

<template>
    <DashboardLayout :title="'Past Submissions'">
        <template #content>
            <BackButton />
            <FirstMonthList
                :month="route.params.month"
                :year="route.params.year"
            />
        </template>
    </DashboardLayout>
</template>
