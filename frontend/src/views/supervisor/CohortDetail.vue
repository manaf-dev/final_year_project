<script setup>
    import { ref, onMounted } from "vue";
    import { useRoute } from "vue-router";
    import apiClient from "@/services/api";
    import Loader from "@/components/loader.vue";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import BackButton from "@/components/BackButton.vue";

    const route = useRoute();
    const interns = ref([]);
    const loading = ref(false);

    onMounted(async () => {
        loading.value = true;
        try {
            const response = await apiClient.get(
                `accounts/cohort/${route.params.year}/interns/`
            );
            interns.value = response.data;
        } catch (error) {
            console.error("Error fetching cohort details:", error);
        } finally {
            loading.value = false;
        }
    });
</script>

<template>
    <DashboardLayout :title="route.params.year + ' Cohort'">
        <template #content>
            <div class="p-6 bg-gray-50 min-h-screen">
                <div class="mb-6">
                    <BackButton />
                </div>
                
                <div class="mb-8">
                    <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ route.params.year }} Cohort Details</h2>
                    <div class="flex items-center text-gray-600">
                        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                        </svg>
                        <span>Total Interns: <span class="font-semibold text-gray-900">{{ interns.interns_count || 0 }}</span></span>
                    </div>
                </div>

                <div v-if="loading" class="flex justify-center items-center py-12">
                    <Loader />
                </div>
                
                <div v-else class="bg-white shadow-xl rounded-xl border border-gray-200 overflow-hidden">
                    <div class="bg-maroon px-6 py-4">
                        <h3 class="text-lg font-semibold text-white">
                            Intern Directory
                        </h3>
                        <p class="text-white text-opacity-80 text-sm mt-1">Complete list of registered interns</p>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        Student ID
                                    </th>
                                    <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        Full Name
                                    </th>
                                    <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        Contact
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                <tr
                                    v-for="intern in interns.interns"
                                    :key="intern.id"
                                    class="hover:bg-gray-50 transition-colors duration-150"
                                >
                                    <td class="px-6 py-4">
                                        <div class="flex items-center">
                                            
                                            <div>
                                                <div class="text-sm font-semibold text-gray-900">
                                                    {{ intern.username }}
                                                </div>
                                                <div class="text-xs text-gray-500">
                                                    Student ID
                                                </div>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4">
                                        <div class="text-sm font-medium text-gray-900">
                                            {{ intern.last_name }} {{ intern.first_name }}
                                            <span v-if="intern.other_names" class="text-gray-600">{{ intern.other_names }}</span>
                                        </div>
                                        <div class="text-sm text-gray-500">
                                            {{ route.params.year }} Cohort Intern
                                        </div>
                                    </td>
                                    <td class="px-6 py-4">
                                        <div class="text-sm text-gray-900">
                                            {{ intern.phone || 'N/A' }}
                                        </div>
                                    </td>
                                </tr>
                                
                                <tr v-if="!interns.interns || !interns.interns.length">
                                    <td colspan="3" class="px-6 py-12 text-center">
                                        <div class="flex flex-col items-center">
                                            <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                                                <span class="text-2xl text-gray-400">👥</span>
                                            </div>
                                            <h3 class="text-lg font-medium text-gray-900 mb-1">No interns registered</h3>
                                            <p class="text-gray-500">This cohort doesn't have any registered interns yet.</p>
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
