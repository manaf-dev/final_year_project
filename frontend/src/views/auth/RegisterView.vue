<script setup>
import { ref, reactive, computed, onMounted, watch } from "vue";
import { useToast } from "vue-toastification";
import { useAuthStore } from "@/stores/auth";
import aamustedlogo from "@/assets/imgs/aamustedlogo.png";
import apiClient from "@/services/api";
import router from "@/router";

const toast = useToast();
const authStore = useAuthStore();
const titles = ref(["mr", "mrs", "miss", "dr", "prof"]);
const loading = ref(false);
const showPassword1 = ref(false);
const showPassword2 = ref(false);
const departments = ref({});


const form = reactive({
  username: "",
  email: "",
  password: "",
  title: "",
  first_name: "",
  last_name: "",
  phone: "",
  department: "",
});
const password2 = ref("");

const isEmailValid = computed(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(form.email);
});

const isPasswordValid = computed(() => {
  return form.password.length >= 8;
});

const passwordsMatch = computed(() => {
  return form.password === password2.value;
});

const handleSignup = () => {
  if (!isEmailValid.value) {
    toast.error("Invalid email provided");
    return;
  }
  if (!isPasswordValid.value) {
    toast.error("Password must be at least 8 characters long");
    return;
  }
  if (!passwordsMatch.value) {
    toast.error("Passwords do not match");
    return;
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
    // console.log("REG ERROR:", error);
    const errorMessage = error.response?.data?.detail || "Registration failed";
    toast.error(errorMessage);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  try {
    const dep_response = await apiClient.get("accounts/departments/");
    departments.value = dep_response.data;
  } catch (error) {
    console.log(error);
  }
});

const faculty = ref('Select Faculty');
watch(
    () => form.department,
    (newDepartmentId) => {
        if (!newDepartmentId) {
            faculty.value = "Select Faculty";
            return;
        }
        const selectedDepartment = Array.isArray(departments.value)
            ? departments.value.find((dep) => dep.id === newDepartmentId)
            : null;
        faculty.value = selectedDepartment?.faculty?.name || "Unknown Faculty";
    }
);
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
    <div class="container mx-auto px-4">
      <!-- Header Section -->
      <div class="text-center mb-8">
        <img
          :src="aamustedlogo"
          alt="University Logo"
          class="mx-auto w-24 mb-4"
        />
        <h1 class="text-2xl font-semibold text-gray-800 mb-2">TIPSS</h1>
        <p class="text-xs text-gray-500 mb-4">
          Teaching Internship Portfolio Submission System
        </p>
        <p class="text-gray-600 text-sm">
          Register and start managing your internship portfolio.
        </p>
      </div>

      <!-- Signup Form -->
      <div
        class="max-w-4xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden"
      >
        <!-- Registration Form -->
        <div class="p-8 lg:p-12">
          <form @submit.prevent="handleSignup" class="space-y-6">
            <!-- Personal Information Section -->
            <div>
              <h3
                class="text-xl font-semibold text-gray-800 mb-4 pb-2 border-b border-gray-200"
              >
                Personal Information
              </h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label
                    for="id"
                    class="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Student ID <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="form.username"
                    type="text"
                    id="id"
                    placeholder="Enter your student ID"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
                    required
                  />
                </div>
                <div>
                  <label
                    for="title"
                    class="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Title <span class="text-red-500">*</span>
                  </label>
                  <select
                    v-model="form.title"
                    id="title"
                    required
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg capitalize focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
                  >
                    <option value="">Select Title</option>
                    <option v-for="title in titles" :key="title" :value="title">
                      {{ title }}.
                    </option>
                  </select>
                </div>
                <div>
                  <label
                    for="fname"
                    class="block text-sm font-medium text-gray-700 mb-2"
                  >
                    First Name <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="form.first_name"
                    type="text"
                    id="fname"
                    placeholder="Enter your first name"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
                    required
                  />
                </div>
                <div>
                  <label
                    for="lname"
                    class="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Last Name <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="form.last_name"
                    type="text"
                    id="lname"
                    placeholder="Enter your last name"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
                    required
                  />
                </div>
              </div>
            </div>

            <!-- Contact Information Section -->
            <div>
              <h3
                class="text-xl font-semibold text-gray-800 mb-4 pb-2 border-b border-gray-200"
              >
                Contact Information
              </h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label
                    for="phone"
                    class="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Phone Number <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="form.phone"
                    type="tel"
                    id="phone"
                    placeholder="Enter your phone number"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
                    required
                  />
                </div>
                <div>
                  <label
                    for="email"
                    class="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Email Address <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="form.email"
                    type="email"
                    id="email"
                    placeholder="Enter your email address"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
                    :class="{ 'border-red-500': form.email && !isEmailValid }"
                    required
                  />
                  <p
                    v-if="form.email && !isEmailValid"
                    class="text-red-500 text-sm mt-1"
                  >
                    Please enter a valid email address
                  </p>
                </div>
              </div>
            </div>

            <!-- Academic Information Section -->
            <div>
              <h3
                class="text-xl font-semibold text-gray-800 mb-4 pb-2 border-b border-gray-200"
              >
                Academic Information
              </h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label
                    for="department"
                    class="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Department <span class="text-red-500">*</span>
                  </label>
                  <select
                    v-model="form.department"
                    id="department"
                    required
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
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
                  <label
                    for="faculty"
                    class="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Faculty <span class="text-red-500">*</span>
                  </label>
                  <select
                    id="faculty"
                    required
                    disabled
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
                  >
                    <option value="">{{faculty}}</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Security Section -->
            <div>
              <h3
                class="text-xl font-semibold text-gray-800 mb-4 pb-2 border-b border-gray-200"
              >
                Security
              </h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label
                    for="password1"
                    class="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Password <span class="text-red-500">*</span>
                  </label>
                  <div class="relative">
                    <input
                      v-model="form.password"
                      :type="showPassword1 ? 'text' : 'password'"
                      id="password1"
                      placeholder="Create a strong password"
                      class="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
                      :class="{
                        'border-red-500': form.password && !isPasswordValid,
                      }"
                      required
                    />
                    <button
                      type="button"
                      @click="showPassword1 = !showPassword1"
                      class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 transition duration-200"
                    >
                      <i
                        :class="showPassword1 ? 'pi pi-eye-slash' : 'pi pi-eye'"
                      ></i>
                    </button>
                  </div>
                  <p class="text-gray-500 text-xs mt-1">
                    Password must be at least 8 characters long
                  </p>
                  <p
                    v-if="form.password && !isPasswordValid"
                    class="text-red-500 text-sm mt-1"
                  >
                    Password must be at least 8 characters long
                  </p>
                </div>
                <div>
                  <label
                    for="password2"
                    class="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Confirm Password <span class="text-red-500">*</span>
                  </label>
                  <div class="relative">
                    <input
                      v-model="password2"
                      :type="showPassword2 ? 'text' : 'password'"
                      id="password2"
                      placeholder="Confirm your password"
                      class="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200"
                      :class="{
                        'border-red-500': password2 && !passwordsMatch,
                      }"
                      required
                    />
                    <button
                      type="button"
                      @click="showPassword2 = !showPassword2"
                      class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 transition duration-200"
                    >
                      <i
                        :class="showPassword2 ? 'pi pi-eye-slash' : 'pi pi-eye'"
                      ></i>
                    </button>
                  </div>
                  <p
                    v-if="password2 && !passwordsMatch"
                    class="text-red-500 text-sm mt-1"
                  >
                    Passwords do not match
                  </p>
                </div>
              </div>
            </div>

            <!-- Submit Button -->
            <div class="pt-6">
              <button
                type="submit"
                :disabled="loading"
                class="w-full py-3 text-white bg-green rounded-lg hover:bg-[#00562e] transition disabled:opacity-50"
              >
                <span v-if="!loading" class="flex items-center justify-center">
                  <i class="pi pi-user-plus mr-2"></i>
                  Create Account
                </span>
                <span v-else class="flex items-center justify-center">
                  <i class="pi pi-spin pi-spinner mr-2"></i>
                  Creating Account...
                </span>
              </button>
            </div>

            <!-- Login Link -->
            <div class="text-center pt-4 border-t border-gray-200">
              <p class="text-gray-600">
                Already have an account?
                <router-link
                  :to="{ name: 'login' }"
                  class="text-maroon hover:underline"
                >
                  Sign in here
                </router-link>
              </p>
            </div>
          </form>
        </div>
      </div>

      <!-- Footer -->
      <div class="text-center mt-8">
        <p class="text-sm text-gray-500">
          © 2025 AAMUSTED. All rights reserved.
        </p>
      </div>
    </div>
  </div>
</template>
