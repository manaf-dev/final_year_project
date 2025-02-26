<script setup>
    import router from "@/router";

    const goBack = () => {
        router.back();
    };
</script>

<template>
    <button
        @click="goBack"
        class="inline-flex items-center px-4 py-2 bg-green text-white text-sm font-medium rounded-md hover:bg-green-dark focus:outline-none focus:ring focus:ring-green"
    >
        <i class="pi pi-arrow-left mr-1"></i>
        Back
    </button>
</template>
