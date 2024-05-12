import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import base64

uri = "mongodb+srv://AlifDB:alifnadillah1404@chorddatabase.t0jwv4a.mongodb.net/?retryWrites=true&w=majority&appName=ChordDatabase"
# Create a new client and connect to the server
client = MongoClient(uri, tlsCAFile=certifi.where())
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    #Navigate to the GCR's app database - contains collection of document collections
    db = client['GCR_Database']
    #Navigate to the chordCollection - contains the collection of individual JSONs
    collection = db['ChordCollection']


    # A major chord tablatures (Inversions)
    # Read binary data from image file
    with open('C:/Users/alifs/GCR_WebVersion/inversionsPic/B major open chord.png', 'rb') as f:
        open_bytes = base64.b64encode(f.read())
    with open('C:/Users/alifs/GCR_WebVersion/inversionsPic/B major root tab.png', 'rb') as f:
        root_inversion_bytes = base64.b64encode(f.read())
    with open('C:/Users/alifs/GCR_WebVersion/inversionsPic/B major first inv tab.png', 'rb') as f:
        first_inversion_bytes = base64.b64encode(f.read())
    with open('C:/Users/alifs/GCR_WebVersion/inversionsPic/B major second inversion tab.png', 'rb') as f:
        second_inversion_bytes = base64.b64encode(f.read())

# c d e f g a b
# a major - a c e
    #first inv - e a c
    #second inv - c e a

# b major - b d f
    #first inv - f b d
    #sec inv - d f b

# c major - c e g
    #first inv - g c e
    #secinv - e g c




    # chord document (json) to store the chord name, tablature of inversions, and references(video link)
    chord_document = {
        "chordName": "B Major",
        "tablaturePictures": [
            {
                "data": open_bytes,
                "description": "Open chord tablature"
            },
            {
                "data": root_inversion_bytes,
                "description": "Root inversion tablature"
            },
            {
                "data": first_inversion_bytes,
                "description": "First inversion tablature"
            },
            {
                "data": second_inversion_bytes,
                "description": "Second inversion tablature"
            },
        ],
        "tutorialVideoLink": ""
    }

    # Insert document into collection
    result = collection.insert_one(chord_document)
    print("Inserted document ID:", result.inserted_id)

except Exception as e:
    print(e)
