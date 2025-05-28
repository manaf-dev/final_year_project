<script setup>
    import { ref } from "vue";

    const props = defineProps({
        submissionVideo: {
            type: Object,
            required: true,
        },
    });

    const videoError = ref(false);
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
        </div>
    </div>
</template>
