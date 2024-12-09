import os

import numpy as np
import torch
import yaml

from synthesize import synthesize, generate_synthesis_args, preprocess_english, preprocess_mandarin
from text.emotion import process_emotion
from utils.model import get_model, get_vocoder

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def generate_emotions_args(text="Stop shouting at me with 8 again, you bastard", speaker_id=8, emotion="Surprise"):
    args_dict = {
        "restore_step": 18000,
        "mode": "single",
        "preprocess_config": "./config/ESD/preprocess.yaml",
        "model_config": "./config/ESD/model.yaml",
        "train_config": "./config/ESD/train.yaml",
        # 这里修改文本
        "text": text,
        # 这里修改说话者
        "speaker_id": speaker_id,
        # 这里修改情感
        "emotion": emotion
    }
    args_list = []
    for key, value in args_dict.items():
        args_list.append(f"--{key}")
        args_list.append(str(value))
    args = generate_synthesis_args(args_list)
    return args

def generate_run():
    os.makedirs("./output/ckpt/ESD", exist_ok=True)
    os.makedirs("./output/result/ESD", exist_ok=True)
    args = generate_emotions_args()
    preprocess_config = yaml.load(
        open(args.preprocess_config, "r"), Loader=yaml.FullLoader
    )
    model_config = yaml.load(open(args.model_config, "r"), Loader=yaml.FullLoader)
    train_config = yaml.load(open(args.train_config, "r"), Loader=yaml.FullLoader)
    configs = (preprocess_config, model_config, train_config)

    # Get model
    model = get_model(args, configs, device, train=False)

    # Load vocoder
    vocoder = get_vocoder(model_config, device)

    ids = raw_texts = [args.text[:100]]
    speakers = np.array([args.speaker_id])
    emotion = np.array([process_emotion(args.emotion)])
    print(f"emotion={emotion}")
    if preprocess_config["preprocessing"]["text"]["language"] == "en":
        texts = np.array([preprocess_english(args.text, preprocess_config)])
    elif preprocess_config["preprocessing"]["text"]["language"] == "zh":
        texts = np.array([preprocess_mandarin(args.text, preprocess_config)])
    text_lens = np.array([len(texts[0])])
    batchs = [(ids, raw_texts, speakers, emotion, texts, text_lens, max(text_lens))]


    control_values = args.pitch_control, args.energy_control, args.duration_control

    synthesize(model, args.restore_step, configs, vocoder, batchs, control_values)


def main():
    generate_run()


if __name__ == "__main__":
    main()
