<script setup>
import { ref, computed, watch } from "vue";
import { useToast } from "vue-toastification";
import apiClient from "@/services/api";

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  month: {
    type: String,
    required: true,
  },
});

const emit = defineEmits(["close", "submitted"]);

const toast = useToast();

// Modal state
const selectedType = ref("images");
const submitting = ref(false);

// File states
const selectedImages = ref([]);
const imagePreviews = ref([]);
const philosophyFile = ref([]);
const cvFile = ref([]);
const reflectiveFile = ref([]);
const videoUrl = ref("");

// Computed properties
const canSubmit = computed(() => {
  switch (selectedType.value) {
    case "images":
      return selectedImages.value.length > 0;
    case "philosophy":
      return philosophyFile.value.length > 0;
    case "cv":
      return cvFile.value.length > 0;
    case "reflective":
      return reflectiveFile.value.length > 0;
    case "video":
      return videoUrl.value.trim().length > 0;
    default:
      return false;
  }
});

// Image handling
const handleImageChange = (event) => {
  const files = Array.from(event.target.files);

  files.forEach((file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreviews.value.push(e.target.result);
    };
    reader.readAsDataURL(file);
    selectedImages.value.push(file);
  });
};

const removeImage = (index) => {
  imagePreviews.value.splice(index, 1);
  selectedImages.value.splice(index, 1);
};

// Philosophy file handling
const handlePhilosophyChange = (e) => {
  const file = e.target.files[0];
  if (file) {
    philosophyFile.value = [file];
  }
};

const removePhilosophyFile = () => {
  philosophyFile.value = [];
};

// CV file handling
const handleCvChange = (e) => {
  const file = e.target.files[0];
  if (file) {
    cvFile.value = [file];
  }
};

const removeCvFile = () => {
  cvFile.value = [];
};

// Reflective file handling
const handleReflectiveChange = (e) => {
  const file = e.target.files[0];
  if (file) {
    reflectiveFile.value = [file];
  }
};

const removeReflectiveFile = () => {
  reflectiveFile.value = [];
};

// Modal methods
const closeModal = () => {
  if (!submitting.value) {
    resetForm();
    emit("close");
  }
};

const resetForm = () => {
  selectedType.value = "images";
  selectedImages.value = [];
  imagePreviews.value = [];
  philosophyFile.value = [];
  cvFile.value = [];
  reflectiveFile.value = [];
  videoUrl.value = "";
};

// Submission methods
const handleSubmit = async () => {
  try {
    switch (selectedType.value) {
      case "images":
        await handleImageSubmit();
        break;
      case "philosophy":
        await handlePhilosophySubmit();
        break;
      case "cv":
        await handleCvSubmit();
        break;
      case "reflective":
        await handleReflectiveSubmit();
        break;
      case "video":
        await handleVideoSubmit();
        break;
    }
  } catch (error) {
    console.error("Submission error:", error);
  }
};

const handleFileSubmit = async (endpoint, files) => {
  const formData = new FormData();
  formData.append("month", props.month);
  files.forEach((file) => {
    formData.append("file", file);
  });

  submitting.value = true;
  try {
    const response = await apiClient.post(endpoint, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    toast.success(response.data.detail);
    emit("submitted");
    closeModal();
  } catch (error) {
    toast.error(error.response?.data?.detail || "Error uploading file");
  } finally {
    submitting.value = false;
  }
};

const handleImageSubmit = async () => {
  await handleFileSubmit("submissions/upload/img/", selectedImages.value);
};

const handlePhilosophySubmit = async () => {
  await handleFileSubmit(
    "submissions/upload/philosophy/",
    philosophyFile.value
  );
};

const handleCvSubmit = async () => {
  await handleFileSubmit("submissions/upload/cv/", cvFile.value);
};

const handleReflectiveSubmit = async () => {
  await handleFileSubmit(
    "submissions/upload/reflective/",
    reflectiveFile.value
  );
};

const handleVideoSubmit = async () => {
  if (!videoUrl.value) {
    toast.error("Please enter a valid video URL");
    return;
  }

  submitting.value = true;
  try {
    const response = await apiClient.post("submissions/submit/video/", {
      month: props.month,
      video_url: videoUrl.value,
    });

    toast.success(response.data.detail);
    emit("submitted");
    closeModal();
  } catch (error) {
    toast.error(error.response?.data?.detail || "Error uploading video URL");
  } finally {
    submitting.value = false;
  }
};

// Reset form when modal opens
watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal) {
      resetForm();
    }
  }
);
</script>


<template>
  <teleport to="body">
    <div
      v-if="isOpen"
      class="fixed inset-0 z-50 overflow-y-auto"
      @click.self="closeModal"
    >
      <!-- Backdrop -->
      <div
        class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity"
      ></div>

      <!-- Modal -->
      <div class="flex min-h-full items-center justify-center p-4">
        <div
          class="w-full max-w-2xl transform rounded-xl bg-white shadow-2xl transition-all"
          @click.stop
        >
          <!-- Header -->
          <div
            class="flex items-center justify-between border-b border-gray-200 px-6 py-4"
          >
            <h2 class="text-xl font-semibold text-gray-900">
              Submit Portfolio - Month {{ month }}
            </h2>
            <button
              @click="closeModal"
              class="rounded-lg p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors"
            >
              <i class="pi pi-times text-lg"></i>
            </button>
          </div>

          <!-- Content -->
          <div class="px-6 py-4 space-y-6">
            <!-- Submission Type Selector -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-3">
                What would you like to submit?
              </label>
              <div class="grid grid-cols-1 gap-3">
                <!-- Portfolio Images -->
                <div
                  @click="selectedType = 'images'"
                  :class="[
                    'relative cursor-pointer rounded-lg border-2 p-4 transition-all',
                    selectedType === 'images'
                      ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                      : 'border-gray-200 hover:border-gray-300',
                  ]"
                >
                  <div class="flex items-center space-x-3">
                    <div class="flex-shrink-0">
                      <i class="pi pi-images text-2xl text-blue-600"></i>
                    </div>
                    <div class="flex-1">
                      <h3 class="text-sm font-medium text-gray-900">
                        Portfolio Images
                      </h3>
                      <p class="text-sm text-gray-500">
                        Upload images showcasing your work
                      </p>
                    </div>
                    <div v-if="selectedType === 'images'" class="flex-shrink-0">
                      <i class="pi pi-check-circle text-blue-600"></i>
                    </div>
                  </div>
                </div>

                <!-- Month 4 Options -->
                <template v-if="month === '4'">
                  <!-- Teaching Philosophy -->
                  <div
                    @click="selectedType = 'philosophy'"
                    :class="[
                      'relative cursor-pointer rounded-lg border-2 p-4 transition-all',
                      selectedType === 'philosophy'
                        ? 'border-green-500 bg-green-50 ring-2 ring-green-200'
                        : 'border-gray-200 hover:border-gray-300',
                    ]"
                  >
                    <div class="flex items-center space-x-3">
                      <div class="flex-shrink-0">
                        <i class="pi pi-file-edit text-2xl text-green-600"></i>
                      </div>
                      <div class="flex-1">
                        <h3 class="text-sm font-medium text-gray-900">
                          Teaching Philosophy
                        </h3>
                        <p class="text-sm text-gray-500">
                          Upload your teaching philosophy document
                        </p>
                      </div>
                      <div
                        v-if="selectedType === 'philosophy'"
                        class="flex-shrink-0"
                      >
                        <i class="pi pi-check-circle text-green-600"></i>
                      </div>
                    </div>
                  </div>

                  <!-- CV -->
                  <div
                    @click="selectedType = 'cv'"
                    :class="[
                      'relative cursor-pointer rounded-lg border-2 p-4 transition-all',
                      selectedType === 'cv'
                        ? 'border-yellow-500 bg-yellow-50 ring-2 ring-yellow-200'
                        : 'border-gray-200 hover:border-gray-300',
                    ]"
                  >
                    <div class="flex items-center space-x-3">
                      <div class="flex-shrink-0">
                        <i class="pi pi-file-pdf text-2xl text-yellow-600"></i>
                      </div>
                      <div class="flex-1">
                        <h3 class="text-sm font-medium text-gray-900">
                          Curriculum Vitae (CV)
                        </h3>
                        <p class="text-sm text-gray-500">
                          Upload your updated CV in PDF format
                        </p>
                      </div>
                      <div v-if="selectedType === 'cv'" class="flex-shrink-0">
                        <i class="pi pi-check-circle text-yellow-600"></i>
                      </div>
                    </div>
                  </div>

                  <!-- Reflective Teaching Document -->
                  <div
                    @click="selectedType = 'reflective'"
                    :class="[
                      'relative cursor-pointer rounded-lg border-2 p-4 transition-all',
                      selectedType === 'reflective'
                        ? 'border-orange-500 bg-orange-50 ring-2 ring-orange-200'
                        : 'border-gray-200 hover:border-gray-300',
                    ]"
                  >
                    <div class="flex items-center space-x-3">
                      <div class="flex-shrink-0">
                        <i class="pi pi-file-word text-2xl text-orange-600"></i>
                      </div>
                      <div class="flex-1">
                        <h3 class="text-sm font-medium text-gray-900">
                          Reflective Teaching
                        </h3>
                        <p class="text-sm text-gray-500">
                          Upload your reflective teaching document
                        </p>
                      </div>
                      <div
                        v-if="selectedType === 'reflective'"
                        class="flex-shrink-0"
                      >
                        <i class="pi pi-check-circle text-orange-600"></i>
                      </div>
                    </div>
                  </div>

                  <!-- Teaching Video URL -->
                  <div
                    @click="selectedType = 'video'"
                    :class="[
                      'relative cursor-pointer rounded-lg border-2 p-4 transition-all',
                      selectedType === 'video'
                        ? 'border-purple-500 bg-purple-50 ring-2 ring-purple-200'
                        : 'border-gray-200 hover:border-gray-300',
                    ]"
                  >
                    <div class="flex items-center space-x-3">
                      <div class="flex-shrink-0">
                        <i class="pi pi-video text-2xl text-purple-600"></i>
                      </div>
                      <div class="flex-1">
                        <h3 class="text-sm font-medium text-gray-900">
                          Teaching Video
                        </h3>
                        <p class="text-sm text-gray-500">
                          Submit a video URL from YouTube or other platform
                        </p>
                      </div>
                      <div
                        v-if="selectedType === 'video'"
                        class="flex-shrink-0"
                      >
                        <i class="pi pi-check-circle text-purple-600"></i>
                      </div>
                    </div>
                  </div>
                </template>
              </div>
            </div>

            <!-- Dynamic Upload Section -->
            <div v-if="selectedType" class="border-t pt-6">
              <!-- Portfolio Images Upload -->
              <div v-if="selectedType === 'images'" class="space-y-4">
                <div class="flex items-center justify-between">
                  <h3 class="text-lg font-medium text-gray-900">
                    Upload Portfolio Images
                  </h3>
                  <span class="text-sm text-gray-500"
                    >Multiple files allowed</span
                  >
                </div>

                <div class="mt-4">
                  <div
                    class="relative border-2 border-dashed border-gray-300 rounded-lg p-6 hover:border-gray-400 transition-colors"
                  >
                    <input
                      type="file"
                      @change="handleImageChange"
                      accept="image/*"
                      multiple
                      class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />
                    <div class="text-center">
                      <i
                        class="pi pi-cloud-upload text-3xl text-gray-400 mb-3"
                      ></i>
                      <p class="text-sm text-gray-600">
                        <span class="font-medium text-blue-600"
                          >Click to upload</span
                        >
                        or drag and drop
                      </p>
                      <p class="text-xs text-gray-500 mt-1">
                        PNG, JPG, GIF up to 10MB each
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Image Previews -->
                <div
                  v-if="imagePreviews.length"
                  class="grid grid-cols-2 md:grid-cols-3 gap-4 mt-4"
                >
                  <div
                    v-for="(preview, index) in imagePreviews"
                    :key="index"
                    class="relative group aspect-square rounded-lg overflow-hidden bg-gray-100"
                  >
                    <img
                      :src="preview"
                      :alt="`Preview ${index + 1}`"
                      class="w-full h-full object-cover"
                    />
                    <button
                      @click="removeImage(index)"
                      class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <i class="pi pi-times text-xs"></i>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Teaching Philosophy Upload -->
              <div v-if="selectedType === 'philosophy'" class="space-y-4">
                <div class="flex items-center justify-between">
                  <h3 class="text-lg font-medium text-gray-900">
                    Upload Teaching Philosophy
                  </h3>
                  <span class="text-sm text-gray-500">PDF, DOC, DOCX</span>
                </div>

                <div class="mt-4">
                  <div
                    class="relative border-2 border-dashed border-gray-300 rounded-lg p-6 hover:border-gray-400 transition-colors"
                  >
                    <input
                      type="file"
                      @change="handlePhilosophyChange"
                      accept=".pdf,.doc,.docx"
                      class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />
                    <div class="text-center">
                      <i
                        class="pi pi-file-edit text-3xl text-green-400 mb-3"
                      ></i>
                      <p class="text-sm text-gray-600">
                        <span class="font-medium text-green-600"
                          >Click to upload</span
                        >
                        your teaching philosophy
                      </p>
                      <p class="text-xs text-gray-500 mt-1">
                        PDF, DOC, DOCX up to 10MB
                      </p>
                    </div>
                  </div>
                </div>

                <!-- File Preview -->
                <div
                  v-if="philosophyFile.length"
                  class="bg-green-50 border border-green-200 rounded-lg p-4"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-3">
                      <i class="pi pi-file-edit text-2xl text-green-600"></i>
                      <span class="text-sm font-medium text-gray-900">
                        {{ philosophyFile[0].name }}
                      </span>
                    </div>
                    <button
                      @click="removePhilosophyFile"
                      class="text-red-500 hover:text-red-700 transition-colors"
                    >
                      <i class="pi pi-times"></i>
                    </button>
                  </div>
                </div>
              </div>

              <!-- CV Upload -->
              <div v-if="selectedType === 'cv'" class="space-y-4">
                <div class="flex items-center justify-between">
                  <h3 class="text-lg font-medium text-gray-900">Upload CV</h3>
                  <span class="text-sm text-gray-500">PDF only</span>
                </div>

                <div class="mt-4">
                  <div
                    class="relative border-2 border-dashed border-gray-300 rounded-lg p-6 hover:border-gray-400 transition-colors"
                  >
                    <input
                      type="file"
                      @change="handleCvChange"
                      accept="application/pdf"
                      class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />
                    <div class="text-center">
                      <i
                        class="pi pi-file-pdf text-3xl text-yellow-400 mb-3"
                      ></i>
                      <p class="text-sm text-gray-600">
                        <span class="font-medium text-yellow-600"
                          >Click to upload</span
                        >
                        your CV
                      </p>
                      <p class="text-xs text-gray-500 mt-1">PDF up to 10MB</p>
                    </div>
                  </div>
                </div>

                <!-- File Preview -->
                <div
                  v-if="cvFile.length"
                  class="bg-yellow-50 border border-yellow-200 rounded-lg p-4"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-3">
                      <i class="pi pi-file-pdf text-2xl text-yellow-600"></i>
                      <span class="text-sm font-medium text-gray-900">
                        {{ cvFile[0].name }}
                      </span>
                    </div>
                    <button
                      @click="removeCvFile"
                      class="text-red-500 hover:text-red-700 transition-colors"
                    >
                      <i class="pi pi-times"></i>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Reflective Teaching Document Upload -->
              <div v-if="selectedType === 'reflective'" class="space-y-4">
                <div class="flex items-center justify-between">
                  <h3 class="text-lg font-medium text-gray-900">
                    Upload Reflective Teaching Document
                  </h3>
                  <span class="text-sm text-gray-500">PDF, DOC, DOCX</span>
                </div>

                <div class="mt-4">
                  <div
                    class="relative border-2 border-dashed border-gray-300 rounded-lg p-6 hover:border-gray-400 transition-colors"
                  >
                    <input
                      type="file"
                      @change="handleReflectiveChange"
                      accept=".pdf,.doc,.docx"
                      class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />
                    <div class="text-center">
                      <i
                        class="pi pi-file-word text-3xl text-orange-400 mb-3"
                      ></i>
                      <p class="text-sm text-gray-600">
                        <span class="font-medium text-orange-600"
                          >Click to upload</span
                        >
                        your reflective teaching document
                      </p>
                      <p class="text-xs text-gray-500 mt-1">
                        PDF, DOC, DOCX up to 10MB
                      </p>
                    </div>
                  </div>
                </div>

                <!-- File Preview -->
                <div
                  v-if="reflectiveFile.length"
                  class="bg-orange-50 border border-orange-200 rounded-lg p-4"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-3">
                      <i class="pi pi-file-word text-2xl text-orange-600"></i>
                      <span class="text-sm font-medium text-gray-900">
                        {{ reflectiveFile[0].name }}
                      </span>
                    </div>
                    <button
                      @click="removeReflectiveFile"
                      class="text-red-500 hover:text-red-700 transition-colors"
                    >
                      <i class="pi pi-times"></i>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Teaching Video URL -->
              <div v-if="selectedType === 'video'" class="space-y-4">
                <div class="flex items-center justify-between">
                  <h3 class="text-lg font-medium text-gray-900">
                    Submit Teaching Video URL
                  </h3>
                  <span class="text-sm text-gray-500"
                    >YouTube, Vimeo, etc.</span
                  >
                </div>

                <div class="mt-4">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Video URL
                  </label>
                  <input
                    type="url"
                    v-model="videoUrl"
                    placeholder="https://www.youtube.com/watch?v=..."
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors"
                  />
                  <p class="text-xs text-gray-500 mt-2">
                    Please upload your video to YouTube or any video hosting
                    platform and paste the link here.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div
            class="flex items-center justify-end space-x-3 border-t border-gray-200 px-6 py-4"
          >
            <button
              @click="closeModal"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              @click="handleSubmit"
              :disabled="!canSubmit || submitting"
              :class="[
                'px-6 py-2 text-sm font-medium text-white rounded-lg transition-all',
                canSubmit && !submitting
                  ? 'bg-blue-600 hover:bg-blue-700'
                  : 'bg-gray-400 cursor-not-allowed',
              ]"
            >
              <span v-if="submitting" class="flex items-center space-x-2">
                <i class="pi pi-spinner pi-spin"></i>
                <span>Submitting...</span>
              </span>
              <span v-else>Submit</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Loading Overlay -->
      <div
        v-if="submitting"
        class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-60"
      >
        <div class="bg-white rounded-lg p-6 shadow-xl">
          <div class="flex items-center space-x-3">
            <i class="pi pi-spinner pi-spin text-2xl text-blue-600"></i>
            <span class="text-lg font-medium text-gray-900"
              >Uploading your submission...</span
            >
          </div>
        </div>
      </div>
    </div>
  </teleport>
</template>

