<script setup>
    import { ref } from "vue";
    import BeatLoader from "vue-spinner/src/BeatLoader.vue";

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
        loadingSubmissions: {
            type: Boolean,
            default: false,
        },
    });

    defineEmits(["submitView"]);
    // Loading states
    const isDeleting = ref(null);
    const isDownloading = ref(null);

    // Delete handling
    const confirmDelete = async (fileId) => {
        if (confirm("Are you sure you want to delete this file?")) {
            isDeleting.value = fileId;
            try {
                emit("delete", fileId);
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
            emit("download", file);
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

<template>
    <div class="max-w-4xl mx-auto p-6 space-y-8 bg-white rounded-lg shadow">
        <div class="pb-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
                <h3 class="text-lg font-medium">Portfolio For The Month</h3>
                <span
                    :class="[
                        'px-2 py-1 text-xs font-medium rounded-full',
                        submissions.graded
                            ? 'bg-green-100 text-green-800'
                            : 'bg-yellow-100 text-yellow-800',
                    ]"
                >
                    {{ submissions.graded ? "Graded" : "Not graded" }}
                </span>
            </div>
        </div>

        <BeatLoader :loading="loadingSubmissions" />

        <section v-if="!loadingSubmissions" class="mt-4">
            <div v-if="submissions.images?.length" class="space-y-4">
                <h3 class="text-sm font-medium text-gray-900">
                    Portfolio Images
                </h3>
                <div class="flex flex-col space-y-4 text-sm text-gray-500">
                    <figure class="flex flex-row items-center flex-wrap gap-5">
                        <img
                            v-for="submission in submissions.images"
                            :key="submission.id"
                            :src="submission.image"
                            class="mr-1 h-32"
                        />
                    </figure>
                </div>
            </div>

            <div
                v-if="!submissions.images?.length"
                class="text-center text-gray-500 rounded-lg"
            >
                <div class="flex items-center justify-between">
                    <h3 class="text-lg font-medium">No submissions found</h3>
                    <button
                        class="px-2 py-1 ml-5 bg-a-green text-white rounded"
                        @click="$emit('submitView')"
                    >
                        Submit here
                    </button>
                </div>
            </div>

            <!-- Documents Section -->
            <div v-if="month === 4" class="space-y-4">
                <h3 class="text-sm font-medium text-gray-900 mt-8">
                    Submitted Documents
                </h3>
                <div
                    class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6"
                >
                    <template v-if="submissions.files">
                        <div
                            v-for="file in submissions.files"
                            :key="file.id"
                            class="flex flex-col items-center bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow"
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
                                    title="Teaching Philosophy"
                                >
                                    Teaching Philosophy.pdf
                                </p>
                                <a
                                    :href="`http://localhost:8000/${file.file}`"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="w-full flex items-center justify-center gap-1 text-sm px-4 py-1.5 bg-blue-50 text-blue-600 rounded-md hover:bg-blue-100 transition-colors"
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
                                    View File
                                </a>
                            </div>
                        </div>
                    </template>
                    <div v-else class="col-span-full">
                        <p class="text-gray-500 text-center">
                            No documents submitted yet
                        </p>
                    </div>
                </div>
            </div>
            <!-- Comments Section -->
            <!-- <div class="border-t pt-4">
                <h4 class="font-medium mb-2">Supervisor Comments</h4>
                <div
                    v-for="(comment, idx) in submission.comments"
                    :key="idx"
                    class="bg-gray-50 p-3 rounded-md mb-2"
                >
                    <div
                        class="flex justify-between text-sm text-gray-600"
                    >
                        <span class="font-medium">{{
                            comment.author
                        }}</span>
                        <span>{{ comment.date }}</span>
                    </div>
                    <p class="mt-1 text-gray-700">{{ comment.text }}</p>
                </div>
            </div> -->
        </section>
    </div>
</template>
