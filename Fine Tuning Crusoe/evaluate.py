import json
from concurrent.futures import ThreadPoolExecutor

import torch
from dotenv import load_dotenv
from openai import OpenAI
from peft import PeftModel
from transformers import AutoModelForImageTextToText, AutoTokenizer

load_dotenv()

with open("labels.json") as file:
    labels = json.load(file)

with open("eval.jsonl") as file:
    products = [json.loads(line) for line in file]

CATEGORY_LIST_PROMPT = "Assign the product to one of these categories. Answer with the category only:\n" + "\n".join(labels)
FINE_TUNED_PROMPT = "Classify the product into its e-commerce category. Answer with the category only."


def accuracy(predictions):
    correct = sum(prediction == product["label"] for prediction, product in zip(predictions, products))
    return correct / len(products)


def evaluate_openai(model):
    client = OpenAI()

    def classify(product):
        response = client.responses.create(model=model, instructions=CATEGORY_LIST_PROMPT, input=product["text"])
        return response.output_text.strip()

    predictions = []

    with ThreadPoolExecutor(8) as pool:
        for prediction in pool.map(classify, products):
            predictions.append(prediction)

            if len(predictions) % 50 == 0:
                print(f"{model}: {len(predictions)}/{len(products)}")

    return accuracy(predictions)


def evaluate_qwen(model_name, adapter=None):
    tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side="left")
    model = AutoModelForImageTextToText.from_pretrained(model_name, dtype=torch.bfloat16).cuda()

    if adapter:
        model = PeftModel.from_pretrained(model, adapter)
        system_prompt = FINE_TUNED_PROMPT
    else:
        system_prompt = CATEGORY_LIST_PROMPT

    predictions = []

    for start in range(0, len(products), 16):
        prompts = [
            tokenizer.apply_chat_template(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": product["text"]},
                ],
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False,
            )
            for product in products[start : start + 16]
        ]

        inputs = tokenizer(prompts, return_tensors="pt", padding=True).to("cuda")
        outputs = model.generate(**inputs, max_new_tokens=40, do_sample=False)
        answers = tokenizer.batch_decode(outputs[:, inputs.input_ids.shape[1]:], skip_special_tokens=True)
        predictions += [answer.strip() for answer in answers]

        print(f"{model_name}: {len(predictions)}/{len(products)}")

    return accuracy(predictions)


print(f"GPT-6 Luna: {evaluate_openai('gpt-6-luna'):.1%}")
print(f"Qwen3.5 2B: {evaluate_qwen('Qwen/Qwen3.5-2B'):.1%}")
print(f"Qwen3.5 4B: {evaluate_qwen('Qwen/Qwen3.5-4B'):.1%}")
print(f"Qwen3.5 2B fine-tuned: {evaluate_qwen('Qwen/Qwen3.5-2B', 'adapters/2b'):.1%}")
print(f"Qwen3.5 4B fine-tuned: {evaluate_qwen('Qwen/Qwen3.5-4B', 'adapters/4b'):.1%}")

