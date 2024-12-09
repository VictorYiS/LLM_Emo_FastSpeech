from transformers import pipeline

import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
dict_map = {'joy': 'Happy', 'sadness': 'Sad', 'anger': 'Angry', 'fear': 'Neutral', 'neutral': 'Neutral',
            'surprise': 'Surprise', 'disgust': 'Angry'}
classifier = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier", device=0)


def gen_emotion(text):
    emotion = classifier(text)
    return dict_map[emotion[0]['label']]


# gen_emotion("I am disgust")
