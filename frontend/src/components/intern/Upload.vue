<script setup>
    import apiClient from "@/services/api";
    import { ref } from "vue";
    import { useToast } from "vue-toastification";
    import Loader from "../loader.vue";

    const emits = defineEmits(["submissionCompleted"]);

    const props = defineProps({
        month: {
            type: String,
            required: true,
        },
    });

    const toast = useToast();

    // File states
    const selectedImages = ref([]);
    const imagePreviews = ref([]);
const philosophyFile = ref([]);
const cvFile = ref([]);
const submitting = ref(false);
const videoUrl = ref("");

// Image handling
const handleImageChange = (event) => {
    const files = Array.from(event.target.files);
    let filesToAdd = files;
    const availableSlots = 5 - selectedImages.value.length;
    console.log("Available slots:", availableSlots);
    if (availableSlots <= 0) {
        toast.info("Only 5 images are allowed for this month.");
        return;
    }
    console.log("Files to add:", filesToAdd);
    if (files.length > availableSlots) {
        filesToAdd = files.slice(0, availableSlots);
        toast.info("Only 5 images are allowed for this month.");
    }
    console.log("Files to add after limit check:", filesToAdd);
    filesToAdd.forEach((file) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreviews.value.push(e.target.result);
        };
        reader.readAsDataURL(file);
        selectedImages.value.push(file);
    });
};

const removeImage = (index) => {
    imagePreviews.value.splice(index, 1);
    selectedImages.value.splice(index, 1);
};

const handlePhilosophyChange = (e) => {
    const file = e.target.files[0];
    philosophyFile.value.push(file);
};

const removePhilosophyFile = () => {
    philosophyFile.value = [];
};

const handleCvChange = (e) => {
    const cv = e.target.files[0];
    cvFile.value.push(cv);
};

const removeCvFile = (type) => {
    cvFile.value = [];
};

// File submission functions
const handleSubmit = async (endpoint, files) => {
    const formData = new FormData();
    formData.append("month", props.month);
    // formData.append("file", file);
    files.forEach((file) => {
        formData.append("file", file);
    });

    submitting.value = true;
    try {
        const response = await apiClient.post(endpoint, formData, {
            headers: { "Content-Type": "multipart/form-data" },
        });

        toast.success(response.data.detail);
        emits("submissionCompleted");
    } catch (error) {
        // console.log("error", error, "error-r", error.response);
        toast.error(error.response?.data?.detail || "Error uploading file");
    } finally {
        submitting.value = false;
    }
};

const handleImageSubmit = async () => {
    await handleSubmit("submissions/upload/img/", selectedImages.value);
    selectedImages.value = [];
    imagePreviews.value = [];
};

const handlePhilosophySubmit = async () => {
    await handleSubmit(
        "submissions/upload/philosophy/",
        philosophyFile.value
    );
    philosophyFile.value = [];
};

const handleCvSubmit = async () => {
    await handleSubmit("submissions/upload/cv/", cvFile.value);
    cvFile.value = [];
};

const handleVideoSubmit = async () => {
    if (!videoUrl.value) {
        toast.error("Please enter a valid video URL");
        return;
    }

    submitting.value = true;
    try {
        const response = await apiClient.post("submissions/submit/video/", {
            month: props.month,
            video_url: videoUrl.value,
        });

        toast.success(response.data.detail);
        emits("submissionCompleted");
    } catch (error) {
        toast.error(
            error.response?.data?.detail || "Error uploading video URL"
        );
    } finally {
        submitting.value = false;
    }
};
</script>

<template>
    <div class="container mx-auto p-4">
        <div class="bg-gray-100 p-4">
            <!-- Upload Sections -->
            <div class="mt-4 space-y-8">
                <!-- Portfolio Images Upload -->
                <div class="bg-white rounded-lg shadow p-6">
                    <h2 class="text-lg font-semibold text-[#8c003b] mb-4">
                        Portfolio Images
                    </h2>
                    <form @submit.prevent="handleImageSubmit" class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700">
                                Upload Images
                            </label>
                            <input type="file" @change="handleImageChange" accept="image/*" multiple
                                class="py-3 px-3 block w-full text-sm text-gray-500 rounded-lg border border-gray-300 focus:ring-[#8c003b] focus:border-[#8c003b]" />
                        </div>

                        <!-- Image Previews -->
                        <div v-if="imagePreviews.length" class="flex flex-wrap gap-4 mt-4">
                            <div v-for="(preview, index) in imagePreviews" :key="index"
                                class="relative w-32 h-32 bg-gray-100 rounded-lg shadow-lg overflow-hidden group">
                                <img :src="preview" class="w-full h-full object-cover" />
                                <span @click="removeImage(index)"
                                    class="absolute top-1 right-1 bg-red-500 text-white p-1 rounded-full hover:opacity-90 cursor-pointer">
                                    <i class="pi pi-times"></i>
                                </span>
                            </div>
                        </div>

                        <button type="submit" :disabled="!selectedImages.length"
                            class="w-full py-2 px-4 bg-[#006938] text-white font-medium rounded-lg hover:bg-[#008f4f]">
                            <i class="pi pi-upload mr-2"></i> Submit Images
                        </button>
                    </form>
                </div>

                <!-- Teaching Philosophy Upload (Month 4) -->
                <div v-if="month === '4'" class="bg-white rounded-lg shadow p-6">
                    <h2 class="text-lg font-semibold text-[#006938] mb-4">
                        Teaching Philosophy
                    </h2>
                    <form @submit.prevent="handlePhilosophySubmit" class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700">
                                Upload Philosophy (PDF)
                            </label>
                            <input type="file" @change="handlePhilosophyChange" accept="application/pdf"
                                class="py-3 px-3 block w-full text-sm text-gray-500 rounded-lg border border-gray-300 focus:ring-[#006938] focus:border-[#006938]" />
                        </div>

                        <!-- File Preview -->
                        <div v-if="philosophyFile.length"
                            class="flex items-center justify-between bg-gray-50 p-3 rounded-lg">
                            <div class="flex items-center">
                                <i class="pi pi-file-pdf text-2xl text-[#8c003b] mr-3"></i>
                                <span class="text-sm">{{
    philosophyFile[0].name
}}</span>
                            </div>
                            <span @click="removePhilosophyFile" class="text-red-500 hover:text-red-700 cursor-pointer">
                                <i class="pi pi-times"></i>
                            </span>
                        </div>

                        <button type="submit" :disabled="!philosophyFile"
                            class="w-full py-2 px-4 bg-[#8c003b] text-white font-medium rounded-lg hover:bg-[#a00048]">
                            <i class="pi pi-upload mr-2"></i> Submit Philosophy
                        </button>
                    </form>
                </div>

                <!-- CV Upload (Month 4) -->
                <div v-if="month === '4'" class="bg-white rounded-lg shadow p-6">
                    <h2 class="text-lg font-semibold text-[#ffc712] mb-4">
                        CV
                    </h2>
                    <form @submit.prevent="handleCvSubmit" class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700">
                                Upload CV (PDF)
                            </label>
                            <input type="file" @change="handleCvChange" accept="application/pdf"
                                class="py-3 px-3 block w-full text-sm text-gray-500 rounded-lg border border-gray-300 focus:ring-[#ffc712] focus:border-[#ffc712]" />
                        </div>

                        <!-- File Preview -->
                        <div v-if="cvFile.length" class="flex items-center justify-between bg-gray-50 p-3 rounded-lg">
                            <div class="flex items-center">
                                <i class="pi pi-file-pdf text-2xl text-[#006938] mr-3"></i>
                                <span class="text-sm">{{ cvFile[0].name }}</span>
                            </div>
                            <span @click="removeCvFile" class="text-red-500 hover:text-red-700 cursor-pointer">
                                <i class="pi pi-times"></i>
                            </span>
                        </div>

                        <button type="submit" :disabled="!cvFile"
                            class="w-full py-2 px-4 bg-[#ffc712] text-black font-medium rounded-lg hover:bg-[#ffd83e]">
                            <i class="pi pi-upload mr-2"></i> Submit CV
                        </button>
                    </form>
                </div>

                <div v-if="month === '4'" class="bg-white rounded-lg shadow p-6">
                    <h2 class="text-lg font-semibold text-[#8c003b] mb-4">
                        Video Url
                    </h2>
                    <p class="text-sm text-gray-600 mb-4">
                        Please upload your video to YouTube or any video hosting
                        platform and paste the link below.
                    </p>
                    <div>
                        <form @submit.prevent="handleVideoSubmit" class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700">
                                    Video URL
                                </label>
                                <input type="url" v-model="videoUrl"
                                    class="py-3 px-3 block w-full text-sm text-gray-500 rounded-lg border border-gray-300 focus:ring-[#8c003b] focus:border-[#8c003b]" />
                            </div>

                            <button type="submit" :disabled="!videoUrl"
                                class="w-full py-2 px-4 bg-[#8c003b] text-white font-medium rounded-lg hover:bg-[#a00048]">
                                <i class="pi pi-upload mr-2"></i> Submit Video
                                URL
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="submitting"
            class="absolute inset-0 bg-black opacity-50 flex items-center justify-center rounded-lg z-20">
            <Loader />
        </div>
    </div>
</template>
