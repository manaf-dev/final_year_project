<script setup>
    import apiClient from "@/services/api";
    import { ref, onMounted } from "vue";
    import SubmissionDisplay from "./SubmissionDisplay.vue";
    import Upload from "./Upload.vue";

    const props = defineProps({ month: Number });

    const activeTab = ref("view");
    const submissions = ref({});

    const loadingSubmissions = ref(false);

    const getSubmissions = async () => {
        loadingSubmissions.value = true;
        console.log("headers", apiClient.defaults.headers);

        try {
            const response = await apiClient.get(`portfolio/${props.month}/`);
            submissions.value = response.data;
        } catch (error) {
            console.error(error);
        } finally {
            loadingSubmissions.value = false;
        }
    };

    onMounted(getSubmissions);

    const uploaded = () => {
        activeTab.value = "view";
        getSubmissions();
    };
</script>

<template>
    <div class="container mx-auto p-4 max-w-4xl">
        <div class="border-b border-gray-200">
            <nav class="flex -mb-px">
                <button
                    @click="activeTab = 'view'"
                    :class="[
                        'py-4 px-6',
                        activeTab === 'view'
                            ? 'border-b-2 text-blue-600'
                            : 'text-gray-500',
                    ]"
                >
                    View Submissions
                </button>
                <button
                    @click="activeTab = 'submit'"
                    :class="[
                        'py-4 px-6',
                        activeTab === 'submit'
                            ? 'border-b-2 text-blue-600'
                            : 'text-gray-500',
                    ]"
                >
                    Submit Work
                </button>
            </nav>
        </div>

        <div v-if="activeTab === 'view'" class="mt-6 space-y-4">
            <SubmissionDisplay
                @submit-view="activeTab = 'submit'"
                :submissions="submissions"
                :month="props.month"
                :loading-submissions="loadingSubmissions"
            />
        </div>

        <div v-if="activeTab === 'submit'" class="mt-6">
            <div class="bg-white rounded-lg shadow">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h2 class="text-lg font-medium">Submit New Work</h2>
                </div>
                <Upload
                    v-if="!submissions.graded"
                    :month="props.month"
                    @submission-completed="uploaded"
                />

                <div v-else class="py-8">
                    <p class="text-lg text-gray-500 text-center">
                        Submission Completed
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>
