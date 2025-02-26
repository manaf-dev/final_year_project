<script setup>
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import { computed, ref } from "vue";
    import apiClient from "@/services/api";
    import Loader from "@/components/loader.vue";

    const notificationOpen = ref(false);
    const notifications = ref([]);
    const loading = ref(false);
    const marking = ref(false);
    const deleting = ref(false);

    const isAllRead = computed(() => {
        if (!notifications.value.length) {
            return false;
        } else {
            return notifications.value.every(
                (notification) => notification.read
            );
        }
    });

    const get_notifications = async () => {
        loading.value = true;
        try {
            const response = await apiClient.get("notifications/");
            notifications.value = response.data;
        } catch (error) {
            console.log("Error loading notifications", error);
        } finally {
            loading.value = false;
        }
    };

    get_notifications();

    const markAsRead = async (notification_id) => {
        marking.value = true;
        try {
            const response = await apiClient.put(
                `notification/mark-as-read/${notification_id}/`
            );
            get_notifications();
        } catch (error) {
            console.log("Error marking as read", error);
        } finally {
            marking.value = false;
        }
    };

    const deleteNotification = async (notification_id) => {
        deleting.value = true;
        try {
            const response = await apiClient.delete(
                `notification/delete/${notification_id}/`
            );
            get_notifications();
        } catch (error) {
            console.log("Error deleting", error);
        } finally {
            deleting.value = false;
        }
    };

    const markAllAsRead = async () => {
        marking.value = true;
        try {
            const response = await apiClient.put(
                `notification/mark-all-as-read/`
            );
            get_notifications();
        } catch (error) {
            console.log("Error marking as read", error);
        } finally {
            marking.value = false;
        }
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
            <div class="bg-gray-100 min-h-screen p-8">
                <!-- Header -->
                <div
                    class="bg-maroon text-white rounded-lg shadow-lg px-6 py-4 flex justify-between items-center"
                >
                    <h1 class="text-2xl font-bold">Notifications</h1>
                    <button
                        v-if="!isAllRead"
                        @click="markAllAsRead"
                        class="bg-yellow text-black px-4 py-2 rounded-lg shadow hover:bg-[#ffd83e] flex items-center"
                    >
                        <i class="pi pi-check mr-2"></i> Mark All as Read
                    </button>
                </div>

                <!-- Notifications List -->
                <div v-if="!loading" class="mt-8 space-y-4">
                    <div
                        v-for="(notification, index) in notifications"
                        :key="index"
                        :class="[
                            'bg-white rounded-lg shadow p-4 flex items-start justify-between',
                            notification.read ? 'opacity-70' : 'opacity-100',
                        ]"
                    >
                        <!-- Notification Content -->
                        <div class="flex items-start space-x-4">
                            <i
                                class="pi pi-bell text-2xl"
                                :class="
                                    notification.read
                                        ? 'text-gray-400'
                                        : 'text-maroon'
                                "
                            ></i>
                            <div>
                                <p class="font-medium text-lg text-maroon">
                                    {{ notification.title }}
                                </p>
                                <p class="text-gray-600 text-sm mt-1">
                                    {{ notification.content }}
                                </p>
                                <span class="text-xs text-gray-400 capitalize">
                                    {{ formatDate(notification.timestamp) }}
                                </span>
                            </div>
                        </div>

                        <!-- Actions -->
                        <div class="flex items-center space-x-2">
                            <button
                                v-if="!notification.read"
                                @click="markAsRead(notification.id)"
                                class="text-green bg-[#e8f5e9] px-3 py-1 rounded-md hover:bg-[#d0f0db] font-medium"
                            >
                                <i class="pi pi-check mr-1"></i> Mark as Read
                            </button>
                            <button
                                @click="deleteNotification(notification.id)"
                                class="text-red-500 bg-red-100 px-3 py-1 rounded-md hover:bg-red-200 font-medium"
                            >
                                <i class="pi pi-trash mr-1"></i> Delete
                            </button>
                        </div>
                    </div>

                    <!-- No Notifications -->
                    <div
                        v-if="notifications.length === 0"
                        class="text-center text-gray-500"
                    >
                        <i class="pi pi-info-circle text-4xl"></i>
                        <p class="mt-2">No notifications at the moment.</p>
                    </div>
                </div>

                <Loader v-else />
            </div>
            <div
                v-if="marking || deleting"
                class="absolute inset-0 bg-black opacity-50 flex items-center justify-center rounded-lg z-20"
            >
                <Loader />
            </div>
        </template>
    </DashboardLayout>
</template>
