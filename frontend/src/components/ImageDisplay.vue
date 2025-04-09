<script setup>
    import { ref } from "vue";
    import { useToast } from "vue-toastification";
    import { useAuthStore } from "@/stores/auth";
    import ImageModal from "./ImageModal.vue";
    import ConfirmModal from "./ConfirmModal.vue";
    import Loader from "./loader.vue";
    import apiClient from "@/services/api";

    defineProps({
        images: { type: Object, required: true, default: () => ({}) },
        showDelete: { type: Boolean, default: true },
    });
    const emit = defineEmits(["refreshPage"]);

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
        // console.log("opening modal");
        selectedImage.value = image;
        isConfirmOpen.value = true;
        // console.log(selectedImage.value, "--", isConfirmOpen.value);
    };

    const cancelDelete = () => {
        selectedImage.value = null;
        isConfirmOpen.value = false;
    };

    const confirmDelete = async (img_id) => {
        isConfirmOpen.value = false;
        deleting.value = true;
        // console.log("deleting...", deleting.value);

        // console.log("headers", apiClient.defaults.headers);
        try {
            const response = await apiClient.delete(
                `portfolio/img/delete/${img_id}/`
            );
            toast.success(response.data.detail || "Deleted Successfully");
            emit("refreshPage");
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
        class="group relative bg-white rounded-lg shadow-md overflow-hidden"
    >
        <!-- Portfolio Item -->
        <div class="">
            <img
                :src="item.image"
                alt="portfolio image"
                class="w-full h-32 object-cover transform group-hover:scale-105 transition-transform duration-300"
            />
        </div>

        <div class="py-4 flex align-center justify-around">
            <button
                @click="openImageModal(item)"
                class="w-2/5 flex items-center justify-center gap-1 text-sm px-4 py-1.5 bg-blue-50 text-blue-600 rounded-md hover:bg-blue-100 transition-colors"
            >
                <i class="pi pi-window-maximize" style="font-size: 1rem"></i>
            </button>
            <button
                v-if="authStore.isIntern && showDelete"
                @click="openConfirmModal(item)"
                class="w-2/5 flex items-center justify-center gap-1 text-sm px-4 py-1.5 bg-red-50 text-red-600 rounded-md hover:bg-red-100 transition-colors"
            >
                <i class="pi pi-trash" style="font-size: 1rem"></i>
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
        <Loader />
    </div>
</template>
