#a function where it fetches the relevant info for a specific chord
import certifi
from pymongo import MongoClient, errors
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
    uri = ("mongodb+srv://***********@chorddatabase.t0jwv4a.mongodb.net/?retryWrites=true&w=majority"
           "&appName=ChordDatabase")
    try:
        # Establish connection

        # Create a new client and connect to the server
        client = MongoClient(uri, tlsCAFile=certifi.where())
        # Navigate to the GCR's app database - contains collection of document collections
        db = client['GCR_Database']
        # Navigate to the chordCollection - contains the collection of individual JSONs
        collection = db['ChordCollection']
    except errors.ConnectionFailure:
        return {"error": "Failed to connect to MongoDB"}

    #Mapping of predictions
    prediction_to_id = {
        'Chord A': '663f5c33fe15c02cfb545434',
        'Chord B': '663f5c62088ee3da7d33e774',
        'Chord C': '663f53af00fffdb8f9d93fd6',
        'Chord D': '663f55a78b13f10494f75d7d',
        'Chord E': '663f56e0f9dd440adca9de94',
        'Chord F': '663f581dea01434c59e41ba1',
        'Chord G': '663f59a1f179ce359f9dbb13'
    }
    if prediction in prediction_to_id:
        id = ObjectId(prediction_to_id[prediction])

        try:
            #query by id and store in chord_json
            chord_document = collection.find_one({"_id": id})

            if not chord_document:
                return {"error:" "Chord data not found"}

            chord_name = chord_document["chordName"]
            tab_pictures = chord_document["tablaturePictures"]
            video_link = chord_document["tutorialVideoLink"]

            #instance a class to store chord data
            chord = Chord(chord_name, tab_pictures, video_link)

            return chord
        except errors.PyMongoError:
            return {"error": "Failed to fetch data from MongoDB"}
    else:
        return {"error": "Invalid prediction"}
