<script setup>
    import { onMounted } from "vue";
    import { RouterLink, RouterView } from "vue-router";
    import { useAuthStore } from "./stores/auth";

    const authStore = useAuthStore();

    if (authStore.isAuthenticated) {
        // Fetch user info on initial load
        authStore.getUserInfo();
        setInterval(() => {
            authStore.getUserInfo();
        }, 1000 * 60 * 2); // Refresh every 3 minutes
    }

</script>

<template>
    <RouterView />
</template>
