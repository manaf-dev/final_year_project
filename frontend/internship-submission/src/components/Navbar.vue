<!-- <template>
    <aside
        :class="is_expanded ? 'w-64' : 'w-16'"
        class="flex flex-col bg-gray-800 text-white min-h-screen transition-all duration-200"
    >
        <div class="logo mb-4">
            <img :src="logoURL" alt="Vue" class="w-8" />
        </div>

        <div
            class="menu-toggle-wrap flex justify-end mb-4 relative transition-all duration-200"
        >
            <button class="menu-toggle" @click="ToggleMenu">
                <span
                    class="material-icons text-2xl text-white transition-all duration-200 hover:text-blue-500 hover:transform hover:translate-x-2"
                    >keyboard_double_arrow_right</span
                >
            </button>
        </div>

        <h3
            class="text-gray-400 text-sm mb-2 uppercase transition-opacity duration-300"
            :class="is_expanded ? 'opacity-100' : 'opacity-0'"
        >
            Menu
        </h3>
        <div class="menu space-y-2">
            <router-link
                to="/"
                class="button flex items-center p-2 transition-all duration-200 hover:bg-gray-700"
                active-class="bg-gray-700 border-r-4 border-blue-500"
            >
                <span class="material-icons text-2xl">home</span>
                <span
                    class="text ml-4 transition-opacity duration-300"
                    :class="is_expanded ? 'opacity-100' : 'opacity-0'"
                    >Home</span
                >
            </router-link>
            <router-link
                to="/about"
                class="button flex items-center p-2 transition-all duration-200 hover:bg-gray-700"
                active-class="bg-gray-700 border-r-4 border-blue-500"
            >
                <span class="material-icons text-2xl">description</span>
                <span
                    class="text ml-4 transition-opacity duration-300"
                    :class="is_expanded ? 'opacity-100' : 'opacity-0'"
                    >About</span
                >
            </router-link>
            <router-link
                to="/team"
                class="button flex items-center p-2 transition-all duration-200 hover:bg-gray-700"
                active-class="bg-gray-700 border-r-4 border-blue-500"
            >
                <span class="material-icons text-2xl">group</span>
                <span
                    class="text ml-4 transition-opacity duration-300"
                    :class="is_expanded ? 'opacity-100' : 'opacity-0'"
                    >Team</span
                >
            </router-link>
            <router-link
                to="/contact"
                class="button flex items-center p-2 transition-all duration-200 hover:bg-gray-700"
                active-class="bg-gray-700 border-r-4 border-blue-500"
            >
                <span class="material-icons text-2xl">email</span>
                <span
                    class="text ml-4 transition-opacity duration-300"
                    :class="is_expanded ? 'opacity-100' : 'opacity-0'"
                    >Contact</span
                >
            </router-link>
        </div>

        <div class="flex-1"></div>

        <div class="menu space-y-2">
            <router-link
                to="/settings"
                class="button flex items-center p-2 transition-all duration-200 hover:bg-gray-700"
                active-class="bg-gray-700 border-r-4 border-blue-500"
            >
                <span class="material-icons text-2xl">settings</span>
                <span
                    class="text ml-4 transition-opacity duration-300"
                    :class="is_expanded ? 'opacity-100' : 'opacity-0'"
                    >Settings</span
                >
            </router-link>
        </div>
    </aside>
</template> -->
