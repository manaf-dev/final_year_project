<script setup>
import DashboardLayout from "@/components/Dashboard/DashboardLayout.vue";
import Scores from "@/components/supervisor/Scores.vue";
</script>

<template>
  <DashboardLayout :title="'Intern Scores'">
    <template #content>
      <Scores />
    </template>
  </DashboardLayout>
</template>
