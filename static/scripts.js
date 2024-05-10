window.addEventListener('DOMContentLoaded', (event) => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const snap = document.getElementById('snap');
    const uploadCaptured = document.getElementById('uploadCaptured');
    const context = canvas.getContext('2d');

    // Get access to the camera
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                video.srcObject = stream;
                video.play();
                console.log('Webcam Active')
            })
            .catch(function(error) {
                console.error('Error accessing the webcam:', error);
            });
    }

    // Capture the photo
    snap.addEventListener("click", function() {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        console.log('Captured Image')
    });

    // Upload the captured image
    uploadCaptured.addEventListener('click', function() {
        canvas.toBlob(function(blob) {
            const formData = new FormData();
            formData.append('file', blob, 'capture.png');
            fetch('/upload', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }, 'image/png');
    });
});


window.addEventListener('DOMContentLoaded',() => {
    const form = document.querySelector('form');
    const input = document.querySelector('input[type="file"]');
    const predictionsDiv = document.getElementById('predictions');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('video', input.files[0]);

        try{
            const response = await fetch('/upload_video', {
                method: 'POST',
                body: formData
            });

            if(response.ok){

                const data = await response.json();
                displayPredictions(data.predictions);
                alert('Video uploaded successfully!');
            }
            else{
                alert('Failed to upload video.');
            }
        } catch(error){
            console.error('Error:', error);
            alert('An error occured while uploading the video.');
        }
    });

    function displayPredictions(predictions){
    predictionsDiv.innerHTML = '';
    predictions.forEach(prediction => {
        const p  =document.createElement('p');
        p.textContent = prediction;
        predictionsDiv.appendChild(p);
    })
    }
});
