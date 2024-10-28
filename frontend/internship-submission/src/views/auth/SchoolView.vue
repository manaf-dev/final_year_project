<script setup>
    import { ref, reactive } from "vue";
    import { useAuthStore } from "@/stores/auth";
    import InputField from "@/components/InputField.vue";
    import SubmitButton from "@/components/SubmitButton.vue";
    import apiClient from "@/services/api";
    import router from "@/router";

    const auth = useAuthStore();
    const emit = defineEmits(["goNext"]);

    const school_form = reactive({
        region: "",
        district: "",
        school: "",
        location: "",
    });

    const submitSchool = async () => {
        const updateData = {
            region: school_form.region,
            district: school_form.district,
            school: school_form.school,
            location: school_form.location,
        };

        try {
            const response = await apiClient.put(
                `accounts/auth/user/${auth.user.pk}/`,
                updateData
            );
            emit("goNext");
        } catch (error) {
            console.log("School update error:", error);
        }
        // console.log("school", school_form);
        // user.user_data["school"] = {
        //     region: school_form.region,
        //     district: school_form.district,
        //     school: school_form.school,
        //     location: school_form.location,
        // };
        // console.log(user.user_data);
        // console.log(
        //     "school:",
        //     school_form.region,
        //     school_form.district,
        //     school_form.school,
        //     school_form.location
        // );
        // }
    };
</script>

<template>
    <div class="max-w-md mx-auto mt-10">
        <h2 class="text-2xl font-bold mb-6">Internship School Information</h2>

        <InputField
            id="region"
            label="Region"
            v-model="school_form.region"
            type="text"
        />
        <InputField
            id="district"
            label="district"
            v-model="school_form.district"
            type="text"
        />
        <InputField
            id="school"
            label="school"
            v-model="school_form.school"
            type="text"
        />
        <InputField
            id="location"
            label="Location"
            v-model="school_form.location"
            type="text"
        />
        <SubmitButton label="Next" @clicked="submitSchool" />
    </div>
</template>
