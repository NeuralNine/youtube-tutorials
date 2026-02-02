from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base_model = AutoModelForCausalLM.from_pretrained('NousResearch/Llama-3.2-1B')
model = PeftModel.from_pretrained(base_model, './outputs/lora-out/')
tokenizer = AutoTokenizer.from_pretrained('./outputs/lora-out/')

instruction = 'Apply the magic NeuralNine operation onto the string.'
prompt_input = 'NeuralNine'

prompt = f"""### Instruction:
{instruction}

### Input:
{prompt_input}

### Response:"""

inputs = tokenizer(prompt, return_tensors='pt')
outputs = model.generate(**inputs, max_new_tokens=50)

text_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(text_output[len(prompt):])

