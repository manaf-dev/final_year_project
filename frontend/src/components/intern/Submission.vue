<script setup>
    import apiClient from "@/services/api";
    import { computed, ref, onMounted, watch } from "vue";
    import { useAuthStore } from "@/stores/auth";
    import { onBeforeRouteUpdate } from "vue-router";
    import { useToast } from "vue-toastification";
    import SubmissionDisplay from "../SubmissionDisplay.vue";
    import SubmissionModal from "./SubmissionModal.vue";
    import SubmissionLock from "./SubmissionLock.vue";

    const toast = useToast();
    const props = defineProps({ month: String });
    const authStore = useAuthStore();
    const submissions = ref({});
    const loadingSubmissions = ref(false);
    const showSubmissionModal = ref(false);

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
                    `submissions/portfolio/${authStore.user.username}/${props.month}/`
                );
                // console.log(response.data);
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
        getSubmissions();
    });

    const handleSubmissionCompleted = () => {
        showSubmissionModal.value = false;
        getSubmissions();
    };

    const selectedType = ref("images");
    const openSubmissionModal = (type) => {
        if (submissions.value.images?.length >= 5 && type === "images") {
            toast.info("You have reached the maximum number of images for this month.");
            return;
        }
        
        if (!submissions.value.graded) {
            selectedType.value = type || "images";
            showSubmissionModal.value = true;
        }
    };
</script>

<template>
    <div v-if="isMonthPeriod" class="container mx-auto p-4">
        <!-- Main Content Container -->
        <div class="bg-white rounded-xl shadow-lg overflow-hidden">
            <!-- Enhanced Header -->
            <div class="bg-gradient-to-r from-[#8c003b] to-[#a00048] text-white px-6 py-6">
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                    <div>
                        <h1 class="text-2xl font-bold mb-2">
                            Month {{ month }} Portfolio
                        </h1>
                        <p class="text-white/80 text-sm">
                            View your submissions and track your progress
                        </p>
                    </div>
                    
                    <!-- Status Badge and Submit Button -->
                    <div class="flex items-center space-x-4 mt-4 sm:mt-0">
                        <!-- Grading Status -->
                        <div class="flex flex-col sm:flex-row sm:items-center sm:space-x-4 space-y-2 sm:space-y-0 w-full">
                            <!-- Grading Status -->
                            <div :class="[
                                'px-3 py-1.5 rounded-full text-sm font-medium w-full sm:w-auto text-center',
                                submissions.graded
                                    ? 'bg-green-100 text-green-800 border border-green-200'
                                    : 'bg-yellow-100 text-yellow-800 border border-yellow-200'
                            ]">
                                <i :class="[
                                    'pi mr-1.5',
                                    submissions.graded ? 'pi-check-circle' : 'pi-clock'
                                ]"></i>
                                {{ submissions.graded ? `Graded (${submissions.grade}/10)` : 'Pending Review' }}
                            </div>

                            <!-- Locked Badge -->
                            <div v-if="!submissions.intern?.cohort?.active && !submissions.graded" class="inline-flex items-center justify-center px-4 py-2 bg-gray-200 text-gray-600 rounded-lg font-medium w-full sm:w-auto">
                                <i class="pi pi-lock mr-2"></i>
                                Locked
                            </div>
                            
                            <!-- Submit Button -->
                            <button
                                v-else-if="!submissions.graded"
                                @click="openSubmissionModal('images')"
                                class="inline-flex items-center justify-center px-4 py-2 bg-white text-[#8c003b] rounded-lg font-medium hover:bg-gray-50 transition-all duration-200 shadow-sm hover:shadow-md w-full sm:w-auto"
                            >
                                <i class="pi pi-plus mr-2"></i>
                                New Submission
                            </button>

                            <!-- Completed Badge -->
                            <div v-else class="inline-flex items-center justify-center px-4 py-2 bg-white/20 text-white rounded-lg font-medium w-full sm:w-auto">
                                <i class="pi pi-check-circle mr-2"></i>
                                Completed
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Quick Stats (if there are submissions) -->
            <div v-if="Object.keys(submissions).length" class="border-b border-gray-200 px-6 py-4">
                <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-4">
                    <!-- Images Count -->
                    <div class="text-center">
                        <div class="text-2xl font-bold text-blue-600">
                            {{ submissions.images?.length || 0 }}
                        </div>
                        <div class="text-xs text-gray-500">Portfolio Images</div>
                    </div>
                    
                    <!-- Month 4 specific stats -->
                    <template v-if="month === '4'">
                        <!-- Teaching Philosophy Count -->
                        <div class="text-center">
                            <div class="text-2xl font-bold text-green-600">
                                {{ submissions.files?.filter(f => f.file_type === 'teaching_philosophy').length || 0 }}
                            </div>
                            <div class="text-xs text-gray-500">Teaching Philosophy</div>
                        </div>
                        
                        <!-- CV Count -->
                        <div class="text-center">
                            <div class="text-2xl font-bold text-yellow-600">
                                {{ submissions.files?.filter(f => f.file_type === 'cv').length || 0 }}
                            </div>
                            <div class="text-xs text-gray-500">CV</div>
                        </div>
                        
                        <!-- Reflective Teaching Count -->
                        <div class="text-center">
                            <div class="text-2xl font-bold text-orange-600">
                                {{ submissions.files?.filter(f => f.file_type === 'reflective').length || 0 }}
                            </div>
                            <div class="text-xs text-gray-500">Reflective Teaching</div>
                        </div>
                        
                        <!-- Video Status -->
                        <div class="text-center">
                            <div class="text-2xl font-bold text-purple-600">
                                <i :class="submissions.video ? 'pi pi-check' : 'pi pi-times'"></i>
                            </div>
                            <div class="text-xs text-gray-500">Teaching Video</div>
                        </div>
                    </template>
                    
                    <!-- Comments Count -->
                    <div class="text-center">
                        <div class="text-2xl font-bold text-gray-600">
                            {{ submissions.comments?.length || 0 }}
                        </div>
                        <div class="text-xs text-gray-500">Comments</div>
                    </div>
                </div>
            </div>

            <!-- Main Submission Display -->
            <div class="p-6">
                <SubmissionDisplay
                    @submit-view="openSubmissionModal"
                    @refresh-page="getSubmissions"
                    :submissions="submissions"
                    :month="props.month"
                    :loading-submissions="loadingSubmissions"
                />
            </div>
        </div>

        <!-- Submission Modal -->
        <SubmissionModal
            :is-open="showSubmissionModal"
            :month="props.month"
            :selected-type="selectedType"
            @close="showSubmissionModal = false"
            @submitted="handleSubmissionCompleted"
        />
    </div>

    <SubmissionLock v-else />
</template>
