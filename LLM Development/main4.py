from llama_cpp import Llama

llm = Llama.from_pretrained(
    repo_id='TheBloke/Llama-2-7B-GGUF',
    filename='llama-2-7b.Q2_K.gguf'
)

prompt = """
Classify the sentiment of the following sentences as Positive, Negative, or Neutral.

Sentence: This is the best pizza I've ever had!
Sentiment: Positive

Sentence: The movie was quite boring and predictable.
Sentiment: Negative

Sentence: The report is due by 5 PM today.
Sentiment: Neutral

Sentence: I'm really disappointed with the customer service.
Sentiment:""" 

output = llm(
    prompt,
    max_tokens=10,
    stop=['\n', 'Sentence:', 'Sentiment:'],
    echo=False
)

predicted_sentiment = output['choices'][0]['text'].strip()
print(predicted_sentiment)
