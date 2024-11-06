<script setup>
    import { useAuthStore } from "@/stores/auth";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import { ref } from "vue";

    const authStore = useAuthStore();

    const school = ref({
        name: "Kadjeb-Asato Senior High School",
        location: "Kadjebi",
        district: "Kadjebi-Akan",
        region: "Oti",
    });
</script>

<template>
    <DashboardLayout>
        <template #title> Internship School </template>
        <template #content>
            <div class="container mx-auto px-4 py-8 max-w-5xl">
                <div
                    class="bg-white w-2/3 shadow-lg rounded-lg overflow-hidden"
                >
                    <div class="border-b border-gray-200">
                        <div class="-mb-px flex">
                            <span
                                class="w-1/3 py-4 pl-4 font-medium text-sm border-b-2 transition-all duration-300 border-blue-500 border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300,"
                            >
                                School Details
                            </span>
                        </div>
                    </div>

                    <!-- Tab Content -->
                    <div class="p-6">
                        <!-- Personal Details Tab -->
                        <div class="space-y-4">
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
            </div>
        </template>
    </DashboardLayout>
</template>
