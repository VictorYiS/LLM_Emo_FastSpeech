import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset
from datasets import Dataset


def parse_conversations(file_path):
    """Parse Friends conversation text file into dialogue format."""
    conversations = []
    current_conversation = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                if current_conversation:
                    conversations.append('\n'.join(current_conversation))
                    current_conversation = []
                continue

            current_conversation.append(line)

        # Add last conversation if exists
        if current_conversation:
            conversations.append('\n'.join(current_conversation))

    return conversations


print("Load pre-trained model and tokenizer")

# Load pre-trained model and tokenizer
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# device = torch.device("cpu")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Set pad token if not already set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = model.config.eos_token_id


print("Start parse conversations")

# Load conversations from txt file
conversations = parse_conversations('./friends_script/cleaned_dialogues_capical.txt')

print("Number of conversations:", len(conversations))

dataset = Dataset.from_dict({'conversation': conversations})

print("Dataset complete")


# Preprocessing function
def preprocess_function(examples):
    inputs = tokenizer(
        examples['conversation'],
        truncation=True,
        padding='max_length',
        max_length=512,
        return_attention_mask=True
    )
    inputs['labels'] = inputs['input_ids'].copy()
    return inputs


# Prepare dataset
processed_dataset = dataset.map(
    preprocess_function,
    batched=True
)

# Training arguments
training_args = TrainingArguments(
    output_dir='./dialogpt_friends_model',
    num_train_epochs=6,
    per_device_train_batch_size=4,
    save_steps=10_000,
    save_total_limit=2,
    learning_rate=5e-5,
    weight_decay=0.01,
    logging_dir='./logs',
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=processed_dataset
)

# Start training
trainer.train()

# Save final model
trainer.save_model('./dialogpt_friends_model_final_new')