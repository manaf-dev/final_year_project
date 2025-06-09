<script setup>
    import { onMounted, ref } from "vue";
    import DefaultProfile from "@/assets/imgs/defaultProfile.png";
    import apiClient from "@/services/api";

    const notificationOpen = ref(false);
    const notifications = ref({});

    const get_notifications = async () => {
        try {
            const response = await apiClient.get("submissions/notifications/");
            notifications.value = response.data;
        } catch (error) {
            throw new Error("Error fetching notifications");
        }
    };

    onMounted(get_notifications);

    const toggleNotifications = () => {
        notificationOpen.value = !notificationOpen.value;
    };
</script>

<template>
    <div class="relative">
        <button
            @click="toggleNotifications"
            class="flex mx-4 text-gray-600 focus:outline-none"
        >
            <svg
                class="w-6 h-6"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
            >
                <path
                    d="M15 17H20L18.5951 15.5951C18.2141 15.2141 18 14.6973 18 14.1585V11C18 8.38757 16.3304 6.16509 14 5.34142V5C14 3.89543 13.1046 3 12 3C10.8954 3 10 3.89543 10 5V5.34142C7.66962 6.16509 6 8.38757 6 11V14.1585C6 14.6973 5.78595 15.2141 5.40493 15.5951L4 17H9M15 17V18C15 19.6569 13.6569 21 12 21C10.3431 21 9 19.6569 9 18V17M15 17H9"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                ></path>
            </svg>
        </button>

        <div
            v-if="notificationOpen"
            @click="toggleNotifications"
            class="fixed inset-0 z-10 w-full h-full"
        ></div>

        <div
            v-if="notificationOpen"
            class="absolute right-0 z-10 mt-2 overflow-hidden bg-white rounded-lg shadow-xl w-80"
            style="width: 20rem"
        >
            <router-link
                v-for="notification in notifications"
                :key="notification.id"
                :to="{ name: 'notifications' }"
                class="flex items-center px-4 py-3 -mx-2 text-gray-600 hover:text-white hover:bg-indigo-600"
            >
                <img
                    class="object-cover w-8 h-8 mx-1 rounded-full"
                    :src="DefaultProfile"
                    alt="avatar"
                />
                <p class="mx-2 text-sm">
                    <span class="font-bold text-indigo-400">{{
                        notification.title
                    }}</span
                    ><br />
                    <span class="">View detail</span>
                </p>
            </router-link>
        </div>
    </div>
</template>
