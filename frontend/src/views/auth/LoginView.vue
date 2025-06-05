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
const showPassword = ref(false);

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
    <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8">
            <!-- Header Card -->
            <div class="bg-white rounded-2xl shadow-xl p-8">
                <!-- Logo and Title Section -->
                <div class="text-center mb-8">
                    <!-- <div class="mx-auto w-20 h-20 bg-gradient-to-br from-green-100 to-green-200 rounded-full flex items-center justify-center mb-4"> -->
                        <img
                            :src="aamustedlogo"
                            alt="University Logo"
                            class="mx-auto w-16"
                        />
                    <!-- </div> -->
                    <h1 class="text-2xl font-semibold text-gray-800 mb-1">TIPSS</h1>
                    <p class="text-xs text-gray-500 mb-4">Teaching Internship Portfolio Submission System</p>
                    <p class="text-gray-600">
                        Sign in to access your account
                    </p>
                </div>

                <!-- Login Form -->
                <form @submit.prevent="validateLogin" class="space-y-6">
                    <div>
                        <label
                            for="id"
                            class="block text-sm font-medium text-gray-700 mb-2"
                        >
                            ID or Email
                        </label>
                        <div class="relative">
                            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <i class="pi pi-user text-gray-400"></i>
                            </div>
                            <input
                                v-model="username_or_email"
                                type="text"
                                id="id"
                                placeholder="Enter your ID or email"
                                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
                                required
                            />
                        </div>
                    </div>

                    <div>
                        <label
                            for="password"
                            class="block text-sm font-medium text-gray-700 mb-2"
                        >
                            Password
                        </label>
                        <div class="relative">
                            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <i class="pi pi-lock text-gray-400"></i>
                            </div>
                            <input
                                v-model="password"
                                :type="showPassword ? 'text' : 'password'"
                                id="password"
                                placeholder="Enter your password"
                                class="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
                                required
                            />
                            <button
                                type="button"
                                @click="showPassword = !showPassword"
                                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 transition duration-200"
                            >
                                <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
                            </button>
                        </div>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center">
                            <input
                                id="remember-me"
                                name="remember-me"
                                type="checkbox"
                                class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                            />
                            <label for="remember-me" class="ml-2 block text-sm text-gray-700">
                                Remember me
                            </label>
                        </div>

                        <div class="text-sm">
                            <router-link
                                :to="{ name: 'password-reset' }"
                                class="text-green hover:text-[#00562e] font-medium hover:underline transition duration-200"
                            >
                                Forgot password?
                            </router-link>
                        </div>
                    </div>

                    <button
                        type="submit"
                        :disabled="loading"
                        class="w-full py-3 text-white bg-green rounded-lg hover:bg-[#00562e] transition disabled:opacity-50"
                    >
                        <span v-if="!loading" class="flex items-center justify-center">
                            <i class="pi pi-sign-in mr-2"></i>
                            Sign In
                        </span>
                        <span v-else class="flex items-center justify-center">
                            <i class="pi pi-spin pi-spinner-dotted mr-2"></i>
                            Signing In...
                        </span>
                    </button>
                </form>

                <!-- Register Link -->
                <div class="mt-6 text-center pt-6 border-t border-gray-200">
                    <p class="text-gray-600">
                        Don't have an account?
                        <router-link
                            :to="{ name: 'register' }"
                            class="text-maroon hover:underline"
                        >
                            Create one here
                        </router-link>
                    </p>
                </div>
            </div>

            <!-- Footer -->
            <div class="text-center">
                <p class="text-sm text-gray-500">
                    © 2025 AAMUSTED. All rights reserved.
                </p>
            </div>
        </div>
    </div>
</template>