<script setup>
    import { ref, reactive } from "vue";
    import { useAuthStore } from "@/stores/auth";
    import { useToast } from "vue-toastification";
    import SchoolDetailForm from "@/components/auth/SchoolDetailForm.vue";
    import MentorDetailForm from "@/components/auth/MentorDetailForm.vue";
    import router from "@/router";
    import apiClient from "@/services/api";

    const toast = useToast();
    const authStore = useAuthStore();
    const currentStep = ref(1);

    const handleSubmittedSchool = async (school) => {
        console.log("submit school", school);

        try {
            
            const response = await apiClient.post(
                "accounts/intern-school/new/",
                school
            );
            toast.success(response.data.detail);
            currentStep.value++;
        } catch (error) {
            toast.error(error.response?.data?.detail || "Saving school failed");
        }
    };

    const handleSubmittedMentor = async (mentor) => {
        console.log("submit mentor", mentor);

        try {
            const response = await apiClient.post(
                "accounts/mentor/new/",
                mentor
            );
            toast.success(response.data.detail);
            router.push("/dashboard");
        } catch (error) {
            toast.error(error.response?.data?.detail || "Saving mentor failed");
        }
    };
</script>
<template>
    <div class="max-w-2xl mx-auto p-6">
        <div class="my-8">
            <div class="flex justify-between">
                <span
                    :class="[
                        'px-4 py-2 rounded-lg',
                        currentStep === 1
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-200',
                    ]"
                >
                    School Details
                </span>
                <span
                    :class="[
                        'px-4 py-2 rounded-lg',
                        currentStep === 2
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-200',
                    ]"
                >
                    Mentor Details
                </span>
            </div>
        </div>

        <SchoolDetailForm
            v-if="currentStep === 1"
            @school-submitted="handleSubmittedSchool"
        />

        <MentorDetailForm
            v-if="currentStep === 2"
            @mentor-submitted="handleSubmittedMentor"
        />
    </div>
</template>
