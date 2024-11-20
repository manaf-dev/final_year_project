<script setup>
    import apiClient from "@/services/api";
    import { ref, onMounted } from "vue";
    import { useToast } from "vue-toastification";

    const props = defineProps({ month: Number });
    const toast = useToast();

    const activeTab = ref("view");
    const submissions = ref({});
    const portfolioImgs = ref([]);
    const philosophyFile = ref(null);
    const cvFile = ref(null);
    const loading = ref(false);

    const getSubmissions = async () => {
        try {
            const response = await apiClient(`portfolio/${props.month}/`);
            submissions.value = response.data;
        } catch (error) {
            console.error(error);
        }
    };

    onMounted(getSubmissions);

    // File handling for different types
    const handlePortfolioChange = (e) => {
        portfolioImgs.value = e.target.files;
    };
    const handlePhilosophyChange = (e) => {
        philosophyFile.value = e.target.files[0];
    };
    const handleCvChange = (e) => {
        cvFile.value = e.target.files[0];
    };

    // File submission functions
    const handleSubmit = async (endpoint, files) => {
        const formData = new FormData();
        formData.append("month", props.month);
        files.forEach((file) => {
            formData.append("files", file);
        });

        loading.value = true;
        try {
            const response = await apiClient.post(endpoint, formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            toast.success(response.data.detail);
            activeTab.value = "view";
        } catch (error) {
            toast.error(error.response?.data?.detail || "Error uploading file");
        } finally {
            loading.value = false;
        }
    };

    const handlePortfolioSubmit = () =>
        handleSubmit(
            "submissions/upload/img/",
            Array.from(portfolioImgs.value)
        );
    const handlePhilosophySubmit = () =>
        handleSubmit("submissions/upload/philosophy/", [philosophyFile.value]);
    const handleCvSubmit = () =>
        handleSubmit("submissions/upload/cv/", [cvFile.value]);
</script>

<template>
    <div class="container mx-auto p-4 max-w-4xl">
        <div class="border-b border-gray-200">
            <nav class="flex -mb-px">
                <button
                    @click="activeTab = 'view'"
                    :class="[
                        'py-4 px-6',
                        activeTab === 'view'
                            ? 'border-b-2 text-blue-600'
                            : 'text-gray-500',
                    ]"
                >
                    View Submissions
                </button>
                <button
                    @click="activeTab = 'submit'"
                    :class="[
                        'py-4 px-6',
                        activeTab === 'submit'
                            ? 'border-b-2 text-blue-600'
                            : 'text-gray-500',
                    ]"
                >
                    Submit Work
                </button>
            </nav>
        </div>

        <div v-if="activeTab === 'view'" class="mt-6 space-y-4">
            <div
                v-if="submissions.images?.length > 0"
                class="bg-white rounded-lg shadow"
            >
                <div class="px-6 py-4 border-b border-gray-200">
                    <div class="flex items-center justify-between">
                        <h3 class="text-lg font-medium">
                            Portfolio For The Month
                        </h3>
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

                <div class="p-6 space-y-4">
                    <div class="flex flex-col space-y-4 text-sm text-gray-500">
                        <figure
                            class="flex flex-row items-center flex-wrap gap-5"
                        >
                            <img
                                v-for="submission in submissions.images"
                                :key="submission.id"
                                :src="submission.image"
                                class="mr-1 h-32"
                            />
                        </figure>
                        <span class="flex items-center">
                            <span class="mr-1">Portfolio Images</span>
                        </span>
                    </div>
                    <div class="flex flex-col space-y-4 text-sm text-gray-500">
                        <div class="flex flex-col">
                            <a
                                v-for="submission in submissions.files"
                                :key="submission.id"
                                :href="`http://localhost:8000/${submission.file}`"
                                target="_blank"
                                rel="noopener noreferrer"
                                >{{ submission.file_type }}</a
                            >
                        </div>
                        <span class="flex items-center">
                            <span class="mr-1">Portfolio Files</span>
                        </span>
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
                </div>
            </div>
            <div v-else class="bg-white rounded-lg shadow">
                <div class="px-6 py-6">
                    <div class="flex items-center justify-between">
                        <h3 class="text-lg font-medium">
                            You have not made any submission yet.
                            <button
                                class="px-2 py-1 ml-5 bg-a-green text-white rounded"
                                @click="activeTab = 'submit'"
                            >
                                Submit here
                            </button>
                        </h3>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="activeTab === 'submit'" class="mt-6">
            <div class="bg-white rounded-lg shadow">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h2 class="text-lg font-medium">Submit New Work</h2>
                </div>
                <div class="p-6">
                    <form
                        @submit.prevent="handlePortfolioSubmit"
                        class="space-y-4"
                    >
                        <div>
                            <label
                                class="block text-sm font-medium text-gray-700"
                                >Upload Portfolio Images</label
                            >
                            <div class="mt-1 flex items-center">
                                <input
                                    type="file"
                                    @change="handlePortfolioChange"
                                    accept="
                                        image/*
                                    "
                                    :multiple="true"
                                    class="py-3 px-3 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 outline outline-1 rounded hover:file:bg-blue-100"
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            :disabled="portfolioImgs.length < 1"
                            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-a-green hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                        >
                            {{
                                loading
                                    ? "Submitting Portfolio... "
                                    : "Submit Portfolio"
                            }}
                        </button>
                    </form>

                    <div class="flex gap-8 mt-6">
                        <form
                            v-if="month === 4"
                            @submit.prevent="handlePhilosophySubmit"
                            class="space-y-4"
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

                            <button
                                type="submit"
                                :disabled="philosophyFile === null"
                                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-a-green hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                            >
                                {{
                                    loading
                                        ? "Submitting Philosophy... "
                                        : "Submit Philosophy"
                                }}
                            </button>
                        </form>
                        <form
                            v-if="month === 4"
                            @submit.prevent="handleCvSubmit"
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

                            <button
                                type="submit"
                                :disabled="cvFile === null"
                                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-a-green hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                            >
                                {{
                                    loading ? "Submitting CV... " : "Submit CV"
                                }}
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
