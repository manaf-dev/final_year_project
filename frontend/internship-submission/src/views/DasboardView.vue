<script setup>
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import { useAuthStore } from "@/stores/auth";

    const authStore = useAuthStore();

    console.log("intern", authStore.isIntern);
    console.log("auth", authStore.isAuthenticated);
    console.log("sup", authStore.isSupervisor);
    console.log("getuser", authStore.getUser);
    console.log("details", authStore.hasProvidedDetails);
</script>

<template>
    <DashboardLayout />
</template>
