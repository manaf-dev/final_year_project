<script setup>
    defineProps({
        label: String,
        disabled: { type: Boolean, default: false },
    });
</script>

<template>
    <button
        :disabled="disabled"
        @click="$emit('clicked')"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
    >
        {{ label }}
    </button>
</template>
