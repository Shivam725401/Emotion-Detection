from keras.models import load_model
from keras.utils import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import eel
from collections import Counter
import os
import random
import re

face_classifier = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
classifier =load_model(r'model.h5')
eel.init("WD_INNOVATIVE")
emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']

def get_emo():
    cap = cv2.VideoCapture(0)
    Captures = []
    try:
        for i in range(25):
            _, frame = cap.read()
            labels = []
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray)

            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
                roi_gray = gray[y:y+h,x:x+w]
                roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray])!=0:
                    roi = roi_gray.astype('float')/255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi,axis=0)

                    prediction = classifier.predict(roi)[0]
                    label=emotion_labels[prediction.argmax()]
                    label_position = (x,y-10)
                    cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                else:
                    cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                cv2.waitKey(1)
                cv2.imshow('Emotion Detector',frame)
                Captures.append(label)
        return Captures
    except:
        None
    finally:
        cap.release()
        cv2.destroyAllWindows()
    

@eel.expose
def get_emotion():
    Captures = get_emo()
    if Captures:
        emotion = Counter(Captures)
        emotion = max(emotion,key=emotion.get)
        return emotion
    else:
        return "Neutral"


@eel.expose
def get_songs(mood):
    path = os.listdir("WD_INNOVATIVE\\Songs\\"+mood+"\\")
    path = [s.replace(".mp3","") for s in path]
    random.shuffle(path)
    return path

@eel.expose
def random_play():
    path = os.listdir("WD_INNOVATIVE\\Songs\\")
    random.shuffle(path)
    random.shuffle(path)
    songs = [os.listdir("WD_INNOVATIVE\\Songs\\"+path[x]+"\\") for x in range(len(path))]
    songlist = []
    playlist = []
    for i in range(len(songs)):
        for j in songs[i]:
            List = "Songs\\" + path[i] + "\\" + j
            playlist.append(List)
    random.shuffle(playlist)
    random.shuffle(playlist)
    for i in range(len(playlist)):
        start_char = "Songs\\"
        end_char = "\\"
        pattern = f"{re.escape(start_char)}.*?{re.escape(end_char)}"
        song = re.sub(pattern,"",playlist[i])
        song = song.replace(".mp3","")
        songlist.append(song)
    return {"songlist":songlist,"playlist":playlist}

eel.start('main.html',mode = "chrome--app")