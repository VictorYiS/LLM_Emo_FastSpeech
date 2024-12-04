import numpy as np

valid_emotions = ["Angry", "Sad", "Neutral", "Happy", "Surprise"]
# valid_emotions = ["angry", "calm", "disgust", "fearful", "happy", "neutral", "sad", "surprised"]


def process_emotion(emotion):
    if emotion not in valid_emotions:
        print(f"Emotion {emotion} not valid. Setting to Neutral.")
        emotion = "Neutral"
    return valid_emotions.index(emotion)

