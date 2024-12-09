from transformers import pipeline

classifier = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier")
def gen_emotion(text):
    emotion = classifier(text)
    print(emotion)

# gen_emotion("I am happy")