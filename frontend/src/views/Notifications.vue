<script setup>
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import { computed, onMounted } from "vue";
    import { useNotificationStore } from "@/stores/notifications";
    import Loader from "@/components/loader.vue";

    const notificationStore = useNotificationStore();

    const isAllRead = computed(() => {
        if (!notificationStore.notifications.length) {
            return false;
        } else {
            return notificationStore.notifications.every(
                (notification) => notification.read
            );
        }
    });

    onMounted(() => {
        notificationStore.fetchNotifications();
    });

    const markAsRead = async (notification_id) => {
        await notificationStore.markAsRead(notification_id);
    };

    const deleteNotification = async (notification_id) => {
        await notificationStore.deleteNotification(notification_id);
    };

    const markAllAsRead = async () => {
        await notificationStore.markAllAsRead();
    };

    const formatDate = (dateStr) => {
        const date = new Date(dateStr);
        return date.toLocaleDateString("en-GB", {
            year: "numeric",
            month: "numeric",
            day: "numeric",
            hour: "numeric",
            minute: "numeric",
            hour12: true,
        });
    };
</script>

<template>
    <DashboardLayout :title="'Notifications'">
        <template #content>
            <div class="bg-gray-100 min-h-screen p-4 sm:p-8">
                <!-- Header -->
                <div
                    class="bg-maroon text-white rounded-lg shadow-lg px-4 py-3 sm:px-6 sm:py-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3"
                >
                    <h1 class="text-xl sm:text-2xl font-bold">Notifications</h1>
                    <button
                        v-if="!isAllRead"
                        @click="markAllAsRead"
                        class="bg-yellow text-black px-3 py-2 rounded-lg shadow hover:bg-[#ffd83e] flex items-center text-sm sm:text-base"
                    >
                        <i class="pi pi-check mr-2"></i> Mark All as Read
                    </button>
                </div>

                <!-- Notifications List -->
                <div v-if="!notificationStore.loading" class="mt-6 sm:mt-8 space-y-4">
                    <div
                        v-for="(notification, index) in notificationStore.notifications"
                        :key="index"
                        :class="[
                            'bg-white rounded-lg shadow p-3 sm:p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3',
                            notification.read ? 'opacity-70' : 'opacity-100',
                        ]"
                    >
                        <!-- Notification Content -->
                        <div class="flex items-start space-x-3 sm:space-x-4 w-full">
                            <i
                                class="pi pi-bell text-xl sm:text-2xl"
                                :class="
                                    notification.read
                                        ? 'text-gray-400'
                                        : 'text-maroon'
                                "
                            ></i>
                            <div class="flex-1">
                                <p class="font-medium text-base sm:text-lg text-maroon break-words">
                                    {{ notification.title }}
                                </p>
                                <p class="text-gray-600 text-sm mt-1 break-words">
                                    {{ notification.content }}
                                </p>
                                <span class="text-xs text-gray-400 capitalize block mt-1">
                                    {{ formatDate(notification.timestamp) }}
                                </span>
                            </div>
                        </div>

                        <!-- Actions -->
                        <div class="flex items-center space-x-2 self-end sm:self-auto">
                            <button
                                v-if="!notification.read"
                                @click="markAsRead(notification.id)"
                                class="text-green bg-[#e8f5e9] px-2 py-1 rounded-md hover:bg-[#d0f0db] font-medium text-xs sm:text-sm"
                            >
                                <i class="pi pi-check mr-1"></i> Mark as Read
                            </button>
                            <button
                                @click="deleteNotification(notification.id)"
                                class="text-red-500 bg-red-100 px-2 py-1 rounded-md hover:bg-red-200 font-medium text-xs sm:text-sm"
                            >
                                <i class="pi pi-trash mr-1"></i> Delete
                            </button>
                        </div>
                    </div>

                    <!-- No Notifications -->
                    <div
                        v-if="notificationStore.notifications.length === 0"
                        class="text-center text-gray-500"
                    >
                        <i class="pi pi-info-circle text-3xl sm:text-4xl"></i>
                        <p class="mt-2 text-sm sm:text-base">No notifications at the moment.</p>
                    </div>
                </div>

                <Loader v-else />
            </div>
            <div
                v-if="notificationStore.loading"
                class="fixed inset-0 bg-black opacity-50 flex items-center justify-center rounded-lg z-20"
            >
                <Loader />
            </div>
        </template>
    </DashboardLayout>
</template>
