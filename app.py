import base64
from io import BytesIO

import cv2
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, redirect
from ultralytics import YOLO
import tensorflow as tf

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'upload/'

modelSegment = YOLO('C:/Users/alifs/Desktop/FYP/GuitarChordRecognition/runs/detect/train29/weights/best.pt')
modelClassifier = tf.keras.models.load_model(
    'C:/Users/alifs/Desktop/FYP/GuitarChordRecognition/CNN_CHORD_CLASSIFIER.keras')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload-file')
def upload_file():
    return render_template('upload_file.html')


@app.route('/webcam-capture')
def webcam_capture():
    return render_template('webcam_capture.html')


@app.route('/upload', methods=['POST'])
# perform prediction
def upload_image():
    class_mapping = {
        0: 'Chord A',
        1: 'Chord B',
        2: 'Chord C',
        3: 'Chord D',
        4: 'Chord E',
        5: 'Chord F',
        6: 'Chord G',
    }
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        imgBytes = file.read()

        img = Image.open(BytesIO(imgBytes))
        #img = preprocess_yolo(img)
        img_array_yolo = np.array(img)
        bboxSegment = modelSegment.predict(source=img_array_yolo)

        if bboxSegment and len(bboxSegment[0]) > 0:
            # Get the first result
            result = bboxSegment[0]
            original_img = np.copy(result.orig_img)

            # Get bounding box coordinates of the first detected object
            obj = result[0]  # Get the first detected object
            x1, y1, x2, y2 = obj.boxes.xyxy.cpu().numpy().squeeze().astype(np.int32)

            # Crop image to the bounding box
            cropped_img = original_img[y1:y2, x1:x2]

            # Preprocess the cropped image for classifier detection
            classifier_input = preprocess_classifier(cropped_img)

            prediction = modelClassifier.predict(classifier_input)

            #Extract the prediction based on the class

            #Extract the highest probability from the prediction
            chord_prediction_index = np.argmax(prediction)

            predicted_class_name = class_mapping[chord_prediction_index]

            return render_template('display_image.html', predicted_chord=predicted_class_name)
        return "No object detected"
    return "Invalid File"


def preprocess_yolo(img):
    # Implement preprocessing image for yolo
    # Resize the image into 704 width and height
    resized_image = img.resize((704, 704))

    return resized_image


def preprocess_classifier(img):
    # Convert image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the grayscale image
    blurred = cv2.GaussianBlur(gray_img, (3, 3), 0)

    # Apply Sobel filter to the blurred image
    sobel_filtered = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=5)
    sobel_img = cv2.convertScaleAbs(sobel_filtered)

    # Resize the Sobel image to 80x80
    resized_img = cv2.resize(sobel_img, (80, 80))

    # Convert resized image to 3 channels (RGB)
    resized_img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_GRAY2RGB)

    # Normalize the resized image to the range [0, 1]
    resized_img_normalized = resized_img_rgb / 255.0

    # Expand dimensions to match the expected input shape of the model
    resized_img_expanded = np.expand_dims(resized_img_normalized, axis=0)

    return resized_img_expanded


if __name__ == '__main__':
    app.run(debug=True)
