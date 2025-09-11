import os
import time

import requests
from dotenv import load_dotenv

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END

load_dotenv()

BRIGHTDATA_API_KEY = os.getenv('BRIGHTDATA_API_KEY')
BRIGHTDATA_SERP_ZONE = os.getenv('BRIGHTDATA_SERP_ZONE')
BRIGHTDATA_GPT_DATASET_ID = os.getenv('BRIGHTDATA_GPT_DATASET_ID')
BRIGHTDATA_PERPLEXITY_DATASET_ID = os.getenv('BRIGHTDATA_PERPLEXITY_DATASET_ID')

HEADERS = {
    'Authorization': f'Bearer {BRIGHTDATA_API_KEY}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}


@tool(description='Search using Google')
def google_search(query):
    print('Google tool is being used...')

    payload = {
        'zone': BRIGHTDATA_SERP_ZONE,
        'url': f'https://google.com/search?q={requests.utils.quote(query)}&brd_json=1',
        'format': 'raw',
        'country': 'US'
    }

    data = requests.post('https://api.brightdata.com/request?async=true', headers=HEADERS, json=payload).json()

    results = []

    for item in data.get('organic'):
        results.append(f"Title: {item['title']}\nLink: {item['link']}\nSnippet: {item.get('description', '')}")

    return '\n\n'.join(results)[:10000]


@tool(description='Search using Bing')
def bing_search(query):
    print('Bing tool is being used...')

    payload = {
        'zone': BRIGHTDATA_SERP_ZONE,
        'url': f'https://bing.com/search?q={requests.utils.quote(query)}&brd_json=1',
        'format': 'raw',
        'country': 'US'
    }

    data = requests.post('https://api.brightdata.com/request?async=true', headers=HEADERS, json=payload).json()

    results = []

    for item in data.get('organic'):
        results.append(f"Title: {item['title']}\nLink: {item['link']}\nSnippet: {item.get('description', '')}")

    return '\n\n'.join(results)[:10000]


@tool(description='Search using Reddit')
def reddit_search(query):
    print('Reddit tool is being used...')

    payload = {
        'zone': BRIGHTDATA_SERP_ZONE,
        'url': f"https://google.com/search?q={requests.utils.quote('site:reddit.com ' + query)}&brd_json=1",
        'format': 'raw',
        'country': 'US'
    }

    data = requests.post('https://api.brightdata.com/request?async=true', headers=HEADERS, json=payload).json()

    results = []

    for item in data.get('organic'):
        results.append(f"Title: {item['title']}\nLink: {item['link']}\nSnippet: {item.get('description', '')}")

    return '\n\n'.join(results)[:10000]


@tool(description='Search using X')
def x_search(query):
    print('X tool is being used...')

    payload = {
        'zone': BRIGHTDATA_SERP_ZONE,
        'url': f"https://google.com/search?q={requests.utils.quote('site:x.com ' + query)}&brd_json=1",
        'format': 'raw',
        'country': 'US'
    }

    data = requests.post('https://api.brightdata.com/request?async=true', headers=HEADERS, json=payload).json()

    results = []

    for item in data.get('organic'):
        results.append(f"Title: {item['title']}\nLink: {item['link']}\nSnippet: {item.get('description', '')}")

    return '\n\n'.join(results)[:10000]


@tool(description='Use ChatGPT to get an answer to a question')
def gpt_prompt(query):
    print('GPT tool is being used...')

    payload = [
        {
            "url": "https://chatgpt.com",
            "prompt": query
        }
    ]

    url = f'https://api.brightdata.com/datasets/v3/trigger?dataset_id={BRIGHTDATA_GPT_DATASET_ID}&format=json&custom_output_fields=answer_text_markdown'

    response = requests.post(url, headers=HEADERS, json=payload)

    snapshot_id = response.json()['snapshot_id']

    while requests.get(f'https://api.brightdata.com/datasets/v3/progress/{snapshot_id}', headers=HEADERS).json()['status'] != 'ready':
        time.sleep(5)

    data = requests.get(f'https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format=json', headers=HEADERS).json()[0]

    return data['answer_text_markdown']


@tool(description='Use Perplexity to do some research for a question')
def perplexity_prompt(query):
    print('Perplexity tool is being used...')

    payload = [
        {
            "url": "https://www.perplexity.ai",
            "prompt": query
        }
    ]

    url = f'https://api.brightdata.com/datasets/v3/trigger?dataset_id={BRIGHTDATA_PERPLEXITY_DATASET_ID}&format=json&custom_output_fields=answer_text_markdown|sources'

    response = requests.post(url, headers=HEADERS, json=payload)

    snapshot_id = response.json()['snapshot_id']

    while requests.get(f'https://api.brightdata.com/datasets/v3/progress/{snapshot_id}', headers=HEADERS).json()['status'] != 'ready':
        time.sleep(5)

    data = requests.get(f'https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format=json', headers=HEADERS).json()[0]

    return data['answer_text_markdown'] + '\n\n' + str(data.get('sources', []))


llm = ChatOpenAI(model_name='gpt-4o', temperature=0)

agent = create_react_agent(
    model = llm,
    tools = [google_search, bing_search, gpt_prompt, perplexity_prompt, reddit_search, x_search],
    debug = False,
    prompt = 'Use all tools at your disposal to answer user questions. Always use at least two tools. Preferably more. When giving an answer aggregate and summarize all information you get. Always provide a complete list of all sources which you used to find the information you provided. Make sure to add ALL links and sources here. Not just a few superficial ones.'
)


def agent_node(state):
    result = agent.invoke({'messages': [('human', state['query'])]})
    state['answer'] = result['messages'][-1].content

    return state


graph = StateGraph(dict)
graph.add_node('agent', agent_node)
graph.set_entry_point('agent')
graph.add_edge('agent', END)
app = graph.compile()


if __name__ == '__main__':
    query = input("Query> ")
    print(app.invoke({'query': query})['answer'])

