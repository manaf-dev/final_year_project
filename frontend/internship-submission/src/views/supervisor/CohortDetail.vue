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
    <DashboardLayout>
        <template #title>Cohort {{ route.params.year }}</template>
        <template #content>
            <div class="p-6 bg-gray-50 min-h-screen">
                <BackButton />
                <p class="text-gray-600 mb-4">Cohort Interns List</p>
                <div v-if="loading" class="flex justify-center items-center">
                    <Loader />
                </div>
                <div v-else>
                    <table
                        class="table-auto w-full border-collapse bg-white shadow-md rounded-lg"
                    >
                        <thead>
                            <tr class="bg-maroon text-white">
                                <th class="border px-4 py-2 text-left">
                                    Studend ID
                                </th>
                                <th class="border px-4 py-2 text-left">Name</th>
                                <th class="border px-4 py-2 text-left">
                                    Phone
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="intern in interns"
                                :key="intern.id"
                                class="hover:bg-gray-200 hover:bg-opacity-20 even:bg-gray-100"
                            >
                                <td class="border px-4 py-2">
                                    {{ intern.username }}
                                </td>
                                <td class="border px-4 py-2">
                                    {{ intern.last_name }}
                                    {{ intern.first_name }}
                                </td>
                                <td class="border px-4 py-2">
                                    {{ intern.phone }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </template>
    </DashboardLayout>
</template>
