<script setup>
    import router from "@/router";
    import apiClient from "@/services/api";
    import { useAuthStore } from "@/stores/auth";
    import { reactive, ref } from "vue";
    import { useToast } from "vue-toastification";

    const authStore = useAuthStore();
    const toast = useToast();
    const loading = ref(false);

    const mentorDetails = reactive({ name: "", phone: "", email: "" });

    const handleMentorDetailsSubmit = async () => {
        loading.value = true;
        try {
            const response = await apiClient.post(
                "accounts/mentor/create/",
                mentorDetails
            );
            authStore.getUserInfo();
            toast.success(response.data.details || "Mentor details added");
            router.push({ name: "intern-dashboard" });
        } catch (error) {
            console.log("creating mentor", error);
            toast.error("Error adding mentor");
        } finally {
            loading.value = false;
        }
    };
</script>

<template>
    <div class="min-h-screen bg-gray-100 py-6">
        <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-xl font-bold text-center text-maroon mb-4">
                Internship Details
            </h2>

            <form @submit.prevent="handleMentorDetailsSubmit">
                <h3 class="text-lg font-medium text-gray-700 mb-2">
                    Mentor Details
                </h3>

                <div class="mb-4">
                    <label
                        for="mentor-name"
                        class="block text-sm font-medium text-gray-700"
                        >Mentor Name</label
                    >
                    <input
                        v-model="mentorDetails.name"
                        type="text"
                        id="mentor-name"
                        placeholder="Enter mentor's name"
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-maroon focus:border-maroon"
                        required
                    />
                </div>

                <div class="mb-4">
                    <label
                        for="mentor-phone"
                        class="block text-sm font-medium text-gray-700"
                        >Mentor Phone Number</label
                    >
                    <input
                        v-model="mentorDetails.phone"
                        type="tel"
                        id="mentor-phone"
                        placeholder="Enter mentor's phone number"
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-maroon focus:border-maroon"
                        required
                    />
                </div>

                <div class="mb-4">
                    <label
                        for="mentor-email"
                        class="block text-sm font-medium text-gray-700"
                        >Mentor Email</label
                    >
                    <input
                        v-model="mentorDetails.email"
                        type="email"
                        id="mentor-email"
                        placeholder="Enter mentor's email"
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-maroon focus:border-maroon"
                        required
                    />
                </div>

                <button
                    type="submit"
                    :disabled="loading"
                    class="mt-4 w-full py-2 text-white bg-green rounded-md hover:bg-[#00562e] transition"
                >
                    Submit
                    <i
                        v-if="loading"
                        class="pi pi-spin pi-spinner-dotted text-xl ml-4"
                    ></i>
                </button>
            </form>
        </div>
    </div>
</template>
