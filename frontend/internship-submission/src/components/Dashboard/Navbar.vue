<script setup>
    import { ref } from "vue";
    import ProfileDropdown from "./ProfileDropdown.vue";
    import NotificationMenu from "./NotificationMenu.vue";

    defineProps({
        sidebarOpen: Boolean,
    });
    const sidebarOpen = ref(false);
</script>

<template>
    <header
        class="flex items-center justify-between px-6 py-4 bg-white border-b-4 border-red-700"
    >
        <div class="flex items-center">
            <button
                @click="$emit('openSidebar')"
                class="text-gray-500 focus:outline-none lg:hidden"
            >
                <svg
                    class="w-6 h-6"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <path
                        d="M4 6H20M4 12H20M4 18H11"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    ></path>
                </svg>
            </button>
        </div>

        <div class="flex items-center">
            <NotificationMenu />
            <ProfileDropdown />
        </div>
    </header>
</template>
