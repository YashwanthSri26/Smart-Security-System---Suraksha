import pyaudio
import wave
import pyttsx3
import pandas as pd
import numpy
import csv
import sys
import os
import signal
import smtplib
import requests
from cv2 import *
import speech_recognition as sr
import cv2
from playsound import playsound
#import os
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist, euclidean, cosine
from glob import glob
from model import vggvox_model
from wav_reader import get_fft_spectrum
import constants as c
from pygame import mixer    
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
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
def SendMessage(number):
    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=FSTSMS&message=Security breach detected during authentication&language=english&route=p&numbers="+str(number)
    headers = {'authorization': "QJat06RV1Q3Kt3287Dn7sTWGvoB3yXh6gOFp9RucuhnyVc0jwt0fxO6zrUZo",'Content-Type': "application/x-www-form-urlencoded",'Cache-Control': "no-cache",}
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)   

def ClickPic():
    cam = VideoCapture(0)
    ret,frame = cam.read() # return a single frame in variable `frame`
    cv2.imwrite('c1.png',frame)
    cv2.destroyAllWindows()
    cam.release()


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
engine = pyttsx3.init()
rate = engine.getProperty('rate')
voice=engine.getProperty('voice')
engine.setProperty('voice','f4')
engine.setProperty('rate', 160)
#engine.say('Hey there . I am Suraksha speaking . May i know your name please?')
##engine.runAndWait()
#x=input("Enter your name in caps: ")
x="Unknown"
f=open("id_verify.txt", "r")
contents2=f.read()
f.close()
t=str(os.path.dirname(os.path.realpath('_file_')))
df=pd.read_csv(t+"/database.csv")   
#df=pd.read_csv()
for i in range(0,len(df.index)):
    if contents2==df['Email'][i]:
        x=df['FullName'][i]
        break
engine.say(' hi '+ x )
data=pd.read_csv('/home/yashwanth/Suraksha_files/extract.csv')
result=data['speak'][data.speaker_name==x]
result=result.tolist()
if len(result)==0:
    print("WARNING! UNAUTHORIZED ACCESS")
    engine.say("Warning! . unauthorized access  i repeat   unauthorized access")
    engine.runAndWait()
    f=open("id_verify.txt", "r")
    contents2=f.read()
    f.close()
    ClickPic()
    mixer.init() 
    mixer.music.load("buzzer.mp3") 
    mixer.music.play(4)
    SendMail('c1.png',contents2)                
    t=str(os.path.dirname(os.path.realpath('_file_')))
    df=pd.read_csv(t+"/database.csv")          
    for i in range(0,len(df.index)):
        if contents2==df['Email'][i]:
            number=df['Number'][i]
            break
    SendMessage(number)    
    quit()
   
speak=result[0] 
print(speak)
row=['/home/yashwanth/Suraksha_files/output.wav',speak]
with open('/home/yashwanth/Suraksha_files/cfg/test_list.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)
csvFile.close()
print("----------------VOICE  AUTHENTICATION  REQUIRED!------------------")
engine.say('VOICE Authentication Required! . Please record Your voice for first step verification.')
engine.runAndWait()
engine.stop()
for q in range(1,4):
    if(q==1):
        engine.say('I AM RECORDING YOUR VOICE for the first time . START SPEAKING')
        engine.runAndWait()
    if(q==2):
        engine.say('I AM RECORDING YOUR VOICE for the second time . START SPEAKING')
        engine.runAndWait()
    if(q==3):
        engine.say(x+"warning! this is your last attempt. I AM RECORDING YOUR VOICE for the last time . START SPEAKING")
        engine.runAndWait()

    WAVE_OUTPUT_FILENAME ="output.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)

    print("* recording started")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("* recording done")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    engine.say('I AM DONE RECORDING . NOW PROCEEDING FORWARD TO PROCESS YOUR VOICE SAMPLE')
    engine.runAndWait()
    wf.close()

    AUDIO_FILE = ("output.wav") 
    a = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source: 
        audio = a.record(source)
    try: 
        code1=a.recognize_google(audio).lower()
        engine.say('Speech detected . STARTING VERIFICATION')
        engine.runAndWait()
        print("Speech detected")
        break;
    except sr.UnknownValueError:
           print(q)
           if q==3:
               engine.say("I AM TERMINATING THE PROCESS SINCE NO SPEECH IS DETECTED")
               engine.runAndWait()
               f=open("id_verify.txt", "r")
               contents2=f.read()
               f.close()
               ClickPic()
               mixer.init() 
               mixer.music.load("buzzer.mp3") 
               mixer.music.play(4)
               SendMail('c1.png',contents2)                
               t=str(os.path.dirname(os.path.realpath('_file_')))
               df=pd.read_csv(t+"/database.csv")   
            
               for i in range(0,len(df.index)):
                   if contents2==df['Email'][i]:
                       number=df['Number'][i]
                       break
               SendMessage(number)
               quit() 
           else :
               engine.say('Suraksha could not understand audio . Please record again.')
               engine.runAndWait()
def build_buckets(max_sec, step_sec, frame_step):
    buckets = {}
    frames_per_sec = int(1/frame_step)
    end_frame = int(max_sec*frames_per_sec)
    step_frame = int(step_sec*frames_per_sec)
    for i in range(0, end_frame+1, step_frame):
        s = i
        s = np.floor((s-7+2)/2) + 1  # conv1
        s = np.floor((s-3)/2) + 1  # mpool1
        s = np.floor((s-5+2)/2) + 1  # conv2
        s = np.floor((s-3)/2) + 1  # mpool2
        s = np.floor((s-3+2)/1) + 1  # conv3
        s = np.floor((s-3+2)/1) + 1  # conv4
        s = np.floor((s-3+2)/1) + 1  # conv5
        s = np.floor((s-3)/2) + 1  # mpool5
        s = np.floor((s-1)/1) + 1  # fc6
        if s > 0:
            buckets[i] = int(s)
    return buckets
def get_embeddings_from_list_file(model, list_file, max_sec):
    buckets = build_buckets(max_sec, c.BUCKET_STEP, c.FRAME_STEP)
    result = pd.read_csv(list_file, delimiter=",")
    result['features'] = result['filename'].apply(lambda x: get_fft_spectrum(x, buckets))
    result['embedding'] = result['features'].apply(lambda x: np.squeeze(model.predict(x.reshape(1,*x.shape,1))))
    return result[['filename','speaker','embedding']]
def get_id_result():
    print("Loading model weights from [{}]....".format(c.WEIGHTS_FILE))
    model = vggvox_model()
    model.load_weights(c.WEIGHTS_FILE)
    model.summary()

    print("Processing enroll samples....")
    enroll_result = get_embeddings_from_list_file(model, c.ENROLL_LIST_FILE, c.MAX_SEC)
    enroll_embs = np.array([emb.tolist() for emb in enroll_result['embedding']])
    speakers = enroll_result['speaker']

    print("Processing test samples....")
    test_result = get_embeddings_from_list_file(model, c.TEST_LIST_FILE, c.MAX_SEC)
    test_embs = np.array([emb.tolist() for emb in test_result['embedding']])

    print("Comparing test samples against enroll samples....")
    distances = pd.DataFrame(cdist(test_embs, enroll_embs, metric=c.COST_METRIC), columns=speakers)

    scores = pd.read_csv(c.TEST_LIST_FILE, delimiter=",",header=0,names=['test_file','test_speaker'])
    scores = pd.concat([scores, distances],axis=1)
    scores['result'] = scores[speakers].idxmin(axis=1)
    scores['correct'] = (scores['result'] == scores['test_speaker'])*1. # bool to int

    print("Writing outputs to [{}]....".format(c.RESULT_FILE))
    result_dir = os.path.dirname(c.RESULT_FILE)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    with open(c.RESULT_FILE, 'w') as f:
        scores.to_csv(f, index=False)


if __name__ == '__main__':
    get_id_result()
data=pd.read_csv('/home/yashwanth/Suraksha_files/res/results.csv')

with open('/home/yashwanth/Suraksha_files/cfg/test_list.csv','rt') as fh:
    mylist = []
    myreader = csv.DictReader(fh)
    headers = myreader.fieldnames
    for row in myreader:
       mylist.append(row)
mylist = mylist[0:-1]
outref = open('/home/yashwanth/Suraksha_files/cfg/test_list.csv','w+')
mywriter = csv.DictWriter(outref, fieldnames = headers)
headerdict = dict((col,col) for col in headers) # create a dict with col headings)
mywriter.writerow(headerdict) #writeout the column headings first
mywriter.writerows(mylist)    #write the data
outref.close()



data=pd.read_csv('/home/yashwanth/Suraksha_files/res/results.csv')
rate = engine.getProperty('rate')
engine.setProperty('rate', 160)
if (data['correct'].iloc[-1]==1):
    engine.say(x+"first step verification successful! . access granted to complete next step verification")
    engine.runAndWait()
    print("first step verification successful! . access granted to next step verification")
    def code():
        global code
        r = sr.Recognizer()                                                                                   
        with sr.Microphone() as source: 
            engine.say('please say the code phrase to complete last step verification')  
            engine.runAndWait()                                                                    
            print("Speak:")   
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=5)                                                                                 
            audio = r.listen(source)   
        try:
            code = r.recognize_google(audio).lower()
            if 'open sesame' in code:
                print('Authorization completed now you may access your secure data')
                engine.say(x+'Authorization completed . Now you may accesss your secure data')
                engine.runAndWait()
                os.system("xdg-open sample_data.ods")

            elif 'open suraksha' in code:
                print('Authorization completed now you may access your secure data')
                engine.say(x+'Authorization completed . Now you may access your secure data')
                engine.runAndWait()
                f=open("id_verify.txt", "r")
                contents2=f.read()
                f.close()
                ClickPic()
                os.system("xdg-open fake_data.ods")
                SendMail('c1.png',contents2)                
                t=str(os.path.dirname(os.path.realpath('_file_')))
                df=pd.read_csv(t+"/database.csv")   
            
                for i in range(0,len(df.index)):
                    if contents2==df['Email'][i]:
                        number=df['Number'][i]
                        break
                #print(number)
                SendMessage(number)
                quit()

            else:
                print("WARNING! WARNING! . AUTHENTICATION FAILED")
                engine.say("Warning! voice authentication failed    i repeat voice authentication failed ")
                engine.runAndWait()             
                f=open("id_verify.txt", "r")
                contents2=f.read()
                f.close()
                ClickPic()
                mixer.init() 
                mixer.music.load("buzzer.mp3") 
                mixer.music.play(4)
                SendMail('c1.png',contents2)                
                t=str(os.path.dirname(os.path.realpath('_file_')))
                df=pd.read_csv(t+"/database.csv")   
            
                for i in range(0,len(df.index)):
                    if contents2==df['Email'][i]:
                        number=df['Number'][i]
                        break
                #print(number)
                SendMessage(number)
                quit()
                
        except sr.UnknownValueError:
            print("Could not understand audio")
            engine.say('could not understand audio . please record again')
            engine.runAndWait()
            code=code()
        return code
    code()
else:
    print("WARNING! WARNING! . AUTHENTICATION FAILED")
    engine.say("Warning! voice authentication failed    i repeat voice authentication failed")
    engine.runAndWait()
    f=open("id_verify.txt", "r")
    contents2=f.read()
    f.close()
    ClickPic()
    mixer.init() 
    mixer.music.load("buzzer.mp3") 
    mixer.music.play(4)
    SendMail('c1.png',contents2)                
    t=str(os.path.dirname(os.path.realpath('_file_')))
    df=pd.read_csv(t+"/database.csv")   
        
    for i in range(0,len(df.index)):
        if contents2==df['Email'][i]:
            number=df['Number'][i]
            break
    #print(number)
    SendMessage(number)    
    quit()