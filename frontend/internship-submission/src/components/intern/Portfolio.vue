<script setup>
    import { ref } from "vue";

    import apiClient from "@/services/api";
    import ImageModal from "../ImageModal.vue";
    import DocumentsDisplay from "../DocumentsDisplay.vue";
    import ImageDisplay from "../ImageDisplay.vue";

    const loading = ref(false);
    const selectedItem = ref(null);
    const isModalOpen = ref(false);

    const portfolios = ref({});

    const formatDate = (date) => {
        return new Intl.DateTimeFormat("en-US", {
            month: "long",
            day: "numeric",
            year: "numeric",
        }).format(new Date(date));
    };

    const openModal = (item) => {
        selectedItem.value = item;
        isModalOpen.value = true;
    };

    const closeModal = () => {
        isModalOpen.value = false;
        setTimeout(() => {
            selectedItem.value = null;
        }, 200);
    };

    // Lifecycle
    const fetchPortfolios = async () => {
        loading.value = true;
        try {
            // Replace with actual API call
            const response = await apiClient.get("portfolio/all/");
            portfolios.value = response.data;
        } catch (error) {
            console.error("Failed to fetch portfolios:", error);
        } finally {
            loading.value = false;
        }
    };

    fetchPortfolios();
</script>

<template>
    <div class="min-h-screen bg-gray-100 py-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <!-- Header Section -->
            <div class="mb-8">
                <h1 class="text-2xl font-semibold text-gray-900">
                    Portfolio Gallery
                </h1>
                <p class="mt-1 text-sm text-gray-500">
                    Browse through all portfolio submissions across different
                    months
                </p>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="flex justify-center items-center py-12">
                <div
                    class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"
                ></div>
            </div>

            <!-- Portfolio Grid -->
            <div
                v-else
                class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
            >
                <ImageDisplay :images="portfolios.images" />

                <!-- Empty State -->
                <div
                    v-if="!portfolios"
                    class="col-span-full flex flex-col items-center justify-center py-12"
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
                        class="text-gray-400 mb-4"
                    >
                        <path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path>
                        <path d="M22 12A10 10 0 0 0 12 2v10z"></path>
                    </svg>
                    <p class="text-gray-500">No portfolios found</p>
                </div>
            </div>

            <ImageModal
                v-if="isModalOpen"
                :image="selectedItem.image"
                :is-modal-open="isModalOpen"
                @close-modal="closeModal"
            />
            <div
                class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mt-8"
            >
                <DocumentsDisplay :submission-files="portfolios.files" />
            </div>
        </div>
    </div>
</template>
