<script setup>
    import { useAuthStore } from "@/stores/auth";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";

    const authStore = useAuthStore();
    const supervisor = authStore.user.supervisor;
</script>

<template>
    <DashboardLayout>
        <template #title> Dashboard </template>
        <template #content>
            <div class="mt-4">
                <div class="flex flex-wrap -mx-6">
                    <div class="w-full px-6 sm:w-1/2 xl:w-1/3">
                        <div
                            class="flex items-center px-5 py-6 bg-white rounded-md shadow-sm"
                        >
                            <div
                                class="p-3 bg-a-red bg-opacity-75 rounded-full"
                            ></div>
                            <div class="mx-5">
                                <h4
                                    class="text-2xl font-semibold text-gray-700"
                                >
                                    0 of 4
                                </h4>
                                <div class="text-gray-500">
                                    Completed Submissions
                                </div>
                                <div class="mt-6">
                                    <RouterLink
                                        :to="{ name: 'intern-portfolio' }"
                                        class="px-4 py-2 mt-5 bg-a-red text-white"
                                        >Make a Submission</RouterLink
                                    >
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="w-full px-6 mt-6 sm:w-1/2 xl:w-1/3 sm:mt-0">
                        <div
                            class="flex items-center px-5 py-6 bg-white rounded-md shadow-sm"
                        >
                            <div
                                class="p-3 bg-opacity-75 bg-a-green rounded-full"
                            ></div>

                            <div class="mx-5">
                                <h4
                                    class="text-2xl font-semibold text-gray-700"
                                >
                                    30%
                                </h4>
                                <div class="text-gray-500">
                                    Completed Portfolio
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="w-full px-6 mt-6 sm:w-1/2 xl:w-1/3 xl:mt-0">
                        <div
                            class="flex items-center px-5 py-6 bg-white rounded-md shadow-sm"
                        >
                            <div
                                class="p-3 bg-opacity-75 bg-a-yellow rounded-full"
                            ></div>

                            <div class="mx-5">
                                <h4
                                    class="text-2xl font-semibold text-gray-700"
                                >
                                    Supervisor
                                </h4>
                                <div class="text-gray-500 capitalize">
                                    {{ supervisor.title }}.
                                    {{ supervisor.last_name }}
                                    {{ supervisor.first_name }}
                                </div>
                                <div class="text-gray-500">
                                    {{ supervisor.phone }}
                                </div>
                                <div class="text-gray-500">
                                    {{ supervisor.email }}
                                </div>
                                <div class="text-gray-500">
                                    {{ supervisor.department.name }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </DashboardLayout>
</template>

<style>
    .bg-a-red {
        background-color: #8c003b;
    }
    .bg-a-green {
        background-color: #006938;
    }
    .bg-a-yellow {
        background-color: #ffc712;
    }
</style>
