import base64
from io import BytesIO
import os

import cv2
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, redirect, send_from_directory
from ultralytics import YOLO
import tensorflow as tf
import tempfile
from flask import jsonify
import json
from pymongo.mongo_client import MongoClient

from database import fetch_chord_data, convert_bytes_to_base64

app = Flask(__name__)





chord_folder = os.path.join('static', 'chord_photo')
#app.config['UPLOAD_FOLDER'] = 'upload/'
app.config['UPLOAD_FOLDER'] = chord_folder

# load custom-trained YOLO model 
#modelSegment = YOLO('C:/Users/alifs/Desktop/FYP/GuitarChordRecognition/runs/detect/train29/weights/best.pt')
#modelSegment = YOLO('C:/Users/alifs/Desktop/FYP/GuitarChordRecognition/Notebooks/runs/detect/train/weights/last.pt') # new YOLO trained version
#modelSegment = YOLO('C:/Users/alifs/Desktop/FYP/GuitarChordRecognition/Notebooks/runs/detect/train3/weights/last.pt') # new YOLO trained on Egohands dataset
modelSegment = YOLO('C:/Users/alifs/Desktop/FYP/GuitarChordRecognition/Notebooks/runs/detect/train8/weights/last.pt')
modelClassifier = tf.keras.models.load_model(
    'C:/Users/alifs/Desktop/FYP/GuitarChordRecognition/CNN_CHORD_CLASSIFIER.keras')



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload-file')
def upload_file():
    return render_template('upload_file.html')

@app.route('/real_time')
def real_time():
    return render_template('real_time.html')

#@app.route('/webcam-capture')
#def webcam_capture():
#    return render_template('webcam_capture.html')

@app.route('/video_upload')
def video_upload():
    return render_template('video_upload.html')


# prediction based on video uploaded
@app.route('/upload_video', methods=['POST'])
# perform prediction on video
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file part in the request"}), 400
    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({"error": "No selected video file"}), 400

    try:
        #Read the video file

        video_bytes = video_file.read()

        video_array = np.frombuffer(video_bytes, np.uint8)

        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
            temp_file.write(video_bytes)
            temp_file_path = temp_file.name

        # Crate instance to capture video
        video_capture = cv2.VideoCapture(temp_file_path)

        #store predictions detected in the whole video
        predictions = []

        #iterate through all frames in the video
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            #segmentation
            bboxSegment = modelSegment.predict(source=frame)

            cropped = extract_bounding_box(bboxSegment)
            if cropped is None:
                print("No bbox detected in the frame.")
                continue
            else:
                #Preprocess 4 classification
                cnn_input = preprocess_classifier(cropped)

                # Perform classification
                prediction = modelClassifier.predict(cnn_input)

                #Extract result
                prediction_class = determine_chord(prediction)
                predictions.append(prediction_class)

        video_capture.release()
        os.remove(temp_file_path)
        #PREDICTION ACHIEVED
        print("Predictions: ", predictions)

        # pass predictions array (contain chord_name,link,and description only)
        chords_data_list = render_chords_page(predictions)

        print("Chords Data before being passed: ", chords_data_list)

        return jsonify({"success": True, "chords_data": chords_data_list})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error: ": str(e)}), 500


def render_chords_page(prediction):
    # Shortlist the most relevant chords
    shortlist_chords = shortlist_chord(prediction)

    # List to store chord information
    chords_data = []

    for chord in shortlist_chords:
        # Fetch data for each element in the array
        # holds chord object
        #retrieve only name, link, and description
        chord_Object = fetch_chord_data(chord)

        if isinstance(chord_Object, dict) and "error" in chord_Object:
            return render_template('ErrorPage.html', error_message=chord_Object["error"])
        else:

            # Extract information
            open_chord = chord_Object.tablature_pictures[0]
            root = chord_Object.tablature_pictures[1]
            first = chord_Object.tablature_pictures[2]
            second = chord_Object.tablature_pictures[3]

            # Convert images to base64
            open_chord_image = convert_bytes_to_base64(open_chord["data"])
            root_image = convert_bytes_to_base64(root["data"])
            first_image = convert_bytes_to_base64(first["data"])
            second_image = convert_bytes_to_base64(second["data"])

            # Descriptions
            desc_open = open_chord["description"]
            desc_root = root["description"]
            desc_first = first["description"]
            desc_second = second["description"]


            # Store chord information in a dictionary
            # Replace the base 64 images for url of the images
            chord_info = {
                "chord_name": chord_Object.chord_name,
                "video_link": chord_Object.tutorial_video_link,
                "open_chord_image": open_chord_image,
                "root_image": root_image,
                "first_image": first_image,
                "second_image": second_image,
                "desc_open": desc_open,
                "desc_root": desc_root,
                "desc_first": desc_first,
                "desc_second": desc_second
            }

        # Append the chord information to the list
        if not any(existing_chord["chord_name"] == chord_info['chord_name'] for existing_chord in chords_data):
            chords_data.append(chord_info)

    print("Chords Data: ", chords_data)
    return chords_data


@app.route('/display_result_video', methods=['POST']) #change the method to POST method
def display_result_video():
    chords_data = request.json.get('chords_data')
    if chords_data:
       print("Chords Data received in /display_result_video:", chords_data)  # Debugging log
       return render_template('display_result_video.html', chords_data=chords_data)
    else:
        return "No chords data available", 400


def shortlist_chord(predArray):
    #accept array parameter
    #chord counter

    #Initialize a mapping 
    chord_counters = {
        'Chord A': 0,
        'Chord B': 0,
        'Chord C': 0,
        'Chord D': 0,
        'Chord E': 0,
        'Chord F': 0,
        'Chord G': 0
    }
    #find the frequency of each chords based on prediction array (percentages)

    # Count the occurrences of each chord
    for chord in predArray:
        if chord in chord_counters:
            chord_counters[chord] += 1

    # Calculate the total number of predictions
    total_predictions = len(predArray)

    #Calculate percentages
    chord_percentages = {
        chord: (count / total_predictions) * 100 for chord, count in chord_counters.items()
    }
    chord_shortlisted = []
    #take the highest frequency of chords or more (>25)
    for chord, percent in chord_percentages.items():
        if percent >= 25:
            chord_shortlisted.append(chord)
    #ACHIEVED
    print("shortlisted chords: ", chord_shortlisted)
    return chord_shortlisted


@app.route('/upload', methods=['POST'])
# perform prediction
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        imgBytes = file.read()

        img = Image.open(BytesIO(imgBytes))
        img_array_yolo = np.array(img)
        #need to add code to ensure that the img_array is in 3 channels
        img_array_yolo = ensure_three_channels(img_array_yolo)

        bboxSegment = modelSegment.predict(source=img_array_yolo)

        if bboxSegment is None or len(bboxSegment) == 0:
            return render_template('ErrorPage.html', error_message="The image cannot be processed. 1.0") #No bounding box detected

        try:

            #Crop image based on the bounding box detected by YOLO model
            croppedimg = extract_bounding_box(bboxSegment)

            #Apply sobel and appropriate preprocessing for classifier
            feature_extracted_img = preprocess_classifier(croppedimg)

            #Classifier perform prediction
            prediction = modelClassifier.predict(feature_extracted_img)

            predicted_class_name = determine_chord(prediction)

            #Fetch chord information based on the prediction
            chord_Object = fetch_chord_data(predicted_class_name)

            #if error detected because of pyMongo connection/chord information cant be fetched/no chord data exist
            #go to errorpage.html

            if isinstance(chord_Object, dict) and "error" in chord_Object:
                return render_template('ErrorPage.html', error_message=chord_Object["error"])
            else:

                open_chord = chord_Object.tablature_pictures[0]
                root = chord_Object.tablature_pictures[1]
                first = chord_Object.tablature_pictures[2]
                second = chord_Object.tablature_pictures[3]

               
                open_chord_image = convert_bytes_to_base64(open_chord["data"])
                root_image = convert_bytes_to_base64(root["data"])
                first_image = convert_bytes_to_base64(first["data"])
                second_image = convert_bytes_to_base64(second["data"])

                desc_open = open_chord["description"]
                desc_root = root["description"]
                desc_first = first["description"]
                desc_second = second["description"]

                thumbnail_link = extract_video_id(chord_Object.tutorial_video_link)

            return render_template('display_image.html', predicted_chord=predicted_class_name,
                                   chord_name=chord_Object.chord_name, video_link=chord_Object.tutorial_video_link,
                                   open_chord_image=open_chord_image, root_image=root_image, first_image=first_image,
                                   second_image=second_image, desc_open=desc_open, desc_root=desc_root,
                                   desc_first=desc_first, desc_second=desc_second, thumbnail_id = thumbnail_link)
        except Exception as e:
            #Error Bounding box not detected 2.0 - YOLO cant segmentize the image
            return render_template('ErrorPage.html', error_message="Image cant be processed 2.0")
                                                                   

    return render_template('ErrorPage.html', error_messsage="No file is detected and uploaded.")

@app.route('/realPredict', methods=['POST'])
def predict():
    data = request.json
    image_data = data['image'].split(',')[1]
    image = base64.b64decode(image_data)
    nparr = np.frombuffer(image, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


    bboxSegment = modelSegment.predict(source=frame)
    cropped = extract_bounding_box(bboxSegment)
    if cropped is None:
        return jsonify({"success": False, "error": "No bounding box detected"})
    else:
        #Apply sobel and appropriate preprocessing for classifier
        feature_extracted_img = preprocess_classifier(cropped)

        #Classifier perform prediction
        prediction = modelClassifier.predict(feature_extracted_img)

        predicted_class_name = determine_chord(prediction)

    return jsonify({"success":True, "chord":predicted_class_name})



def extract_bounding_box(boundingbox):
    # Extract and crop the image based on bounding box
    if boundingbox and len(boundingbox[0]) > 0:
        # Get the first result
        result = boundingbox[0]
        original_img = np.copy(result.orig_img)

        # Get bounding box coordinates of the first detected object
        obj = result[0]  # Get the first detected object
        x1, y1, x2, y2 = obj.boxes.xyxy.cpu().numpy().squeeze().astype(np.int32)

        # Crop image to the bounding box
        cropped_img = original_img[y1:y2, x1:x2]

        return cropped_img

    # need to add error handling if bounding box is not detected


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
    # need to add error handling if there is no cropped image


def determine_chord(pred):
    class_mapping = {
        0: 'Chord A',
        1: 'Chord B',
        2: 'Chord C',
        3: 'Chord D',
        4: 'Chord E',
        5: 'Chord F',
        6: 'Chord G',
    }
    chord_prediction_index = np.argmax(pred)

    predicted_class_name = class_mapping[chord_prediction_index]

    return predicted_class_name

    # add error handling


def ensure_three_channels(image):
    if image.shape[2] == 4:  # Check if the image has 4 channels (RGBA)
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    elif image.shape[2] == 1:  # Check if the image has 1 channel (grayscale)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    return image

import re

def extract_video_id(url):
    # Regular expression to extract the video ID
    video_id_pattern = r"v=([a-zA-Z0-9_-]+)"
    
    # Search for the pattern in the URL
    match = re.search(video_id_pattern, url)
    
    # If a match is found, return the video ID
    if match:
        return match.group(1)
    else:
        return None


if __name__ == '__main__':
    app.run(debug=True)
