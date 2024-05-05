window.addEventListener('DOMContentLoaded', (event) => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const snap = document.getElementById('snap');
    const uploadCaptured = document.getElementById('uploadCaptured');
    const context = canvas.getContext('2d');

    // Get access to the camera
    // through video variable
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
            video.srcObject = stream;
            video.play();
        });
    }

    // Capture the photo
    // through snap variable
    snap.addEventListener("click", function() {
        context.drawImage(video, 0, 0, 640, 480);
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
