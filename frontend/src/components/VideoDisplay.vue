<script setup>
import { ref, computed } from "vue";
import apiClient from "@/services/api";
import { useToast } from "vue-toastification";
import ConfirmModal from "./ConfirmModal.vue";

const props = defineProps({
    submissionVideo: {
        type: Object,
        required: true,
    },
    showDelete: {
        type: Boolean,
        default: false,
    },
});

const emits = defineEmits(["refresh"]);

const toast = useToast();
const deleting = ref(false);
const isOpen = ref(false);
const selectedVideo = ref(null);
const videoError = ref(false);

// Helper to check if the URL is a YouTube link
const isYouTube = computed(() => {
    const url = props.submissionVideo.video_url || "";
    return url.includes("youtube.com") || url.includes("youtu.be");
});

// Extract YouTube video ID and build embed URL
const youTubeEmbedUrl = computed(() => {
    const url = props.submissionVideo.video_url || "";
    let videoId = "";
    if (url.includes("youtube.com")) {
        const match = url.match(/[?&]v=([^&]+)/);
        videoId = match ? match[1] : "";
    } else if (url.includes("youtu.be")) {
        const match = url.match(/youtu\.be\/([^?&]+)/);
        videoId = match ? match[1] : "";
    }
    return videoId ? `https://www.youtube.com/embed/${videoId}` : "";
});

const deleteVideo = async (video_id) => {
    if (deleting.value) return;

    deleting.value = true;
    try {
        await apiClient.delete(`/submissions/video/${props.submissionVideo.id}/delete/`);
        toast.success("Video deleted successfully.");
        emits("refresh");
    } catch (error) {
        console.error("Error deleting video:", error);
        toast.error("Failed to delete video.");
    } finally {
        deleting.value = false;
    }
};
const openConfirmModal = () => {
    selectedVideo.value = props.submissionVideo;
    isOpen.value = true;
};


</script>

<template>
    <div class="w-full lg:w-1/2 space-y-8 bg-white rounded-lg shadow">

        <!-- Video Player -->
        <div class="p-6">
            <template v-if="isYouTube">
                <iframe
                    :src="youTubeEmbedUrl"
                    class="w-full h-72 rounded-lg"
                    frameborder="0"
                    allowfullscreen
                ></iframe>
            </template>
            <template v-else>
                <video
                    controls
                    class="w-full h-auto rounded-lg"
                    :src="submissionVideo.video_url"
                    type="video/mp4"
                    @error="videoError = true"
                    v-show="!videoError"
                ></video>
                <div v-if="videoError" class="mt-4 text-red-600">
                    Video cannot be played.
                    <span>
                        <a
                            :href="submissionVideo.video_url"
                            target="_blank"
                            class="underline text-blue-600"
                        >
                            Click here to open the video
                        </a>
                        or copy the URL:
                        <span class="break-all bg-gray-100 px-2 py-1 rounded">{{
                            submissionVideo.video_url
                        }}</span>
                    </span>
                </div>
            </template>

            <!-- Video URL -->
            <div class="p-4 ml-8 text-sm text-gray-600">
                <span class="font-semibold">Video URL: </span>
                <a
                    :href="submissionVideo.video_url"
                    target="_blank"
                    class="underline text-blue-600"
                >
                    {{ submissionVideo.video_url }}
                </a>
            </div>

            <!-- Delete -->
            <div v-if="showDelete" class="mt-4">
                <button
                    @click="openConfirmModal"
                    class="px-4 py-2 bg-red-50 text-red-600 rounded-md hover:bg-red-100 transition-colors"
                >
                    <i class="pi pi-trash" style="font-size: 1.4rem"></i>
                </button>
            </div>
        </div>
    </div>

    <ConfirmModal
        v-if="showDelete"
        :is-open="isOpen"
        @confirmDelete="deleteVideo(selectedVideo.id)"
        @cancelDelete="isOpen = false"
    />
</template>
