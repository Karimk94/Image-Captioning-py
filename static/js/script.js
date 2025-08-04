// static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('caption-form');
    const resultContainer = document.getElementById('result-container');
    const captionOutput = document.getElementById('caption-output');
    const imagePreview = document.getElementById('image-preview');
    const imagePreviewContainer = document.getElementById('image-preview-container');
    const errorContainer = document.getElementById('error-container');
    const errorMessage = document.getElementById('error-message');
    const submitBtn = document.querySelector('.submit-btn');
    const fileInput = document.getElementById('image_file');
    const urlInput = document.getElementById('image_url');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Reset UI
        resultContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
        captionOutput.innerHTML = '<p>Loading...</p>';
        submitBtn.disabled = true;
        submitBtn.textContent = 'Generating...';

        const formData = new FormData(form);

        // Show preview
        let previewSrc = '#';
        if (fileInput.files[0]) {
            previewSrc = URL.createObjectURL(fileInput.files[0]);
        } else if (urlInput.value) {
            previewSrc = urlInput.value;
        }
        
        if (previewSrc !== '#') {
            imagePreview.src = previewSrc;
            resultContainer.classList.remove('hidden');
        }


        try {
            const response = await fetch('/generate_caption', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                captionOutput.innerHTML = `<p>${data.caption}</p>`;
            } else {
                showError(data.error || 'An unknown error occurred.');
                resultContainer.classList.add('hidden');
            }

        } catch (error) {
            showError('Failed to connect to the server. Please try again.');
            resultContainer.classList.add('hidden');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Generate Caption';
            // Clear the other input field to avoid confusion
            fileInput.addEventListener('change', () => urlInput.value = '');
            urlInput.addEventListener('input', () => fileInput.value = '');
        }
    });

    function showError(message) {
        errorMessage.textContent = message;
        errorContainer.classList.remove('hidden');
    }
});
