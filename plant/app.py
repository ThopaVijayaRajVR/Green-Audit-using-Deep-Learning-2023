
import requests
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
from tensorflow.python.keras.backend import set_session

app = Flask(__name__)

#load the plant models
model=load_model(r"plant.h5",compile=False)


#home page
@app.route('/')
def home():
    return render_template('home.html')

#prediction page
@app.route('/prediction')
def prediction():
    return render_template('predict.html')


@app.route('/predict',methods=['POST'])		
def predict():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        img = image.load_img(file_path, target_size=(64, 64))
        
        x = image.img_to_array(img) # Converting image into array
        x = np.expand_dims(x,axis=0) # expanding Dimensions
        pred = np.argmax(model.predict(x)) # Predicting the higher probablity index
        op = ['aloevara and it produce approximately 132 milligrams of oxygen daily', 'mango  and it produce around 5 to 9 kilogram of oxygen daily', 'nagfani', 'neem and it produce around 5 to 9 kilogram of oxygen daily', 'tulsi and it produce approximately 140 milligrams of oxygen daily'] # Creating list
        op[pred]
        result = op[pred]
        result='The predicted output is {}'.format(str(result))
        print(result)
    return render_template('predict.html',text=result)
@app.route('/check', methods=['POST'])
def check():
    num = int(request.form['numberInput'])
    result = ""

    if num == 1:
        result = "The oxygen produced by the plant is not sufficient we need to grow 3 plants"
    elif num <= 10:
        result = "The oxygen produced by the plant is not sufficient we need to grow 70 to 80 plants"
    elif num <= 20:
        result = "The oxygen produced by the plant is not sufficient we need to grow 120 to 150 plants"
    else:
        result = "The oxygen produced by the plant is not sufficient"

    return render_template('predict.html', result=result)
if __name__ == "__main__":
    app.run(debug=True)
 