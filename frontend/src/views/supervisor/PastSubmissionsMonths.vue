<script setup>
    import BackButton from "@/components/BackButton.vue";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import { useRoute } from "vue-router";

    const route = useRoute();
    const months = [
        { id: 1, desc: "First Month" },
        { id: 2, desc: "Second Month" },
        { id: 3, desc: "Third Month" },
        { id: 4, desc: "Fourth Month" },
    ];
</script>

<template>
    <DashboardLayout :title="'Past Submissions'">
        <template #content>
            <div class="p-6 bg-gray-50 min-h-screen">
                <div class="mb-6">
                    <BackButton />
                </div>
                
                <div class="mb-8">
                    <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ route.params.year }} Cohort</h2>
                    <p class="text-gray-600">Select a month to view submissions from this cohort</p>
                </div>

                <div class="bg-white shadow-xl rounded-xl border border-gray-200 overflow-hidden">
                    <div class="bg-maroon px-6 py-4">
                        <h3 class="text-lg font-semibold text-white">
                            Internship Months
                        </h3>
                        <p class="text-white text-opacity-80 text-sm mt-1">Browse submissions by month</p>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        Month Period
                                    </th>
                                    <th class="px-6 py-4 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                <tr
                                    v-for="month in months"
                                    :key="month.id"
                                    class="hover:bg-gray-50 transition-colors duration-150"
                                >
                                    <td class="px-6 py-4">
                                        <div class="flex items-center">
                                            
                                            <div>
                                                <div class="text-sm font-semibold text-gray-900">
                                                    {{ month.desc }}
                                                </div>
                                                <div class="text-sm text-gray-500">
                                                    Internship period {{ month.id }} of 4
                                                </div>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 text-right">
                                        <router-link
                                            :to="{
                                                name: 'past-submissions-interns',
                                                params: {
                                                    month: month.id,
                                                    year: route.params.year,
                                                },
                                            }"
                                            class="inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg text-white bg-green hover:bg-green hover:opacity-90 transition-all duration-150 shadow-sm hover:shadow-md"
                                        >
                                            View Submissions
                                        </router-link>
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
