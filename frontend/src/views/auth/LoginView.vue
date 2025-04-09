<script setup>
    import { ref, reactive, onMounted, computed } from "vue";
    import { useToast } from "vue-toastification";
    import { useAuthStore } from "@/stores/auth";
    import aamustedlogo from "@/assets/imgs/aamustedlogo.png";
    import router from "@/router";

    const toast = useToast();
    const authStore = useAuthStore();
    const username_or_email = ref("");
    const password = ref("");
    const loading = ref(false);

    const validateLogin = () => {
        if (username_or_email.value == "") {
            toast.error("Provide username or email");
            return;
        } else if (password.value == "") {
            toast.error("Provide Password");
            return;
        } else {
            const userCredentials = {};
            if (username_or_email.value.includes("@")) {
                userCredentials.email = username_or_email.value;
            } else {
                userCredentials.username = username_or_email.value;
            }
            userCredentials.password = password.value;
            login(userCredentials);
        }
    };

    const login = async (credentials) => {
        loading.value = true;
        try {
            await authStore.login(credentials);
            if (authStore.isIntern) {
                router.push({ name: "intern-dashboard" });
            } else {
                router.push({ name: "supervisor-dashboard" });
            }
        } catch (error) {
            console.log(error);
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
                <h1 class="text-2xl font-semibold text-maroon">TIPSS</h1>
                <p class="text-sm text-gray-500">
                    Login to access your account
                </p>
            </div>

            <!-- Login Form -->
            <form @submit.prevent="validateLogin">
                <div class="mb-4">
                    <label
                        for="id"
                        class="block text-sm font-medium text-gray-700"
                        >Username</label
                    >
                    <input
                        v-model="username_or_email"
                        type="text"
                        id="id"
                        placeholder="Enter your ID or email"
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-maroon focus:border-maroon"
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
                        v-model="password"
                        type="password"
                        id="password"
                        placeholder="Enter your password"
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-maroon focus:border-maroon"
                        required
                    />
                </div>

                <p class="mb-4 text-md text-gray-600">
                    Forgot password?
                    <router-link
                        :to="{ name: 'password-reset' }"
                        class="text-green hover:underline"
                        >Reset</router-link
                    >
                </p>

                <button
                    type="submit"
                    :disabled="loading"
                    class="w-full py-2 text-white bg-maroon rounded-md hover:bg-maroon transition disabled:opacity-50"
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
                    class="text-green hover:underline"
                    >Register</router-link
                >
            </p>
        </div>
    </div>
</template>
