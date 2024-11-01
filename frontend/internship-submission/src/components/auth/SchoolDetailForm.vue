<script setup>
    import { ref, reactive } from "vue";

    const emit = defineEmits(["schoolSubmitted"]);

    const schoolData = reactive({
        name: "",
        address: "",
        location: "",
        district: "",
        region: "",
    });

    const handleSubmit = () => {
        // console.log("School Form submitted:", schoolData);
        emit("schoolSubmitted", schoolData);
    };
</script>

<template>
    <form @submit.prevent="handleSubmit">
        <!-- School Details Step -->
        <div>
            <h2 class="text-2xl font-bold mb-6">School Details</h2>

            <div class="space-y-4">
                <div>
                    <label class="block mb-2">School Name</label>
                    <input
                        v-model="schoolData.name"
                        type="text"
                        class="w-full px-4 py-2 border rounded"
                        required
                    />
                </div>

                <div>
                    <label class="block mb-2">Address</label>
                    <input
                        v-model="schoolData.address"
                        type="text"
                        class="w-full px-4 py-2 border rounded"
                        required
                    />
                </div>

                <div>
                    <label class="block mb-2">Location</label>
                    <input
                        v-model="schoolData.location"
                        type="text"
                        class="w-full px-4 py-2 border rounded"
                        required
                    />
                </div>
                <div>
                    <label class="block mb-2">District</label>
                    <input
                        v-model="schoolData.district"
                        type="text"
                        class="w-full px-4 py-2 border rounded"
                        required
                    />
                </div>
                <div>
                    <label class="block mb-2">Region</label>
                    <select
                        v-model="schoolData.region"
                        class="w-full px-4 py-2 border rounded"
                        required
                    >
                        <option value="">Select Region</option>
                        <option value="Ashanti">Ashanti Region</option>
                        <option value="Ahafo">Ahafo Region</option>
                        <option value="Bono">Bono Region</option>
                        <option value="Bono East">Bono East Region</option>
                        <option value="Central">Central Region</option>
                        <option value="Eastern">Eastern Region</option>
                        <option value="Greater Accra">
                            Greater Accra Region
                        </option>
                        <option value="Nothern">Nothern Region</option>
                        <option value="North East">North East Region</option>
                        <option value="Oti">Oti Region</option>
                        <option value="Savannah">Savannah Region</option>
                        <option value="Upper East">Upper East Region</option>
                        <option value="Upper West">Upper West Region</option>
                        <option value="Volta">Volta Region</option>
                        <option value="Western">Western Region</option>
                        <option value="Western North">
                            Western North Region
                        </option>
                    </select>
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
