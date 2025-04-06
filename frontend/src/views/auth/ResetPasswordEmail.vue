<script setup>
    import { ref } from "vue";
    import { useToast } from "vue-toastification";
    import apiClient from "@/services/api";
    import router from "@/router";

    const toast = useToast();

    const email = ref("");
    const loading = ref(false);

    const handleResetRequest = async () => {
        if (!email.value) {
            toast.error("Email is required.");
            return;
        }

        loading.value = true;

        try {
            const response = await apiClient.post("accounts/password/reset/", {
                email: email.value,
            });
            console.log(response);
            toast.success(response.data.detail);
            router.push({ name: "email-sent" });
        } catch (error) {
            toast.error("An error occurred. Please try again later.");
            console.error("Error sending reset email:", error);
        } finally {
            loading.value = false;
        }
    };
</script>

<template>
    <div class="bg-gray-100 min-h-screen flex items-center justify-center px-4">
        <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-2xl font-semibold text-gray-800 text-center mb-4">
                Reset Password
            </h2>
            <p class="text-sm text-gray-500 text-center mb-6">
                Enter your email address, and we’ll send you instructions to
                reset your password.
            </p>
            <form @submit.prevent="handleResetRequest" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700"
                        >Email Address</label
                    >
                    <input
                        type="email"
                        v-model="email"
                        required
                        class="mt-1 py-2 px-4 w-full border rounded-md shadow-sm text-gray-700 focus:ring-[#006938] focus:border-[#006938]"
                        placeholder="example@example.com"
                    />
                </div>
                <button
                    type="submit"
                    :disabled="loading"
                    class="w-full bg-[#8c003b] hover:bg-[#a00449] text-white font-medium py-2 px-4 rounded-md shadow transition disabled:opacity-50"
                >
                    Send Reset Link
                    <i
                        v-if="loading"
                        class="pi pi-spin pi-spinner-dotted text-xl ml-4"
                    ></i>
                </button>
            </form>
        </div>
    </div>
</template>
