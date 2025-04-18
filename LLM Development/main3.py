import torch
import wikipediaapi
from datasets import Dataset
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling, pipeline

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_name = "gpt2"
output_dir = "./gpt2-finetuned"
wiki_pages = ["Python (programming language)"]
generation_prompt = "Python is"
max_length_generation = 150

tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name).to(device)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = model.config.eos_token_id

base_outputs = pipeline('text-generation', model=model, tokenizer=tokenizer, device=device)(
    generation_prompt,
    max_length=max_length_generation,
    pad_token_id=tokenizer.eos_token_id
)

wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI, user_agent="MyScript/1.0")
text = ""
for title in wiki_pages:
    page = wiki.page(title)
    if page.exists():
        t = page.text.replace("\n\n", "\n").strip()
        if len(t) > 100:
            text += t + " "
text = text.strip()

tokenized_text = tokenizer(text)["input_ids"]
block_size = 128
total_length = (len(tokenized_text) // block_size) * block_size  # round to nearest multiple of block size
tokenized_text = tokenized_text[:total_length]
chunks = [tokenized_text[i : i + block_size] for i in range(0, total_length, block_size)]
dataset = Dataset.from_dict({"input_ids": chunks, "labels": chunks.copy()})

training_args = TrainingArguments(
    output_dir=output_dir,
    num_train_epochs=15,
    per_device_train_batch_size=2,
    learning_rate=5e-5,
    fp16=torch.cuda.is_available()
)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=data_collator,
    tokenizer=tokenizer,
)
trainer.train()
trainer.save_model(output_dir)
tokenizer.save_pretrained(output_dir)

fine_tuned_model = GPT2LMHeadModel.from_pretrained(output_dir).to(device)
fine_tuned_tokenizer = GPT2Tokenizer.from_pretrained(output_dir)
finetuned_outputs = pipeline('text-generation', model=fine_tuned_model, tokenizer=fine_tuned_tokenizer, device=device)(
    generation_prompt,
    max_length=max_length_generation,
    pad_token_id=fine_tuned_tokenizer.eos_token_id
)



print("\n--- BASE MODEL OUTPUT ---")
print(base_outputs[0]['generated_text'])
print("\n--- FINE-TUNED MODEL OUTPUT ---")
print(finetuned_outputs[0]['generated_text'])
