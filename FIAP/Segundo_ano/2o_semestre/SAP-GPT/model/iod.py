from ultralytics import YOLO
import cv2
import math 
import streamlit as st
import os
from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("/Users/henricobela/Desktop/Estudos/Challenge/SAP-GPT/model/model/newmodel/keras_model.h5", compile=False)

# Load the labels
class_names = open("/Users/henricobela/Desktop/Estudos/Challenge/SAP-GPT/model/model/newmodel/labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
# camera = cv2.VideoCapture(0)


run = st.checkbox("Run")
FRAME_WINDOW = st.image([])
cap = cv2.VideoCapture(1)
TH_CONFIDENCE = 0.1

# model = YOLO("/Users/henricobela/Desktop/Estudos/Challenge/SAP-GPT/model/model.pt")
# model = YOLO("/home/henrico/Github/SAP-GPT/model/model.pt")

# classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
#               "traffic light", "fire hydrant", "stop sign", "parkpiping meter", "bench", "bird", "cat",
#               "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
#               "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
#               "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
#               "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
#               "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
#               "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
#               "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
#               "teddy bear", "hair drier", "toothbrush", "glasses", "wallet",
#               ]


# with open("yolo_cfg/yolov3.txt", "r") as file:  
#     classNames = file.readlines()


# while run:
#     success, img = cap.read()
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = model(img, stream=True)

#     for r in results:
#         boxes = r.boxes

#         for box in boxes:
#             confidence = math.ceil((box.conf[0]*100))/100

#             if confidence > TH_CONFIDENCE:

#                 x1, y1, x2, y2 = box.xyxy[0]
#                 x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

#                 cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

#                 cls = int(box.cls[0])
#                 print("Class name -->", classNames[cls])
#                 os.system("clear")
                
                

#                 org = [x1, y1]
#                 font = cv2.FONT_HERSHEY_SIMPLEX
#                 fontScale = 1
#                 color = (255, 0, 0)
#                 thickness = 2
#                 org_conf = [x2, y2]

#                 cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
#                 cv2.putText(img, f"{confidence}", org_conf, font, fontScale, color, thickness)

#     FRAME_WINDOW.image(img)







while run:
    # Grab the webcamera's image.
    ret, image = cap.read()
    img = image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    label = "Produto: {}\nConf: {}%".format(class_name[2:], str(np.round(confidence_score * 100))[:-2])
    img = cv2.putText(img, label, (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    
    FRAME_WINDOW.image(img)
