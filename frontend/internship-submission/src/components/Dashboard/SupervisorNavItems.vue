<script setup>
    import { ref, onMounted, computed } from "vue";
    import { useRoute } from "vue-router";

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

    const isActiveLink = (routePath) => {
        const route = useRoute();
        return route.path == routePath;
    };
</script>

<template>
    <nav class="mt-10">
        <RouterLink
            :class="[
                'flex',
                'items-center',
                'px-6',
                'py-2',
                'mt-3',
                isActiveLink('/sp/dashboard')
                    ? 'text-gray-100 bg-opacity-25 bg-gray-700'
                    : 'text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
            ]"
            :to="{ name: 'supervisor-dashboard' }"
        >
            <span><i class="pi pi-home" style="font-size: 1rem"></i></span>
            <span class="mx-3"> Dashboard</span>
        </RouterLink>

        <div class="flex flex-col">
            <button
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
            </button>
            <div v-show="isDropdownOpen" class="flex flex-col">
                <RouterLink
                    :class="[
                        'flex',
                        'items-center',
                        'px-6',
                        'py-2',

                        'ml-6',
                        isActiveLink('/sp/submissions/1')
                            ? 'text-gray-100 bg-opacity-25 bg-gray-700'
                            : 'text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
                    ]"
                    :to="'/sp/submissions/1'"
                    ><i class="pi pi-file" style="font-size: 1rem"></i>
                    <span class="mx-3">First Month</span>
                </RouterLink>
                <RouterLink
                    :class="[
                        'flex',
                        'items-center',
                        'px-6',
                        'py-2',

                        'ml-6',
                        isActiveLink('/sp/submissions/2')
                            ? 'text-gray-100 bg-opacity-25 bg-gray-700'
                            : 'text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
                    ]"
                    :to="'/sp/submissions/2'"
                    ><i class="pi pi-file" style="font-size: 1rem"></i>
                    <span class="mx-3">Second Month</span></RouterLink
                >
                <RouterLink
                    :class="[
                        'flex',
                        'items-center',
                        'px-6',
                        'py-2',

                        'ml-6',
                        isActiveLink('/sp/submissions/3')
                            ? 'text-gray-100 bg-opacity-25 bg-gray-700'
                            : 'text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
                    ]"
                    :to="'/sp/submissions/3'"
                    ><i class="pi pi-file" style="font-size: 1rem"></i>
                    <span class="mx-3">Third Month</span></RouterLink
                >
                <RouterLink
                    :class="[
                        'flex',
                        'items-center',
                        'px-6',
                        'py-2',

                        'ml-6',
                        isActiveLink('/sp/submissions/4')
                            ? 'text-gray-100 bg-opacity-25 bg-gray-700'
                            : 'text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
                    ]"
                    :to="'/sp/submissions/4'"
                    ><i class="pi pi-file" style="font-size: 1rem"></i>
                    <span class="mx-3">Fourth Month</span></RouterLink
                >
            </div>
        </div>

        <RouterLink
            :class="[
                'flex',
                'items-center',
                'px-6',
                'py-2',
                'mt-3',
                isActiveLink('/sp/submissions/past')
                    ? 'text-gray-100 bg-opacity-25 bg-gray-700'
                    : 'text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
            ]"
            :to="{ name: 'past-submissions' }"
        >
            <span><i class="pi pi-briefcase" style="font-size: 1rem"></i></span>
            <span class="mx-3">Past Submissions</span>
        </RouterLink>
    </nav>
</template>
