<script setup>
    import ProfileDropdown from "./ProfileDropdown.vue";
    import NotificationMenu from "./NotificationMenu.vue";
</script>

<template>
    <header
        class="flex items-center justify-between px-6 py-4 bg-white border-b-4 border-red-700"
    >
        <button
            @click="$emit('openSidebar')"
            class="text-gray-500 focus:outline-none lg:hidden"
        >
            <i class="pi pi-align-left" style="font-size: 1.3rem"></i>
        </button>

        <div class="flex items-center">
            <NotificationMenu />
            <ProfileDropdown />
        </div>
    </header>
</template>
