<script setup>
    import { ref, reactive, onMounted, computed } from "vue";
    import { useToast } from "vue-toastification";
    import { useAuthStore } from "@/stores/auth";
    import aamustedlogo from "@/assets/imgs/aamustedlogo.png";
    import router from "@/router";

    const toast = useToast();
    const authStore = useAuthStore();
    const loginForm = reactive({ username: "", password: "" });
    const loading = ref(false);

    const handleLogin = () => {
        if (loginForm.username == "") {
            toast.error("Provide Student ID");
        } else if (loginForm.password == "") {
            toast.error("Provide Password");
        } else {
            login(loginForm);
        }
    };

    const login = async (credentials) => {
        loading.value = true;
        try {
            await authStore.login(credentials);
            if (authStore.isIntern) {
                if (!authStore.user.intern_school) {
                    router.push({ name: "school" });
                } else if (!authStore.user.mentor) {
                    router.push({ name: "mentor" });
                } else {
                    router.push({ name: "intern-dashboard" });
                }
            } else {
                router.push({ name: "supervisor-dashboard" });
            }
        } catch (error) {
            console.log("Login Error:", error);
        } finally {
            loading.value = false;
        }
    };
</script>

<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-100">
        <div class="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
            <!-- Logo Section -->
            <div class="text-center mb-6">
                <img
                    :src="aamustedlogo"
                    alt="University Logo"
                    class="mx-auto w-24"
                />
                <h1 class="text-2xl font-semibold text-[#8c003b]">TIPS</h1>
                <p class="text-sm text-gray-500">
                    Login to access your account
                </p>
            </div>

            <!-- Login Form -->
            <form @submit.prevent="handleLogin">
                <div class="mb-4">
                    <label
                        for="id"
                        class="block text-sm font-medium text-gray-700"
                        >Student ID</label
                    >
                    <input
                        v-model="loginForm.username"
                        type="text"
                        id="id"
                        placeholder="Enter your student ID"
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#8c003b] focus:border-[#8c003b]"
                        required
                    />
                </div>

                <div class="mb-4">
                    <label
                        for="password"
                        class="block text-sm font-medium text-gray-700"
                        >Password</label
                    >
                    <input
                        v-model="loginForm.password"
                        type="password"
                        id="password"
                        placeholder="Enter your password"
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#8c003b] focus:border-[#8c003b]"
                        required
                    />
                </div>

                <button
                    type="submit"
                    :disabled="loading"
                    class="w-full py-2 text-white bg-[#8c003b] rounded-md hover:bg-[#70002e] transition disabled:opacity-50"
                >
                    Login
                    <i
                        v-if="loading"
                        class="pi pi-spin pi-spinner-dotted text-xl ml-4"
                    ></i>
                </button>
            </form>

            <p class="mt-4 text-center text-sm text-gray-600">
                First time here?
                <router-link
                    :to="{ name: 'register' }"
                    class="text-[#006938] hover:underline"
                    >Register</router-link
                >
            </p>
        </div>
    </div>
</template>
