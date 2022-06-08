import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras_preprocessing import image


def class_convert(classess):
    pred=[]
    for i in classess:
        if i ==0:
            pred.append('Cardboard')
        elif i==1:
            pred.append('metal_aluminum')
        elif i==2:
            pred.append('paper_container')
        elif i==3:
            pred.append('Plastic')
        elif i==4:
            pred.append('Trash')
    return pred

model = tf.keras.models.load_model('./model_v3.h5/')


def classify_image(my_image):
  custom_image = image.load_img(my_image, target_size=(224, 224))
  img_array = image.img_to_array(custom_image)
  processed_img = keras.applications.efficientnet_v2.preprocess_input(img_array).astype(np.float32)
  swapped = np.moveaxis(processed_img, 0,1)
  arr4d = np.expand_dims(swapped, 0)
  new_prediction= class_convert(np.argmax(model.predict(arr4d), axis = -1))   #用class_convert進行文字分類
  print('Your item is: ', new_prediction[0])


classify_image('./test_images/metal_test.jpeg')
classify_image('./test_images/123.jpg')



