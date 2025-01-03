<script setup>
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import Submission from "@/components/intern/Submission.vue";
    import NewSubmission from "@/components/intern/NewSubmission.vue";
    import { computed, ref } from "vue";
    import { onBeforeRouteUpdate, useRoute } from "vue-router";

    const route = useRoute();
    const month = ref("");
    month.value = route.params.month;

    onBeforeRouteUpdate((to, from) => {
        month.value = to.params.month;
    });

    const viewTitle = computed(() => {
        console.log("switch value ", month.value);
        switch (month.value) {
            case "1":
                return "First Month Submissions";
                break;
            case "2":
                return "Second Month Submissions";
                break;
            case "3":
                return "Third Month Submissions";
                break;
            case "4":
                return "Fourth Month Submissions";
                break;

            default:
                return "Month Submissions";
                break;
        }
    });
</script>

<template>
    <DashboardLayout :title="viewTitle">
        <template #content> <Submission :month="month" /> </template>
    </DashboardLayout>
</template>
