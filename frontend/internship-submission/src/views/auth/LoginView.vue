<script setup>
    import { ref, reactive, onMounted } from "vue";
    import { useToast } from "vue-toastification";
    import { useAuthStore } from "@/stores/auth";
    import InputField from "@/components/InputField.vue";
    import SubmitButton from "@/components/SubmitButton.vue";
    import router from "@/router";

    const toast = useToast();
    const authStore = useAuthStore();
    const loginForm = reactive({ username: "", password: "" });

    const handleLogin = () => {
        if (loginForm.username == "" || loginForm.password == "") {
            toast.error("Provide Student ID and Password");
        } else {
            const credentials = {
                username: loginForm.username,
                password: loginForm.password,
            };
            login(credentials);
        }
    };

    const login = async (credentials) => {
        const status = await authStore.login(credentials);
    };

    // const redirect = () => {
    //     if (authStore.isAuthenticated && authStore.accessToken) {
    //         if (authStore.user.intern_account) {
    //             if (authStore.user.intern_school) {
    //                 router.push("/dashboard");
    //             } else {
    //                 router.push("/school");
    //             }
    //         } else {
    //             router.push("/dashboard");
    //         }
    //     } else router.push("/login");
    // };

    onMounted(() => {
        authStore.redirect();
    });
</script>

<template>
    <div class="max-w-md mx-auto mt-10">
        <h2 class="text-2xl font-bold mb-6">Login</h2>
        <InputField
            id="username"
            label="Student ID"
            v-model="loginForm.username"
            type="text"
        />
        <InputField
            id="password"
            label="Password"
            v-model="loginForm.password"
            type="password"
        />
        <SubmitButton label="Login" @click="handleLogin" />
    </div>
</template>
