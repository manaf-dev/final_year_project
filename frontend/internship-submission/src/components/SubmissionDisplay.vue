<script setup>
    import { ref } from "vue";
    import DocumentsDisplay from "./DocumentsDisplay.vue";
    import ImageDisplay from "./ImageDisplay.vue";
    import Loader from "./loader.vue";
    import { useAuthStore } from "@/stores/auth";

    const props = defineProps({
        submissions: {
            type: Object,
            required: true,
            default: () => ({}),
        },
        month: {
            type: String,
            required: true,
        },
        loadingSubmissions: {
            type: Boolean,
            default: false,
        },
    });

    const authStore = useAuthStore();

    defineEmits(["submitView"]);

    const formatDate = (dateStr) => {
        const date = new Date(dateStr);
        return date.toLocaleDateString("en-GB", {
            year: "numeric",
            month: "numeric",
            day: "numeric",
        });
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
                    {{
                        submissions.graded
                            ? `Graded  (${submissions.grade}/10)`
                            : "Not graded"
                    }}
                </span>
            </div>
        </div>

        <Loader v-if="loadingSubmissions" />

        <section v-if="!loadingSubmissions" class="mt-4">
            <div v-if="submissions.images?.length" class="space-y-4">
                <h3 class="text-sm font-medium text-gray-900">
                    Portfolio Images
                </h3>
                <div
                    class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
                >
                    <ImageDisplay :images="submissions.images" />
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
            <div v-if="month === '4'" class="space-y-4">
                <h3 class="text-sm font-medium text-gray-900 mt-8">
                    Submitted Documents
                </h3>
                <div
                    class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6"
                >
                    <DocumentsDisplay
                        v-if="submissions.files"
                        :submission-files="
                            submissions.files ? submissions.files : []
                        "
                    />

                    <div v-else class="col-span-full">
                        <p class="text-gray-500 text-center">
                            No documents submitted yet
                        </p>
                    </div>
                </div>
            </div>

            <!-- Comments Section -->
            <div class="border-t pt-4">
                <h4 class="font-medium mb-2">Supervisor Comments</h4>
                <div
                    v-if="submissions.comments"
                    v-for="comment in submissions.comments"
                    :key="comment.id"
                    class="bg-gray-50 p-3 rounded-md mb-2"
                >
                    <div class="flex justify-between text-sm text-gray-500">
                        <span
                            v-if="authStore.isIntern"
                            class="font-medium capitalize"
                            >{{ comment.author.title }}.
                            {{ comment.author.last_name }}
                            {{ comment.author.first_name }}</span
                        >
                        <span v-else class="font-medium capitalize">You</span>
                        <span>{{ formatDate(comment.updated_at) }}</span>
                    </div>
                    <p class="mt-1 pl-2 text-base text-gray-700">
                        {{ comment.content }}
                    </p>
                </div>

                <div
                    v-if="!submissions?.comments?.length"
                    class="bg-gray-50 p-3 rounded-md mb-2"
                >
                    <p class="mt-1 text-gray-700">No comments</p>
                </div>
            </div>
        </section>
    </div>
</template>
