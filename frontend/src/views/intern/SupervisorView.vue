<script setup>
    import { useAuthStore } from "@/stores/auth";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import { ref, computed } from "vue";

    const authStore = useAuthStore();
    const supervisor = authStore.user.supervisor;

    // Compute initials for avatar
    const supervisorInitials = computed(() => {
        if (!supervisor) return 'S';
        const firstName = supervisor.first_name?.charAt(0) || '';
        const lastName = supervisor.last_name?.charAt(0) || '';
        return (firstName + lastName).toUpperCase() || 'S';
    });

    // Quick actions
    const sendEmail = () => {
        if (supervisor?.email) {
            window.location.href = `mailto:${supervisor.email}`;
        }
    };

    const callPhone = () => {
        if (supervisor?.phone) {
            window.location.href = `tel:${supervisor.phone}`;
        }
    };
</script>

<template>
    <DashboardLayout :title="'Your Supervisor'">
        <template #content>
            <div class="container mx-auto px-4 py-8 max-w-6xl">
                <!-- Header Section -->
                <div class="mb-8">
                    <div class="bg-gradient-to-r from-maroon via-green to-green rounded-2xl p-8 text-white relative overflow-hidden">
                        <div class="absolute inset-0 bg-black/10"></div>
                        <div class="relative z-10">
                            <div class="flex items-center space-x-6">
                                
                                <!-- Info -->
                                <div class="flex-1">
                                    <h1 class="text-3xl font-bold mb-2 capitalize">
                                        {{ supervisor?.title }}. {{ supervisor?.last_name }} {{ supervisor?.first_name }} {{ supervisor.other_names }}
                                    </h1>
                                    <p class="text-gray-100 text-lg">
                                        {{ supervisor?.department?.name }}
                                    </p>
                                    <div class="mt-4 flex flex-wrap gap-2">
                                        <span class="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-sm border border-white/30">
                                            Academic Supervisor
                                        </span>
                                        <span class="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-sm border border-white/30">
                                            Active
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Decorative elements -->
                        <div class="absolute -top-8 -right-8 w-32 h-32 rounded-full bg-white/10"></div>
                        <div class="absolute -bottom-4 -left-4 w-24 h-24 rounded-full bg-white/5"></div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <!-- Contact Information Card -->
                    <div class="lg:col-span-2">
                        <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
                            <div class="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b">
                                <h2 class="text-xl font-semibold text-gray-800 flex items-center">
                                    <svg class="w-5 h-5 mr-2 text-maroon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                                    </svg>
                                    Contact Information
                                </h2>
                            </div>
                            
                            <div class="p-6 space-y-6">
                                <!-- Full Name -->
                                <div class="flex items-start space-x-4">
                                    <div class="flex-shrink-0 w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                                        <svg class="w-5 h-5 text-maroon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                                        </svg>
                                    </div>
                                    <div class="flex-1">
                                        <label class="block text-sm font-medium text-gray-600 mb-1">Full Name</label>
                                        <p class="text-lg font-semibold text-gray-900 capitalize">
                                            {{ supervisor?.title }}. {{ supervisor?.last_name }} {{ supervisor?.first_name }} {{ supervisor.other_names }}
                                        </p>
                                    </div>
                                </div>

                                <!-- Department -->
                                <div class="flex items-start space-x-4">
                                    <div class="flex-shrink-0 w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                                        <svg class="w-5 h-5 text-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                                        </svg>
                                    </div>
                                    <div class="flex-1">
                                        <label class="block text-sm font-medium text-gray-600 mb-1">Department</label>
                                        <p class="text-lg font-semibold text-gray-900">
                                            {{ supervisor?.department?.name }}
                                        </p>
                                    </div>
                                </div>

                                <!-- Email -->
                                <div class="flex items-start space-x-4">
                                    <div class="flex-shrink-0 w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
                                        <svg class="w-5 h-5 text-yellow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                                        </svg>
                                    </div>
                                    <div class="flex-1">
                                        <label class="block text-sm font-medium text-gray-600 mb-1">Email Address</label>
                                        <p class="text-lg font-semibold text-gray-900 break-all">
                                            {{ supervisor?.email }}
                                        </p>
                                    </div>
                                </div>

                                <!-- Phone -->
                                <div class="flex items-start space-x-4">
                                    <div class="flex-shrink-0 w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                                        <svg class="w-5 h-5 text-maroon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                                        </svg>
                                    </div>
                                    <div class="flex-1">
                                        <label class="block text-sm font-medium text-gray-600 mb-1">Phone Number</label>
                                        <p class="text-lg font-semibold text-gray-900">
                                            {{ supervisor?.phone || 'Not provided' }}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Quick Actions Card -->
                    <div class="space-y-6">
                        <!-- Contact Actions -->
                        <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
                            <div class="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b">
                                <h3 class="text-lg font-semibold text-gray-800 flex items-center">
                                    <svg class="w-5 h-5 mr-2 text-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                                    </svg>
                                    Quick Actions
                                </h3>
                            </div>
                            
                            <div class="p-6 space-y-3">
                                <!-- Send Email Button -->
                                <button 
                                    @click="sendEmail"
                                    class="w-full flex items-center justify-center px-4 py-3 bg-gradient-to-r from-maroon to-red-600 text-white rounded-xl font-medium hover:from-red-600 hover:to-red-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                                >
                                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                                    </svg>
                                    Send Email
                                </button>

                            </div>
                        </div>

                        <!-- Tips Card -->
                        <div class="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-2xl border border-yellow-200 overflow-hidden">
                            <div class="p-6">
                                <div class="flex items-start space-x-3">
                                    <div class="flex-shrink-0">
                                        <svg class="w-6 h-6 text-yellow-600 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                                        </svg>
                                    </div>
                                    <div>
                                        <h4 class="font-semibold text-yellow-800 mb-2">Communication Tips</h4>
                                        <ul class="text-sm text-yellow-700 space-y-1">
                                            <li>• Schedule meetings in advance</li>
                                            <li>• Be clear about your questions</li>
                                            <li>• Prepare agenda before meetings</li>
                                            <li>• Follow up with summaries</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </DashboardLayout>
</template>
