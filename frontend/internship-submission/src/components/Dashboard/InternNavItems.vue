<script setup>
    import { ref, onMounted, computed } from "vue";
    import { useRoute } from "vue-router";

    const isDropdownOpen = ref(true);

    const isActiveLink = (routePath) => {
        const route = useRoute();
        return route.path == routePath;
    };

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
        <RouterLink
            :class="[
                'flex',
                'items-center',
                'px-6',
                'py-2',
                'mt-3',
                isActiveLink('/in/dashboard')
                    ? 'text-gray-100 bg-opacity-25 bg-gray-700'
                    : 'text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
            ]"
            :to="{ name: 'intern-dashboard' }"
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
                <span class="mx-3">Submissions</span>
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
                        isActiveLink('/in/submission/1')
                            ? 'text-gray-100 bg-opacity-25 bg-gray-700'
                            : 'text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
                    ]"
                    :to="{ name: 'first-submission', params: { month: 1 } }"
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
                        isActiveLink('/in/submission/2')
                            ? 'text-gray-100 bg-opacity-25 bg-gray-700'
                            : 'text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
                    ]"
                    :to="{ name: 'first-submission', params: { month: 2 } }"
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
                        isActiveLink('/in/submission/3')
                            ? 'text-gray-100 bg-opacity-25 bg-gray-700'
                            : 'text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
                    ]"
                    :to="{ name: 'first-submission', params: { month: 3 } }"
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
                        isActiveLink('/in/submission/4')
                            ? 'text-gray-100 bg-opacity-25 bg-gray-700'
                            : 'text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
                    ]"
                    :to="{ name: 'first-submission', params: { month: 4 } }"
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
                isActiveLink('/in/portfolio')
                    ? 'text-gray-100 bg-opacity-25 bg-gray-700'
                    : 'text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
            ]"
            :to="{ name: 'intern-portfolio' }"
        >
            <span><i class="pi pi-briefcase" style="font-size: 1rem"></i></span>
            <span class="mx-3">Your Portfolio</span>
        </RouterLink>

        <RouterLink
            :class="[
                'flex',
                'items-center',
                'px-6',
                'py-2',
                'mt-3',
                isActiveLink('/in/supervisor')
                    ? 'text-gray-100 bg-opacity-25 bg-gray-700'
                    : 'text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
            ]"
            :to="{ name: 'intern-supervisor' }"
        >
            <span><i class="pi pi-user" style="font-size: 1rem"></i></span>
            <span class="mx-3">Supervisor</span>
        </RouterLink>
        <RouterLink
            :class="[
                'flex',
                'items-center',
                'px-6',
                'py-2',
                'mt-3',
                isActiveLink('/in/school')
                    ? 'text-gray-100 bg-opacity-25 bg-gray-700'
                    : 'text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
            ]"
            :to="{ name: 'intern-school' }"
        >
            <span><i class="pi pi-building" style="font-size: 1rem"></i></span>
            <span class="mx-3">School</span>
        </RouterLink>
        <!-- <RouterLink
            :class="[
                'flex',
                'items-center',
                'px-6',
                'py-2',
                'mt-3',
                isActiveLink('/in/mentor')
                    ? 'text-gray-100 bg-opacity-25 bg-gray-700'
                    : 'text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
            ]"
            :to="{ name: 'intern-mentor' }"
        >
            <span><i class="pi pi-users" style="font-size: 1rem"></i></span>
            <span class="mx-3">Mentor</span>
        </RouterLink> -->
    </nav>
</template>
