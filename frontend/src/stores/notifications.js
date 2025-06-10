import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '@/services/api'

export const useNotificationStore = defineStore('notifications', {
    state: () => ({
        notifications: [],
        unreadCount: 0,
        loading: false,
        refreshInterval: null
    }),
    getters: {
        hasUnreadNotifications: (state) => state.unreadCount > 0,
        displayUnreadCount: (state) => state.unreadCount > 99 ? '99+' : state.unreadCount.toString()
    },
    actions: {
        async fetchNotifications() {
            this.loading = true
            try {
                const response = await apiClient.get('submissions/notifications/')
                this.notifications = response.data
                this.unreadCount = this.notifications.filter(notification => !notification.read).length
            } catch (error) {
                console.error('Error fetching notifications:', error)
            } finally {
                this.loading = false
            }
        },
        async fetchUnreadCount() {
            try {
                const response = await apiClient.get('submissions/notifications/unread-count/')
                this.unreadCount = response.data.unread_count
            } catch (error) {
                console.error('Error fetching unread count:', error)
            }
        },
        async markAsRead(notificationId) {
            try {
                await apiClient.put(`submissions/notification/mark-as-read/${notificationId}/`)
                const notification = this.notifications.find(n => n.id === notificationId)
                if (notification && !notification.read) {
                    notification.read = true
                    this.unreadCount = Math.max(0, this.unreadCount - 1)
                }
            } catch (error) {
                console.error('Error marking notification as read:', error)
            }
        },
        async markAllAsRead() {
            try {
                await apiClient.put('submissions/notification/mark-all-as-read/')
                this.notifications.forEach(notification => {
                    notification.read = true
                })
                this.unreadCount = 0
            } catch (error) {
                console.error('Error marking all notifications as read:', error)
            }
        },
        async deleteNotification(notificationId) {
            try {
                await apiClient.delete(`submissions/notification/delete/${notificationId}/`)
                const index = this.notifications.findIndex(n => n.id === notificationId)
                if (index !== -1) {
                    const notification = this.notifications[index]
                    if (!notification.read) {
                        this.unreadCount = Math.max(0, this.unreadCount - 1)
                    }
                    this.notifications.splice(index, 1)
                }
            } catch (error) {
                console.error('Error deleting notification:', error)
            }
        },
        startAutoRefresh() {
            if (this.refreshInterval) return
            this.refreshInterval = setInterval(() => {
                this.fetchUnreadCount()
            }, 30000)
        },
        stopAutoRefresh() {
            if (this.refreshInterval) {
                clearInterval(this.refreshInterval)
                this.refreshInterval = null
            }
        }
    }
})
