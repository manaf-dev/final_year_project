<script setup>
    import {
        Dialog,
        DialogPanel,
        TransitionChild,
        TransitionRoot,
    } from "@headlessui/vue";
    import { ref } from "vue";

    // const isModalOpen = ref(true);

    const props = defineProps({ image: String, isModalOpen: Boolean });
    const emits = defineEmits(["closeModal"]);
</script>

<template>
    <!-- Modal -->
    <TransitionRoot appear :show="props.isModalOpen" as="template">
        <Dialog as="div" @close="$emit('closeModal')" class="relative z-50">
            <!-- Backdrop -->
            <TransitionChild
                as="template"
                enter="ease-out duration-300"
                enter-from="opacity-0"
                enter-to="opacity-100"
                leave="ease-in duration-200"
                leave-from="opacity-100"
                leave-to="opacity-0"
            >
                <div class="fixed inset-0 bg-black/25" />
            </TransitionChild>

            <!-- Modal Content -->
            <div class="fixed inset-0 overflow-y-auto">
                <div
                    class="flex min-h-full items-center justify-center p-4 text-center"
                >
                    <TransitionChild
                        as="template"
                        enter="ease-out duration-300"
                        enter-from="opacity-0 scale-95"
                        enter-to="opacity-100 scale-100"
                        leave="ease-in duration-200"
                        leave-from="opacity-100 scale-100"
                        leave-to="opacity-0 scale-95"
                    >
                        <DialogPanel
                            class="relative w-full max-w-3xl transform rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
                        >
                            <!-- Close Button -->
                            <button
                                @click="$emit('closeModal')"
                                class="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="24"
                                    height="24"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                >
                                    <line x1="18" y1="6" x2="6" y2="18"></line>
                                    <line x1="6" y1="6" x2="18" y2="18"></line>
                                </svg>
                            </button>

                            <!-- Image -->
                            <div class="mt-4">
                                <img
                                    :src="image"
                                    alt="image"
                                    class="w-full h-auto rounded-lg"
                                />
                            </div>
                        </DialogPanel>
                    </TransitionChild>
                </div>
            </div>
        </Dialog>
    </TransitionRoot>
</template>
