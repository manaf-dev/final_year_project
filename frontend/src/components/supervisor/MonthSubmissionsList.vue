<script setup>
    import apiClient from "@/services/api";
    import { useAuthStore } from "@/stores/auth";
    import { computed, onMounted, ref, watch } from "vue";
    import { onBeforeRouteUpdate, useRoute } from "vue-router";
    import Loader from "../loader.vue";
import { subscribe } from "node:diagnostics_channel";

    const authStore = useAuthStore();
    const props = defineProps({
        month: String,
        year: { type: String, default: String(new Date().getFullYear()) },
    });

    const month_submissions = ref([]);
    const loading = ref(false);
    const route = useRoute();

    const get_month_submissions = async () => {
        // console.log("calling...");
        loading.value = true;
        try {
            const response = await apiClient.get(
                `submissions/cohort/${props.year}/${props.month}/`
            );
            month_submissions.value = response.data;
            // console.log(month_submissions.value);
        } catch (error) {
            throw new Error("Error fetching month submissions");
        } finally {
            loading.value = false;
        }
    };

    onMounted(get_month_submissions);

    // watch(route, (newRoute) => {
    //     month.value = route.params.month;
    //     get_month_submissions;
    // });

    onBeforeRouteUpdate((to, from) => {
        month_submissions.value = [];
        get_month_submissions();
    });
</script>

<template>
    <div class="max-w-7xl mx-auto px-6 lg:px-8 pb-8">
        <div class="flex flex-col mt-6">
            <div class="overflow-hidden bg-white shadow-xl rounded-xl border border-gray-200">
                <div class="bg-maroon px-6 py-4">
                    <h3 class="text-lg font-semibold text-white">Month {{ props.month }} Submissions</h3>
                    <p class="text-white text-opacity-80 text-sm mt-1">Review and grade intern submissions  ({{ month_submissions.length }} Submitted)</p>
                </div>
                
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Intern Details
                                </th>
                                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Contact
                                </th>
                                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Status
                                </th>
                                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Grade
                                </th>
                                <th class="px-6 py-4 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Actions
                                </th>
                            </tr>
                        </thead>

                        <tbody class="bg-white divide-y divide-gray-200" v-if="!loading">
                            <tr
                                v-for="submission in month_submissions"
                                :key="submission.id"
                                class="hover:bg-gray-50 transition-colors duration-150"
                            >
                                <td class="px-6 py-4">
                                    <div class="flex items-center">
                                        
                                        <div>
                                            <div class="text-sm font-semibold text-gray-900">
                                                {{ submission.intern.username }}
                                            </div>
                                            <div class="text-sm text-gray-500">
                                                {{ submission.intern.last_name }}
                                                {{ submission.intern.first_name }}
                                                {{ submission.intern.other_names }}
                                            </div>
                                        </div>
                                    </div>
                                </td>

                                <td class="px-6 py-4">
                                    <div class="space-y-1">
                                        <div class="text-sm text-gray-900">
                                            {{ submission.intern.phone }}
                                        </div>
                                        <div class="text-sm text-gray-500">
                                            {{ submission.intern.email }}
                                        </div>
                                    </div>
                                </td>

                                <td class="px-6 py-4">
                                    <span
                                        :class="[
                                            'inline-flex items-center px-3 py-1 rounded-full text-xs font-medium',
                                            submission.graded
                                                ? 'bg-green-100 text-green-800'
                                                : 'bg-yellow-100 text-yellow-800',
                                        ]"
                                    >
                                        <span
                                            :class="[
                                                'w-2 h-2 rounded-full mr-2',
                                                submission.graded
                                                    ? 'bg-green'
                                                    : 'bg-yellow',
                                            ]"
                                        ></span>
                                        {{ submission.graded ? "Graded" : "Not graded" }}
                                    </span>
                                </td>

                                <td class="px-6 py-4">
                                    <div class="flex items-center">
                                        <div
                                            class="text-md font-bold mr-2 "
                                        >
                                            {{ submission.grade || '--' }}
                                        </div>
                                        <span class="text-sm text-gray-500">{{ month === '4' ? '/50' : '/10' }}</span>
                                    </div>
                                </td>

                                <td class="px-6 py-4 text-right">
                                    <RouterLink
                                        :to="{
                                            name: 'submission-detail',
                                            params: {
                                                intern: submission.intern.username,
                                                month: month,
                                            },
                                        }"
                                        class="inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg text-white bg-maroon hover:bg-maroon hover:opacity-90 transition-all duration-150 shadow-sm hover:shadow-md"
                                    >
                                        Review
                                    </RouterLink>
                                </td>
                            </tr>
                            
                            <tr v-if="!month_submissions.length">
                                <td colspan="5" class="px-6 py-12 text-center">
                                    <div class="flex flex-col items-center">
                                        <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                                            <span class="text-2xl text-gray-400">📄</span>
                                        </div>
                                        <h3 class="text-lg font-medium text-gray-900 mb-1">No submissions yet</h3>
                                        <p class="text-gray-500">No submissions have been made for this month.</p>
                                    </div>
                                </td>
                            </tr>
                        </tbody>

                        <tbody v-if="loading">
                            <tr>
                                <td colspan="5" class="px-6 py-12">
                                    <div class="flex justify-center">
                                        <Loader />
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>
