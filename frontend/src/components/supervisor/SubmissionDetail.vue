<script setup>
    import apiClient from "@/services/api";
    import { ref, computed, onMounted } from "vue";
    import { useRoute } from "vue-router";
    import SubmissionDisplay from "../SubmissionDisplay.vue";
    import { useToast } from "vue-toastification";
    import Loader from "../loader.vue";
    import BackButton from "../BackButton.vue";

    const route = useRoute();
    const toast = useToast();

    const portfolio = ref({});
    const loadingSubmissions = ref(false);
    const supervisorComment = ref("");
    const grade = ref("");
    const submittingReview = ref(false);

    const get_portfolio = async () => {
        loadingSubmissions.value = true;

        try {
            const response = await apiClient.get(
                `portfolio/${route.params.intern}/${route.params.month}/`
            );
            portfolio.value = response.data;
            // console.log(portfolio.value);
        } catch (error) {
            console.error(error);
        } finally {
            loadingSubmissions.value = false;
        }
    };

    onMounted(get_portfolio);

    const submitReview = async () => {
        // console.log("submitting review...");
        // console.log(supervisorComment.value);
        // console.log(grade.value);

        submittingReview.value = true;

        try {
            const commentData = {
                submission_id: portfolio.value.id,
                content: supervisorComment.value,
                grade: grade.value,
            };

            const response = await apiClient.post(
                "comment/create/",
                commentData
            );
            toast.success(response.data.detail);
            get_portfolio();
        } catch (error) {
            toast.error(
                error.response?.data?.detail || "Error submitting review"
            );
            console.error(error);
        } finally {
            submittingReview.value = false;
            supervisorComment.value = "";
        }
    };

    const grades = computed(() => {
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    });
</script>

<template>
    <div class="mb-4">
        <BackButton />
    </div>
    <SubmissionDisplay :submissions="portfolio" :month="route.params.month" />

    <div v-if="portfolio" class="bg-white p-8 mb-8 rounded-md">
        <form @submit.prevent="submitReview">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2"
                    >Supervisor Comments</label
                >
                <textarea
                    v-model="supervisorComment"
                    placeholder="Enter your comments for the intern"
                    class="w-full border rounded-md p-2"
                    rows="4"
                    required
                ></textarea>
            </div>

            <!-- Grade Selection -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2"
                    >Grade</label
                >
                <select v-model="grade" class="w-full border rounded-md p-2">
                    <option value="" selected disabled>Select Grade</option>
                    <option v-for="grade in grades" :key="grade" :value="grade">
                        {{ grade }}
                    </option>
                </select>
            </div>

            <div class="flex justify-end mt-4">
                <button
                    type="submit"
                    :disabled="submittingReview"
                    class="bg-green text-white px-4 py-2 rounded hover:bg-[#04c66b] disabled:opacity-50"
                >
                    {{ submittingReview ? "Submitting..." : "Submit Review" }}
                </button>
            </div>
        </form>
    </div>

    <div
        v-if="loadingSubmissions"
        class="absolute inset-0 bg-black opacity-50 flex items-center justify-center rounded-lg z-20"
    >
        <Loader />
    </div>
</template>
