import os
import pandas as pd
from functools import partial
from tkinter import StringVar
import tkinter as tk
from tkinter import ttk
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
try:
    import tkinter.filedialog as tkfd
except ImportError:
    import tkFileDialog as tkfd
import shutil
import csv
import face_recognition
import pickle
import cv2
import os
import pyaudio
import wave
import pyttsx3
import pandas as pd
import numpy
import cv2
from PIL import Image, ImageTk

#%matplotlib qt

LARGE_FONT= ("Verdana", 12)
keys=[]
values=[]

class GraphPlot(tk.Tk):

    def __init__(self, *args, **kwargs):       
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Suraksha")       
        
        self.geometry("1500x900")
        self.resizable(0,0)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (PageOne,):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageOne)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        

class PageOne(tk.Frame):
    def _resize_image(self,event):
        new_width = event.width
        new_height = event.height
        self.image = self.img_copy.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)
        global flag

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.image = Image.open("/home/yashwanth/Suraksha_files/pic.jpg")
        self.img_copy= self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)
        global Fullname
        global Email
        global var
        global num
        global pas
        global flag
        flag=0
        Fullname=StringVar()
        Email=StringVar()
        var = IntVar()
        num=StringVar()    
        pas= StringVar()

             
        label_0 = Label(self,bg="white", text="Registration Form",width=30,font=("TkFixedFont", 30))
        label_0.place(x=135,y=60)

        label_1 = Label(self, bg="white", text="FullName",width=13,font=("TkFixedFont", 18))
        label_1.place(x=175,y=170)

        entry_1 = Entry(self,width=50,textvar=Fullname)
        entry_1.place(x=400,y=170)

        label_2 = Label(self,bg="white",  text="Email",width=13,font=("TkFixedFont", 18))
        label_2.place(x=175,y=240)

        entry_2 = Entry(self,width=50,textvar=Email)
        entry_2.place(x=400,y=240)

        label_3 = Label(self,bg="white",  text="Gender",width=13,font=("TkFixedFont", 18))
        label_3.place(x=175,y=310)

        rb1 = Radiobutton(self,bg="white",  text="M",padx = 5, variable=var, value=1).place(x=425,y=310)
        rb2 = Radiobutton(self, bg="white", text="F",padx = 20, variable=var, value=2).place(x=475,y=310)

        label_4 = Label(self, bg="white", text="Mobile Number",width=13,font=("TkFixedFont", 18))
        label_4.place(x=175,y=380)

        entry_3 = Entry(self,width=50,textvar=num)
        entry_3.place(x=400,y=380)

        label_4 = Label(self, bg="white", text="Password",width=13,font=("TkFixedFont", 18))
        label_4.place(x=175,y=450)

        entry_4 = Entry(self,width=50,textvar=pas,show = "*")
        entry_4.place(x=400,y=450)

        def insert_row(idx,df,df_insert):
            return df.iloc[:idx,].append(df_insert).append(df.iloc[idx:,]).reset_index(drop=True)


        def load_images_from_folder(folder):
            all_face_encodings = {}
            for filename in os.listdir(folder):                
                img1 = face_recognition.load_image_file(os.path.join(folder,filename))
                all_face_encodings[filename[:-4]]=face_recognition.face_encodings(img1)[0]
            with open('dataset_faces.dat', 'wb') as fa:
                pickle.dump(all_face_encodings, fa)
   
        def clearFunc():
            entry_1.delete(0, END)
            entry_2.delete(0, END)
            entry_3.delete(0, END)
            entry_4.delete(0, END)
            


        def writeToFile(a,b,c,d,e):
            global flag
            global check
            check = 0
            df=pd.read_csv("/home/yashwanth/Suraksha_files/database.csv")
            for i in range(0,len(df.index)):
                if b==df['Email'][i]:
                    check = 1
                    break 
            if(a!="NULL" and b!="NULL" and c!="NULL" and d!="NULL" and e!="NULL" and flag==2 and check == 0):
                if(c == 1):
                    df2=pd.DataFrame([[a,b,'M',d,e]],columns=['FullName','Email','Gender','Number','Password'])
                if(c == 2):
                    df2=pd.DataFrame([[a,b,'F',d,e]],columns=['FullName','Email','Gender','Number','Password'])
                rc=int(df.shape[0])+1
                df=insert_row(rc,df,df2)
                df.to_csv("/home/yashwanth/Suraksha_files/database.csv",encoding='utf-8',index=False)
                load_images_from_folder("input_images")
                clearFunc()
            else:
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
                engine.say('Please enter proper details')
                engine.runAndWait()
                engine.stop()
                clearFunc()
                
        
        def selectimage():
            global flag
            video_capture = cv2.VideoCapture(0)
            while True:
                ret, frame = video_capture.read()   
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]    
                cv2.imshow('Video', frame)
                if cv2.waitKey(1) & 0xFF == ord('y'):
                #ret,frame = video_capture.read()
                    cv2.destroyAllWindows()
                    video_capture.release()
                    path='/home/yashwanth/Suraksha_files/input_images/'  #give the path name here
                    b=entry_2.get()
                    name=str(b) + ".png"       #give the email_id here
                    cv2.imwrite(str(path)+str(name),frame)    
                    flag = flag + 1
                    break   
        
        button4 = tk.Button(self,bg="white",cursor="circle",activebackground="aqua",  text="Take Picture",command= selectimage, font=("TkFixedFont", 18))
        button4.place(x=275, y=520)      

        def selectaudio():
            global flag
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
            x=entry_1.get()
            engine.say(' hi '+ x )
            print("---------------------INITIALIZING PROCESS!------------------------")
            engine.say('PROCEED FORWARD FOR REGISTERING YOUR VOICE')
            engine.runAndWait()
            engine.stop()
            WAVE_OUTPUT_FILENAME ="/home/yashwanth/Suraksha_files/data/wav/enroll/"+x+".wav"
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
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
                flag = flag + 1
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

        
        button5 = tk.Button(self, bg="white",cursor="circle",activebackground="aqua", text="Record Audio",command= selectaudio, font=("TkFixedFont", 18))
        button5.place(x=550, y=520)      
         
        button3 = tk.Button(self,bg="white",cursor="circle",activebackground="aqua", width=12, text="Submit",command=lambda:writeToFile(entry_1.get(), entry_2.get(), var.get(), entry_3.get(), entry_4.get()), font=("TkFixedFont", 25))
        button3.place(x=380,y=590)

        entry_1.delete(0 , END)

app = GraphPlot()
app.mainloop()