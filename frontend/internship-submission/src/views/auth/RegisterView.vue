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
    const isLoading = ref(false);

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
    const formErrors = ref([]);

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
        console.log(form);
        console.log("empty", isFieldEmpty);
        if (!isFieldEmpty.value) formErrors.value.push("Field cannot be empty");
        if (!isEmailValid.value) formErrors.value.push("Email is not valid.");
        if (!isPasswordValid.value)
            formErrors.value.push("Password must be at least 8 characters");
        if (!passwordsMatch.value)
            formErrors.value.push("Passwords do not match");

        if (formErrors.value.length > 0) {
            console.log(formErrors.value);
            toast.error(formErrors.value[0]);
            formErrors.value = [];
        } else {
            signup();
        }
    };

    const signup = async () => {
        isLoading.value = true;
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

        await authStore.register(newUser);
        isLoading.value = false;
    };

    onMounted(() => {
        if (authStore.isAuthenticated) {
            authStore.redirect();
        }
    });
</script>

<template>
    <div class="max-w-md mx-auto mt-10">
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
        <SubmitButton label="Signup" @clicked="handleFormSubmit" />
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
    </div>
</template>
