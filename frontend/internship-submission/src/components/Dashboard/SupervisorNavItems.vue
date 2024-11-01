<script setup>
    import { ref, onMounted, computed } from "vue";

    const isDropdownOpen = ref(true);

    const toggleDropdown = () => {
        isDropdownOpen.value = !isDropdownOpen.value;
    };

    const dropdownIcon = computed(() =>
        isDropdownOpen.value ? "pi pi-chevron-up" : "pi pi-chevron-down"
    );

    onMounted(() => {
        isDropdownOpen.value = true;
    });
</script>

<template>
    <nav class="mt-10">
        <a
            class="flex items-center px-6 py-2 mt-3 text-gray-100 bg-gray-700 bg-opacity-25"
            href="#"
        >
            <span><i class="pi pi-home" style="font-size: 1rem"></i></span>
            <span class="mx-3"> Dashboard</span>
        </a>

        <div class="flex flex-col">
            <a
                class="flex items-center px-6 py-2 mt-3 text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100 cursor-pointer"
                @click="toggleDropdown"
            >
                <span
                    ><i class="pi pi-folder" style="font-size: 1rem"></i
                ></span>
                <span class="mx-3">Current Submissions</span>
                <span class="ml-auto"
                    ><i :class="dropdownIcon" style="font-size: 1rem"></i
                ></span>
            </a>
            <div v-show="isDropdownOpen" class="flex flex-col">
                <a
                    class="flex items-center px-6 py-2 ml-6 text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100"
                    href="#"
                    ><i class="pi pi-file" style="font-size: 1rem"></i>
                    <span class="mx-3">First Month</span></a
                >
                <a
                    class="flex items-center px-6 py-2 ml-6 text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100"
                    href="#"
                    ><i class="pi pi-file" style="font-size: 1rem"></i>
                    <span class="mx-3">Second Month</span></a
                >
                <a
                    class="flex items-center px-6 py-2 ml-6 text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100"
                    href="#"
                    ><i class="pi pi-file" style="font-size: 1rem"></i>
                    <span class="mx-3">Third Month</span></a
                >
                <a
                    class="flex items-center px-6 py-2 ml-6 text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100"
                    href="#"
                    ><i class="pi pi-file" style="font-size: 1rem"></i>
                    <span class="mx-3">Fourth Month</span></a
                >
            </div>
        </div>

        <a
            class="flex items-center px-6 py-2 mt-3 text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100"
            href="#"
        >
            <span><i class="pi pi-briefcase" style="font-size: 1rem"></i></span>
            <span class="mx-3">Past Submissions</span>
        </a>
    </nav>
</template>
