<script setup>
    defineProps({
        id: String,
        label: String,
        modelValue: String,
        type: {
            type: String,
            default: "text",
        },
        required: {
            type: Boolean,
            default: true,
        },
    });
    const emits = defineEmits(["update:modelValue"]);
</script>

<template>
    <div class="mb-4">
        <label :for="id" class="block text-sm font-medium text-gray-700">{{
            label
        }}</label>
        <input
            :id="id"
            :type="type"
            :value="modelValue"
            :requred="required"
            @input="$emit('update:modelValue', $event.target.value)"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        />
    </div>
</template>
