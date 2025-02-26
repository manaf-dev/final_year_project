<script setup>
    import { ref } from "vue";
    import defaultProfile from "@/assets/imgs/defaultProfile.png";
    import { useAuthStore } from "@/stores/auth";
    const dropdownOpen = ref(false);

    const authStore = useAuthStore();
    const toggleDropdown = () => {
        dropdownOpen.value = !dropdownOpen.value;
    };
</script>

<template>
    <div class="relative">
        <button
            @click="toggleDropdown"
            class="relative block w-8 h-8 overflow-hidden rounded-full shadow focus:outline-none"
        >
            <img
                class="object-cover w-full h-full"
                :src="defaultProfile"
                alt="Your avatar"
            />
        </button>

        <div
            v-if="dropdownOpen"
            @click="toggleDropdown"
            class="fixed inset-0 z-10 w-full h-full"
        ></div>

        <div
            v-if="dropdownOpen"
            class="absolute right-0 z-10 w-48 mt-2 overflow-hidden bg-white rounded-md shadow-xl"
        >
            <RouterLink
                :to="{ name: 'profile' }"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-indigo-600 hover:text-white"
            >
                Profile
            </RouterLink>

            <button
                @click="authStore.logout()"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-indigo-600 hover:text-white w-full text-left"
            >
                Logout
            </button>
        </div>
    </div>
</template>
