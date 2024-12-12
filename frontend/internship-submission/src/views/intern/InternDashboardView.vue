<script setup>
    import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
    import InternHome from "@/components/intern/InternHome.vue";
</script>

<template>
    <DashboardLayout>
        <template #title> Dashboard </template>
        <template #content>
            <InternHome />
        </template>
    </DashboardLayout>
</template>

<style>
    .bg-a-red {
        background-color: #8c003b;
    }
    .bg-a-green {
        background-color: #006938;
    }
    .bg-a-yellow {
        background-color: #ffc712;
    }
</style>
