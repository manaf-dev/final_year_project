<script setup>
    import { ref, reactive } from "vue";

    const emit = defineEmits(["mentorSubmitted"]);

    const mentorData = reactive({
        name: "",
        phone: "",
        email: "",
    });

    const handleSubmit = () => {
        // console.log("Form submitted:", mentorData);
        emit("mentorSubmitted", mentorData);
    };
</script>

<template>
    <form @submit.prevent="handleSubmit">
        <!-- Mentor Details Step -->
        <div>
            <h2 class="text-2xl font-bold mb-6">Mentor Details</h2>

            <div class="space-y-4">
                <div>
                    <label class="block mb-2">Full Name</label>
                    <input
                        v-model="mentorData.name"
                        type="text"
                        class="w-full px-4 py-2 border rounded"
                        required
                    />
                </div>

                <div>
                    <label class="block mb-2">Phone Number</label>
                    <input
                        v-model="mentorData.phone"
                        type="tel"
                        class="w-full px-4 py-2 border rounded"
                        required
                    />
                </div>

                <div>
                    <label class="block mb-2">Email (optional)</label>
                    <input
                        v-model="mentorData.email"
                        type="email"
                        class="w-full px-4 py-2 border rounded"
                    />
                </div>
            </div>
        </div>

        <!-- Navigation Buttons -->
        <div class="mt-8 flex justify-between">
            <button
                type="submit"
                class="px-6 py-2 bg-green-500 text-white rounded hover:bg-green-600"
            >
                Submit
            </button>
        </div>
    </form>
</template>
