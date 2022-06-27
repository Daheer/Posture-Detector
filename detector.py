#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import cv2
import numpy as np
from IPython.display import display, Image
import ipywidgets as widgets
from fastai import *
import fastbook
from fastbook import *
from plyer import notification
from PIL import Image


# In[2]:


# fastbook.setup_book()


# In[3]:


posture_model = load_learner('posture_detector_model.pkl') # Load detector model fine-tuned on various sitting postures


# In[4]:


posture = widgets.Label()


# In[5]:


def notify(posture): # Sends system notification to report bad sitting posture
    notification.notify(title = 'Posture Notification', message = 'Your current posture is BAD, Please Fix!', app_icon = 'notify-icon.ico',timeout = 10) 


# In[6]:


#display(posture) 


# In[8]:


def startPostureDetection():
    try:
        detector = cv2.VideoCapture(0) # Launch camera
    except:
        print("Cannot Open Device")
    try:
        ret, frame = detector.read() # Store current position of the computer user
        count = 0
        while(ret == True):
            ret, frame = detector.read() # Store current position of the computer user
            posture.value = posture_model.predict(frame)[0] # Predict the user's posture
            if (posture.value == 'bad'):
                count += 1
                if count == 50:
                    notify(posture.value) # Only send reports of a bad posture when the user has been in that position 
                    count = 0             # for a significant while
            if not ret:
                detector.release() # Clean up memory
                print ("Released Video Resource")
                break            
    except KeyboardInterrupt:
        detector.release() # Clean up memory
        print("Released Video Resource from KeyboardInterrupt") 
    pass

startPostureDetection()


# In[ ]:




