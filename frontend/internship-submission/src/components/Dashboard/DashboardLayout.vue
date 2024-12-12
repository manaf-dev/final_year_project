<script setup>
    import Sidebar from "./Sidebar.vue";
    import Navbar from "./Navbar.vue";
    import { ref } from "vue";

    const sidebarOpen = ref(false);
</script>

<template>
    <div class="flex h-screen bg-gray-200">
        <Sidebar
            :sidebarOpen="sidebarOpen"
            @close-sidebar="sidebarOpen = false"
        />
        <div class="flex flex-col flex-1 overflow-hidden">
            <Navbar @open-sidebar="sidebarOpen = true" />
            <main class="flex-1 overflow-y-auto bg-gray-200">
                <div class="container px-6 py-8 mx-auto">
                    <h3 class="text-3xl font-medium text-gray-700">
                        <slot name="title">Dashboard</slot>
                    </h3>
                    <slot name="content"></slot>
                </div>
            </main>
        </div>
    </div>
</template>
