import requests

url = 'http://localhost:8080/v1/chat/completions'

headers = {
    'Content-Type': 'application/json',
}

payload = {
    # 'model': 'openai/gpt-4o-mini',
    # 'model': 'mistral/mistral-small-2506',
    'model': 'ollama/qwen3:0.6b',
    # 'messages': [{'role': 'user', 'content': 'What is Python? Answer in one short sentence.'}]
    'messages': [{'role': 'user', 'content': 'Who are you? What model? Answer in one short sentence.'}]
}

response = requests.post(url, headers=headers, json=payload)
print(response.text)

print(response.json()['choices'][0]['message']['content'])
