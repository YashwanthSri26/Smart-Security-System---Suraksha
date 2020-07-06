from functools import partial
from tkinter import StringVar
import tkinter as tk
from tkinter import ttk
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
try:
    import tkinter.filedialog as tkfd
except ImportError:
    import tkFileDialog as tkfd
from PIL import Image, ImageTk
import pyttsx3
import pyaudio

LARGE_FONT= ("Verdana", 12)
keys=[]
values=[]

class GraphPlot(tk.Tk):

    def __init__(self, *args, **kwargs):       
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Suraksha")       
        
        self.geometry("1550x900")
        self.resizable(0,0)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, ):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class StartPage(tk.Frame):  
    
    def sofiaResponse(self,audio):
        "speaks audio passed as argument"
        # print(audio)
        engine = pyttsx3.init()
        engine.setProperty('rate', 150) 
        # Speed percent (can go over 100)
        engine.setProperty('volume', 1)
        engine.setProperty('voice', 'english+f4')
        engine.say(audio) 
        engine.runAndWait()

    def _resize_image(self,event):
        new_width = event.width
        new_height = event.height
        self.image = self.img_copy.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)
      
    def __init__(self, parent, controller):        
        tk.Frame.__init__(self,parent)

        self.image = Image.open("/home/yashwanth/Suraksha_files/2.png")
        self.img_copy= self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)
        
        global txts
        txts = StringVar()
        global label_var

        label_0 = Label(self, bg="white", text="Suraksha", font=("TkFixedFont",50))
        label_0.place(x=380,y=60)    
        label_var = Label(self, bg="white",textvariable=txts, font=("TkFixedFont",30))
        txts.set("Enter Login Details to Proceed")
        label_var.place(x=230,y=190)

        global xyz

        xyz=0
        
 
        global username_verify
        global password_verify
 
        username_verify = StringVar()
        password_verify = StringVar()
 
        global username_login_entry
        global password_login_entry
        l1=ttk.Label(self, textvariable=label_var)
        
        
        label_2 = Label(self, bg="white", text="Email", font=("TkFixedFont",20))
        label_2.place(x=280,y=300)
        username_login_entry = Entry(self,width=40, textvariable=username_verify)
        username_login_entry.place(x=450,y=300)

        label_3 = Label(self,bg="white", text="Password ",font=("TkDixedFont",20))
        label_3.place(x=280,y=380)
        password_login_entry = Entry(self,width=40, textvariable=password_verify, show= '*')
        password_login_entry.place(x=450,y=380)

        Label(self, text="")
        button_0 = tk.Button(self,bg="white",cursor="circle",activebackground="aqua",width=12, text="Login", height=1, command = self.login_verify, font=("TkFixedFont", 25))
        button_0.place(x=415,y=450)
        #button4 = tk.Button(self, text="Back",font=('Helvetica','25'),command=lambda: controller.show_frame(StartPage))
        #button4.pack()
        
        #Button(self, text="Forgot Password", width=10, height=1).pack()
 

    
    def login_verify(self):
        username1 = username_verify.get()
        password1 = password_verify.get()
        #print(username1)
        username_login_entry.delete(0, END)
        password_login_entry.delete(0, END) 
        t=str(os.path.dirname(os.path.realpath('_file_')))
        df=pd.read_csv(t+"/database.csv")        
        #print(len(df.index)
        # )
        flag=0
        for i in range(0,len(df.index)):
            if username1==df['Email'][i] and i!=len(df.index):
                #print('success')
                flag=1
                if password1==df['Password'][i]:
                    self.login_sucess(username1)
                else:
                    self.password_not_recognised()
        if flag==0:
            self.user_not_found()             
        
 
# Designing popup for login success

 
    def login_sucess(self,name):
        global xyz               
        global label_var
        global use
        global txts
        txts.set("Login success!")
        #Label(self, text="Login Success").pack()        
        #Label(self, text="").pack()
        if xyz>0:
            self.b1.destroy()
        self.b1= Button(self,bg="white",cursor="circle",activebackground="aqua",width="12", text="Proceed", command=self.delete_login_success,font=("TkFixedFont", 25))        
        self.b1.place(x=415,y=520)
        self.sofiaResponse("Login successful press the proceed button") 
        xyz+=1      
        f= open("id_verify.txt","w+")
        f.write(name)
        f.close()
    def forgot_password(self):
        label_4 = Label(self,bg="white", text="Login Success",font=("TkFixedFont", 20))
        label_4.place(x=415,y=600)
        Button(self, text="Proceed", command=self.delete_login_success).pack()
        
 
# Designing popup for login invalid password
 
    def password_not_recognised(self):
        global label_var, xyz
        global txts
        txts.set("Invalid password")
        self.sofiaResponse("Invalid password please try again")
        #global b1
        if xyz>0:
            self.b1.destroy()                   
        
        #Button(self, text="OK", command=self.delete_password_not_recognised).pack()
 
# Designing popup for user not found
 
    def user_not_found(self):
        global label_var, xyz
        global txts
        txts.set("User not found")
        self.sofiaResponse("User not founnd please register")
        #global b1
        if xyz>0:
            self.b1.destroy()

# Deleting popups
 
    def delete_login_success(self):
        self.b1.destroy() 
        os.system("python abc.py")
 
    #def delete_password_not_recognised(self):
     #   self.password_not_recog_screen.destroy()
 
 
    #def delete_user_not_found_screen(self):
     #   self.user_not_found_screen.destroy()
 
app = GraphPlot()
app.mainloop()
