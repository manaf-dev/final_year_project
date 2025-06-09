<template>
  <div v-if="score === null || score === undefined" class="text-gray-400 text-sm">Not graded</div>
  <div v-else-if="score === -1" class="text-gray-400 text-sm">Not submitted</div>
  <div v-else>
    <div class="text-sm font-medium" :class="getScoreColor(score)">
      {{ score }}
    </div>
  </div>
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
  if (score === null || score === undefined) return "text-gray-400";
  if (props.month === "4") {
    if (score >= 40) return "text-green-600";
    if (score >= 30) return "text-blue-600";
    if (score >= 20) return "text-yellow-600";
    return "text-red-600";
  }
  if (score >= 8) return "text-green-600";
  if (score >= 6) return "text-blue-600";
  if (score >= 4) return "text-yellow-600";
  return "text-red-600";
};
</script>
