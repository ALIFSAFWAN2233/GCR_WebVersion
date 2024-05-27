
window.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const input = document.querySelector('input[type="file"]');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('video', input.files[0]);

        try {
            const response = await fetch('/upload_video', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Server response data:', data); // Debugging log
                if (data.success) {
                    alert('Video uploaded successfully!');
                    const queryParams = new URLSearchParams({
                        chords_data: JSON.stringify(data.chords_data)
                    });
                    console.log('Redirecting to:', `/display_result_video?${queryParams.toString()}`); // Debugging log
                    window.location.href = `/display_result_video?${queryParams.toString()}`;
                } else {
                    alert('Error: ' + data.error);
                }
            } else {
                alert('Failed to upload video.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while uploading the video.');
        }
    });
});

