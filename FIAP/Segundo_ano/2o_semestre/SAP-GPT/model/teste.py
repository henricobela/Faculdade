from ultralytics import YOLO
import cv2
import math 
import streamlit as st
import os
import tensorflow as tf
from PIL import Image
import numpy as np
from keras.applications.vgg16 import preprocess_input


run = st.checkbox("Run")
FRAME_WINDOW = st.image([])
cap = cv2.VideoCapture(1)
TH_CONFIDENCE = 0.1

new_model = tf.keras.models.load_model('/Users/henricobela/Downloads/model/model-refri.h5')


while run:
    success, img = cap.read()
    img_to_predict = Image.fromarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    validation_batch = np.stack([preprocess_input(np.array(img_to_predict.resize((224,224))))])
    preds = new_model.predict(validation_batch)

    coca_conf = preds[0,0] * 100
    fanta_conf = preds[0,1] * 100

    print("{:.0f}% Coca, {:.0f}% Fanta".format(coca_conf, fanta_conf))

    label = "{:.0f}% Coca, {:.0f}% Fanta".format(coca_conf, fanta_conf)
    img = cv2.putText(img, label, (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)


    FRAME_WINDOW.image(img)
