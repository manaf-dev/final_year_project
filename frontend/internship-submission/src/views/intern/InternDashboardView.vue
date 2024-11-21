<script setup>
    import { useAuthStore } from "@/stores/auth";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import Home from "@/components/intern/Home.vue";

    const authStore = useAuthStore();
    const supervisor = authStore.user.supervisor;
</script>

<template>
    <DashboardLayout>
        <template #title> Dashboard </template>
        <template #content>
            <Home />
        </template>
    </DashboardLayout>
</template>

<style>
    .bg-a-red {
        background-color: #8c003b;
    }
    .bg-a-green {
        background-color: #006938;
    }
    .bg-a-yellow {
        background-color: #ffc712;
    }
</style>
