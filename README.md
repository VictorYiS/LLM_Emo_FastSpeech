# LLM_Emo_FastSpeech
You can install the dependencies listed in the requirements.txt file using versions that suit your needs; there's no need to stick to the exact versions I used.

If you want to train on your own dataset, you can refer to the dataset preparation process of ESD. First, pre-align the dataset, then perform the MFA operation (you need to download the MFA tool from the official MFA website), and finally preprocess the data before training.

```bash
python prepare_align.py config/ESD/preprocess.yaml
mfa model download acoustic english_us_arpa
mfa model download dictionary english_us_arpa
mfa align ./raw_data/ESD/ english_us_arpa english_us_arpa preprocessed_data/ESD/TextGrid
python preprocess.py -p config/ESD/preprocess.yaml
python train.py -p config/ESD/preprocess.yaml
```
To generate emotion-infused audio, you can use the following command to utilize the pre-trained model (make sure to place the model files in output/ckpt/ESD beforehand). Update the file configuration to modify the text, speaker, and emotion:

Pre-trained model:https://drive.google.com/file/d/1VU4KXx6IehDgaB1MooL1HBg3EG2WqAQN/view?usp=sharing
```bash
python generate_with_emotion.py
```
Call the TTS interface and modify the text, speaker, and emotion:
```python
from generate_with_emotion import generate_emotions_args
# "Angry", "Sad", "Neutral", "Happy", "Surprise"
generate_emotions_args("Today is a good day", 1, "Happy")
```
If you want to use the pre-trained GPT-2 model, you can refer to the following command. Currently, emotion injection is not implemented. Place model.safetensors and optimizer.pt in the directory gpt/dialogpt_friends_model/checkpoint-4536.

File links::https://drive.google.com/file/d/1EEduisSNpwWcTTv7qgeAjlQODtVw9Zyv/view?usp=sharing, https://drive.google.com/file/d/1_mKkQGISWw7Y8oVywWBhKPoNjiWymCFo/view?usp=sharing：
```bash
from gpt.dialogpt_tune_dialouge_generate import generate_dialogue_with_emotion
generate_dialogue_with_emotion("I am happy")
```