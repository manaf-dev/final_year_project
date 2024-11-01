<script setup>
    import { useAuthStore } from "@/stores/auth";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";

    const authStore = useAuthStore();
</script>

<template>
    <DashboardLayout>
        <template #title> Internship School </template>
        <template #content>This is Internship School content</template>
    </DashboardLayout>
</template>
