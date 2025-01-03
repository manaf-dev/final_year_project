<script setup>
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import apiClient from "@/services/api";
    import { ref } from "vue";

    const loading = ref(false);

    const get_portfolio = async () => {
        loading.value = true;

        try {
            const response = await apiClient.get(
                `portfolio/${route.params.intern}/${route.params.month}/`
            );
            portfolio.value = response.data;
            console.log(portfolio.value);
        } catch (error) {
            console.error(error);
        } finally {
            loading.value = false;
        }
    };

    onMounted(get_portfolio);
</script>

<template>
    <DashboardLayout :title="'Intern Portfolio'">
        <template #content
            ><SubmissionDisplay
                :submissions="portfolio"
                :month="route.params.month"
        /></template>
    </DashboardLayout>
</template>
