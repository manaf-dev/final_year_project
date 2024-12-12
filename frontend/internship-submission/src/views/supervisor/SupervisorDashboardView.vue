<template>
    <DashboardLayout>
        <template #title> Dashboard </template>
        <template #content> <SupervisorHome /> </template>
    </DashboardLayout>
</template>

<script setup>
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import SupervisorHome from "@/components/supervisor/SupervisorHome.vue";
</script>
