#!/bin/python3
# import the required modules
import cv2
# import matplotlib.pyplot as plt
from deepface import DeepFace

total={
    'angry': 0,
    'disgust': 0,
    'fear': 0,
    'happy': 0,
    'sad': 0,
    'surprise': 0,
    'neutral': 0
}
total_avg={
    'angry': 0,
    'disgust': 0,
    'fear': 0,
    'happy': 0,
    'sad': 0,
    'surprise': 0,
    'neutral': 0
}
num_songs = 0

def print_status(stats):
    val = f"Current Frame Status: Primary: {str(stats[0]['dominant_emotion'])}\n"
    for emot in stats[0]['emotion']:
        val += f"{emot}: {str(stats[0]['emotion'][emot])}\n"
    print(val, end="")
    print('---------------------------------------------')

def next_song(s_total):
    num_songs += 1

    for elem in s_total.keys():
        total[elem] += s_total[elem]
    
    for elem in total_avg.keys():
        total_avg[elem] = total[elem] / num_songs


def main():
    song_total={
        'angry': 0,
        'disgust': 0,
        'fear': 0,
        'happy': 0,
        'sad': 0,
        'surprise': 0,
        'neutral': 0
    }

    song_avg={
        'angry': 0,
        'disgust': 0,
        'fear': 0,
        'happy': 0,
        'sad': 0,
        'surprise': 0,
        'neutral': 0
    }

    song_frame_num = 0

    while(True):
        # Create a VideoCapture object to access the webcam
        cap = cv2.VideoCapture(0)

        # Check if the webcam is opened successfully
        if not cap.isOpened():
            print("Cannot access the webcam")
            exit()

        # Read a frame from the webcam
        ret, frame = cap.read()

        # Check if the frame is successfully read
        if not ret:
            print("Cannot capture a frame")
            exit()

        # Release the VideoCapture object and close all windows
        cap.release()
        cv2.destroyAllWindows()

        # read image
        img=frame

        # call imshow() using plt object
        # plt.imshow(img[:,:,::-1])

        # display that image
        # plt.show()

        # storing the result
        result = DeepFace.analyze(img,actions=['emotion'])

        # print result
        # print(result)

        # print(result[0])
        # print('dominant emotion: ' + str(result[0]['dominant_emotion']))
        # print('angry: ' + str(result[0]['emotion']['angry']))
        # print('disgust: ' + str(result[0]['emotion']['disgust']))
        # print('fear: ' + str(result[0]['emotion']['fear']))
        # print('happy: ' + str(result[0]['emotion']['happy']))
        # print('sad: ' + str(result[0]['emotion']['sad']))
        # print('surprise: ' + str(result[0]['emotion']['surprise']))
        # print('neutral: ' + str(result[0]['emotion']['neutral']))
        # print('---------------------------------------------')
        print_status(result)
        song_frame_num += 1
        for emot in result[0]['emotion']:
            song_total[emot] += result[0]['emotion'][emot]
            song_avg[emot] = song_total[emot]/song_frame_num
        # song_total['angry'] = song_total['angry']+result[0]['emotion']['angry']
        # song_total['disgust'] = song_total['disgust']+result[0]['emotion']['disgust']
        # song_total['fear'] = song_total['fear']+result[0]['emotion']['fear']
        # song_total['happy'] = song_total['happy']+result[0]['emotion']['happy']
        # song_total['sad'] = song_total['sad']+result[0]['emotion']['sad']
        # song_total['surprise'] = song_total['surprise']+result[0]['emotion']['surprise']
        # song_total['neutral'] = song_total['neutral']+result[0]['emotion']['neutral']
        # song_frame_num = song_frame_num + 1
        # song_avg['angry'] = song_total['angry']/song_frame_num
        # song_avg['disgust'] = song_total['disgust']/song_frame_num
        # song_avg['fear'] = song_total['fear']/song_frame_num
        # song_avg['happy'] = song_total['happy']/song_frame_num
        # song_avg['sad'] = song_total['sad']/song_frame_num
        # song_avg['surprise'] = song_total['surprise']/song_frame_num
        # song_avg['neutral'] = song_total['neutral']/song_frame_num

        print(song_avg)
        print(song_total)

main()
