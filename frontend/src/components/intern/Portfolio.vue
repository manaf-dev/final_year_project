<script setup>
    import { ref } from "vue";

    import apiClient from "@/services/api";
    import ImageModal from "../ImageModal.vue";
    import DocumentsDisplay from "../DocumentsDisplay.vue";
    import ImageDisplay from "../ImageDisplay.vue";
    import VideoDisplay from "../VideoDisplay.vue";
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
            const response = await apiClient.get("submissions/portfolio/all/");
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
    <div class="container mx-auto p-4">
        <!-- Main Content Container -->
        <div class="bg-white rounded-xl shadow-lg overflow-hidden">
            <!-- Enhanced Header -->
            <div class="bg-gradient-to-r from-[#8c003b] to-[#a00048] text-white px-6 py-6">
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                    <div>
                        <h1 class="text-2xl font-bold mb-2">
                            Complete Portfolio
                        </h1>
                        <p class="text-white/80 text-sm">
                            View all your submitted work across all months
                        </p>
                    </div>
                    
                    <!-- Status Badge -->
                    <div class="flex items-center space-x-4 mt-4 sm:mt-0">
                        <div class="px-3 py-1.5 rounded-full text-sm font-medium bg-green-100 text-green-800 border border-green-200">
                            <i class="pi pi-folder mr-1.5"></i>
                            Complete View
                        </div>
                        
                    </div>
                </div>
            </div>

            <!-- Quick Stats -->
            <div class="border-b border-gray-200 px-6 py-4">
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                    <!-- Images Count -->
                    <div class="text-center">
                        <div class="text-2xl font-bold text-[#8c003b]">
                            {{ portfolios.images?.length || 0 }}
                        </div>
                        <div class="text-xs text-gray-500">Portfolio Images</div>
                    </div>
                    
                    <!-- Documents Count -->
                    <div class="text-center">
                        <div class="text-2xl font-bold text-[#006938]">
                            {{ portfolios.files?.length || 0 }}
                        </div>
                        <div class="text-xs text-gray-500">Documents</div>
                    </div>
                    
                    <!-- Video Status -->
                    <div class="text-center">
                        <div class="text-2xl font-bold text-[#ffc712]">
                            <i :class="portfolios.video ? 'pi pi-check' : 'pi pi-times'"></i>
                        </div>
                        <div class="text-xs text-gray-500">Teaching Video</div>
                    </div>
                    
                    <!-- Total Items -->
                    <div class="text-center">
                        <div class="text-2xl font-bold text-gray-600">
                            {{ (portfolios.images?.length || 0) + (portfolios.files?.length || 0) + (portfolios.video ? 1 : 0) }}
                        </div>
                        <div class="text-xs text-gray-500">Total Items</div>
                    </div>
                </div>
            </div>

            <Loader v-if="loading" />

            <div v-else class="space-y-8">
                <!-- Portfolio Images Section -->
                <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
                    <div class="bg-gradient-to-r from-red-50 to-red-100 px-6 py-4 border-b border-red-200">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-3">
                                <div class="w-10 h-10 bg-[#8c003b] rounded-xl flex items-center justify-center">
                                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                    </svg>
                                </div>
                                <div>
                                    <h2 class="text-xl font-bold text-gray-900">Portfolio Images</h2>
                                    <p class="text-sm text-gray-600">Visual documentation of your teaching experience</p>
                                </div>
                            </div>
                            <div class="text-right">
                                <div class="text-2xl font-bold text-[#8c003b]">{{ portfolios.images?.length || 0 }}</div>
                                <div class="text-sm text-gray-600">Images</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="p-6">
                        <div v-if="portfolios.images?.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                            <ImageDisplay
                                :images="portfolios.images"
                                :show-delete="false"
                                @refresh-page="fetchPortfolios"
                            />
                        </div>
                        <div v-else class="text-center py-12">
                            <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                            </svg>
                            <p class="text-gray-500 text-lg font-medium">No portfolio images submitted yet</p>
                            <p class="text-gray-400 text-sm mt-1">Upload images through your monthly submissions</p>
                        </div>
                    </div>
                </div>

                <!-- Portfolio Documents Section -->
                <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
                    <div class="bg-gradient-to-r from-green-50 to-green-100 px-6 py-4 border-b border-green-200">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-3">
                                <div class="w-10 h-10 bg-[#006938] rounded-xl flex items-center justify-center">
                                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                    </svg>
                                </div>
                                <div>
                                    <h2 class="text-xl font-bold text-gray-900">Portfolio Documents</h2>
                                    <p class="text-sm text-gray-600">Teaching philosophy, reflections, and CV</p>
                                </div>
                            </div>
                            <div class="text-right">
                                <div class="text-2xl font-bold text-[#006938]">{{ portfolios.files?.length || 0 }}</div>
                                <div class="text-sm text-gray-600">Documents</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="p-6">
                        <div v-if="portfolios.files?.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                            <DocumentsDisplay
                                :submission-files="portfolios.files"
                                :show-delete="false"
                                @refresh-page="fetchPortfolios"
                            />
                        </div>
                        <div v-else class="text-center py-12">
                            <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                            <p class="text-gray-500 text-lg font-medium">No documents submitted yet</p>
                            <p class="text-gray-400 text-sm mt-1">Submit documents through your monthly submissions</p>
                        </div>
                    </div>
                </div>

                <!-- Portfolio Video Section -->
                <div v-if="portfolios.video" class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
                    <div class="bg-gradient-to-r from-yellow-50 to-yellow-100 px-6 py-4 border-b border-yellow-200">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-3">
                                <div class="w-10 h-10 bg-[#ffc712] rounded-xl flex items-center justify-center">
                                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                                    </svg>
                                </div>
                                <div>
                                    <h2 class="text-xl font-bold text-gray-900">Portfolio Video</h2>
                                    <p class="text-sm text-gray-600">Video presentation of your teaching experience</p>
                                </div>
                            </div>
                            <div class="text-right">
                                <div class="text-2xl font-bold text-[#ffc712]">1</div>
                                <div class="text-sm text-gray-600">Video</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="p-6">
                        <VideoDisplay :submission-video="portfolios.video" />
                    </div>
                </div>

                <!-- Empty Video Section Placeholder -->
                <div v-else class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
                    <div class="bg-gradient-to-r from-yellow-50 to-yellow-100 px-6 py-4 border-b border-yellow-200">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-3">
                                <div class="w-10 h-10 bg-[#ffc712] rounded-xl flex items-center justify-center">
                                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                                    </svg>
                                </div>
                                <div>
                                    <h2 class="text-xl font-bold text-gray-900">Portfolio Video</h2>
                                    <p class="text-sm text-gray-600">Video presentation of your teaching experience</p>
                                </div>
                            </div>
                            <div class="text-right">
                                <div class="text-2xl font-bold text-[#ffc712]">0</div>
                                <div class="text-sm text-gray-600">Videos</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="p-6">
                        <div class="text-center py-12">
                            <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                            </svg>
                            <p class="text-gray-500 text-lg font-medium">No video submitted yet</p>
                            <p class="text-gray-400 text-sm mt-1">Submit a video through your monthly submissions</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <ImageModal
            v-if="isModalOpen"
            :image="selectedItem?.image"
            :is-modal-open="isModalOpen"
            @close-modal="closeModal"
        />
    </div>
</template>
