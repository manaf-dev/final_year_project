<script setup>
    import { useAuthStore } from "@/stores/auth";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import Portfolio from "@/components/intern/Portfolio.vue";

    const authStore = useAuthStore();
</script>

<template>
    <DashboardLayout>
        <template #title> Your Portfolio </template>
        <template #content><Portfolio /></template>
    </DashboardLayout>
</template>
