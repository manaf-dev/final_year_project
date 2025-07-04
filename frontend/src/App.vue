<script setup>
    import { onMounted } from "vue";
    import { RouterLink, RouterView } from "vue-router";
    import { useAuthStore } from "./stores/auth";

    const authStore = useAuthStore();

    if (authStore.isAuthenticated) {
        authStore.getUserInfo();
    }

</script>

<template>
    <RouterView />
</template>
