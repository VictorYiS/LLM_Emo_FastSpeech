# LLM_Emo_FastSpeech
安装requirements.txt中的依赖包，可以安装符合自己的版本，不用按照我这个版本安装。

如果要训练自己的数据集，可以参考ESD的数据集准备，需要首先pre_align数据集，然后执行mfa操作(需要参照mfa官网下载好mfa工具)，然后再preprocess再训练。

```bash
python prepare_align.py config/ESD/preprocess.yaml
mfa model download acoustic english_us_arpa
mfa model download dictionary english_us_arpa
mfa align ./raw_data/ESD/ english_us_arpa english_us_arpa preprocessed_data/ESD/TextGrid
python preprocess.py -p config/ESD/preprocess.yaml
python train.py -p config/ESD/preprocess.yaml
```
需要生成带情感的音频，可以执行如下命令来使用预训练好的模型(需要事先在output/ckpt/ESD中放入模型文件)，在文件配置中更改text，说话人和情感：
训练好的模型:https://drive.google.com/file/d/1VU4KXx6IehDgaB1MooL1HBg3EG2WqAQN/view?usp=sharing
```bash
python generate_with_emotion.py
```
调用tts接口，更改text，说话人和情感：
```python
from generate_with_emotion import generate_emotions_args
# "Angry", "Sad", "Neutral", "Happy", "Surprise"
generate_emotions_args("Today is a good day", 1, "Happy")
```
如果需要使用预训练的gpt2模型，可以参考如下命令，目前还没实现注入情感，需要把model.safetensors和optimizer.pt放到gpt/dialogpt_friends_model/checkpoint-4536下面，文件链接:https://drive.google.com/file/d/1EEduisSNpwWcTTv7qgeAjlQODtVw9Zyv/view?usp=sharing, https://drive.google.com/file/d/1_mKkQGISWw7Y8oVywWBhKPoNjiWymCFo/view?usp=sharing：
```bash
from gpt.dialogpt_tune_dialouge_generate import generate_dialogue_with_emotion
generate_dialogue_with_emotion("I am happy")
```