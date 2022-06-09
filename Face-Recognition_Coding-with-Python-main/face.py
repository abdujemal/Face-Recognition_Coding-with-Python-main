from cmath import e
import json
from random import Random

import face_recognition as fr
import os
import cv2
import datetime
import face_recognition
import numpy as np
from time import sleep

from numpy import array
import pyrebase
import serial
import requests
import pyttsx3
import send_fcm

engine = pyttsx3.init()

def talk(text):
    engine.say(text)
    engine.runAndWait()

talk("Face Recognition Started")

firebaseConfig = {
  "apiKey": "AIzaSyBs-GCIDS6TtF6YJtlX1AzZcOVloKFsv2I",
  "authDomain": "faceiddoorlock.firebaseapp.com",
  "databaseURL": "https://faceiddoorlock-default-rtdb.firebaseio.com",
  "projectId": "faceiddoorlock",
  "storageBucket": "faceiddoorlock.appspot.com",
  "messagingSenderId": "722050499613",
  "appId": "1:722050499613:web:301800e4afa76d993572f4",
  "measurementId": "G-9Z8P2GCDPH"
}

dev = serial.Serial("COM9", baudrate=9600, timeout=.1)

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

storage = firebase.storage()

jsonFile = open("Face-Recognition_Coding-with-Python-main/face_encodings.json", "r")

faces = json.load(jsonFile)

isOnVoiceCall = False

def openDoor(val):
    dev.write(bytes('1','utf-8'))
    sleep(5.0)
    dev.write(bytes('0','utf-8'))
    print("door opened")
    global isOnVoiceCall
    if isOnVoiceCall:
        dev.write(bytes('4','utf-8'))
    

    

db.child("ring").stream(openDoor)

def showRecording(val):
    print(val['data'])
    global isOnVoiceCall
    isOnVoiceCall = val['data']
    if val['data']:
        dev.write(bytes('4','utf-8'))
    else:
        dev.write(bytes('0','utf-8'))


db.child("audioStarted").stream(showRecording)

for key in faces.keys():
    faces[key] = array(faces[key])

def classify_face():
    countUnknown = 0

    openCount = 0

    cap = cv2.VideoCapture(0)

    while True:

        ret, framae = cap.read()

        img1 = cv2.flip(framae,1)

        img = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

        faces_encoded = list(faces.values())
        known_face_names = list(faces.keys())

        global isOnVoiceCall

        face_locations = face_recognition.face_locations(img)
        unknown_face_encodings = face_recognition.face_encodings(img, face_locations, num_jitters=2)

        face_names = []
        for face_encoding in unknown_face_encodings:

            matches = face_recognition.compare_faces(faces_encoded, face_encoding, tolerance=0.5)
            name = "Unknown"

            face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                countUnknown = 0

                if openCount == 3:
                    openCount = 0
                    # opening the door 
                    rndm = Random()
                    dev.write(bytes('1','utf-8'))
                    talk("WelCome Home "+name)
                    sleep(5.0)
                    dev.write(bytes('0','utf-8'))
                    
                    if isOnVoiceCall:
                        dev.write(bytes('4','utf-8'))
    
                    print("door is opened")
                else:
                    dev.write(bytes('3','utf-8'))
                    sleep(0.3)
                    
                    if isOnVoiceCall:
                        dev.write(bytes('4','utf-8'))

                openCount += 1
                
            else:
                dev.write(b'2')
                sleep(2)
               
                if isOnVoiceCall:
                    dev.write(bytes('4','utf-8'))

                openCount = 0
                # sending the persons photo to the owner
                
                if countUnknown == 5:
                    rndm = Random()
                    imgName = str(rndm.randint(0,1000000))
                    cv2.imwrite("unknwon.jpg",img1)
                    talk("I am sending your photo to my boss.")
                    try:
                        storage.child("Persons/"+imgName).put("unknwon.jpg")
                        img_url = storage.child("Persons/"+imgName).get_url(None)
                        db.child("Persons").push({
                            "date_time": str(datetime.datetime.now()),
                            "img_url": img_url})
                        send_fcm.sendNotification("userA","የማይታወቁ ሰዎች", "ደጃፍዎ ላይ የማላውቀው ሰው ቆሟል።", img_url)
                    
                    except Exception as e:
                        print(e)
                    print("Photo sent")
                    countUnknown = 0
                else:
                    talk("Access Denied "+str(countUnknown+1))
                    
                countUnknown += 1

            face_names.append(name)

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                w = right - left
                h = bottom - top
                cv2.circle(img1, (left+int(w/2), top+int(h/2)),int(h/2)+15, (255, 0, 0), 2)

                # cv2.rectangle(img, (left - 20, top - 10), (right + 20, bottom + 15), (300, 0, 0), 2)

                cv2.rectangle(img1, (left - 20, bottom - 10), (right + 20, bottom + 15), (500, 0, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(img1, name, (left - 10, bottom + 10), font, 0.5, (300, 300, 300), 1)

        cv2.imshow("Face Id", img1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            jsonFile.close()
            return face_names


print(classify_face())  # You can either try to find people "test2.jpg" or "test1.jpg" in the string.
