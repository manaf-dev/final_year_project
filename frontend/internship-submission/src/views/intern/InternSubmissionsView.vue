<script setup>
    import { useAuthStore } from "@/stores/auth";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";

    const authStore = useAuthStore();
</script>

<template>
    <DashboardLayout>
        <template #title> Submissions </template>
        <template #content> <h1>This is the content</h1> </template>
    </DashboardLayout>
</template>
