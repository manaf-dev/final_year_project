<template>
    <div class="max-w-4xl mx-auto p-6">
        <!-- Profile Header -->
        <div
            class="bg-blue-100 rounded-lg shadow-md p-6 flex items-center space-x-6"
        >
            <img
                :src="profile.avatar"
                alt="Profile Picture"
                class="w-28 h-28 rounded-full shadow-md border-2 border-blue-500"
            />
            <div>
                <h2 class="text-2xl font-bold text-gray-800">
                    {{ profile.username }}
                </h2>
                <p class="text-gray-600">{{ profile.email }}</p>
            </div>
        </div>

        <!-- Profile Form -->
        <div class="bg-white shadow-md rounded-lg mt-6 p-6">
            <h3 class="text-lg font-semibold text-gray-700 mb-4">
                Edit Profile
            </h3>
            <form @submit.prevent="updateProfile">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label
                            for="first_name"
                            class="block text-sm font-medium text-gray-700"
                            >First Name</label
                        >
                        <input
                            v-model="profile.first_name"
                            type="text"
                            id="first_name"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>
                    <div>
                        <label
                            for="last_name"
                            class="block text-sm font-medium text-gray-700"
                            >Last Name</label
                        >
                        <input
                            v-model="profile.last_name"
                            type="text"
                            id="last_name"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>
                </div>
                <div class="mt-6">
                    <label
                        for="profile_picture"
                        class="block text-sm font-medium text-gray-700"
                        >Profile Picture</label
                    >
                    <input
                        type="file"
                        id="profile_picture"
                        @change="uploadProfilePicture"
                        class="mt-1 block w-full text-gray-700 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                    />
                </div>
                <button
                    type="submit"
                    class="mt-6 w-full bg-green-500 text-white font-semibold py-2 rounded-md shadow hover:bg-green-600"
                >
                    Save Changes
                </button>
            </form>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    import axios from "axios";
    import { useAuthStore } from "@/stores/auth";

    const authStore = useAuthStore();
    // Reactive profile data
    const profile = authStore.user;

    // Default profile picture
    const defaultProfilePicture = "/default-profile.png"; // Replace with your actual default picture path

    // Fetch profile data
    const fetchProfile = async () => {
        try {
            const response = await axios.get("/api/profile/");
            profile.value = response.data;
        } catch (error) {
            console.error("Error fetching profile:", error);
        }
    };

    // Update profile
    const updateProfile = async () => {
        try {
            await axios.put("/api/profile/", profile.value);
            alert("Profile updated successfully!");
        } catch (error) {
            console.error("Error updating profile:", error);
        }
    };

    // Upload profile picture
    const uploadProfilePicture = (event) => {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append("profile_picture", file);
            axios
                .post("/api/profile/upload_picture/", formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                })
                .then((response) => {
                    profile.value.profile_picture =
                        response.data.profile_picture;
                    alert("Profile picture updated!");
                })
                .catch((error) => {
                    console.error("Error uploading profile picture:", error);
                });
        }
    };

    // Fetch profile on component mount
    onMounted(() => {
        fetchProfile();
    });
</script>

<style scoped>
    /* Add custom styles if needed */
</style>
