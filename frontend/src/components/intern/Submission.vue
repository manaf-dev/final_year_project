<script setup>
    import apiClient from "@/services/api";
    import { computed, ref, onMounted, watch } from "vue";
    import { useAuthStore } from "@/stores/auth";
    import { onBeforeRouteUpdate } from "vue-router";
    import SubmissionDisplay from "../SubmissionDisplay.vue";
    import Upload from "./Upload.vue";
    import SubmissionLock from "./SubmissionLock.vue";

    const props = defineProps({ month: String });
    const authStore = useAuthStore();
    const activeTab = ref("view");
    const submissions = ref({});
    const loadingSubmissions = ref(false);

    const currentDate = ref(new Date().toISOString().slice(0, 10));

    const isMonthPeriod = computed(() => {
        const startDate = new Date(authStore.user.cohort.start_date);
        const currentDateValue = new Date(currentDate.value);
        if (props.month === "1" && startDate < currentDateValue) return true;
        if (
            props.month === "2" &&
            new Date(startDate.setDate(startDate.getDate() + 30)) <
                currentDateValue
        )
            return true;
        if (
            props.month === "3" &&
            new Date(startDate.setDate(startDate.getDate() + 60)) <
                currentDateValue
        )
            return true;
        if (
            props.month === "4" &&
            new Date(startDate.setDate(startDate.getDate() + 90)) <
                currentDateValue
        )
            return true;
        return false;
    });

    const getSubmissions = async () => {
        if (isMonthPeriod.value) {
            loadingSubmissions.value = true;
            try {
                const response = await apiClient.get(
                    `portfolio/${authStore.user.username}/${props.month}/`
                );
                console.log(response.data);
                submissions.value = response.data;
            } catch (error) {
                console.error(error);
            } finally {
                loadingSubmissions.value = false;
            }
        }
    };

    onMounted(getSubmissions);

    onBeforeRouteUpdate((to, from) => {
        submissions.value = {};
        activeTab.value = "view";
        getSubmissions();
    });

    const uploaded = () => {
        activeTab.value = "view";
        getSubmissions();
    };
</script>

<template>
    <div v-if="isMonthPeriod" class="container mx-auto p-4">
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

        <div v-if="activeTab === 'view'" class="mt-2 space-y-4">
            <SubmissionDisplay
                @submit-view="activeTab = 'submit'"
                @refresh-page="getSubmissions"
                :submissions="submissions"
                :month="props.month"
                :loading-submissions="loadingSubmissions"
            />
        </div>

        <div v-if="activeTab === 'submit'" class="mt-2">
            <div class="bg-white rounded-lg shadow">
                <!-- Header -->
                <div
                    class="bg-[#8c003b] text-white rounded-lg shadow-lg px-6 py-4 flex justify-between items-center"
                >
                    <h1 class="text-xl font-medium">Upload Portfolio</h1>
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

    <SubmissionLock v-else />
</template>
