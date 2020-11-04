# -*- coding: utf-8 -*-

import tensorflow as tf 
from PIL import Image
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

model = tf.keras.models.load_model('D:/Project/M/project2.h5') 

UPLOAD_FOLDER = 'D:/Project/project/TempFile'
ALLOWED_EXTENSIONS = set(['wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 
                                   filename))
            return redirect(url_for('analysis',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route("/project/<filename>")
def analysis(filename):
    picPath = 'D:/Project/project/1.png' #路徑待修改
    y, sr = librosa.load("D:/Project/project/TempFile/"+filename, sr=44100) #載入音檔 #待修改
    melspec = librosa.feature.melspectrogram(y, sr, n_fft=1024, hop_length=512, n_mels=128)
    logmelspec = librosa.power_to_db(melspec)
    plt.figure()
    librosa.display.specshow(logmelspec, sr=sr, x_axis='time', y_axis='mel')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.tight_layout()
    plt.savefig(picPath)
    testImg = []
    im=Image.open(picPath)
    image = im.resize((144,216), Image.BILINEAR)
    testImg.append(np.array(image))
    TestImg = np.array(testImg).astype('float32') / 255.0  
    result = model.predict(TestImg)
    ans=0
    if result[0,0] >0.7:
        #ans="this file is OK" 
        ans="0"
        print('this file is OK')
        print('0 的機率是',result[0,0])
        print('1 的機率是',result[0,1])
    else:
        #ans="this file is fail"
        ans="1"
        print('this file is fail')
        print('0 的機率是',result[0,0])
        print('1 的機率是',result[0,1])
    delect(picPath)
    return ans

def delect(picPath):
    try:
        os.remove(picPath)
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")
        
@app.route("/")
def hello():
    return "765765!"

if __name__ == "__main__":
    app.run()