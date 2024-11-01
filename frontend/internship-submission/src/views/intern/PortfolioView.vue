<script setup>
    import { useAuthStore } from "@/stores/auth";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";

    const authStore = useAuthStore();
</script>

<template>
    <DashboardLayout>
        <template #title> Your Portfolio </template>
        <template #content>This is your Portfolio</template>
    </DashboardLayout>
</template>
