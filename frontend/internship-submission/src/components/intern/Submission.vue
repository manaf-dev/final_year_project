<script setup>
    import apiClient from "@/services/api";
    import { onMounted, ref, watch } from "vue";
    import { useToast } from "vue-toastification";
    const props = defineProps({ month: Number });

    const files = ref([]);
    const toast = useToast();
    const activeTab = ref("view");
    const submissions = ref([]);
    const submission = ref({ status: "approved" });

    const get_submissions = async () => {
        try {
            const response = await apiClient(`portfolio/imgs/${props.month}/`);
            console.log(response.data);
            submissions.value = response.data;
        } catch (error) {
            console.log(error);
        }
    };

    onMounted(async () => {
        await get_submissions();
    });

    watch(activeTab, async (currentTab) => {
        if (currentTab === "view") {
            await get_submissions();
        }
    });

    const handleSubmit = async () => {
        try {
            console.log("Submitting:", files.value);
            const data = { month: "1", portfolio_imgs: files.value };
            console.log(data);
            const response = await apiClient.post("submissions/upload/", data, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            toast.success("Successful uploaded");
        } catch (error) {
            toast.error("Error uploading portfolio images");
        }
    };

    const handleFileChange = (event) => {
        files.value = event.target.files;
    };
</script>

<template>
    <div class="container mx-auto p-4 max-w-4xl">
        <!-- Tabs -->
        <div class="border-b border-gray-200">
            <nav class="flex -mb-px">
                <button
                    @click="activeTab = 'view'"
                    :class="[
                        'py-4 px-6 font-medium text-sm',
                        activeTab === 'view'
                            ? 'border-b-2 border-blue-500 text-blue-600'
                            : 'text-gray-500 hover:text-gray-700 hover:border-gray-300',
                    ]"
                >
                    View Submissions
                </button>

                <button
                    @click="activeTab = 'submit'"
                    :class="[
                        'py-4 px-6 font-medium text-sm',
                        activeTab === 'submit'
                            ? 'border-b-2 border-blue-500 text-blue-600'
                            : 'text-gray-500 hover:text-gray-700 hover:border-gray-300',
                    ]"
                >
                    Submit Work
                </button>
            </nav>
        </div>

        <!-- View Submissions -->
        <div v-if="activeTab === 'view'" class="mt-6 space-y-4">
            <div
                v-if="submissions.length >= 1"
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
                                submission.status === 'approved'
                                    ? 'bg-green-100 text-green-800'
                                    : 'bg-yellow-100 text-yellow-800',
                            ]"
                        >
                            {{ submission.status }}
                        </span>
                    </div>
                </div>

                <div class="p-6 space-y-4">
                    <div class="flex flex-col space-y-4 text-sm text-gray-500">
                        <figure
                            class="flex flex-row items-center flex-wrap gap-5"
                        >
                            <img
                                v-for="submission in submissions"
                                :key="submission.id"
                                :src="submission.image"
                                class="mr-1 h-32"
                            />
                        </figure>
                        <span class="flex items-center">
                            <span class="mr-1">Portfolio Images</span>
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

        <!-- Submit Work Form -->
        <div v-if="activeTab === 'submit'" class="mt-6">
            <div class="bg-white rounded-lg shadow">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h2 class="text-lg font-medium">Submit New Work</h2>
                </div>
                <div class="p-6">
                    <form @submit.prevent="handleSubmit" class="space-y-4">
                        <div>
                            <label
                                class="block text-sm font-medium text-gray-700"
                                >Upload File</label
                            >
                            <div class="mt-1 flex items-center">
                                <input
                                    type="file"
                                    @change="handleFileChange"
                                    :accept="
                                        month === 4
                                            ? 'image/*, application/pdf'
                                            : 'image/*'
                                    "
                                    :multiple="true"
                                    class="py-3 px-3 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 outline outline-1 rounded hover:file:bg-blue-100"
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            :disabled="files.length < 1"
                            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-a-green hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                        >
                            Submit Work
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
