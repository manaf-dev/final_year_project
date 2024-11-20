<template>
    <div class="max-w-4xl mx-auto p-6 space-y-8">
        <!-- Images Section -->
        <section v-if="submissions.images?.length" class="space-y-4">
            <h3 class="text-lg font-medium text-gray-900">Portfolio Images</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                <div
                    v-for="file in submissions.images"
                    :key="file.id"
                    class="flex flex-col items-center bg-white rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow relative group"
                >
                    <!-- Delete Button -->
                    <button
                        @click="confirmDelete(file.id)"
                        class="absolute -top-2 -right-2 z-10 bg-red-100 hover:bg-red-200 text-red-600 rounded-full p-1.5 opacity-0 group-hover:opacity-100 transition-opacity"
                        :disabled="isDeleting === file.id"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                        >
                            <path d="M3 6h18"></path>
                            <path
                                d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"
                            ></path>
                            <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                        </svg>
                    </button>

                    <!-- Loading Overlay -->
                    <div
                        v-if="isDeleting === file.id"
                        class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center rounded-lg z-20"
                    >
                        <div
                            class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"
                        ></div>
                    </div>

                    <div class="relative group">
                        <img
                            :src="file.image"
                            :alt="file.name"
                            class="w-48 h-36 object-cover rounded-md mb-2"
                            :class="{ 'opacity-50': isDeleting === file.id }"
                        />
                        <div
                            class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity rounded-md flex items-center justify-center"
                        >
                            <div class="flex gap-2">
                                <!-- View Button -->
                                <a
                                    :href="file.image"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="opacity-0 group-hover:opacity-100 bg-white text-gray-800 px-3 py-1 rounded-full flex items-center gap-1 text-sm hover:bg-gray-100 transition-all"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="16"
                                        height="16"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        stroke-width="2"
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                    >
                                        <path
                                            d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"
                                        />
                                        <circle cx="12" cy="12" r="3" />
                                    </svg>
                                    View
                                </a>
                            </div>
                        </div>
                    </div>

                    <div class="w-full space-y-2">
                        <p
                            class="text-sm text-gray-600 text-center truncate px-2"
                            :title="file.name"
                        >
                            {{ file.name || `Image ${file.id}` }}
                        </p>
                        <div class="flex gap-2">
                            <!-- View Button -->
                            <a
                                :href="file.image"
                                target="_blank"
                                rel="noopener noreferrer"
                                class="flex-1 flex items-center justify-center gap-1 text-sm px-4 py-1.5 bg-blue-50 text-blue-600 rounded-md hover:bg-blue-100 transition-colors"
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
                            <!-- Download Button -->
                            <button
                                @click="downloadFile(file)"
                                class="flex-1 flex items-center justify-center gap-1 text-sm px-4 py-1.5 bg-gray-50 text-gray-600 rounded-md hover:bg-gray-100 transition-colors"
                                :disabled="isDownloading === file.id"
                            >
                                <svg
                                    v-if="isDownloading !== file.id"
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
                                        d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"
                                    />
                                    <polyline points="7 10 12 15 17 10" />
                                    <line x1="12" y1="15" x2="12" y2="3" />
                                </svg>
                                <div
                                    v-else
                                    class="animate-spin rounded-full h-3 w-3 border-b-2 border-gray-600"
                                ></div>
                                Download
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Documents Section (Similar enhancements applied) -->
        <section v-if="month === 4" class="space-y-4">
            <h3 class="text-lg font-medium text-gray-900">
                Submitted Documents
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                <template v-if="submissions.philosophy || submissions.cv">
                    <!-- Teaching Philosophy -->
                    <div
                        v-if="submissions.philosophy"
                        class="flex flex-col items-center bg-white rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow relative group"
                    >
                        <!-- Similar delete, loading, and download features as images section -->
                        <!-- ... (similar structure as image items) ... -->
                    </div>

                    <!-- CV (Similar structure) -->
                    <!-- ... -->
                </template>
                <div v-else class="col-span-full">
                    <p class="text-gray-500 text-center">
                        No documents submitted yet
                    </p>
                </div>
            </div>
        </section>

        <div
            v-if="!submissions.images?.length && month !== 4"
            class="text-center text-gray-500"
        >
            No submissions found
        </div>
    </div>
</template>

<script setup>
    import { ref } from "vue";
    import { defineProps, defineEmits } from "vue";

    const props = defineProps({
        submissions: {
            type: Object,
            required: true,
            default: () => ({}),
        },
        month: {
            type: Number,
            required: true,
        },
    });

    const emit = defineEmits(["delete", "download"]);

    // Loading states
    const isDeleting = ref(null);
    const isDownloading = ref(null);

    // Delete handling
    const confirmDelete = async (fileId) => {
        if (confirm("Are you sure you want to delete this file?")) {
            isDeleting.value = fileId;
            try {
                await emit("delete", fileId);
            } catch (error) {
                console.error("Delete failed:", error);
                alert("Failed to delete file. Please try again.");
            } finally {
                isDeleting.value = null;
            }
        }
    };

    // Download handling
    const downloadFile = async (file) => {
        isDownloading.value = file.id;
        try {
            await emit("download", file);
            // Actual download logic would be implemented in the parent component
            const response = await fetch(file.image);
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = file.name || `file-${file.id}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error("Download failed:", error);
            alert("Failed to download file. Please try again.");
        } finally {
            isDownloading.value = null;
        }
    };
</script>
