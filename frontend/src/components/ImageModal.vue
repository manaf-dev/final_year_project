<script setup>
    import {
        Dialog,
        DialogPanel,
        TransitionChild,
        TransitionRoot,
    } from "@headlessui/vue";
    import { ref, computed, onMounted, onUnmounted, watch } from "vue";

    const props = defineProps({ 
        image: String, 
        isModalOpen: Boolean,
        images: {
            type: Array,
            default: () => []
        },
        currentIndex: {
            type: Number,
            default: 0
        }
    });
    
    const emits = defineEmits(["closeModal", "navigate"]);

    // Modal state
    const isFullscreen = ref(false);
    const zoom = ref(1);
    const isDragging = ref(false);
    const dragStart = ref({ x: 0, y: 0 });
    const imagePosition = ref({ x: 0, y: 0 });
    const imageRef = ref(null);
    const containerRef = ref(null);

    // Computed properties
    const canNavigate = computed(() => props.images && props.images.length > 1);
    const hasNext = computed(() => props.currentIndex < props.images.length - 1);
    const hasPrev = computed(() => props.currentIndex > 0);
    const currentImage = computed(() => {
        if (props.images && props.images.length > 0) {
            return props.images[props.currentIndex];
        }
        return props.image;
    });

    // Image transforms
    const imageStyle = computed(() => ({
        transform: `scale(${zoom.value}) translate(${imagePosition.value.x}px, ${imagePosition.value.y}px)`,
        cursor: zoom.value > 1 ? (isDragging.value ? 'grabbing' : 'grab') : 'zoom-in',
        transition: isDragging.value ? 'none' : 'transform 0.3s ease'
    }));
    // Methods
    const closeModal = () => {
        resetView();
        emits('closeModal');
    };

    const resetView = () => {
        zoom.value = 1;
        imagePosition.value = { x: 0, y: 0 };
        isDragging.value = false;
    };

    const zoomIn = () => {
        zoom.value = Math.min(zoom.value * 1.5, 5);
    };

    const zoomOut = () => {
        zoom.value = Math.max(zoom.value / 1.5, 0.5);
        if (zoom.value <= 1) {
            resetView();
        }
    };

    const toggleFullscreen = () => {
        if (!document.fullscreenElement) {
            containerRef.value?.requestFullscreen();
            isFullscreen.value = true;
        } else {
            document.exitFullscreen();
            isFullscreen.value = false;
        }
    };

    const navigateNext = () => {
        if (hasNext.value) {
            resetView();
            emits('navigate', props.currentIndex + 1);
        }
    };

    const navigatePrev = () => {
        if (hasPrev.value) {
            resetView();
            emits('navigate', props.currentIndex - 1);
        }
    };

    // Image drag functionality
    const startDrag = (event) => {
        if (zoom.value <= 1) return;
        isDragging.value = true;
        dragStart.value = {
            x: event.clientX - imagePosition.value.x,
            y: event.clientY - imagePosition.value.y
        };
    };

    const drag = (event) => {
        if (!isDragging.value) return;
        imagePosition.value = {
            x: event.clientX - dragStart.value.x,
            y: event.clientY - dragStart.value.y
        };
    };

    const endDrag = () => {
        isDragging.value = false;
    };

    // Image click to zoom
    const handleImageClick = (event) => {
        if (zoom.value === 1) {
            zoomIn();
            // Center zoom on click point
            const rect = imageRef.value.getBoundingClientRect();
            const x = event.clientX - rect.left - rect.width / 2;
            const y = event.clientY - rect.top - rect.height / 2;
            imagePosition.value = { x: -x * 0.5, y: -y * 0.5 };
        }
    };

    // Keyboard navigation
    const handleKeydown = (event) => {
        if (!props.isModalOpen) return;
        
        switch (event.key) {
            case 'Escape':
                closeModal();
                break;
            case 'ArrowLeft':
                navigatePrev();
                break;
            case 'ArrowRight':
                navigateNext();
                break;
            case '+':
            case '=':
                zoomIn();
                break;
            case '-':
                zoomOut();
                break;
            case '0':
                resetView();
                break;
            case 'f':
            case 'F':
                toggleFullscreen();
                break;
        }
    };

    // Wheel zoom
    const handleWheel = (event) => {
        event.preventDefault();
        if (event.deltaY < 0) {
            zoomIn();
        } else {
            zoomOut();
        }
    };

    // Lifecycle
    onMounted(() => {
        document.addEventListener('keydown', handleKeydown);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', endDrag);
        document.addEventListener('fullscreenchange', () => {
            isFullscreen.value = !!document.fullscreenElement;
        });
    });

    onUnmounted(() => {
        document.removeEventListener('keydown', handleKeydown);
        document.removeEventListener('mousemove', drag);
        document.removeEventListener('mouseup', endDrag);
    });

    // Reset view when image changes
    watch(() => props.currentIndex, () => {
        resetView();
    });

    watch(() => props.isModalOpen, (newVal) => {
        if (!newVal) {
            resetView();
        }
    });
</script>

<template>
    <!-- Enhanced Image Modal -->
    <TransitionRoot appear :show="props.isModalOpen" as="template">
        <Dialog as="div" @close="closeModal" class="relative z-50">
            <!-- Enhanced Backdrop -->
            <TransitionChild
                as="template"
                enter="ease-out duration-300"
                enter-from="opacity-0"
                enter-to="opacity-100"
                leave="ease-in duration-200"
                leave-from="opacity-100"
                leave-to="opacity-0"
            >
                <div class="fixed inset-0 bg-black/90 backdrop-blur-sm" />
            </TransitionChild>

            <!-- Modal Content -->
            <div 
                ref="containerRef"
                class="fixed inset-0 overflow-hidden"
                :class="{ 'bg-black': isFullscreen }"
            >
                <div class="flex min-h-full items-center justify-center">
                    <TransitionChild
                        as="template"
                        enter="ease-out duration-300"
                        enter-from="opacity-0 scale-95"
                        enter-to="opacity-100 scale-100"
                        leave="ease-in duration-200"
                        leave-from="opacity-100 scale-100"
                        leave-to="opacity-0 scale-95"
                    >
                        <DialogPanel
                            class="relative w-full h-full max-w-7xl transform text-left align-middle transition-all flex flex-col"
                            :class="isFullscreen ? 'max-w-none' : 'max-h-[90vh] m-4'"
                        >
                            <!-- Header Controls -->
                            <div 
                                class="absolute top-0 left-0 right-0 z-20 flex items-center justify-between p-4 bg-gradient-to-b from-black/50 to-transparent"
                                :class="{ 'opacity-0 hover:opacity-100 transition-opacity duration-300': isFullscreen }"
                            >
                                <!-- Left Controls -->
                                <div class="flex items-center space-x-4">
                                    <!-- Image Counter -->
                                    <div v-if="canNavigate" class="text-white text-sm bg-black/30 px-3 py-1 rounded-full backdrop-blur-sm">
                                        {{ props.currentIndex + 1 }} / {{ props.images.length }}
                                    </div>
                                    
                                    <!-- Zoom Level -->
                                    <div class="text-white text-sm bg-black/30 px-3 py-1 rounded-full backdrop-blur-sm">
                                        {{ Math.round(zoom * 100) }}%
                                    </div>
                                </div>

                                <!-- Right Controls -->
                                <div class="flex items-center space-x-2">
                                    <!-- Zoom Controls -->
                                    <button
                                        @click="zoomOut"
                                        class="p-2 text-white hover:bg-white/20 rounded-full transition-colors"
                                        title="Zoom Out (-)"
                                    >
                                        <i class="pi pi-minus text-lg"></i>
                                    </button>
                                    
                                    <button
                                        @click="resetView"
                                        class="p-2 text-white hover:bg-white/20 rounded-full transition-colors"
                                        title="Reset View (0)"
                                    >
                                        <i class="pi pi-refresh text-lg"></i>
                                    </button>
                                    
                                    <button
                                        @click="zoomIn"
                                        class="p-2 text-white hover:bg-white/20 rounded-full transition-colors"
                                        title="Zoom In (+)"
                                    >
                                        <i class="pi pi-plus text-lg"></i>
                                    </button>

                                    <!-- Fullscreen Toggle -->
                                    <button
                                        @click="toggleFullscreen"
                                        class="p-2 text-white hover:bg-white/20 rounded-full transition-colors ml-2"
                                        title="Toggle Fullscreen (F)"
                                    >
                                        <i :class="isFullscreen ? 'pi pi-window-minimize' : 'pi pi-window-maximize'" class="text-lg"></i>
                                    </button>

                                    <!-- Close Button -->
                                    <button
                                        @click="closeModal"
                                        class="p-2 text-white hover:bg-white/20 rounded-full transition-colors ml-2"
                                        title="Close (Esc)"
                                    >
                                        <i class="pi pi-times text-lg"></i>
                                    </button>
                                </div>
                            </div>

                            <!-- Navigation Arrows -->
                            <template v-if="canNavigate">
                                <!-- Previous Button -->
                                <button
                                    v-if="hasPrev"
                                    @click="navigatePrev"
                                    class="absolute left-4 top-1/2 transform -translate-y-1/2 z-20 p-3 text-white bg-black/30 hover:bg-black/50 rounded-full transition-all backdrop-blur-sm"
                                    :class="{ 'opacity-0 hover:opacity-100': isFullscreen }"
                                    title="Previous Image (←)"
                                >
                                    <i class="pi pi-chevron-left text-xl"></i>
                                </button>

                                <!-- Next Button -->
                                <button
                                    v-if="hasNext"
                                    @click="navigateNext"
                                    class="absolute right-4 top-1/2 transform -translate-y-1/2 z-20 p-3 text-white bg-black/30 hover:bg-black/50 rounded-full transition-all backdrop-blur-sm"
                                    :class="{ 'opacity-0 hover:opacity-100': isFullscreen }"
                                    title="Next Image (→)"
                                >
                                    <i class="pi pi-chevron-right text-xl"></i>
                                </button>
                            </template>

                            <!-- Image Container -->
                            <div 
                                class="flex-1 flex items-center justify-center overflow-hidden"
                                @wheel="handleWheel"
                            >
                                <div class="relative w-full h-full flex items-center justify-center">
                                    <img
                                        ref="imageRef"
                                        :src="currentImage"
                                        alt="Portfolio Image"
                                        class="max-w-full max-h-full object-contain select-none"
                                        :style="imageStyle"
                                        @mousedown="startDrag"
                                        @click="handleImageClick"
                                        @dragstart.prevent
                                        loading="lazy"
                                    />
                                </div>
                            </div>

                            <!-- Bottom Controls -->
                            <div 
                                class="absolute bottom-0 left-0 right-0 z-20 p-4 bg-gradient-to-t from-black/50 to-transparent"
                                :class="{ 'opacity-0 hover:opacity-100 transition-opacity duration-300': isFullscreen }"
                            >
                                <!-- Thumbnail Navigation -->
                                <div v-if="canNavigate && props.images.length > 1" class="flex items-center justify-center space-x-2 mb-4">
                                    <div class="flex items-center space-x-1 bg-black/30 rounded-lg p-2 backdrop-blur-sm max-w-md overflow-x-auto">
                                        <button
                                            v-for="(img, index) in props.images.slice(Math.max(0, props.currentIndex - 3), props.currentIndex + 4)"
                                            :key="index + Math.max(0, props.currentIndex - 3)"
                                            @click="emits('navigate', index + Math.max(0, props.currentIndex - 3))"
                                            class="flex-shrink-0 w-12 h-12 rounded overflow-hidden border-2 transition-all"
                                            :class="(index + Math.max(0, props.currentIndex - 3)) === props.currentIndex 
                                                ? 'border-white shadow-lg' 
                                                : 'border-transparent opacity-60 hover:opacity-100'"
                                        >
                                            <img 
                                                :src="img" 
                                                :alt="`Thumbnail ${index + 1}`"
                                                class="w-full h-full object-cover"
                                            />
                                        </button>
                                    </div>
                                </div>

                                <!-- Keyboard Shortcuts Help -->
                                <div class="text-center">
                                    <div class="inline-flex items-center space-x-4 text-white/70 text-xs bg-black/20 px-4 py-2 rounded-full backdrop-blur-sm">
                                        <span>← → Navigate</span>
                                        <span>+ - Zoom</span>
                                        <span>F Fullscreen</span>
                                        <span>0 Reset</span>
                                        <span>Esc Close</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Loading Overlay -->
                            <div v-if="!currentImage" class="absolute inset-0 flex items-center justify-center bg-black/50">
                                <div class="flex items-center space-x-3 text-white">
                                    <i class="pi pi-spinner pi-spin text-2xl"></i>
                                    <span class="text-lg">Loading image...</span>
                                </div>
                            </div>
                        </DialogPanel>
                    </TransitionChild>
                </div>
            </div>
        </Dialog>
    </TransitionRoot>
</template>
