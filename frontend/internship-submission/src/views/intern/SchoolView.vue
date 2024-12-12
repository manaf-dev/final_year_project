<script setup>
    import apiClient from "@/services/api";
    import { useAuthStore } from "@/stores/auth";
    import { onMounted, ref, watch } from "vue";
    import { useToast } from "vue-toastification";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";

    const authStore = useAuthStore();
    const toast = useToast();
    const activeTab = ref("school");

    const mentor = authStore.user.mentor;
    const school = authStore.user.intern_school;
</script>

<template>
    <DashboardLayout>
        <template #title> Your Supervisor </template>
        <template #content>
            <div class="container mx-auto p-4 max-w-4xl">
                <!-- Tabs -->
                <div class="border-b border-gray-200">
                    <nav class="flex -mb-px">
                        <button
                            @click="activeTab = 'school'"
                            :class="[
                                'py-4 px-6 font-medium text-sm',
                                activeTab === 'school'
                                    ? 'border-b-2 border-blue-500 text-blue-600'
                                    : 'text-gray-500 hover:text-gray-700 hover:border-gray-300',
                            ]"
                        >
                            School Details
                        </button>

                        <button
                            @click="activeTab = 'mentor'"
                            :class="[
                                'py-4 px-6 font-medium text-sm',
                                activeTab === 'mentor'
                                    ? 'border-b-2 border-blue-500 text-blue-600'
                                    : 'text-gray-500 hover:text-gray-700 hover:border-gray-300',
                            ]"
                        >
                            Mentor Details
                        </button>
                    </nav>
                </div>

                <div v-if="activeTab === 'school'" class="mt-6">
                    <div class="bg-white rounded-lg shadow">
                        <div
                            class="flex items-center justify-between px-6 py-4 border-b border-gray-200"
                        >
                            <h3 class="text-lg font-medium">
                                Internship School Details
                            </h3>
                            <span>Edit</span>
                        </div>
                        <div class="p-6 space-y-4">
                            <div class="grid gap-4">
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
                                        >Name</label
                                    >
                                    <p class="mt-1 text-gray-900">
                                        {{ school.name }}
                                    </p>
                                </div>
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
                                        >Location</label
                                    >
                                    <p class="mt-1 text-gray-900">
                                        {{ school.location }}
                                    </p>
                                </div>
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
                                        >District</label
                                    >
                                    <p class="mt-1 text-gray-900">
                                        {{ school.district }}
                                    </p>
                                </div>
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
                                        >Region</label
                                    >
                                    <p class="mt-1 text-gray-900">
                                        {{ school.region }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="activeTab === 'mentor'" class="mt-6 space-y-4">
                    <div class="bg-white rounded-lg shadow">
                        <div
                            class="flex items-center justify-between px-6 py-4 border-b border-gray-200"
                        >
                            <h3 class="text-lg font-medium">Mentor Details</h3>
                            <span>Edit</span>
                        </div>

                        <div class="p-6 space-y-4">
                            <div class="grid gap-4">
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
                                        >Name</label
                                    >
                                    <p class="mt-1 text-gray-900">
                                        {{ mentor.name }}
                                    </p>
                                </div>

                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
                                        >Email</label
                                    >
                                    <p class="mt-1 text-gray-900">
                                        {{ mentor.email }}
                                    </p>
                                </div>
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
                                        >Phone</label
                                    >
                                    <p class="mt-1 text-gray-900">
                                        {{ mentor.phone }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </DashboardLayout>
</template>
