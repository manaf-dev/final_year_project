<script setup>
    import apiClient from "@/services/api";
    import { ref } from "vue";
    import { useToast } from "vue-toastification";
    import ConfirmModal from "./ConfirmModal.vue";

    const props = defineProps({
        submissionFiles: { type: Array, required: true },
    });

    const emit = defineEmits(["refreshPage"]);

    const toast = useToast();
    const deleting = ref(false);
    const isOpen = ref(false);
    const selectedFile = ref(null);

    const openModal = (file) => {
        // console.log("opening modal");
        selectedFile.value = file;
        isOpen.value = true;
        // console.log(selectedFile.value, "--", isOpen.value);
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
            emit("refreshPage");
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
            <i class="pi pi-file-pdf" style="font-size: 4rem; color: gray"></i>
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
                    <i
                        class="pi pi-window-maximize"
                        style="font-size: 1rem"
                    ></i>
                </a>
                <button
                    @click="openModal(file)"
                    class="w-2/5 flex items-center justify-center gap-1 text-sm px-4 py-1.5 bg-red-50 text-red-600 rounded-md hover:bg-red-100 transition-colors"
                >
                    <i class="pi pi-trash" style="font-size: 1rem"></i>
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
