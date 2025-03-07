# pip3 install llmwhisperer-client

import time
from unstract.llmwhisperer import LLMWhispererClientV2

client = LLMWhispererClientV2(base_url="https://llmwhisperer-api.us-central.unstract.com/api/v2", api_key='<YOUR API KEY>')

result = client.whisper(file_path="documents/scan-biogenx.pdf")

print(result)

while True:
    status = client.whisper_status(whisper_hash=result["whisper_hash"])
    elif status["status"] == "processed":
        resultx = client.whisper_retrieve(
            whisper_hash=result["whisper_hash"]
        )
        break
    time.sleep(5)

extracted_text = resultx['extraction']['result_text']

print(extracted_text)
