<script setup>
    import apiClient from "@/services/api";
    import { ref } from "vue";
    import { useToast } from "vue-toastification";
    import ConfirmModal from "./ConfirmModal.vue";

    const props = defineProps({
        submissionFiles: { type: Array, required: true },
    });

    const toast = useToast();
    const deleting = ref(false);
    const isOpen = ref(false);
    const selectedFile = ref(null);

    const openModal = (file) => {
        console.log("opening modal");
        selectedFile.value = file;
        isOpen.value = true;
        console.log(selectedFile.value, "--", isOpen.value);
    };

    const cancelDelete = () => {
        selectedFile.value = null;
        isOpen.value = false;
    };

    const confirmDelete = async (file_id) => {
        deleting.value = true;

        try {
            const response = await apiClient.delete(
                `portfolio/file/delete/${file_id}/`
            );
            toast.success(response.data.detail || "Deleted Successfully");
        } catch (error) {
            toast.error(error.response?.data?.detail || "Error deleting file");
        } finally {
            deleting.value = false;
            selectedFile.value = null;
            isOpen.value = false;
        }
    };
</script>

<template v-if="props.submissionFiles.length">
    <div
        v-for="file in props.submissionFiles"
        :key="file.id"
        class="flex flex-col items-center bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow py-2"
    >
        <div
            class="w-48 h-36 bg-gray-50 rounded-md flex items-center justify-center mb-2"
        >
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width="48"
                height="48"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="text-gray-400"
            >
                <path
                    d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"
                />
                <polyline points="14 2 14 8 20 8" />
            </svg>
        </div>

        <div class="w-full space-y-2">
            <p
                class="text-sm text-gray-600 text-center truncate px-2"
                title="document"
            >
                {{ file.file_type === "cv" ? "CV" : "Teaching Philosophy" }}
            </p>
            <div class="flex align-center justify-around">
                <a
                    :href="`http://localhost:8000/${file.file}`"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="w-2/5 flex items-center justify-center gap-1 text-sm px-4 py-1.5 bg-blue-50 text-blue-600 rounded-md hover:bg-blue-100 transition-colors"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="14"
                        height="14"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <path
                            d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"
                        />
                        <polyline points="15 3 21 3 21 9" />
                        <line x1="10" x2="21" y1="14" y2="3" />
                    </svg>
                    View
                </a>
                <button
                    @click="openModal(file)"
                    class="w-2/5 flex items-center justify-center gap-1 text-sm px-4 py-1.5 bg-blue-50 text-blue-600 rounded-md hover:bg-blue-100 transition-colors"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="14"
                        height="14"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <path
                            d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"
                        />
                        <polyline points="15 3 21 3 21 9" />
                        <line x1="10" x2="21" y1="14" y2="3" />
                    </svg>
                    Delete
                </button>
            </div>
        </div>
    </div>

    <ConfirmModal
        :is-open="isOpen"
        @confirm-delete="confirmDelete(selectedFile.id)"
        @cancel-delete="cancelDelete"
    />
</template>
