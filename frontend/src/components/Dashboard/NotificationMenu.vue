<script setup>
    import { onMounted, ref, onUnmounted } from "vue";
    import DefaultProfile from "@/assets/imgs/defaultProfile.png";
    import { useNotificationStore } from "@/stores/notifications";

    const notificationOpen = ref(false);
    const notificationStore = useNotificationStore();

    onMounted(() => {
        notificationStore.fetchNotifications();
        notificationStore.fetchUnreadCount();
        notificationStore.startAutoRefresh();
    });

    onUnmounted(() => {
        notificationStore.stopAutoRefresh();
    });

    const toggleNotifications = () => {
        notificationOpen.value = !notificationOpen.value;
        // Refresh notifications when opening the menu
        if (notificationOpen.value) {
            notificationStore.fetchNotifications();
        }
    };

    // Format date for display
    const formatDate = (dateStr) => {
        const date = new Date(dateStr);
        const now = new Date();
        const diffInMinutes = Math.floor((now - date) / (1000 * 60));
        
        if (diffInMinutes < 1) {
            return 'Just now';
        } else if (diffInMinutes < 60) {
            return `${diffInMinutes}m ago`;
        } else if (diffInMinutes < 1440) {
            return `${Math.floor(diffInMinutes / 60)}h ago`;
        } else {
            return date.toLocaleDateString("en-GB", {
                day: "numeric",
                month: "short",
                year: date.getFullYear() !== now.getFullYear() ? "numeric" : undefined,
            });
        }
    };

</script>

<template>
    <div class="relative">
        <button
            @click="toggleNotifications"
            class="flex mx-4 text-gray-600 focus:outline-none relative transition-colors duration-200 hover:text-[#8c003b]"
            :class="{ 'animate-pulse': notificationStore.hasUnreadNotifications }"
        >
            <svg
                class="w-6 h-6 transition-transform duration-200"
                :class="{ 'scale-110': notificationStore.hasUnreadNotifications }"
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
            
            <!-- Notification Badge -->
            <span 
                v-if="notificationStore.hasUnreadNotifications"
                class="absolute -top-2 -right-2 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full min-w-[20px] h-5 notification-badge"
            >
                {{ notificationStore.displayUnreadCount }}
            </span>
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
            <!-- Notification Header -->
            <div class="px-4 py-3 bg-gradient-to-r from-[#8c003b] to-[#a00048] text-white">
                <div class="flex items-center justify-between">
                    <h3 class="text-sm font-semibold">Notifications</h3>
                    <span v-if="notificationStore.hasUnreadNotifications" class="text-xs bg-white/20 px-2 py-1 rounded-full">
                        {{ notificationStore.unreadCount }} new
                    </span>
                </div>
            </div>
            
            <!-- Notifications List -->
            <div class="max-h-80 overflow-y-auto">
                <div v-if="notificationStore.notifications.length === 0" class="px-4 py-6 text-center text-gray-500">
                    <svg class="w-8 h-8 mx-auto mb-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5-5-5h5v-12"></path>
                    </svg>
                    <p class="text-sm">No notifications yet</p>
                </div>
                
                <router-link
                    v-for="notification in notificationStore.notifications"
                    :key="notification.id"
                    :to="{ name: 'notifications' }"
                    class="flex items-start px-4 py-3 text-gray-600 hover:bg-gray-50 border-b border-gray-100 last:border-b-0 transition-colors duration-200"
                    :class="{ 'bg-blue-50 border-l-4 border-l-blue-500': !notification.read }"
                >
                    <img
                        class="object-cover w-8 h-8 mx-1 rounded-full flex-shrink-0"
                        :src="DefaultProfile"
                        alt="avatar"
                    />
                    <div class="ml-2 flex-1 min-w-0">
                        <p class="text-sm">
                            <span class="font-medium" :class="{ 'text-blue-900': !notification.read, 'text-gray-900': notification.read }">
                                {{ notification.title }}
                            </span>
                        </p>
                        <p class="text-xs text-gray-500 mt-1 truncate">
                            {{ notification.content }}
                        </p>
                        <p class="text-xs text-gray-400 mt-1">
                            {{ formatDate(notification.timestamp) }}
                        </p>
                    </div>
                    <div v-if="!notification.read" class="flex-shrink-0 ml-2">
                        <div class="w-2 h-2 bg-blue-600 rounded-full"></div>
                    </div>
                </router-link>
            </div>
            
            <!-- Footer -->
            <div v-if="notificationStore.notifications.length > 0" class="px-4 py-3 bg-gray-50 border-t">
                <router-link 
                    :to="{ name: 'notifications' }" 
                    class="text-sm text-[#8c003b] hover:text-[#a00048] font-medium"
                >
                    View all notifications →
                </router-link>
            </div>
        </div>
    </div>
</template>

<style scoped>
.notification-badge {
    animation: gentle-pulse 2s infinite;
}

@keyframes gentle-pulse {
    0%, 100% {
        transform: translate(50%, -50%) scale(1);
    }
    50% {
        transform: translate(50%, -50%) scale(1.1);
    }
}
</style>
