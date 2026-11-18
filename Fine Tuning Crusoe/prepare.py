import json

from datasets import load_dataset

SYSTEM_PROMPT = "Classify the product into its e-commerce category. Answer with the category only."


def load_products(split):
    columns = ["product_title", "product_description", "ground_truth_category"]
    products = load_dataset("Shopify/product-catalogue", split=split, columns=columns).to_pandas()

    products = products[products.ground_truth_category.str.contains(" > ")]
    products["label"] = products.ground_truth_category.str.split(" > ").str[:2].str.join(" > ")
    descriptions = products.product_description.fillna("").str[:1000]
    products["text"] = "Title: " + products.product_title + "\nDescription: " + descriptions

    return products.reset_index(drop=True)


train_products = load_products("train")
test_products = load_products("test")

labels = sorted(train_products.label.unique())
train_products = train_products.sample(5000, random_state=42)
test_products = test_products[test_products.label.isin(labels)].sample(1000, random_state=42)

with open("train.jsonl", "w") as file:
    for text, label in zip(train_products.text, train_products.label):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
            {"role": "assistant", "content": label},
        ]
        file.write(json.dumps({"messages": messages}) + "\n")

test_products[["text", "label"]].to_json("eval.jsonl", orient="records", lines=True)

with open("labels.json", "w") as file:
    json.dump(labels, file)

