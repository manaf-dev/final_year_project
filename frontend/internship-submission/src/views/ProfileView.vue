<script setup>
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import { useAuthStore } from "@/stores/auth";

    const authStore = useAuthStore();
    const profile = authStore.user;
</script>

<template>
    <DashboardLayout>
        <template #title>{{ profile.account_type }} Profile</template>
        <template #content>
            <div class="max-w-4xl mx-auto p-6">
                <div class="bg-white shadow-md rounded-lg mt-6 p-6">
                    <h3 class="text-lg font-semibold text-gray-700 mb-4">
                        Profile Details
                    </h3>
                    <form>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label
                                    for="title"
                                    class="block text-sm font-medium text-gray-700"
                                    >Title</label
                                >
                                <input
                                    v-model="profile.title"
                                    type="text"
                                    id="title"
                                    readonly
                                    class="mt-1 block w-full rounded-md border-gray-300 outline-none shadow-sm focus:ring-blue-500 focus:border-blue-500 capitalize"
                                />
                            </div>
                            <div>
                                <label
                                    for="first_name"
                                    class="block text-sm font-medium text-gray-700"
                                    >First Name</label
                                >
                                <input
                                    v-model="profile.first_name"
                                    type="text"
                                    id="first_name"
                                    readonly
                                    class="mt-1 block w-full rounded-md border-gray-300 outline-none shadow-sm focus:ring-blue-500 focus:border-blue-500"
                                />
                            </div>
                            <div>
                                <label
                                    for="last_name"
                                    class="block text-sm font-medium text-gray-700"
                                    >Last Name</label
                                >
                                <input
                                    v-model="profile.last_name"
                                    type="text"
                                    id="last_name"
                                    readonly
                                    class="mt-1 block w-full rounded-md border-gray-300 outline-none shadow-sm focus:ring-blue-500 focus:border-blue-500"
                                />
                            </div>
                            <div>
                                <label
                                    for="username"
                                    class="block text-sm font-medium text-gray-700"
                                    >Index No.</label
                                >
                                <input
                                    v-model="profile.username"
                                    type="text"
                                    id="username"
                                    readonly
                                    class="mt-1 block w-full rounded-md border-gray-300 outline-none shadow-sm focus:ring-blue-500 focus:border-blue-500"
                                />
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </template>
    </DashboardLayout>
</template>
