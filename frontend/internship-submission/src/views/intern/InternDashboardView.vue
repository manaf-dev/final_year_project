<script setup>
    import { useAuthStore } from "@/stores/auth";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";

    const authStore = useAuthStore();
</script>

<template>
    <DashboardLayout>
        <template #title> Dashboard </template>
        <template #content>This is Dashboard content</template>
    </DashboardLayout>
</template>
