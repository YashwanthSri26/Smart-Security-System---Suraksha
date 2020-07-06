import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import datetime
import subprocess
from pyowm import OWM
import face_recognition
import json
from bs4 import BeautifulSoup as soup
import wikipedia
import random
from time import strftime
import pyttsx3 
import time
import smtplib
import pickle
import numpy as np
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import pandas as pd
import cv2

def sofiaResponse(audio):
    "speaks audio passed as argument"
    print(audio)
    engine = pyttsx3.init()
    engine.setProperty('rate', 150) 
   # Speed percent (can go over 100)
    engine.setProperty('volume', 1)
    engine.setProperty('voice', 'english+f4')
    engine.say(audio) 
    engine.runAndWait()
    
def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command

def SendMail(ImageFileName,Email):
    img_data = open(ImageFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Security Alert'
    msg['From'] = 'suraksha4u.team@gmail.com'
    msg['To'] = Email
    text = MIMEText("PFA the photograph of the person who tried to perform a security breach.")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImageFileName))
    msg.attach(image)
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    #s.ehlo()
    #s.starttls()
    #s.ehlo()
    s.login('suraksha4u.team@gmail.com', 'Suraksha123$')
    s.sendmail('suraksha4u.team@gmail.com',Email, msg.as_string())
    s.quit()

def assistant(command):
    "if statements for executing commands"
#open subreddit Reddit   
    if 'shutdown' in command:
        sofiaResponse('Bye bye Sir. Have a nice day')
        sys.exit()  
   
    elif "face" in command:
        video_capture = cv2.VideoCapture(0)
        with open('dataset_faces.dat', 'rb') as f:
            all_face_encodings = pickle.load(f)

# Grab the list of names and the list of encodings
        known_face_names = list(all_face_encodings.keys())
        known_face_encodings = np.array(list(all_face_encodings.values()))        
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        sofiaResponse("When the camera window pops up, please show your face")
        sofiaResponse("Press the key Y, when the camera recognizes you")
        name = "Unknown"
        name_display="Unknown"
        while True:    
    # Grab a single frame of video
            ret, frame = video_capture.read()   
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]    
            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:         
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.5)
                    name = "Unknown" 
                    name_display="Unknown"           
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]
                    face_names.append(name)         
            process_this_frame = not process_this_frame
            t=str(os.path.dirname(os.path.realpath('_file_')))
            df=pd.read_csv(t+"/database.csv")   
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4       
                
                for i in range(0,len(df.index)):
                    if name==df['Email'][i]:
                        name_display=df['FullName'][i]
                        break

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)        
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name_display, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)    
            cv2.imshow('Video', frame)                     
            
            if cv2.waitKey(1) & 0xFF == ord('y'):
                if name_display=="Unknown":
                    name="Unknown"
                break
       
        contents1=name
        f=open("id_verify.txt", "r")
        contents2=f.read()       
        f.close()
        if contents1 in contents2 and len(face_names)==1:
            video_capture.release()
            cv2.destroyAllWindows()
            cap = cv2.VideoCapture('/home/yashwanth/Suraksha_files/1.mp4') 
            if (cap.isOpened()== False): 
                print("Error opening video  file") 
            while(cap.isOpened()):
                ret, frame = cap.read() 
                if ret == True: 
                    cv2.imshow('Frame', frame) 
                    if cv2.waitKey(5) & 0xFF == ord('q'): 
                        break
                else:  
                    break
            cap.release() 
            cv2.destroyAllWindows()
            sofiaResponse("Face Recognized. Proceeding to the voice recognition module")
            #os.system("cd vc")     
            os.system("python authenticate3.py")
            sys.exit()
        else:   
            from pygame import mixer          
            ret,frame = video_capture.read() # return a single frame in variable `frame`
            cv2.imwrite('c1.png',frame)
            cv2.destroyAllWindows()
            video_capture.release()
            mixer.init()  
            mixer.music.load("buzzer.mp3") 
            mixer.music.play(7)
            sofiaResponse("SECURITY ALERT! SECURITY ALERT! SECURITY ALERT!")
            SendMail('c1.png',contents2)
            t=str(os.path.dirname(os.path.realpath('_file_')))
            df=pd.read_csv(t+"/database.csv")   
            #df=pd.read_csv()
            #print(len(df.index))
            for i in range(0,len(df.index)):
                print(df['Email'][i])
                if contents2==df['Email'][i]:
                    number=df['Number'][i]
                    break
            print(number)
            url = "https://www.fast2sms.com/dev/bulk"
            payload = "sender_id=FSTSMS&message=Security breach detected during authentication&language=english&route=p&numbers="+str(number)
            headers = {'authorization': "QJat06RV1Q3Kt3287Dn7sTWGvoB3yXh6gOFp9RucuhnyVc0jwt0fxO6zrUZo",'Content-Type': "application/x-www-form-urlencoded",'Cache-Control': "no-cache",}
            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.text)   
            sys.exit()
cap = cv2.VideoCapture('/home/yashwanth/Suraksha_files/1.mp4') 
if (cap.isOpened()== False): 
    print("Error opening video  file") 
while(cap.isOpened()):
    ret, frame = cap.read() 
    if ret == True: 
        cv2.imshow('Frame', frame) 
        if cv2.waitKey(5) & 0xFF == ord('q'): 
            break
    else:  
        break
cap.release() 
cv2.destroyAllWindows()  
    

sofiaResponse('Hello User, I am your guide, Suraksha. Please follow the commands for authentication')
assistant('show face')

