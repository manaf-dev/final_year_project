<script setup>
    import apiClient from "@/services/api";
    import { ref } from "vue";
    import BeatLoader from "vue-spinner/src/BeatLoader.vue";
    import { useToast } from "vue-toastification";

    const emits = defineEmits(["submissionCompleted"]);

    const props = defineProps({
        month: {
            type: Number,
            required: true,
        },
    });

    const toast = useToast();

    // File states
    const selectedImages = ref([]);
    const imagePreviews = ref([]);
    const philosophyFile = ref(null);
    const cvFile = ref(null);
    const submitting = ref(false);

    // Image handling
    const handleImageChange = (event) => {
        const files = Array.from(event.target.files);

        // Create previews
        files.forEach((file) => {
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
        philosophyFile.value = e.target.files[0];
    };

    const removePhilosphyFile = () => {
        philosophyFile.value = null;
    };

    const handleCvChange = (e) => {
        cvFile.value = e.target.files[0];
    };

    const removeCvFile = (type) => {
        cvFile.value = null;
    };

    // File submission functions
    const handleSubmit = async (endpoint, files) => {
        const formData = new FormData();
        formData.append("month", props.month);
        files.forEach((file) => {
            formData.append("files", file);
        });

        submitting.value = true;
        try {
            const response = await apiClient.post(endpoint, formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            toast.success(response.data.detail);
            emits("submissionCompleted");
        } catch (error) {
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
        philosophyFile.value = null;
    };

    const handleCvSubmit = async () => {
        await handleSubmit("submissions/upload/cv/", cvFile.value);
        cvFile.value = null;
    };
</script>

<template>
    <div class="container mx-auto p-4 max-w-4xl">
        <div class="space-y-6">
            <!-- Image Upload -->
            <div class="p-6 border-b-2 border-gray-200">
                <h3 class="text-lg font-medium mb-4">Portfolio Images</h3>
                <div class="mb-4">
                    <form @submit.prevent="handleImageSubmit" class="space-y-4">
                        <div>
                            <label
                                class="block text-sm font-medium text-gray-700"
                                >Upload Portfolio Images</label
                            >
                            <div class="mt-1 flex items-center">
                                <input
                                    type="file"
                                    @change="handleImageChange"
                                    accept="
                                        image/*
                                    "
                                    multiple
                                    class="py-3 px-3 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 outline outline-1 rounded hover:file:bg-blue-100"
                                />
                            </div>
                        </div>

                        <!-- Image Previews -->
                        <div
                            v-if="imagePreviews.length"
                            class="flex flex-wrap items-center gap-4 mt-4"
                        >
                            <div
                                v-for="(preview, index) in imagePreviews"
                                :key="index"
                                class="relative group"
                            >
                                <img
                                    :src="preview"
                                    class="w-full h-32 object-cover rounded-md"
                                />
                                <button
                                    @click="removeImage(index)"
                                    class="absolute top-1 right-1 bg-red-500 text-white p-1 rounded-full group-hover:opacity-100 transition-opacity"
                                >
                                    ✕
                                </button>
                            </div>
                        </div>
                        <button
                            type="submit"
                            :disabled="selectedImages.length < 1"
                            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-a-green hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                        >
                            Submit Images
                        </button>
                    </form>
                </div>
            </div>

            <!-- Philosophy Upload (Only in Month 4) -->
            <div v-if="month === 4" class="p-6 border-b-2 border-gray-200">
                <h3 class="text-lg font-medium mb-4">Teaching Philosophy</h3>
                <div class="mb-4">
                    <form
                        @submit.prevent="handlePhilosophySubmit"
                        v-if="month === 4"
                        class="space-y-4"
                        disabled
                    >
                        <div>
                            <label
                                class="block text-sm font-medium text-gray-700"
                                >Upload Teaching Philosophy</label
                            >
                            <div class="mt-1 flex items-center">
                                <input
                                    type="file"
                                    @change="handlePhilosophyChange"
                                    accept="
                        application/pdf
                    "
                                    class="py-3 px-3 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 outline outline-1 rounded hover:file:bg-blue-100"
                                />
                            </div>
                        </div>

                        <!-- Philosophy File Preview -->
                        <div
                            v-if="philosophyFile"
                            class="mt-4 flex items-center justify-between bg-gray-50 p-3 rounded-md"
                        >
                            <div class="flex items-center">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    class="h-6 w-6 text-gray-500 mr-3"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                                    />
                                </svg>
                                <span class="text-sm">{{
                                    philosophyFile.name
                                }}</span>
                            </div>
                            <button
                                @click="removePhilosphyFile"
                                class="text-red-500 hover:bg-red-50 p-1 rounded"
                            >
                                Remove
                            </button>
                        </div>
                        <button
                            type="submit"
                            :disabled="philosophyFile === null"
                            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-a-green hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                        >
                            Submit Philosophy
                        </button>
                    </form>
                </div>
            </div>

            <!-- CV Upload (Only in Month 4) -->
            <div v-if="month === 4" class="p-6 border-b-2 border-gray-200">
                <h3 class="text-lg font-medium mb-4">CV</h3>
                <div class="mb-4">
                    <form
                        @submit.prevent="handleCvSubmit"
                        v-if="month === 4"
                        class="space-y-4"
                    >
                        <div>
                            <label
                                class="block text-sm font-medium text-gray-700"
                                >Upload CV</label
                            >
                            <div class="mt-1 flex items-center">
                                <input
                                    type="file"
                                    @change="handleCvChange"
                                    accept="
                        application/pdf
                    "
                                    class="py-3 px-3 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 outline outline-1 rounded hover:file:bg-blue-100"
                                />
                            </div>
                        </div>

                        <!-- CV File Preview -->
                        <div
                            v-if="cvFile"
                            class="mt-4 flex items-center justify-between bg-gray-50 p-3 rounded-md"
                        >
                            <div class="flex items-center">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    class="h-6 w-6 text-gray-500 mr-3"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                                    />
                                </svg>
                                <span class="text-sm">{{ cvFile.name }}</span>
                            </div>
                            <button
                                @click="removeCvFile"
                                class="text-red-500 hover:bg-red-50 p-1 rounded"
                            >
                                Remove
                            </button>
                        </div>
                        <button
                            type="submit"
                            :disabled="cvFile === null"
                            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-a-green hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                        >
                            Submit CV
                        </button>
                    </form>
                </div>
            </div>
        </div>

        <div
            v-if="submitting"
            class="absolute inset-0 bg-black opacity-50 flex items-center justify-center rounded-lg z-20"
        >
            <BeatLoader />
        </div>
    </div>
</template>
