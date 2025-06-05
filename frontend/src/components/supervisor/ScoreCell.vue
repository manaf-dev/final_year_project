<template>
  <div v-if="score !== null && score !== undefined">
    <div class="text-sm font-medium" :class="getScoreColor(score)">
      {{ score }}%
    </div>
  </div>
  <div v-else class="text-gray-400 text-sm">Not graded</div>
</template>

<script setup>
const props = defineProps({
  score: {
    type: [Number, null],
    default: null,
  },
  month: {
    type: String,
    required: true,
  },
});

const getScoreColor = (score) => {
  if (score >= 80) return "text-green-600";
  if (score >= 70) return "text-blue-600";
  if (score >= 60) return "text-yellow-600";
  return "text-red-600";
};
</script>
