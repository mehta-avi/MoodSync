#!/bin/python3
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play_music', methods=['POST'])
def play_music():
    # Add your play_music() function logic here
    print("testing")
    return 'Music playback started.'

@app.route('/pause_music', methods=['POST'])
def pause_music():
    # Add your pause_music() function logic here
    return 'Music playback paused.'

@app.route('/skip_music', methods=['POST'])
def skip_music():
    # Add your skip_music() function logic here
    return 'Skipped to the next song.'

import base64
from PIL import Image
from io import BytesIO
import cv2
import numpy
from deepface import DeepFace
@app.route('/eval_frame', methods=['POST'])
def eval_frame():
    print("Eval frame running")
    # print(request)
    base64_data = request.form.get('frameData')
    # decode base64-encoded image data
    image_data = base64_data.split(",")[1]
    binary_data = base64.b64decode(image_data)

    # create PIL image object from binary data
    image = Image.open(BytesIO(binary_data))

    # save the image as a PNG file
    # image.save("image.png", "PNG")
    img = numpy.array(image)
    result = DeepFace.analyze(img,actions=['emotion'])
    # print_status(result)

    res = {
        "success": True,
        "dominant_emotion": result[0]['dominant_emotion'],
        "emotions": result[0]['emotion']
    }
    return res

if __name__ == '__main__':
    app.run(debug=True)
