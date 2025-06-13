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
        
        // Close on escape key
        document.addEventListener('keydown', handleEscape);
    });

    onUnmounted(() => {
        notificationStore.stopAutoRefresh();
        document.removeEventListener('keydown', handleEscape);
    });

    const toggleNotifications = () => {
        notificationOpen.value = !notificationOpen.value;
        // Refresh notifications when opening the menu
        if (notificationOpen.value) {
            notificationStore.fetchNotifications();
        }
    };

    const closeNotifications = () => {
        notificationOpen.value = false;
    };

    const handleEscape = (e) => {
        if (e.key === 'Escape' && notificationOpen.value) {
            closeNotifications();
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
        <!-- Notification Button -->
        <button
            @click="toggleNotifications"
            class="relative p-2 text-gray-600 hover:text-[#8c003b] focus:outline-none focus:ring-2 focus:ring-[#8c003b] focus:ring-offset-2 rounded-lg transition-all duration-200 hover:bg-gray-50"
            :class="{ 'text-[#8c003b]': notificationOpen }"
            aria-label="Open notifications"
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
                />
            </svg>
            
            <!-- Simple notification badge -->
            <span 
                v-if="notificationStore.hasUnreadNotifications"
                class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center shadow-lg"
            >
                {{ notificationStore.displayUnreadCount }}
            </span>
        </button>

        <!-- Mobile overlay -->
        <div
            v-if="notificationOpen"
            @click="closeNotifications"
            class="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 md:hidden"
        ></div>

        <!-- Desktop overlay -->
        <div
            v-if="notificationOpen"
            @click="closeNotifications"
            class="fixed inset-0 z-10 hidden md:block"
        ></div>

        <!-- Notification Panel -->
        <div
            v-if="notificationOpen"
            class="fixed inset-x-4 top-16 z-50 bg-white rounded-lg shadow-xl border border-gray-200
                   md:absolute md:right-0 md:top-auto md:mt-2 md:inset-x-auto md:w-80"
        >
            <!-- Header -->
            <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100 bg-gray-50 rounded-t-lg">
                <h3 class="text-lg font-semibold text-gray-900">Notifications</h3>
                <div class="flex items-center space-x-2">
                    <span 
                        v-if="notificationStore.hasUnreadNotifications" 
                        class="px-2 py-1 text-xs font-medium text-[#8c003b] bg-red-50 rounded-full border border-red-200"
                    >
                        {{ notificationStore.unreadCount }} new
                    </span>
                    <button
                        @click="closeNotifications"
                        class="p-1 hover:bg-gray-200 rounded-full transition-colors"
                        aria-label="Close notifications"
                    >
                        <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
            </div>
            
            <!-- Notifications List -->
            <div class="max-h-96 overflow-y-auto">
                <!-- Empty state -->
                <div v-if="notificationStore.notifications.length === 0" class="px-6 py-12 text-center">
                    <div class="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                        <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
                        </svg>
                    </div>
                    <p class="text-gray-500 font-medium mb-1">No notifications</p>
                    <p class="text-sm text-gray-400">You're all caught up!</p>
                </div>
                
                <!-- Notification items -->
                <router-link
                    v-for="notification in notificationStore.notifications"
                    :key="notification.id"
                    :to="{ name: 'notifications' }"
                    @click="closeNotifications"
                    class="flex items-start p-4 hover:bg-gray-50 border-b border-gray-100 last:border-b-0 transition-colors"
                    :class="{ 'bg-blue-50 border-l-4 border-l-blue-500': !notification.read }"
                >
                    <!-- Avatar -->
                    <div class="flex-shrink-0 mr-3">
                        <img
                            class="w-10 h-10 rounded-full object-cover"
                            :src="DefaultProfile"
                            alt="avatar"
                        />
                        <div v-if="!notification.read" class="w-3 h-3 bg-blue-500 rounded-full -mt-2 ml-7 border-2 border-white"></div>
                    </div>
                    
                    <!-- Content -->
                    <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900 mb-1">
                            {{ notification.title }}
                        </p>
                        <p class="text-sm text-gray-600 mb-2 line-clamp-2">
                            {{ notification.content }}
                        </p>
                        <p class="text-xs text-gray-500">
                            {{ formatDate(notification.timestamp) }}
                        </p>
                    </div>

                    <!-- Arrow -->
                    <div class="flex-shrink-0 ml-2 self-center">
                        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                        </svg>
                    </div>
                </router-link>
            </div>
            
            <!-- Footer -->
            <div v-if="notificationStore.notifications.length > 0" class="p-4 border-t border-gray-100 bg-gray-50 rounded-b-lg">
                <router-link 
                    :to="{ name: 'notifications' }" 
                    @click="closeNotifications"
                    class="block w-full text-center py-2 px-4 text-sm font-medium text-[#8c003b] hover:text-white hover:bg-[#8c003b] border border-[#8c003b] rounded-lg transition-all duration-200"
                >
                    View all notifications
                </router-link>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Line clamp utility for notification content */
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* Smooth backdrop blur */
@supports (backdrop-filter: blur(0)) {
    .backdrop-blur-sm {
        backdrop-filter: blur(4px);
    }
}

/* Enhanced scrollbar for notification list */
.overflow-y-auto::-webkit-scrollbar {
    width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

/* Focus states for accessibility */
button:focus-visible {
    outline: 2px solid #8c003b;
    outline-offset: 2px;
}

/* Mobile-specific adjustments */
@media (max-width: 768px) {
    /* Ensure proper spacing on mobile to prevent cutoff */
    .fixed.inset-x-4 {
        left: 1rem;
        right: 1rem;
        margin-left: 0;
        margin-right: 0;
    }
    
    /* Larger touch targets */
    button {
        min-height: 44px;
        min-width: 44px;
    }
    
    /* Better spacing on mobile */
    .notification-item {
        padding: 1rem;
    }
}

/* Smooth animations */
.transition-all {
    transition-property: all;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 200ms;
}
</style>
