<script setup>
    import { useAuthStore } from "@/stores/auth";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import Submission from "@/components/intern/Submission.vue";
    import NewSubmission from "@/components/intern/NewSubmission.vue";

    const authStore = useAuthStore();
</script>

<template>
    <DashboardLayout>
        <template #title> Second Month Submission </template>
        <template #content> <Submission :month="2" /> </template>
    </DashboardLayout>
</template>
