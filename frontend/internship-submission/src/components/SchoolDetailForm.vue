<script setup>
    import { ref, reactive } from "vue";

    const emit = defineEmits(["formSubmitted"]);

    const currentStep = ref(1);

    const formData = reactive({
        school: {
            name: "",
            address: "",
            phone: "",
            email: "",
        },
        mentor: {
            name: "",
            subject: "",
            experience: "",
            email: "",
        },
    });

    const nextStep = () => {
        if (currentStep.value < 2) {
            currentStep.value++;
        }
    };

    const previousStep = () => {
        if (currentStep.value > 1) {
            currentStep.value--;
        }
    };

    const handleSubmit = () => {
        console.log("Form submitted:", formData);
        emit("formSubmitted", formData);
    };
</script>

<template>
    <div class="max-w-2xl mx-auto p-6">
        <!-- Form Progress -->
        <div class="mb-8">
            <div class="flex justify-between">
                <span
                    :class="[
                        'px-4 py-2 rounded-lg',
                        currentStep === 1
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-200',
                    ]"
                >
                    School Details
                </span>
                <span
                    :class="[
                        'px-4 py-2 rounded-lg',
                        currentStep === 2
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-200',
                    ]"
                >
                    Mentor Details
                </span>
            </div>
        </div>

        <form @submit.prevent="handleSubmit">
            <!-- School Details Step -->
            <div v-if="currentStep === 1">
                <h2 class="text-2xl font-bold mb-6">School Details</h2>

                <div class="space-y-4">
                    <div>
                        <label class="block mb-2">School Name</label>
                        <input
                            v-model="formData.school.name"
                            type="text"
                            class="w-full px-4 py-2 border rounded"
                            required
                        />
                    </div>

                    <div>
                        <label class="block mb-2">Address</label>
                        <input
                            v-model="formData.school.address"
                            type="text"
                            class="w-full px-4 py-2 border rounded"
                            required
                        />
                    </div>

                    <div>
                        <label class="block mb-2">Contact Number</label>
                        <input
                            v-model="formData.school.phone"
                            type="tel"
                            class="w-full px-4 py-2 border rounded"
                            required
                        />
                    </div>

                    <div>
                        <label class="block mb-2">Email</label>
                        <input
                            v-model="formData.school.email"
                            type="email"
                            class="w-full px-4 py-2 border rounded"
                            required
                        />
                    </div>
                </div>
            </div>

            <!-- Mentor Details Step -->
            <div v-if="currentStep === 2">
                <h2 class="text-2xl font-bold mb-6">Mentor Details</h2>

                <div class="space-y-4">
                    <div>
                        <label class="block mb-2">Full Name</label>
                        <input
                            v-model="formData.mentor.name"
                            type="text"
                            class="w-full px-4 py-2 border rounded"
                            required
                        />
                    </div>

                    <div>
                        <label class="block mb-2">Subject Specialization</label>
                        <input
                            v-model="formData.mentor.subject"
                            type="text"
                            class="w-full px-4 py-2 border rounded"
                            required
                        />
                    </div>

                    <div>
                        <label class="block mb-2">Years of Experience</label>
                        <input
                            v-model="formData.mentor.experience"
                            type="number"
                            class="w-full px-4 py-2 border rounded"
                            required
                        />
                    </div>

                    <div>
                        <label class="block mb-2">Contact Email</label>
                        <input
                            v-model="formData.mentor.email"
                            type="email"
                            class="w-full px-4 py-2 border rounded"
                            required
                        />
                    </div>
                </div>
            </div>

            <!-- Navigation Buttons -->
            <div class="mt-8 flex justify-between">
                <button
                    v-if="currentStep > 1"
                    type="button"
                    @click="previousStep"
                    class="px-6 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
                >
                    Back
                </button>
                <button
                    v-if="currentStep < 2"
                    type="button"
                    @click="nextStep"
                    class="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                    Next
                </button>
                <button
                    v-if="currentStep === 2"
                    type="submit"
                    class="px-6 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                >
                    Submit
                </button>
            </div>
        </form>
    </div>
</template>
