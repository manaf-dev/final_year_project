<script setup>
    import { ref, reactive } from "vue";
    import { useAuthStore } from "@/stores/auth";
    import { useToast } from "vue-toastification";
    import SchoolDetailForm from "@/components/SchoolDetailForm.vue";
    import router from "@/router";
    import apiClient from "@/services/api";

    const toast = useToast();
    const authStore = useAuthStore();

    const handleSchoolSubmitted = (school) => {
        console.log("submit school", school);
        // schoolData.value = school;
        // formStep.value++;
    };

    // const handleMentorSubmitted = async (mentor) => {
    //     mentorData.value = mentor;

    //     const payload = { school: schoolData.value, mentor: mentorData.value };
    //     console.log(payload);
    //     // try {
    //     //     response = await apiClient.post(`accounts/intern/${authStore.user.id}/school/`)
    //     //     toast.success('Detail Saved Successfully')
    //     // } catch (error) {
    //     //     toast.error('Error saving details')
    //     // }
    // };
</script>
<template>
    <SchoolDetailForm @form-submitted="handleSchoolSubmitted" />
</template>
