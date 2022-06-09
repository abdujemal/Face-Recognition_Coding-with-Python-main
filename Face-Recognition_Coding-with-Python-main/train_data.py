import json
import os
import face_recognition as fr
import pyrebase
import cv2
import face_recognition

firebaseConfig = {
  "apiKey": "AIzaSyBs-GCIDS6TtF6YJtlX1AzZcOVloKFsv2I",
  "authDomain": "faceiddoorlock.firebaseapp.com",
  "databaseURL": "https://faceiddoorlock-default-rtdb.firebaseio.com",
  "projectId": "faceiddoorlock",
  "storageBucket": "faceiddoorlock.appspot.com",
  "messagingSenderId": "722050499613",
  "appId": "1:722050499613:web:baa7fc83dee643d63572f4",
  "measurementId": "G-YK9BVF9RFZ"
}

# firebase = pyrebase.initialize_app(firebaseConfig)

# db = firebase.database()

# storage = firebase.storage()

def get_encoded_faces():
    
    print("Geting Image From Database")
    # for dirpath, dnames, fnames in os.walk("Face-Recognition_Coding-with-Python-main/face_repository"):
    #     for f in fnames:
    #         if f.endswith(".jpg") or f.endswith(".png"):
    #             os.remove("Face-Recognition_Coding-with-Python-main/face_repository/"+f)
    
    # owners = db.child("Owners").get()

    # for owner in owners.each():
       
    #     storage.child(owner.val()['img_url']).download("","Face-Recognition_Coding-with-Python-main/face_repository/"+owner.val()["name"]+".jpg")
       

    encoded = {}

    print("Encoding Started")
    i = 0
    for dirpath, dnames, fnames in os.walk("Face-Recognition_Coding-with-Python-main/face_repository"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                
                face = fr.load_image_file("Face-Recognition_Coding-with-Python-main/face_repository/"+ f)
                img = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(img)
                encoding = fr.face_encodings(img, face_locations, num_jitters=100)[0].tolist()
                encoded[f.split(".")[0]] = encoding

    return encoded


faces = get_encoded_faces()

# jsnfile = open("face_encodings.json", "r")
# data = json.load(jsnfile)
# data["faces_encoded"] = faces

jsonFile = open("Face-Recognition_Coding-with-Python-main/face_encodings.json", "w")


print(faces)

jsonFile.write(json.dumps(faces))
jsonFile.close()
print("Model trained")
