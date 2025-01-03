<script setup>
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import SupervisorHome from "@/components/supervisor/SupervisorHome.vue";
</script>

<template>
    <DashboardLayout :title="'Dashboard'">
        <template #content> <SupervisorHome /> </template>
    </DashboardLayout>
</template>
