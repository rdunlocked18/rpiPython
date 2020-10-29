from tkinter import *
from tkinter import ttk
#import cv2 # importing cv2 liberary
import numpy as np
# import tensorflow as tf
# import mtcnn
# from PIL import Image
# from mtcnn import MTCNN
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import pandas as pd
import json,requests,math
from datetime import datetime

root = Tk()
root.title('Dashboard')
root.geometry("500x500")

my_notebook = ttk.Notebook(root)
my_notebook.pack(pady=15)

my_frame1 = Frame(my_notebook, width=500, height = 500)#dashboard
my_frame2 = Frame(my_notebook, width=500, height = 500)#Console
my_frame3 = Frame(my_notebook, width=500, height = 500)#auth
my_frame4 = Frame(my_notebook, width=500, height = 500)#CAMERA
my_frame5 = Frame(my_notebook, width=500, height = 500)#FPS
my_frame6 = Frame(my_notebook, width=500, height = 500)#RFID


my_frame1.pack(fill="both", expand=1)
my_frame2.pack(fill="both", expand=1)
my_frame3.pack(fill="both", expand=1)
my_frame4.pack(fill="both", expand=1)
my_frame5.pack(fill="both", expand=1)
my_frame6.pack(fill="both", expand=1)


my_notebook.add(my_frame1, text="Dashboard")
my_notebook.add(my_frame2, text="Console")
my_notebook.add(my_frame3, text="Authenticate")
my_notebook.add(my_frame4, text="CAMERA")
my_notebook.add(my_frame5, text="FPS")
my_notebook.add(my_frame6, text="RFID")



def exit_window():
    root.destroy()
    exit()

def show_logs():
    my_notebook.select(1)
    
def show_auth():
    my_notebook.select(2)
    
def show_camera():
    my_notebook.select(3)
    
def show_FPS():
    my_notebook.select(4)


def show_RFID():
    my_notebook.select(5)
    
e = Entry(my_frame6, width = 50)   
 
def WriteRfid_Done():
    dataLabel = Label(my_frame6, text = "Data Received:"+ e.get())
    dataLabel.grid(row=3 ,column=3)
    
def Write_RFID():    
    e.grid(row=1 ,column=2)
      
def ReadRfid():
    instLabel = Label(my_frame6, text = "Please Place your card")
    instLabel.grid(row=4 ,column=2)    
    #label_id = Label( my_frame6, textvariable=id, relief=RAISED )
    #label_text = Label( my_frame6, textvariable=text, relief=RAISED )
    #label_id.grid(row=6 ,column=2)
    #label_text.grid(row=6 ,column=3)
    reader = SimpleMFRC522()
    
    try:
        id, text = reader.read()
        whitecard = "512344609911"
        bluetag = "111066076445"
        dataLabel = Label(my_frame6, text = "Data Received:"+ text)
        dataLabel.grid(row=5 ,column=2)
        
        if str(id) == bluetag :
            label_rfidRes = Label(my_frame6, text = "Accepted")
            label_rfidRes.grid(row=7 ,column=1)
            print('Accepted')
        else:
            label_rfidRes = Label(my_frame6, text = "Invalid User")
            label_rfidRes.grid(row=7 ,column=1)
            print('Invalid User')
        #print(text)
    finally:
        GPIO.cleanup()
        
def on_start():
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    current_time = current_time.split(":")
    #print(current_time)
    #print("########")
    
    col_list = ["Name", "MacID"]
    df = pd.read_csv("f.csv", usecols=col_list)
    response = requests.get('http://iotrest.herokuapp.com/api/devicefetcher')
    # print(response.json())
    macid = ''
    for i in response.json():
        loginTime = i["loginTime"].split(":")
        print(loginTime) 
        totalLogTime = int(loginTime[0])*3600 + int(loginTime[1])*60 + int(loginTime[2])
        totalCurrentTime = int(current_time[0])*3600 + int(current_time[1])*60 + int(current_time[2])
        if abs(totalCurrentTime-totalLogTime) <= 600:
            macid = i["macId"]
    
    count = 0
    for j in df.MacID:
        if j == macid:
            print("proceed"+macid)
            break
        else:
            count += 1
    
    if count == len(df):
        print("Abort Process")
    
    
def cam_capture():
    cam = cv2.VideoCapture(0)
    
    count = 0
    
    while True:
        ret, img = cam.read()
    
        cv2.imshow("Test", img)
    
        if not ret:
            break
    
        k=cv2.waitKey(1)
    
        if k%256==27:
            #For Esc key
            print("Close")
            break
        elif k%256==32:
            #For Space key
    
            print("Image "+str(count)+"saved")
            file='E:/PROJECTS/FACE/'+str(count)+'.jpg'
            cv2.imwrite(file, img)
            count +=1
    
    cam.release
    cv2.destroyAllWindows()

#face recognition for face_result button
#def cam_capture():
    


#exit Button
exit_button = Button(
        my_frame1,
        width=20,
        height=2,
        text="Exit",
        command=exit_window,
        padx=2,
        pady=2,
        relief=RAISED)
exit_button.grid(row=0 ,column=1)


AccessLog_button = Button(
        my_frame1,
        width=20,
        height=2,
        text="Console",
        command=on_start,
        padx=2,
        pady=2,
        relief=RAISED)
AccessLog_button.grid(row=0 ,column=2)



Authinticate_button = Button(
        my_frame1,
        width=20,
        height=2,
        text="Authinticate",
        command=show_auth,
        padx=2,
        pady=2,
        relief=RAISED)
Authinticate_button.grid(row=0 ,column=3)


Camera_button = Button(
        my_frame3,
        width=20,
        height=2,
        text="Camera",
        command=show_camera,
        padx=2,
        pady=2,
        relief=RAISED)
Camera_button.grid(row=0 ,column=1)


RFID_button = Button(
        my_frame3,
        width=20,
        height=2,
        text="RFID",
        command=show_RFID,
        padx=2,
        pady=2,
        relief=RAISED)
RFID_button.grid(row=0 ,column=2)

FPS_button = Button(
        my_frame3,
        width=20,
        height=2,
        text="FPS",
        command=show_FPS,
        padx=2,
        pady=2,
        relief=RAISED)
FPS_button.grid(row=1 ,column=1)

Bluetooth_button = Button(
        my_frame3,
        width=20,
        height=2,
        text="Connect Bluetooth",
        command=show_auth,
        padx=2,
        pady=2,
        relief=RAISED)
Bluetooth_button.grid(row=1 ,column=2)


CamCapture_button = Button(
        my_frame4,
        width=20,
        height=2,
        text="CamCapture",
        command=cam_capture,
        padx=2,
        pady=2,
        relief=RAISED).pack()

FaceResult_button = Button(
        my_frame4,
        width=20,
        height=2,
        text="Result",
        command=cam_capture,
        padx=2,
        pady=2,
        relief=RAISED).pack()
    
READ_button = Button(
        my_frame6,
        width=20,
        height=2,
        text="READ",  
        command=ReadRfid,
        padx=2,
        pady=2,
        relief=RAISED)
READ_button.grid(row=0,column=1)


WRITE_button = Button(
        my_frame6,
        width=20,
        height=2,
        text="WRITE",
        command=Write_RFID,
        padx=2,
        pady=2,
        relief=RAISED)
WRITE_button.grid(row=1 ,column=1)

WriteRfid_done_button = Button(
        my_frame6,
        width=20,
        height=2,
        text="Write data",
        command=WriteRfid_Done,
        padx=2,
        pady=2,
        relief=RAISED)
WriteRfid_done_button.grid(row=3 ,column=2)

root.mainloop()