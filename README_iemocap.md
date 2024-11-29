## Download IEMOCAP Database

Download the IEMOCAP database and set `corpus_path` in `config/IEMOCAP/preprocess.yaml`. You must get the permission to download the dataset.

```bash
pip install -r requirement_iemocap.txt

python3 prepare_data.py --extract_audio -p config/IEMOCAP/preprocess.yaml

python3 prepare_align.py config/IEMOCAP/preprocess.yaml

python3 prepare_data.py --extract_lexicon -p config/IEMOCAP/preprocess.yaml

conda create -n aligner -c conda-forge montreal-forced-aligner
conda activate aligner
mfa model download acoustic english_mfa
mfa align ./raw_data/IEMOCAP/session1 ./lexicon/iemocap-lexicon.txt english_mfa preprocessed_data/IEMOCAP/TextGrid -j 8 --clean