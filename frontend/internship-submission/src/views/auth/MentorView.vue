<script setup>
    import { ref, reactive } from "vue";
    import { useAuthStore } from "@/stores/auth";
    import InputField from "@/components/InputField.vue";
    import SubmitButton from "@/components/SubmitButton.vue";

    const auth = useAuthStore();

    // const emit = defineEmits(["mentorSubmitted"]);
    const mentor_form = reactive({
        name: "",
        phone: "",
    });

    const submitMentor = async () => {
        const updateData = {
            name: mentor_form.name,
            phone: mentor_form.phone,
        };

        try {
            const response = await apiClient.put(
                `accounts/auth/user/${auth.user.pk}/`,
                updateData
            );
            // emit("mentorSubmitted");
        } catch (error) {
            console.log("School update error:", error);
        }
    };
</script>

<template>
    <div class="max-w-md mx-auto mt-10">
        <h2 class="text-2xl font-bold mb-6">
            School Mentor {{ counter.doubleCount }}
        </h2>

        <InputField
            id="name"
            label="Mentor's Name"
            v-model="mentor_form.name"
            type="text"
        />
        <InputField
            id="phone"
            label="Phone Number"
            v-model="mentor_form.phone"
            type="text"
        />

        <SubmitButton label="Submit" />
    </div>
</template>
