<script setup>
    import { onMounted, ref } from "vue";
    import aamustedlogo from "@/assets/imgs/aamustedlogo.png";
    import InternNavItems from "./InternNavItems.vue";
    import SupervisorNavItems from "./SupervisorNavItems.vue";
    import { useAuthStore } from "@/stores/auth";

    defineProps({ sidebarOpen: Boolean });

    const emits = defineEmits(["closeSidebar"]);

    const authStore = useAuthStore();
</script>

<template>
    <div
        @click="$emit('closeSidebar')"
        :class="[
            'fixed inset-0 z-20 transition-opacity bg-black opacity-50 lg:hidden',
            sidebarOpen ? 'block' : 'hidden',
        ]"
    ></div>

    <div
        :class="[
            'fixed inset-y-0 left-0 z-30 w-64 overflow-y-auto transition duration-300 transform bg-gray-900 lg:translate-x-0 lg:static lg:inset-0',
            sidebarOpen
                ? 'translate-x-0 ease-out'
                : '-translate-x-full ease-in',
        ]"
    >
        <div class="flex items-center justify-center mt-8">
            <div class="flex items-center">
                <img :src="aamustedlogo" alt="logo" class="h-12" />
                <span class="mx-2 text-2xl font-semibold text-white"
                    >TIPSS</span
                >
            </div>
        </div>

        <InternNavItems v-if="authStore.isIntern" />
        <SupervisorNavItems v-else />
    </div>
</template>
