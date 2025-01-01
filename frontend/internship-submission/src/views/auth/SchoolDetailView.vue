<script setup>
    import router from "@/router";
    import apiClient from "@/services/api";
    import { useAuthStore } from "@/stores/auth";
    import { data } from "autoprefixer";
    import { ref, computed, onMounted, reactive } from "vue";
    import { useToast } from "vue-toastification";

    const loading = ref(false);
    const authStore = useAuthStore();
    const toast = useToast();

    const selectedSchool = ref({});
    const schoolDetails = reactive({
        school: "",
        location: "",
        district: "",
        region: "",
    });
    const isCustomSchool = ref(false);
    const dropdownActive = ref(false);
    const schools = ref([]);

    const get_schools = async () => {
        try {
            const response = await apiClient.get(
                "accounts/intern-schools/all/"
            );
            schools.value = response.data;
            console.log(schools.value);
        } catch (error) {
            console.log("Error fetching schools", error);
        }
    };

    onMounted(get_schools);

    const filteredSchools = computed(() => {
        if (!schoolDetails.school) return schools.value; // Show all schools if no search query
        return schools.value.filter((school) =>
            school.school
                .toLowerCase()
                .includes(schoolDetails.school.toLowerCase())
        );
    });

    const selectSchool = (school) => {
        selectedSchool.value = school;
        schoolDetails.school = school.school;
        schoolDetails.location = school.location;
        schoolDetails.district = school.district;
        schoolDetails.region = school.region;
        isCustomSchool.value = false;
        dropdownActive.value = false;
        console.log("school", schoolDetails);
    };

    const handleSchoolDetailsSubmit = async () => {
        loading.value = true;
        try {
            let response;
            if (isCustomSchool.value) {
                response = await apiClient.post(
                    `accounts/intern-school/create/`,
                    schoolDetails
                );
            } else {
                response = await apiClient.put(
                    `accounts/user/${authStore.user.id}/update-school/`,
                    selectedSchool.value
                );
            }
            console.log(response.data);
            authStore.getUserInfo();
            toast.success(response.data.detail || "School details added");
            router.push("/mentor");
        } catch (error) {
            console.log("error", error);
            toast.error(error.response.data.detail || "Error adding school");
        } finally {
            loading.value = false;
        }
    };

    // Dropdown handling for blur
    const handleBlur = () => {
        setTimeout(() => (dropdownActive.value = false), 200); // Delay to allow selection
    };
</script>

<template>
    <div class="min-h-screen bg-gray-100 py-6">
        <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-xl font-bold text-center text-maroon mb-4">
                Internship Details
            </h2>

            <form @submit.prevent="handleSchoolDetailsSubmit">
                <h3 class="text-lg font-medium text-gray-700 mb-2">
                    School Details
                </h3>

                <!-- School Dropdown -->
                <div class="mb-4 relative">
                    <label
                        for="school"
                        class="block text-sm font-medium text-gray-700"
                        >School</label
                    >
                    <div class="relative">
                        <input
                            v-model="schoolDetails.school"
                            @focus="dropdownActive = true"
                            @blur="handleBlur"
                            type="text"
                            id="school"
                            autocomplete="off"
                            placeholder="Search for a school..."
                            class="w-full px-4 py-2 capitalize border rounded-md focus:outline-none focus:ring-2 focus:ring-maroon focus:border-[#8c003b]"
                        />
                        <ul
                            v-show="dropdownActive"
                            class="absolute z-10 w-full bg-white border rounded-md mt-1 max-h-40 overflow-y-auto shadow-lg"
                        >
                            <li
                                v-for="school in filteredSchools"
                                :key="school.id"
                                @mousedown="selectSchool(school)"
                                class="px-4 py-2 hover:bg-gray-100 cursor-pointer capitalize"
                            >
                                {{ school.school }}
                            </li>
                        </ul>
                    </div>
                </div>

                <!-- Location, District, Region -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        <label
                            for="location"
                            class="block text-sm font-medium text-gray-700"
                            >Location</label
                        >
                        <input
                            v-model="schoolDetails.location"
                            type="text"
                            id="location"
                            class="w-full px-4 py-2 capitalize border rounded-md focus:outline-none focus:ring-2 focus:ring-maroon focus:border-[#8c003b]"
                            :readonly="!isCustomSchool"
                            required
                        />
                    </div>

                    <div>
                        <label
                            for="district"
                            class="block text-sm font-medium text-gray-700"
                            >District</label
                        >
                        <input
                            v-model="schoolDetails.district"
                            type="text"
                            id="district"
                            class="w-full px-4 py-2 capitalize border rounded-md focus:outline-none focus:ring-2 focus:ring-maroon focus:border-[#8c003b]"
                            :readonly="!isCustomSchool"
                            required
                        />
                    </div>

                    <div>
                        <label
                            for="region"
                            class="block text-sm font-medium text-gray-700"
                            >Region</label
                        >
                        <input
                            v-model="schoolDetails.region"
                            type="text"
                            id="region"
                            class="w-full px-4 py-2 capitalize border rounded-md focus:outline-none focus:ring-2 focus:ring-maroon focus:border-[#8c003b]"
                            :readonly="!isCustomSchool"
                            required
                        />
                    </div>
                </div>

                <!-- Custom School Checkbox -->
                <div class="mt-4">
                    <label class="flex items-center space-x-2">
                        <input
                            type="checkbox"
                            v-model="isCustomSchool"
                            class="text-[#8c003b]"
                        />
                        <span class="text-sm text-gray-700"
                            >School not listed? Enter manually</span
                        >
                    </label>
                </div>

                <!-- Submit Button -->
                <button
                    type="submit"
                    :disabled="loading"
                    class="mt-4 w-full py-2 text-white bg-maroon rounded-md hover:bg-[#70002e] transition"
                >
                    Submit
                    <i
                        v-if="loading"
                        class="pi pi-spin pi-spinner-dotted text-xl ml-4"
                    ></i>
                </button>
            </form>
        </div>
    </div>
</template>
