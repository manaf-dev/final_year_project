<script setup>
    import { ref, reactive, onMounted, computed } from "vue";
    import { useToast } from "vue-toastification";
    import { useAuthStore } from "@/stores/auth";
    import { LockClosedIcon } from "@heroicons/vue/24/solid";
    import InputField from "@/components/InputField.vue";
    import SubmitButton from "@/components/SubmitButton.vue";
    import router from "@/router";

    const toast = useToast();
    const authStore = useAuthStore();
    const loginForm = reactive({ username: "", password: "" });
    const loading = ref(false);
    const error = ref();

    const handleLogin = () => {
        if (loginForm.username == "" || loginForm.password == "") {
            error.value.push("Provide Student ID and Password");
        } else {
            const credentials = {
                username: loginForm.username,
                password: loginForm.password,
            };
            login(credentials);
        }
    };

    const login = async (credentials) => {
        loading.value = true;
        await authStore.login(credentials);
        loading.value = false;
    };
</script>

<template>
    <div
        class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8"
    >
        <div class="max-w-md w-full space-y-8">
            <div>
                <h2
                    class="mt-6 text-center text-3xl font-extrabold text-gray-900"
                >
                    Sign in to your account
                </h2>
            </div>
            <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
                <div class="rounded-md shadow-sm -space-y-px">
                    <div>
                        <label for="username" class="sr-only">Username</label>
                        <input
                            id="username"
                            v-model="loginForm.username"
                            type="text"
                            required
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            placeholder="Enter student or staff ID"
                        />
                    </div>
                    <div>
                        <label for="password" class="sr-only">Password</label>
                        <input
                            id="password"
                            v-model="loginForm.password"
                            type="password"
                            required
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            placeholder="Password"
                        />
                    </div>
                </div>

                <div v-if="error" class="text-red-500 text-sm text-center">
                    {{ error }}
                </div>

                <div>
                    <button
                        type="submit"
                        :disabled="loading"
                        class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                    >
                        <span
                            class="absolute left-0 inset-y-0 flex items-center pl-3"
                        >
                            <LockClosedIcon
                                class="h-5 w-5 text-green-500 group-hover:text-green-400"
                            />
                        </span>
                        {{ loading ? "Signing in..." : "Sign in" }}
                    </button>
                </div>
            </form>

            <div class="text-center">
                Don't have an account?
                <router-link
                    to="/register"
                    class="font-medium text-green-600 hover:text-green-500"
                >
                    Sign up
                </router-link>
            </div>
        </div>
    </div>
</template>
