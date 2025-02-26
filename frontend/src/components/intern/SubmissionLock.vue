<script setup>
    import { ref } from "vue";
    import { useAuthStore } from "@/stores/auth";
    import router from "@/router";

    const authStore = useAuthStore();

    const nextMonth = new Date();
    nextMonth.setMonth(nextMonth.getMonth() + 1);
    const nextSubmissionMonth = ref(
        nextMonth.toLocaleString("default", { month: "long" })
    );

    const goBack = () => {
        if (authStore.isIntern) {
            router.push({ name: "intern-dashboard" });
        } else {
            router.push({ name: "supervisor-dashboard" });
        }
    };
</script>

<template>
    <div class="bg-gray-100 min-h-screen flex items-center justify-center">
        <div class="bg-white shadow-lg rounded-lg p-8 max-w-lg text-center">
            <!-- Icon -->
            <div class="text-[#8c003b] mb-4">
                <i class="pi pi-clock text-6xl"></i>
            </div>

            <!-- Message -->
            <h1 class="text-2xl font-bold text-[#8c003b]">
                Submission Not Open Yet
            </h1>
            <p class="text-gray-600 mt-4">
                Submissions are not yet open for this month. The designated
                submission window will be available starting
                <span class="font-semibold text-[#006938]">{{
                    nextSubmissionMonth
                }}</span
                >.
            </p>

            <!-- Additional Information -->
            <div class="mt-6 bg-gray-50 p-4 rounded-md border border-gray-200">
                <p class="text-gray-700">
                    Keep preparing your portfolio and ensure all required files
                    are ready for upload when submissions open.
                </p>
            </div>

            <!-- Back to Dashboard Button -->
            <button
                @click="goBack"
                class="mt-6 bg-[#ffc712] hover:bg-[#ffd83e] text-black font-medium py-2 px-4 rounded-lg shadow flex items-center justify-center"
            >
                <i class="pi pi-arrow-left mr-2"></i> Back to Dashboard
            </button>
        </div>
    </div>
</template>
