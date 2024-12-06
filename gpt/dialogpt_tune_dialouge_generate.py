import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import re
from transformers import pipeline


# Load fine-tuned model and tokenizer
model_path = './dialogpt_friends_model/checkpoint-4536'
model = AutoModelForCausalLM.from_pretrained(model_path)

model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)

classifier = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier")

# Set pad token to avoid warnings
model.config.pad_token_id = model.config.eos_token_id

def generate_dialogue(initial_context, max_length=300, num_return_sequences=5):
    """
    Generate dialogue continuation based on initial context.

    Args:
    - initial_context (str): Starting conversation context.
    - max_length (int): Maximum total length of generated sequence.
    - num_return_sequences (int): Number of different dialogue variations to generate.

    Returns:
    List of generated dialogue continuations.
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    # Tokenize input
    input_ids = tokenizer.encode(initial_context, return_tensors='pt').to(device)

    # Generate dialogue
    output = model.generate(
        input_ids,
        max_length=max_length,
        num_return_sequences=num_return_sequences,
        no_repeat_ngram_size=2,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        do_sample=True  # Enable sampling to generate multiple sequences
    )

    # Decode and return generated dialogues
    return [tokenizer.decode(seq, skip_special_tokens=True) for seq in output]


def extract_dialogues(text):
    """
    Extract dialogues by separating character names and their full dialogues.

    Args:
    - text (str): Multi-line dialogue text with character names.

    Returns:
    - List[dict]: A list of dictionaries, each containing 'character' and 'sentence'.
    """
    dialogue_list = []

    # Split the text into lines
    lines = text.strip().split("\n")

    for line in lines:
        # Match lines with the pattern "Character: Sentence"
        match = re.match(r"^(.*?):\s*(.+)$", line)
        if match:
            character, dialogue = match.groups()
            dialogue_list.append({"character": character.strip(), "sentence": dialogue.strip()})

    return dialogue_list


def emotion_classify(dialogue_data):
    for dialogue in dialogue_data:
        emotion = classifier(dialogue['sentence'])
        dialogue['emotion'] = emotion
    return dialogue_data


# Example usage
if __name__ == "__main__":
    # Initial conversation context
    initial_context = "Monica: I hate cleaning the house."

    # Generate dialogues
    generated_dialogues = generate_dialogue(initial_context)

    # Print generated dialogues
    for i, dialogue in enumerate(generated_dialogues, 1):
        # print(f"Generated Dialogue {i}:\n{dialogue}")
        dialogue_data = extract_dialogues(dialogue)
        # print(dialogue_data)
        dialogue_data_with_emotion = emotion_classify(dialogue_data)
        print(dialogue_data_with_emotion)

