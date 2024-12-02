import csv
import json
import os
import re

import librosa
import numpy as np
from scipy.io import wavfile
from tqdm import tqdm

from text import _clean_text


def rename_files(config):
    in_dir = config["path"]["corpus_path"]
    name_mapping_path = os.path.join(in_dir, "name_mapping.json")
    # Load existing name mapping if it exists
    if os.path.exists(name_mapping_path):
        with open(name_mapping_path, "r") as json_file:
            name_mapping = json.load(json_file)
        counter = len(name_mapping)
    else:
        name_mapping = {}
        counter = 0
    for speaker in os.listdir(in_dir):
        print(f"speaker={speaker}")
        speaker_path = os.path.join(in_dir, speaker)
        if not os.path.isdir(speaker_path):
            continue
        for file_name in os.listdir(os.path.join(in_dir, speaker)):
            if file_name[-4:] != ".wav":
                continue

            base_name = file_name[:-4]
            wav_path = os.path.join(speaker_path, "{}.wav".format(base_name))

            # Check if the file name matches the required format
            if not re.match(rf"{speaker}-\d{{4}}", base_name):
                new_base_name = f"{speaker}-{{:04d}}".format(counter)
                counter += 1

                new_wav_path = os.path.join(speaker_path, "{}.wav".format(new_base_name))

                os.rename(wav_path, new_wav_path)

                name_mapping[base_name] = new_base_name

            else:
                new_base_name = base_name

            # Save the name mapping to a JSON file
        with open(os.path.join(in_dir, "name_mapping.json"), "w") as json_file:
            json.dump(name_mapping, json_file, indent=4)

        csv_file_path = os.path.join(in_dir, f"{speaker}_audio_emotions.csv")
        if not os.path.exists(csv_file_path):
            print("No CSV file found for speaker", speaker)
            continue

        if os.path.exists(csv_file_path):
            # Check the file permissions
            if not os.access(csv_file_path, os.W_OK):
                print(f"File {csv_file_path} is not writable. Changing permissions...")
                os.chmod(csv_file_path, 0o666)  # Change the file permissions to be writable
        else:
            print(f"File {csv_file_path} does not exist.")
        # Read and update the CSV file in place
        with open(csv_file_path, "r", newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            rows = list(reader)

        with open(csv_file_path, "w", newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            for row in rows:
                if row[0][:-4] in name_mapping:
                    row[0] = (name_mapping[row[0][:-4]] + '.wav')
                writer.writerow(row)


def extract_lexicon(config):
    pass


def apply_fixed_text(config):
    pass


def prepare_align(config):
    in_dir = config["path"]["corpus_path"]
    out_dir = config["path"]["raw_path"]
    sampling_rate = config["preprocessing"]["audio"]["sampling_rate"]
    max_wav_value = config["preprocessing"]["audio"]["max_wav_value"]
    cleaners = config["preprocessing"]["text"]["text_cleaners"]
    for speaker in tqdm(os.listdir(in_dir)):
        speaker_path = os.path.join(in_dir, speaker)
        if not os.path.isdir(speaker_path):
            continue
        with open(os.path.join(in_dir, f"{speaker}_audio_emotions.csv"), encoding="utf-8") as f:
            for line in tqdm(f):
                parts = line.strip().split("|")
                base_name = parts[0][:-4]
                text = parts[1]
                text = _clean_text(text, cleaners)

                wav_path = os.path.join(in_dir, speaker, "{}.wav".format(base_name))
                if os.path.exists(wav_path):
                    os.makedirs(os.path.join(out_dir, speaker), exist_ok=True)
                    wav, _ = librosa.load(wav_path, sr=sampling_rate)
                    wav = wav / max(abs(wav)) * max_wav_value
                    wavfile.write(
                        os.path.join(out_dir, speaker, "{}.wav".format(base_name)),
                        sampling_rate,
                        wav.astype(np.int16),
                    )
                    with open(
                            os.path.join(out_dir, speaker, "{}.lab".format(base_name)),
                            "w",
                    ) as f1:
                        f1.write(text)
