#a function where it fetches the relevant info for a specific chord
import certifi
from pymongo import MongoClient
from bson.objectid import ObjectId
import base64


def convert_bytes_to_base64(image_bytes):
    return 'data:image/png;base64,' + image_bytes.decode('utf-8')


#chord a id= 663f5c33fe15c02cfb545434
#chord b id= 663f5c62088ee3da7d33e774
#chord c id= 663f53af00fffdb8f9d93fd6
#chord d id= 663f55a78b13f10494f75d7d
#chord e id= 663f56e0f9dd440adca9de94
#chord f id =663f581dea01434c59e41ba1
#chord g id= 663f59a1f179ce359f9dbb13


class Chord:
    #constructor
    def __init__(self, chord_name, tablature_pictures, tutorial_video_link=""):
        self.chord_name = chord_name
        self.tablature_pictures = tablature_pictures
        self.tutorial_video_link = tutorial_video_link

    #getter method
    def getChordName(self):
        return self.chord_name

    def getTabPictures(self):
        return self.getTabPictures()

    def getVideoLink(self):
        return self.getVideoLink()


def fetch_chord_data(prediction):
    # Establish connection
    uri = ("mongodb+srv://AlifDB:alifnadillah1404@chorddatabase.t0jwv4a.mongodb.net/?retryWrites=true&w=majority"
           "&appName=ChordDatabase")
    # Create a new client and connect to the server
    client = MongoClient(uri, tlsCAFile=certifi.where())
    # Navigate to the GCR's app database - contains collection of document collections
    db = client['GCR_Database']
    # Navigate to the chordCollection - contains the collection of individual JSONs
    collection = db['ChordCollection']

    #get the type of chord
    if prediction == 'Chord A':
        #set the id
        id = ObjectId('663f5c33fe15c02cfb545434')

        #query by id and store in chord_json
        chord_document = collection.find_one({"_id": id})
        chord_name = chord_document["chordName"]
        tab_pictures = chord_document["tablaturePictures"]
        video_link = chord_document["tutorialVideoLink"]

        #instance a class to store chord data
        chord = Chord(chord_name, tab_pictures, video_link)

        #returns the class into app.py
        return chord
    elif prediction == 'Chord B':
        #set the id
        id = ObjectId('663f5c62088ee3da7d33e774')

        #query by id and store in chord_json
        chord_document = collection.find_one({"_id": id})
        chord_name = chord_document["chordName"]
        tab_pictures = chord_document["tablaturePictures"]
        video_link = chord_document["tutorialVideoLink"]

        #instance a class to store chord data
        chord = Chord(chord_name, tab_pictures, video_link)

        #returns the class into app.py
        return chord
    elif prediction == 'Chord C':
        #set the id
        id = ObjectId('663f53af00fffdb8f9d93fd6')

        #query by id and store in chord_json
        chord_document = collection.find_one({"_id": id})
        chord_name = chord_document["chordName"]
        tab_pictures = chord_document["tablaturePictures"]
        video_link = chord_document["tutorialVideoLink"]

        #instance a class to store chord data
        chord = Chord(chord_name, tab_pictures, video_link)

        #returns the class into app.py
        return chord
    elif prediction == 'Chord D':
        #set the id
        id = ObjectId('663f55a78b13f10494f75d7d')

        #query by id and store in chord_json
        chord_document = collection.find_one({"_id": id})
        chord_name = chord_document["chordName"]
        tab_pictures = chord_document["tablaturePictures"]
        video_link = chord_document["tutorialVideoLink"]

        #instance a class to store chord data
        chord = Chord(chord_name, tab_pictures, video_link)

        #returns the class into app.py
        return chord
    elif prediction == 'Chord E':
        #set the id
        id = ObjectId('663f56e0f9dd440adca9de94')

        #query by id and store in chord_json
        chord_document = collection.find_one({"_id": id})
        chord_name = chord_document["chordName"]
        tab_pictures = chord_document["tablaturePictures"]
        video_link = chord_document["tutorialVideoLink"]

        #instance a class to store chord data
        chord = Chord(chord_name, tab_pictures, video_link)

        #returns the class into app.py
        return chord
    elif prediction == 'Chord F':
        #set the id
        id = ObjectId('663f581dea01434c59e41ba1')

        #query by id and store in chord_json
        chord_document = collection.find_one({"_id": id})
        chord_name = chord_document["chordName"]
        tab_pictures = chord_document["tablaturePictures"]
        video_link = chord_document["tutorialVideoLink"]

        #instance a class to store chord data
        chord = Chord(chord_name, tab_pictures, video_link)

        #returns the class into app.py
        return chord
    elif prediction == 'Chord G':
        #set the id
        id = ObjectId('663f59a1f179ce359f9dbb13')

        #query by id and store in chord_json
        chord_document = collection.find_one({"_id": id})
        chord_name = chord_document["chordName"]
        tab_pictures = chord_document["tablaturePictures"]
        video_link = chord_document["tutorialVideoLink"]

        #instance a class to store chord data
        chord = Chord(chord_name, tab_pictures, video_link)

        #returns the class into app.py
        return chord
