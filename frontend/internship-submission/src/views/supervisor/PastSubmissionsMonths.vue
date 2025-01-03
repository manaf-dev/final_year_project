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
                <BackButton />
                <p class="text-gray-600 mt-4">
                    {{ route.params.year }} Cohort Months
                </p>
                <div>
                    <table
                        class="table-auto w-full border-collapse bg-white shadow-md rounded-lg"
                    >
                        <thead>
                            <tr class="bg-maroon text-white">
                                <th class="border px-4 py-2 text-left">
                                    Month
                                </th>
                                <th class="border px-4 py-2 text-left">
                                    Action
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="month in months"
                                :key="month.id"
                                class="hover:bg-gray-200 hover:bg-opacity-20 even:bg-gray-100"
                            >
                                <td class="border px-4 py-2">
                                    {{ month.desc }}
                                </td>
                                <td class="border px-4 py-2 text-center">
                                    <router-link
                                        :to="{
                                            name: 'past-submissions-interns',
                                            params: {
                                                month: month.id,
                                                year: route.params.year,
                                            },
                                        }"
                                        class="text-green hover:underline"
                                    >
                                        View
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
