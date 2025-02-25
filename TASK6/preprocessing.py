# -*- coding: utf-8 -*-

# Commented out IPython magic to ensure Python compatibility.
import cv2     # for capturing videos
import math   # for mathematical operations
import matplotlib.pyplot as plt    # for plotting the images
# %matplotlib inline
import pandas as pd
from keras.preprocessing import image   # for preprocessing the images
import numpy as np    # for mathematical operations
from skimage.transform import resize   # for resizing images
import os

from google.colab import drive
drive.mount('/content/drive')

"""##Capture Images from mp4"""

def video_to_frames(videoFile, path_output_dir):
  cap = cv2.VideoCapture(videoFile)   # capturing the video from the given path
  frameRate = cap.get(5) #frame rate (frames per sec)
  print(frameRate)
  x=1
  video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
  print ("Number of frames: ", video_length)
  count = 5258
  #Fire video 1, 461, 890 , 1375, 1863, 2364, 2486, 2974, 3289, 3775, 4060 is last entry
  #not fire 0, 918, 1653, 2148,2810, 3434,4064, 4585, 5258, 5466 is last entry
  while(cap.isOpened()):
      frameId = cap.get(1) #current frame number
      ret, frame = cap.read() 
      if (ret != True):
          break
      if (frameId % 4 == 0):
          filename ="frame%d.jpg" % count;
          cv2.imwrite(os.path.join(path_output_dir, 'frame%d.jpg') % count, frame) #save frames as jpg
          count +=1
  cap.release()
  cv2.destroyAllWindows()
  print ("Done!")

video_to_frames('/content/drive/My Drive/Videos/Not Fire/2020-01-21 20-34-43.mkv', '/content/drive/My Drive/data/notfire')

"""##Plan

plan:
- get list of names of images and put into a text file
- label each with fire or no fire
- label each with video it came from

- convert images to black and white
- shrink images to 256 x 256
- (change the images (rotation, zoom, etc.))

##Directory
"""

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

dirName = '/content/drive/My Drive/data/fire';
# Get the list of all files in directory tree at given path
listOfFiles = getListOfFiles(dirName)

dirName = '/content/drive/My Drive/data/notfire';
# Get the list of all files in directory tree at given path
listOfFilesNF = getListOfFiles(dirName)

display(len(listOfFilesNF), len(listOfFiles))

zeros = [0]*5318

df = pd.DataFrame({'path':listOfFilesNF, 'fire':zeros})
print (df)

ones = [1]*4255

df1 = pd.DataFrame({'path':listOfFiles, 'fire':ones})
print (df1)

df.append(df1, ignore_index = True)

"""##Preprocessing"""

path = '/content/drive/My Drive/data/fire/frame780.jpg'
#load image and convert to gray
img = cv2.imread(path)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

from matplotlib.pyplot import imshow

def show_image(img):
  imshow(np.asarray(img))

from random import shuffle

training_data = []
fire_dir ='/content/drive/My Drive/data/fire';

for img in os.listdir(fire_dir):
    label = [1, 0]
    path = os.path.join(fire_dir,img)
    #print(path)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (1280, 720)) 
    crop_img = img[100:700, 0:1280]
    img = cv2.resize(crop_img, (0,0), fx=0.5, fy=0.5)
    show_image(img)
    training_data.append([np.array(img), label])
    
shuffle(training_data)
print('Fire done!')

len(training_data)

np.save('/content/drive/My Drive/old_data/data1.npy', training_data)

notfire_dir = '/content/drive/My Drive/data/notfire';

for img in os.listdir(notfire_dir):
    label = [0, 1]
    path = os.path.join(notfire_dir,img)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    show_image(img)
    img = cv2.resize(img, (1280, 720)) 
    crop_img = img[100:700, 0:1280]
    img = cv2.resize(crop_img, (0,0), fx=0.5, fy=0.5)
    show_image(img)
    training_data.append([np.array(img), label])

shuffle(training_data)
print('NotFire done!')

np.save('/content/drive/My Drive/old_data/data2.npy', training_data)

len(training_data)

np.save('/content/drive/My Drive/data/datafinal.npy', training_data)
print('Data saved.')

print('\n', training_data)
print("\nScript of preprocessing done.")