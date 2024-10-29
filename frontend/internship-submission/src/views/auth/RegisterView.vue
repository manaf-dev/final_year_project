<script setup>
    import { ref, reactive, computed, onMounted } from "vue";
    import { useToast } from "vue-toastification";
    import { useAuthStore } from "@/stores/auth";
    import InputField from "@/components/InputField.vue";
    import SubmitButton from "@/components/SubmitButton.vue";
    import ScaleLoader from "vue-spinner/src/ScaleLoader.vue";
    import apiClient from "@/services/api";
    import router from "@/router";

    const toast = useToast();
    const authStore = useAuthStore();
    const loading = ref(false);
    const error = ref(null);
    const formErrors = ref([]);

    const form = reactive({
        student_id: "",
        first_name: "",
        last_name: "",
        phone: "",
        email: "",
        department: "",
        password1: "",
        password2: "",
    });

    const isFieldEmpty = computed(() => {
        return (
            form.student_id &&
            form.first_name &&
            form.last_name &&
            form.phone &&
            form.email &&
            form.department &&
            form.password1 &&
            form.password2
        );
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

    const handleFormSubmit = () => {
        if (!isFieldEmpty.value) formErrors.value.push("Field cannot be empty");
        if (!isEmailValid.value) formErrors.value.push("Email is not valid.");
        if (!isPasswordValid.value)
            formErrors.value.push("Password must be at least 8 characters");
        if (!passwordsMatch.value)
            formErrors.value.push("Passwords do not match");

        if (formErrors.value.length > 0) {
            formErrors.value = [];
        } else {
            signup();
        }
    };

    const signup = async () => {
        try {
            loading.value = true;
            const newUser = {
                username: form.student_id,
                first_name: form.first_name,
                last_name: form.last_name,
                phone: form.phone,
                email: form.email,
                department: form.department,
                intern_account: true,
                password1: form.password1,
                password2: form.password2,
            };
            console.log("NEW USER:", newUser);
            await authStore.register(newUser);
        } catch (error) {
            console.log(error);
        } finally {
            loading.value = false;
        }
    };

    const departments = ref({});
    onMounted(async () => {
        try {
            const response = await apiClient.get("accounts/departments/");
            departments.value = response.data;
            console.log(departments.value);
        } catch (error) {
            console.log("Error Getting department:", error);
        }
    });
</script>

<template>
    <!-- <div class="max-w-md mx-auto mt-10">
        <h2 class="text-2xl font-bold mb-6">Signup</h2>
        <InputField
            id="student_id"
            label="Student ID"
            v-model="form.student_id"
            type="text"
        />
        <InputField
            id="first_name"
            label="First Name"
            v-model="form.first_name"
            type="text"
        />
        <InputField
            id="last_name"
            label="Last Name"
            v-model="form.last_name"
            type="text"
        />
        <InputField
            id="phone"
            label="Phone Number"
            v-model="form.phone"
            type="phone"
        />
        <InputField
            id="email"
            label="Email"
            v-model="form.email"
            type="email"
        />
        <InputField
            id="department"
            label="Department"
            v-model="form.department"
            type="text"
        />
        <InputField
            id="password"
            label="Password"
            v-model="form.password1"
            type="password"
        />
        <InputField
            id="confirm-password"
            label="Confirm Password"
            v-model="form.password2"
            type="password"
        />
        <SubmitButton label="Signup" @click="handleFormSubmit" />
        <div
            v-if="isLoading"
            class="mx-auto bg-black-500 h-fit w-fit absolute flex justify-center"
        >
            <ScaleLoader />
        </div>

        <p class="text-2xl">
            Already registered? Login
            <RouterLink to="/login">here</RouterLink>
        </p>
    </div> -->

    <div
        class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8"
    >
        <div class="max-w-md w-full space-y-8">
            <div>
                <h2
                    class="mt-6 text-center text-3xl font-extrabold text-gray-900"
                >
                    Register your Internship
                </h2>
            </div>
            <form class="mt-8 space-y-6" @submit.prevent="handleFormSubmit">
                <div class="rounded-md shadow-sm -space-y-px">
                    <div>
                        <label for="student-id" class="sr-only"
                            >Student ID</label
                        >
                        <input
                            id="student-id"
                            v-model="form.student_id"
                            type="text"
                            required
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            placeholder="Student ID"
                        />
                    </div>
                    <div>
                        <label for="first-name" class="sr-only"
                            >First Name</label
                        >
                        <input
                            id="first-name"
                            v-model="form.first_name"
                            type="text"
                            required
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            placeholder="First Name"
                        />
                    </div>
                    <div>
                        <label for="last-name" class="sr-only">Last Name</label>
                        <input
                            id="last-name"
                            v-model="form.last_name"
                            type="text"
                            required
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            placeholder="Last Name"
                        />
                    </div>
                    <div>
                        <label for="phone" class="sr-only">Phone Number</label>
                        <input
                            id="phone"
                            v-model="form.phone"
                            type="phone"
                            required
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            placeholder="Phone Number"
                        />
                    </div>
                    <div>
                        <label for="email" class="sr-only">Email address</label>
                        <input
                            id="email"
                            v-model="form.email"
                            type="email"
                            required
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            placeholder="Email address"
                        />
                    </div>
                    <div>
                        <label for="department" class="sr-only"
                            >Department</label
                        >
                        <select
                            id="department"
                            v-model="form.department"
                            required
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
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
                    <div>
                        <label for="password1" class="sr-only">Password</label>
                        <input
                            id="password1"
                            v-model="form.password1"
                            type="password"
                            required
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            placeholder="Password"
                        />
                    </div>
                    <div>
                        <label for="password2" class="sr-only"
                            >Confirm Password</label
                        >
                        <input
                            id="password2"
                            v-model="form.password2"
                            type="password"
                            required
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            placeholder="Confirm Password"
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
                        class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                        {{ loading ? "Creating account..." : "Create account" }}
                    </button>
                </div>
            </form>

            <div class="text-center">
                Already have an account?
                <router-link
                    to="/login"
                    class="font-medium text-indigo-600 hover:text-indigo-500"
                >
                    Sign in
                </router-link>
            </div>
        </div>
    </div>
</template>
