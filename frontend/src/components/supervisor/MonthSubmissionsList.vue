<script setup>
    import apiClient from "@/services/api";
    import { useAuthStore } from "@/stores/auth";
    import { computed, onMounted, ref, watch } from "vue";
    import { onBeforeRouteUpdate, useRoute } from "vue-router";
    import Loader from "../loader.vue";

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
    <div class="max-w-7xl mx-auto px-6 lg:px-8 py-8">
    <div class="flex flex-col mt-8">
        <div
            class="py-2 -my-2 overflow-x-auto sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8"
        >
            <div
                class="inline-block min-w-full overflow-hidden align-middle border-b border-gray-200 shadow sm:rounded-lg"
            >
                <table class="min-w-full">
                    <thead>
                        <tr>
                            <th
                                class="px-6 py-3 text-xs font-medium leading-4 tracking-wider text-left text-gray-500 uppercase border-b border-gray-200 bg-gray-50"
                            >
                                Name
                            </th>
                            <th
                                class="px-6 py-3 text-xs font-medium leading-4 tracking-wider text-left text-gray-500 uppercase border-b border-gray-200 bg-gray-50"
                            >
                                Contact
                            </th>
                            <th
                                class="px-6 py-3 text-xs font-medium leading-4 tracking-wider text-left text-gray-500 uppercase border-b border-gray-200 bg-gray-50"
                            >
                                Status
                            </th>
                            <th
                                class="px-6 py-3 text-xs font-medium leading-4 tracking-wider text-left text-gray-500 uppercase border-b border-gray-200 bg-gray-50"
                            >
                                Grade
                            </th>
                            <th
                                class="px-6 py-3 border-b border-gray-200 bg-gray-50"
                            ></th>
                        </tr>
                    </thead>

                    <tbody class="bg-white" v-if="!loading">
                        <tr
                            v-for="submission in month_submissions"
                            :key="submission.id"
                        >
                            <td
                                class="px-6 py-4 whitespace-no-wrap border-b border-gray-200"
                            >
                                <div class="flex items-center">
                                    <div class="mr-4">
                                        <div
                                            class="text-sm font-medium leading-5 text-gray-900"
                                        >
                                            {{ submission.intern.username }}
                                        </div>
                                        <div
                                            class="text-sm leading-5 text-gray-500"
                                        >
                                            {{ submission.intern.last_name }}
                                            {{ submission.intern.first_name }}
                                        </div>
                                    </div>
                                </div>
                            </td>

                            <td
                                class="px-6 py-4 whitespace-no-wrap border-b border-gray-200"
                            >
                                <div class="text-sm leading-5 text-gray-900">
                                    {{ submission.intern.phone }}
                                </div>
                                <div class="text-sm leading-5 text-gray-500">
                                    {{ submission.intern.email }}
                                </div>
                            </td>

                            <td
                                class="px-6 py-4 whitespace-no-wrap border-b border-gray-200"
                            >
                                <span
                                    :class="[
                                        'inline-flex px-2 text-xs font-semibold leading-5 rounded-full',
                                        submission.graded
                                            ? 'bg-green-100 text-green-800'
                                            : 'bg-yellow-100 text-yellow-800',
                                    ]"
                                    >{{
                                        submission.graded
                                            ? "Graded"
                                            : "Not graded"
                                    }}</span
                                >
                            </td>

                            <td
                                class="px-6 py-4 text-sm leading-5 text-gray-500 whitespace-no-wrap border-b border-gray-200"
                            >
                                {{ submission.grade }}/10
                            </td>

                            <td
                                class="px-6 py-4 text-sm font-medium leading-5 text-right whitespace-no-wrap border-b border-gray-200"
                            >
                                <RouterLink
                                    :to="{
                                        name: 'submission-detail',
                                        params: {
                                            intern: submission.intern.username,
                                            month: month,
                                        },
                                    }"
                                    class="text-indigo-600 hover:text-indigo-900"
                                    >View</RouterLink
                                >
                            </td>
                        </tr>
                        <tr v-if="!month_submissions.length">
                            <td
                                class="px-6 py-4 whitespace-no-wrap border-b border-gray-200"
                                colspan="5"
                            >
                                No Submission made for this month.
                            </td>
                        </tr>
                    </tbody>

                    <Loader v-if="loading" />
                </table>
            </div>
        </div>
    </div>
    </div>
</template>
