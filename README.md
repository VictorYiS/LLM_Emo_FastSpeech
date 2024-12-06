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
需要生成带情感的音频，可以执行如下命令来使用预训练好的模型，在文件配置中更改text，说话人和情感：
```bash
python generate_with_emotion.py
```