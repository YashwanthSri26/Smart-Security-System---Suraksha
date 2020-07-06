import os
import pyaudio
import wave
import pyttsx3
import pandas as pd
import numpy
import csv
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 160) 
voice=engine.getProperty('voice')
engine.setProperty('voice','f4')
engine.say('hey there . I am Suraksha speaking . May i know your name please?')
engine.runAndWait()
x=input("Enter your name in caps: ")
engine.say(' hi '+ x )
print("---------------------INITIALIZING PROCESS!------------------------")
engine.say('PROCEED FORWARD FOR REGISTERING YOUR VOICE')
engine.runAndWait()
engine.stop()
WAVE_OUTPUT_FILENAME ="/home/yashwanth/vc/data/wav/enroll/"+x+".wav"
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("* done recording")
stream.stop_stream()
stream.close()
p.terminate()
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
myfile = open('random.txt', "r") # open lorem.txt for reading text
contents = myfile.read()         # read the entire file into a string
myfile.close()                   # close the file
row=['/home/yashwanth/Suraksha_files/data/wav/enroll/'+x+'.wav',int(contents)]
with open('/home/yashwanth/Suraksha_files/cfg/enroll_list.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)
csvFile.close()
row1=[x,int(contents)]
with open('extract.csv', 'a') as csvFile1:
    writer1 = csv.writer(csvFile1)
    writer1.writerow(row1)
csvFile1.close()
f = open('random.txt', 'r+')
f.truncate(0)
f.close()
f1=open('random.txt','w+')
f1.write(str(int(contents)+1))
f1.close()
