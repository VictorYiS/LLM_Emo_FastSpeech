import numpy as np

valid_emotions = ["angry", "calm", "disgust", "fearful", "happy", "neutral", "sad", "surprised"]


def process_emotion(emotion):
    if emotion not in valid_emotions:
        emotion = "neutral"
    return valid_emotions.index(emotion)

