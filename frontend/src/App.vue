<script setup>
    import { onMounted } from "vue";
    import { RouterLink, RouterView } from "vue-router";
    import { useAuthStore } from "./stores/auth";

    const authStore = useAuthStore();

    if (authStore.isAuthenticated) {
        setInterval(() => {
            authStore.getUserInfo();
        }, 1000 * 60 * 3); // Refresh every 3 minutes
    }

</script>

<template>
    <RouterView />
</template>
