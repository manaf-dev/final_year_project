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
    <DashboardLayout>
        <template #title>Cohorts</template>
        <template #content>
            <div class="p-6 bg-gray-50 min-h-screen">
                <div v-if="loading" class="flex justify-center items-center">
                    <Loader />
                </div>
                <div v-else>
                    <table
                        class="table-auto w-full border-collapse bg-white shadow-md rounded-lg"
                    >
                        <thead>
                            <tr class="bg-maroon text-white">
                                <th class="border px-4 py-2 text-center">
                                    Year
                                </th>
                                <th class="border px-4 py-2 text-center">
                                    Action
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="cohort in cohorts"
                                :key="cohort.id"
                                class="hover:bg-gray-200 hover:bg-opacity-20 even:bg-gray-100"
                            >
                                <td class="border px-4 py-2">
                                    {{ cohort.year }} Internship Cohort
                                </td>
                                <td class="border px-4 py-2 text-center">
                                    <router-link
                                        :to="{
                                            name: 'cohort-detail',
                                            params: { year: cohort.year },
                                        }"
                                        class="text-green hover:underline"
                                    >
                                        View Interns
                                    </router-link>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </template>
    </DashboardLayout>
</template>
