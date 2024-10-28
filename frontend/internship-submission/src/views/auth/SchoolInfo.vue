<script setup>
    import { ref, reactive } from "vue";
    import { useAuthStore } from "@/stores/auth";
    import MentorView from "./MentorView.vue";
    import SchoolView from "./SchoolView.vue";
    import router from "@/router";

    const auth = useAuthStore();
    const next_page = ref(false);
    const school_info = reactive({});

    // const submitSchoolData = () => {
    //     // console.log(user.user_data);
    //     alert("Your school infor is saved successfully");
    // };
</script>
<template>
    <div v-if="next_page === false" class="text-center">
        <h3>School</h3>
        <SchoolView @go-next="next_page = true" />
    </div>
    <div v-else class="text-center">
        <h3>Mentor</h3>
        <MentorView " />
    </div>
</template>
