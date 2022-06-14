import time
from pymata4 import pymata4
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras_preprocessing import image


def class_convert(classess):
    pred=[]
    for i in classess:
        if i ==0:
            pred.append('紙類')
        elif i==1:
            pred.append('鐵鋁罐')
        elif i==2:
            pred.append('紙容器')
        elif i==3:
            pred.append('塑膠類')
        elif i==4:
            pred.append('垃圾')
    return pred

model = tf.keras.models.load_model('./model_v3.h5/')


triggerPin = 11
echo_Pin = 12
Cardboard = 10
can = 9
paper_container = 8
Plastic = 7
Trash = 6

def classify_image(my_image):
    custom_image = image.load_img(my_image, target_size=(224, 224))
    img_array = image.img_to_array(custom_image)
    processed_img = keras.applications.efficientnet.preprocess_input(img_array).astype(np.float32)
    swapped = np.moveaxis(processed_img, 0,1)
    arr4d = np.expand_dims(swapped, 0)
    new_prediction = class_convert(np.argmax(model.predict(arr4d), axis = -1))   #用class_convert進行文字分類
    print('Your item is: ', new_prediction[0])
    if new_prediction[0] == "紙類":
        board.set_pin_mode_digital_output(Cardboard)
        board.digital_write(Cardboard, 1)
        print("------------")
        time.sleep(10)
        board.digital_write(Cardboard, 0)
    if new_prediction[0] == "鐵鋁罐":
        board.set_pin_mode_digital_output(can)
        board.digital_write(can, 1)
        print("------------")
        time.sleep(10)
        board.digital_write(can, 0)
    if new_prediction[0] == "紙容器":
        board.set_pin_mode_digital_output(paper_container)
        board.digital_write(paper_container, 1)
        print("------------")
        time.sleep(10)
        board.digital_write(paper_container, 0)
    if new_prediction[0] == "塑膠類":
        board.set_pin_mode_digital_output(Plastic)
        board.digital_write(Plastic, 1)
        print("------------")
        time.sleep(10)
        board.digital_write(Plastic, 0)
    if new_prediction[0] == "垃圾":
        board.set_pin_mode_digital_output(Trash)
        board.digital_write(Trash, 1)
        print("------------")
        time.sleep(10)
        board.digital_write(Trash, 0)

diffdis = [0]

board = pymata4.Pymata4()

def the_callback(data):
    print("距離:", data[2],";", "距離差:", diffdis[0]-data[2])
    if data[2] < 60 and (diffdis[0] - data[2]) > 20:
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, frame = cap.read()
            cv2.imwrite("Me.png", frame)
            del (cap)
            classify_image('./Me.png')
    diffdis[0] = data[2]

board.set_pin_mode_sonar(triggerPin, echo_Pin, the_callback)

while True:
    try:
        time.sleep(5)
        board.sonar_read(triggerPin)
    except Exception:
        board.shutdown()

