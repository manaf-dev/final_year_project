<script setup>
    import FileUpload from "primevue/fileupload";
    import { useToast } from "vue-toastification";

    const toast = useToast();

    const onAdvancedUpload = () => {
        toast.success("File Uploaded");
    };
    const onError = () => {
        toast.error("File Upload failed");
    };
</script>

<template>
    <div class="card">
        <FileUpload
            name="demo[]"
            url="/api/upload"
            @error="onError"
            @upload="onAdvancedUpload()"
            :multiple="true"
            accept="image/*"
            :maxFileSize="1000000"
        >
            <template #empty>
                <span>Drag and drop files to here to upload.</span>
            </template>
        </FileUpload>
    </div>
</template>
