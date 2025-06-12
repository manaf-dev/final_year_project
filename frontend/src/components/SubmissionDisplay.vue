<script setup>
    import { ref } from "vue";
    import DocumentsDisplay from "./DocumentsDisplay.vue";
    import ImageDisplay from "./ImageDisplay.vue";
    import VideoDisplay from "./VideoDisplay.vue";
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

    defineEmits(["submitView", "refreshPage"]);

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
    <div class="space-y-6">
        <Loader v-if="loadingSubmissions" />

        <section v-if="!loadingSubmissions">
            <!-- Portfolio Images Section -->
            <div class="mb-8">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-semibold text-gray-900 flex items-center">
                        <i class="pi pi-images text-blue-600 mr-2"></i>
                        Portfolio Images
                    </h3>
                    <span v-if="submissions.images?.length" class="text-sm text-gray-500">
                        {{ submissions.images.length }} {{ submissions.images.length === 1 ? 'image' : 'images' }}
                    </span>
                </div>

                <div v-if="submissions.images?.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    <ImageDisplay 
                        :images="submissions.images" 
                        :show-delete="!submissions.graded"
                        @refresh-page="$emit('refreshPage')" 
                    />
                </div>

                <div v-else class="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                    <i class="pi pi-images text-4xl text-gray-400 mb-3"></i>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">No portfolio images submitted</h3>
                    <p class="text-gray-500 mb-4">Upload images to showcase your work and progress</p>
                    <button 
                        v-if="authStore.isIntern && !submissions.graded" 
                        class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                        @click="$emit('submitView', 'images')"
                    >
                        <i class="pi pi-plus mr-2"></i>
                        Submit Images
                    </button>
                </div>
            </div>

            

            <!-- Documents Section (Month 4) -->
            <div v-if="month === '4'" class="mb-8 space-y-6">
                <!-- Teaching Philosophy -->
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-900 flex items-center">
                            <i class="pi pi-file-edit text-green-600 mr-2"></i>
                            Teaching Philosophy
                        </h3>
                    </div>

                    <div v-if="submissions.files?.filter(f => f.file_type === 'philosophy').length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                        <DocumentsDisplay :submission-files="submissions.files.filter(f => f.file_type === 'philosophy')" :show-delete="authStore.isIntern && !submissions.graded" @refresh-page="$emit('refreshPage')" />
                    </div>

                    <div v-else class="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                        <i class="pi pi-file-edit text-3xl text-gray-400 mb-3"></i>
                        <h4 class="text-md font-medium text-gray-900 mb-2">No teaching philosophy submitted</h4>
                        <p class="text-gray-500 mb-3 text-sm">Upload your teaching philosophy document</p>
                        <button 
                            v-if="authStore.isIntern && !submissions.graded" 
                            class="inline-flex items-center px-3 py-2 bg-green text-white rounded-lg hover:bg-green-700 transition-colors text-sm"
                            @click="$emit('submitView', 'philosophy')"
                        >
                            <i class="pi pi-plus mr-2"></i>
                            Submit Teaching Philosophy
                        </button>
                    </div>
                </div>

                <!-- CV -->
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-900 flex items-center">
                            <i class="pi pi-file-pdf text-yellow-600 mr-2"></i>
                            Curriculum Vitae (CV)
                        </h3>
                    </div>

                    <div v-if="submissions.files?.filter(f => f.file_type === 'cv').length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                        <DocumentsDisplay :submission-files="submissions.files.filter(f => f.file_type === 'cv')" :show-delete="authStore.isIntern && !submissions.graded" @refresh-page="$emit('refreshPage')" />
                    </div>

                    <div v-else class="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                        <i class="pi pi-file-pdf text-3xl text-gray-400 mb-3"></i>
                        <h4 class="text-md font-medium text-gray-900 mb-2">No CV submitted</h4>
                        <p class="text-gray-500 mb-3 text-sm">Upload your updated CV in PDF format</p>
                        <button 
                            v-if="authStore.isIntern && !submissions.graded" 
                            class="inline-flex items-center px-3 py-2 bg-yellow text-white rounded-lg hover:bg-yellow-700 transition-colors text-sm"
                            @click="$emit('submitView', 'cv')"
                        >
                            <i class="pi pi-plus mr-2"></i>
                            Submit CV
                        </button>
                    </div>
                </div>

                <!-- Reflective Teaching -->
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-900 flex items-center">
                            <i class="pi pi-file-word text-orange-600 mr-2"></i>
                            Reflective Teaching
                        </h3>
                    </div>

                    <div v-if="submissions.files?.filter(f => f.file_type === 'reflective').length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                        <DocumentsDisplay :submission-files="submissions.files.filter(f => f.file_type === 'reflective')" :show-delete="authStore.isIntern && !submissions.graded" @refresh-page="$emit('refreshPage')" />
                    </div>

                    <div v-else class="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                        <i class="pi pi-file-word text-3xl text-gray-400 mb-3"></i>
                        <h4 class="text-md font-medium text-gray-900 mb-2">No reflective teaching document submitted</h4>
                        <p class="text-gray-500 mb-3 text-sm">Upload your reflective teaching document</p>
                        <button 
                            v-if="authStore.isIntern && !submissions.graded" 
                            class="inline-flex items-center px-3 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors text-sm"
                            @click="$emit('submitView', 'reflective')"
                        >
                            <i class="pi pi-plus mr-2"></i>
                            Submit Reflective Teaching
                        </button>
                    </div>
                </div>

                <!-- Teaching Video Section (Month 4) -->
            <div>
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-semibold text-gray-900 flex items-center">
                        <i class="pi pi-video text-purple-600 mr-2"></i>
                        Teaching Video
                    </h3>
                </div>

                <div v-if="submissions.video" class="bg-white border border-gray-200 rounded-lg overflow-hidden">
                    <VideoDisplay :submission-video="submissions.video" :show-delete="authStore.isIntern && !submissions.graded" @refresh="$emit('refreshPage')" />
                </div>

                <div v-else class="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                    <i class="pi pi-video text-4xl text-gray-400 mb-3"></i>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">No teaching video submitted</h3>
                    <p class="text-gray-500 mb-4">Submit a teaching video URL</p>
                    <button 
                        v-if="authStore.isIntern && !submissions.graded" 
                        class="inline-flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
                        @click="$emit('submitView', 'video')"
                    >
                        <i class="pi pi-plus mr-2"></i>
                        Submit Video
                    </button>
                </div>
            </div>
                
            </div>

            <!-- Comments Section -->
                <div class="bg-gray-50 rounded-lg p-6 mb-8">
                    <h4 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                        <i class="pi pi-comments text-orange-600 mr-2"></i>
                        Supervisor Comments
                    </h4>
                    
                    <div v-if="submissions.comments?.length" class="space-y-3">
                        <div 
                            v-for="comment in submissions.comments" 
                            :key="comment.id"
                            class="bg-white border border-gray-200 rounded-lg p-4"
                        >
                            <div class="flex justify-between items-start mb-2">
                                <span v-if="authStore.isIntern" class="font-medium text-gray-900 capitalize">
                                    {{ comment.author.title }}. {{ comment.author.last_name }} {{ comment.author.first_name }}
                                </span>
                                <span v-else class="font-medium text-gray-900">You</span>
                                <span class="text-sm text-gray-500">{{ formatDate(comment.updated_at) }}</span>
                            </div>
                            <p class="text-gray-700 leading-relaxed">{{ comment.content }}</p>
                        </div>
                    </div>
    
                    <div v-else class="text-center py-8">
                        <i class="pi pi-comment text-3xl text-gray-400 mb-3"></i>
                        <p v-if="authStore.isIntern" class="text-gray-500">No comments yet from your supervisor</p>
                        <p v-else class="text-gray-500">You have not commented on this portfolio yet</p>
                        <p class="text-gray-500">Comments will appear here once submitted</p>
                    </div>
                </div>

        </section>
    </div>
</template>
