<script setup>
    import router from "@/router";
    import { useAuthStore } from "@/stores/auth";

    const authStore = useAuthStore();

    const goHome = () => {
        if (authStore.isIntern) {
            router.push({ name: "intern-dashboard" });
        } else {
            router.push({ name: "supervisor-dashboard" });
        }
    };

    const goBack = () => router.back();
</script>

<template>
    <div
        class="bg-gray-100 min-h-screen flex flex-col items-center justify-center"
    >
        <!-- Icon -->
        <div class="text-maroon mb-6">
            <i class="pi pi-exclamation-circle text-7xl"></i>
        </div>

        <!-- Main Message -->
        <h1 class="text-4xl font-bold text-maroon mb-2">404</h1>
        <h2 class="text-2xl font-semibold text-gray-700 mb-4">
            Page Not Found
        </h2>

        <!-- Description -->
        <p class="text-gray-600 text-center max-w-md">
            Oops! The page you are looking for does not exist or has been moved.
            Use the navigation options below to find your way.
        </p>

        <!-- Navigation Buttons -->
        <div class="mt-8 flex space-x-4">
            <button
                @click="goHome"
                class="bg-green hover:bg-[#00894b] text-white font-medium py-2 px-6 rounded-lg shadow flex items-center"
            >
                <i class="pi pi-home mr-2"></i> Go to Dashboard
            </button>
            <button
                @click="goBack"
                class="bg-yellow hover:bg-[#ffd83e] text-black font-medium py-2 px-6 rounded-lg shadow flex items-center"
            >
                <i class="pi pi-arrow-left mr-2"></i> Back to Previous Page
            </button>
        </div>
    </div>
</template>
