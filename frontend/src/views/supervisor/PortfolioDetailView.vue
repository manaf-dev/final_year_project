<script setup>
    import SubmissionDetail from "@/components/supervisor/SubmissionDetail.vue";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
</script>

<template>
    <DashboardLayout :title="'Intern Portfolio'">
        <template #content><SubmissionDetail /></template>
    </DashboardLayout>
</template>
