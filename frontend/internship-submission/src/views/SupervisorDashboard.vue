<template>
    <DashboardLayout>
        <div class="mb-6">
            <h1 class="text-3xl font-bold">Supervisor Dashboard</h1>
        </div>
        <div class="space-y-6">
            <div class="bg-white p-6 rounded-lg shadow">
                <h2 class="text-lg font-medium text-gray-900 mb-4">
                    Intern Submissions
                </h2>
                <div class="space-y-4">
                    <div v-for="year in years" :key="year" class="space-y-2">
                        <h3 class="text-md font-medium text-gray-900">
                            {{ year }}
                        </h3>
                        <table class="w-full">
                            <thead>
                                <tr>
                                    <th class="text-left pb-2">Intern</th>
                                    <th class="text-left pb-2">Month</th>
                                    <th class="text-left pb-2">Portfolio</th>
                                    <th class="text-left pb-2">Comment</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="submission in submissions[year]"
                                    :key="submission.id"
                                    class="border-b"
                                >
                                    <td class="py-2">
                                        {{ submission.intern.fullName }}
                                    </td>
                                    <td class="py-2">{{ submission.month }}</td>
                                    <td class="py-2">
                                        <a
                                            :href="submission.portfolioUrl"
                                            target="_blank"
                                            class="text-indigo-600 hover:text-indigo-500"
                                        >
                                            View
                                        </a>
                                    </td>
                                    <td class="py-2">
                                        <textarea
                                            v-model="submission.comment"
                                            class="w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                                            @input="updateComment(submission)"
                                        ></textarea>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </DashboardLayout>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    import axios from "axios";
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";

    const years = ref([]);
    const submissions = ref({});

    onMounted(async () => {
        try {
            const response = await axios.get("/api/submissions");
            years.value = response.data.years;
            submissions.value = response.data.submissions;
        } catch (error) {
            console.error("Error fetching submissions:", error);
        }
    });

    const updateComment = async (submission) => {
        try {
            await axios.put(`/api/submissions/${submission.id}`, {
                comment: submission.comment,
            });
        } catch (error) {
            console.error(
                `Error updating comment for submission ${submission.id}:`,
                error
            );
        }
    };
</script>
