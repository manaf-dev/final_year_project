<script setup>
    import { ref } from "vue";
    import { useToast } from "vue-toastification";
    import { useAuthStore } from "@/stores/auth";
    import ImageModal from "./ImageModal.vue";
    import ConfirmModal from "./ConfirmModal.vue";
    import BeatLoader from "vue-spinner/src/BeatLoader.vue";
    import apiClient from "@/services/api";

    defineProps({
        images: { type: Object, required: true, default: () => ({}) },
    });
    const authStore = useAuthStore();
    const toast = useToast();
    const deleting = ref(false);
    const selectedImage = ref({});
    const isConfirmOpen = ref(false);
    const isImageOpen = ref(false);

    const openImageModal = (item) => {
        selectedImage.value = item;
        isImageOpen.value = true;
    };

    const closeImageModal = () => {
        isImageOpen.value = false;
        setTimeout(() => {
            selectedImage.value = null;
        }, 200);
    };

    const openConfirmModal = (image) => {
        console.log("opening modal");
        selectedImage.value = image;
        isConfirmOpen.value = true;
        console.log(selectedImage.value, "--", isConfirmOpen.value);
    };

    const cancelDelete = () => {
        selectedImage.value = null;
        isConfirmOpen.value = false;
    };

    const confirmDelete = async (img_id) => {
        isConfirmOpen.value = false;
        deleting.value = true;
        console.log("deleting...", deleting.value);

        console.log("headers", apiClient.defaults.headers);
        try {
            const response = await apiClient.delete(
                `portfolio/img/delete/${img_id}/`
            );
            toast.success(response.data.detail || "Deleted Successfully");
        } catch (error) {
            toast.error(error.response?.data?.detail || "Error deleting image");
        } finally {
            deleting.value = false;
            selectedImage.value = null;
        }
    };
</script>

<template>
    <div
        v-for="item in images"
        :key="item.id"
        class="group relative bg-white rounded-lg shadow-sm overflow-hidden"
    >
        <!-- Portfolio Item -->
        <div class="">
            <img
                :src="item.image"
                alt="portfolio image"
                class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-300"
            />
        </div>

        <div class="flex align-center justify-around">
            <button
                @click="openImageModal(item)"
                class="bg-gray-100 opacity-50 text-gray-900 px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-white"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                >
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    <line x1="11" y1="8" x2="11" y2="14"></line>
                    <line x1="8" y1="11" x2="14" y2="11"></line>
                </svg>
                View
            </button>
            <button
                v-if="authStore.isIntern"
                @click="openConfirmModal(item)"
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

    <ImageModal
        :image="selectedImage?.image"
        :is-modal-open="isImageOpen"
        @close-modal="closeImageModal"
    />

    <ConfirmModal
        :is-open="isConfirmOpen"
        @confirm-delete="confirmDelete(selectedImage.id)"
        @cancel-delete="cancelDelete"
    />

    <div
        v-if="deleting"
        class="absolute inset-0 bg-black opacity-50 flex items-center justify-center rounded-lg z-20"
    >
        <BeatLoader />
    </div>
</template>
