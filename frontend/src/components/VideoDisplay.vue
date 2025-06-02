<script setup>
import { ref, computed } from "vue";

const props = defineProps({
    submissionVideo: {
        type: Object,
        required: true,
    },
});

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
</script>

<template>
    <div class="mx-auto space-y-8 bg-white rounded-lg shadow">
        <!-- Header -->
        <div
            class="bg-[#8c003b] text-white rounded-lg shadow-lg px-6 py-4 flex justify-between items-center"
        >
            <h1 class="text-xl font-medium">Video Submission</h1>
        </div>

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
        </div>
    </div>
</template>
