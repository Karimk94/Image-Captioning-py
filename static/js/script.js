// static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('detection-form');
    const resultContainer = document.getElementById('result-container');
    const resultImage = document.getElementById('result-image');
    const errorContainer = document.getElementById('error-container');
    const errorMessage = document.getElementById('error-message');
    const submitBtn = document.querySelector('.submit-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Reset UI
        resultContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Detecting...';

        const formData = new FormData(form);

        try {
            const response = await fetch('/detect_objects', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                // Set the src to the Base64 encoded image data
                resultImage.src = `data:image/jpeg;base64,${data.image_data}`;
                resultContainer.classList.remove('hidden');
            } else {
                showError(data.error || 'An unknown error occurred.');
            }

        } catch (error) {
            showError('Failed to connect to the server. Please try again.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Detect Objects';
        }
    });

    function showError(message) {
        errorMessage.textContent = message;
        errorContainer.classList.remove('hidden');
    }
});
