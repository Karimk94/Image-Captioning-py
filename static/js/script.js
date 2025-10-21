document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('analysis-form');
    const resultContainer = document.getElementById('result-container');
    const resultImage = document.getElementById('result-image');
    const captionOutput = document.getElementById('caption-output');
    const tagsOutput = document.getElementById('tags-output');
    const errorContainer = document.getElementById('error-container');
    const errorMessage = document.getElementById('error-message');
    const submitBtn = document.querySelector('.submit-btn');
    const imageFileInput = document.getElementById('image_file');

    // Reset UI when a new file is selected
    imageFileInput.addEventListener('change', () => {
        resultContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Reset UI elements for new submission
        resultContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
        tagsOutput.innerHTML = ''; // Clear previous tags
        submitBtn.disabled = true;
        submitBtn.textContent = 'Analyzing...';

        const formData = new FormData(form);

        try {
            // The endpoint is defined in app.py
            const response = await fetch('/process_image', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                // Populate the results
                resultImage.src = `data:image/jpeg;base64,${data.image_data}`;
                captionOutput.textContent = data.caption;

                // Create and append tag elements
                if (data.tags && data.tags.length > 0) {
                    data.tags.forEach(tag => {
                        const tagElement = document.createElement('span');
                        tagElement.className = 'tag-item';
                        tagElement.textContent = tag;
                        tagsOutput.appendChild(tagElement);
                    });
                } else {
                    tagsOutput.innerHTML = '<p>No tags were generated.</p>';
                }

                resultContainer.classList.remove('hidden');
            } else {
                // Show error message from the server
                showError(data.error || 'An unknown error occurred.');
            }

        } catch (error) {
            console.error('Fetch error:', error);
            showError('Failed to connect to the server. Please ensure the backend is running.');
        } finally {
            // Re-enable the button
            submitBtn.disabled = false;
            submitBtn.textContent = 'Analyze Image';
        }
    });

    function showError(message) {
        errorMessage.textContent = message;
        errorContainer.classList.remove('hidden');
    }
});