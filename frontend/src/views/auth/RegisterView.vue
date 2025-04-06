<script setup>
    import { ref, reactive, computed, onMounted } from "vue";
    import { useToast } from "vue-toastification";
    import { useAuthStore } from "@/stores/auth";
    import aamustedlogo from "@/assets/imgs/aamustedlogo.png";
    import apiClient from "@/services/api";
    import router from "@/router";

    const toast = useToast();
    const authStore = useAuthStore();
    const titles = ref(["mr", "mrs", "miss", "dr", "prof"]);
    const loading = ref(false);
    const departments = ref({});
    const cohorts = ref({});

    const form = reactive({
        username: "",
        title: "",
        first_name: "",
        last_name: "",
        phone: "",
        email: "",
        level: "",
        department: "",
        cohort: "",
        password1: "",
        password2: "",
        account_type: "intern",
    });

    const isEmailValid = computed(() => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(form.email);
    });

    const isPasswordValid = computed(() => {
        return form.password1.length >= 8;
    });

    const passwordsMatch = computed(() => {
        return form.password1 === form.password2;
    });

    const handleSignup = () => {
        if (!isEmailValid) {
            toast.error("Invalid email provided");
        }
        if (!isPasswordValid) {
            toast.error("Invalid email provided");
        }
        if (!passwordsMatch) {
            toast.error("Invalid email provided");
        }
        signup(form);
    };

    const signup = async (userData) => {
        loading.value = true;
        try {
            const response = await apiClient.post(
                "accounts/auth/registration/",
                userData
            );
            router.push({ name: "login" });
            toast.success(response.data.detail);
        } catch (error) {
            console.log("REG ERROR:", error);
            toast.error(
                error.response?.data?.detail ||
                    error.response?.data?.username[0] ||
                    "Registration failed"
            );
        } finally {
            loading.value = false;
        }
    };

    onMounted(async () => {
        try {
            const dep_response = await apiClient.get("accounts/departments/");
            departments.value = dep_response.data;
            const coh_response = await apiClient.get("internships/cohorts/");
            cohorts.value = coh_response.data;
            console.log("deps", departments.value, "cohots", cohorts.value);
        } catch (error) {
            console.log("Error Getting departments and cohorts:", error);
        }
    });
</script>

<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-100">
        <div class="w-full max-w-lg p-6 my-8 bg-white rounded-lg shadow-md">
            <!-- Logo Section -->
            <div class="text-center mb-6">
                <img
                    :src="aamustedlogo"
                    alt="University Logo"
                    class="mx-auto w-24"
                />
                <h1 class="text-2xl font-semibold text-green">
                    Register Your Account
                </h1>
                <p class="text-sm text-gray-500">
                    Register to start your internship journey
                </p>
            </div>

            <!-- Signup Form -->
            <form @submit.prevent="handleSignup">
                <div class="mb-4">
                    <label
                        for="id"
                        class="block text-sm font-medium text-gray-700"
                        >Student ID</label
                    >
                    <input
                        v-model="form.username"
                        type="text"
                        id="id"
                        placeholder="Enter your student ID"
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green focus:border-green"
                        required
                    />
                </div>

                <div class="mb-4">
                    <label
                        for="title"
                        class="block text-sm font-medium text-gray-700"
                        >Title</label
                    >
                    <select
                        v-model="form.title"
                        id="title"
                        required
                        class="w-full px-4 py-2 border rounded-md capitalize focus:outline-none focus:ring-2 focus:ring-green focus:border-green"
                    >
                        <option value="">Select Title</option>
                        <option
                            v-for="title in titles"
                            :key="title"
                            :value="title"
                        >
                            {{ title }}.
                        </option>
                    </select>
                </div>

                <div class="mb-4">
                    <label
                        for="fname"
                        class="block text-sm font-medium text-gray-700"
                        >First Name</label
                    >
                    <input
                        v-model="form.first_name"
                        type="text"
                        id="fname"
                        placeholder="Enter your First Name"
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green focus:border-green"
                        required
                    />
                </div>

                <div class="mb-4">
                    <label
                        for="lname"
                        class="block text-sm font-medium text-gray-700"
                        >Last Name</label
                    >
                    <input
                        v-model="form.last_name"
                        type="text"
                        id="lname"
                        placeholder="Enter your Last Name"
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green focus:border-green"
                        required
                    />
                </div>

                <div class="mb-4">
                    <label
                        for="phone"
                        class="block text-sm font-medium text-gray-700"
                        >Phone Number</label
                    >
                    <input
                        v-model="form.phone"
                        type="tel"
                        id="phone"
                        placeholder="Enter your Phone Number"
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green focus:border-green"
                        required
                    />
                </div>

                <div class="mb-4">
                    <label
                        for="email"
                        class="block text-sm font-medium text-gray-700"
                        >Email</label
                    >
                    <input
                        v-model="form.email"
                        type="email"
                        id="email"
                        placeholder="Enter your Email"
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green focus:border-green"
                        required
                    />
                </div>
                <div class="mb-4">
                    <label
                        for="level"
                        class="block text-sm font-medium text-gray-700"
                        >Level</label
                    >
                    <select
                        v-model="form.level"
                        id="level"
                        required
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green focus:border-green"
                    >
                        <option value="">Select Level</option>
                        <option value="100">100</option>
                        <option value="200">200</option>
                        <option value="300">300</option>
                        <option value="400">400</option>
                    </select>
                </div>

                <div class="mb-4">
                    <label
                        for="department"
                        class="block text-sm font-medium text-gray-700"
                        >Department</label
                    >
                    <select
                        v-model="form.department"
                        id="department"
                        required
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green focus:border-green"
                    >
                        <option value="">Select Department</option>
                        <option
                            v-for="department in departments"
                            :key="department.id"
                            :value="department.id"
                        >
                            {{ department.name }}
                        </option>
                    </select>
                </div>
                <div class="mb-4">
                    <label
                        for="cohort"
                        class="block text-sm font-medium text-gray-700"
                        >Cohort</label
                    >
                    <select
                        v-model="form.cohort"
                        id="cohort"
                        required
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green focus:border-green"
                    >
                        <option value="">Select Cohort</option>
                        <option
                            v-for="cohort in cohorts"
                            :key="cohort.id"
                            :value="cohort.id"
                        >
                            {{ cohort.year }} Internship Cohort
                        </option>
                    </select>
                </div>

                <div class="mb-4">
                    <label
                        for="password1"
                        class="block text-sm font-medium text-gray-700"
                        >New Password</label
                    >
                    <input
                        v-model="form.password1"
                        type="password"
                        id="password1"
                        placeholder="Create a new password"
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green focus:border-green"
                        required
                    />
                </div>

                <div class="mb-4">
                    <label
                        for="password2"
                        class="block text-sm font-medium text-gray-700"
                        >Confirm Password</label
                    >
                    <input
                        v-model="form.password2"
                        type="password"
                        id="password2"
                        placeholder="Confirm your password"
                        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green focus:border-green"
                        required
                    />
                </div>

                <button
                    type="submit"
                    :disabled="loading"
                    class="w-full py-2 text-white bg-green rounded-md hover:bg-[#00562e] transition disabled:opacity-50"
                >
                    Register
                    <i
                        v-if="loading"
                        class="pi pi-spin pi-spinner-dotted text-xl ml-4"
                    ></i>
                </button>
            </form>

            <p class="mt-4 text-center text-sm text-gray-600">
                Already have an account?
                <router-link
                    :to="{ name: 'login' }"
                    class="text-maroon hover:underline"
                    >Login</router-link
                >
            </p>
        </div>
    </div>
</template>
