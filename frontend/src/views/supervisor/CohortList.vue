<script setup>
    import { ref, onMounted } from "vue";
    import apiClient from "@/services/api";
    import Loader from "@/components/loader.vue";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";

    const cohorts = ref([]);
    const loading = ref(false);

    onMounted(async () => {
        loading.value = true;
        try {
            const response = await apiClient.get("internships/cohorts/");
            cohorts.value = response.data;
        } catch (error) {
            console.error("Error fetching cohorts:", error);
        } finally {
            loading.value = false;
        }
    });
</script>

<template>
    <DashboardLayout :title="'Cohorts'">
        <template #content>
            <div class="p-6 bg-gray-50 min-h-screen">
                <div class="mb-8">
                    <h2 class="text-2xl font-bold text-gray-900 mb-2">Internship Cohorts</h2>
                    <p class="text-gray-600">Manage and view details of all internship cohorts</p>
                </div>

                <div v-if="loading" class="flex justify-center items-center py-12">
                    <Loader />
                </div>
                
                <div v-else class="bg-white shadow-xl rounded-xl border border-gray-200 overflow-hidden">
                    <div class="bg-maroon px-6 py-4">
                        <h3 class="text-lg font-semibold text-white">
                            Active Cohorts
                        </h3>
                        <p class="text-white text-opacity-80 text-sm mt-1">View intern details by cohort year</p>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        Cohort Information
                                    </th>
                                    <th class="px-6 py-4 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                <tr
                                    v-for="cohort in cohorts"
                                    :key="cohort.id"
                                    class="hover:bg-gray-50 transition-colors duration-150"
                                >
                                    <td class="px-6 py-4">
                                        <div class="flex items-center">
                                            
                                            <div>
                                                <div class="text-lg font-semibold text-gray-900">
                                                    {{ cohort.year }} Internship Cohort
                                                </div>
                                                <div class="text-sm text-gray-500 mt-1">
                                                    Academic Year {{ cohort.year }}
                                                </div>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 text-right">
                                        <router-link
                                            :to="{
                                                name: 'cohort-detail',
                                                params: { year: cohort.year },
                                            }"
                                            class="inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg text-white bg-green hover:bg-green hover:opacity-90 transition-all duration-150 shadow-sm hover:shadow-md"
                                        >
                                            View Interns
                                        </router-link>
                                    </td>
                                </tr>
                                
                                <tr v-if="!cohorts.length">
                                    <td colspan="2" class="px-6 py-12 text-center">
                                        <div class="flex flex-col items-center">
                                            <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                                                <span class="text-2xl text-gray-400">🎓</span>
                                            </div>
                                            <h3 class="text-lg font-medium text-gray-900 mb-1">No cohorts available</h3>
                                            <p class="text-gray-500">There are no cohorts to display at this time.</p>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </template>
    </DashboardLayout>
</template>
