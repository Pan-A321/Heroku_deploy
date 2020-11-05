# -*- coding: utf-8 -*-

#import tensorflow as tf 
from PIL import Image
#import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
        
@app.route("/", methods=['GET', 'POST'])
def hello():
    return "765765!"

if __name__ == "__main__":
    app.run()