## Download IEMOCAP Database

Download the IEMOCAP database and set `corpus_path` in `config/IEMOCAP/preprocess.yaml`. You must get the permission to download the dataset.

```bash
pip install -r requirement_iemocap.txt

python3 prepare_data.py --extract_audio -p config/IEMOCAP/preprocess.yaml

python3 prepare_align.py config/IEMOCAP/preprocess.yaml

python3 prepare_data.py --extract_lexicon -p config/IEMOCAP/preprocess.yaml

mfa align ./raw_data/IEMOCAP/session1 ./lexicon/iemocap-lexicon.txt ./montreal-forced-aligner/iemocap-aligner.zip preprocessed_data/IEMOCAP/TextGrid --speaker_characters prosodylab -j 8 --clean