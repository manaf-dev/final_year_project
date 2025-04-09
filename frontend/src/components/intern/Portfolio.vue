<script setup>
    import { ref } from "vue";

    import apiClient from "@/services/api";
    import ImageModal from "../ImageModal.vue";
    import DocumentsDisplay from "../DocumentsDisplay.vue";
    import ImageDisplay from "../ImageDisplay.vue";
    import Loader from "../loader.vue";

    const loading = ref(false);
    const selectedItem = ref(null);
    const isModalOpen = ref(false);
    const portfolios = ref({});

    const closeModal = () => {
        isModalOpen.value = false;
        setTimeout(() => {
            selectedItem.value = null;
        }, 200);
    };

    const fetchPortfolios = async () => {
        loading.value = true;
        // console.log("loading....", loading.value);
        try {
            // console.log("fetching....");
            const response = await apiClient.get("portfolio/all/");
            portfolios.value = response.data;
        } catch (error) {
            throw new Error("Error fetching portfolios");
        } finally {
            loading.value = false;
            // console.log("loading..", loading.value);
        }
        // console.log("loading....", loading.value);
    };

    fetchPortfolios();
</script>

<template>
    <div class="mx-auto p-6 space-y-8 bg-white rounded-lg shadow">
        <div class="pb-4 border-b border-gray-200">
            <h3 class="text-md font-medium">Your Internship Portfolio</h3>
        </div>

        <Loader v-if="loading" />

        <section v-else class="mt-4">
            <div class="space-y-4">
                <h3 class="text-sm font-medium text-gray-900">
                    Portfolio Images
                </h3>
                <div
                    class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
                >
                    <ImageDisplay
                        v-if="portfolios.images?.length"
                        :images="portfolios.images"
                        :show-delete="false"
                        @refresh-page="fetchPortfolios"
                    />

                    <div v-else class="col-span-full">
                        <p class="text-gray-500 text-center">
                            No portfolio image submitted
                        </p>
                    </div>
                </div>
            </div>

            <!-- Documents Section -->
            <div class="space-y-4">
                <h3 class="text-sm font-medium text-gray-900 mt-8">
                    Portfolio Documents
                </h3>
                <div
                    class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6"
                >
                    <DocumentsDisplay
                        v-if="portfolios.files?.length"
                        :submission-files="portfolios.files"
                        @refresh-page="fetchPortfolios"
                    />

                    <div v-else class="col-span-full">
                        <p class="text-gray-500 text-center">
                            No documents submitted yet
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <ImageModal
            v-if="isModalOpen"
            :image="selectedItem.image"
            :is-modal-open="isModalOpen"
            @close-modal="closeModal"
        />
    </div>
</template>
