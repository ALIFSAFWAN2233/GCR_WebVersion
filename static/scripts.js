
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
                    //query string need to be changed cause of the length limitation of GET
                    //need to use POST method
                    
                    //const queryParams = new URLSearchParams({
                    //    chords_data: JSON.stringify(data.chords_data)
                    //});

                    // Send chords data to /display_result_video using POST request
                    const displayResponse = await fetch('/display_result_video', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ chords_data: data.chords_data })
                    });

                    const displayHtml = await displayResponse.text();

                    // Replace the current document with the new HTML content
                    document.open();
                    document.write(displayHtml);
                    document.close();
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

