import os
import time

import requests

from langchain.agents import create_agent
from langchain.tools import tool

from .models import Snapshot, LLMResult


@tool('search_jobs_linkedin', description='Search for jobs on LinkedIn by multiple parameters. Returns snapshot_id. Use the llm_result_id to attach the snapshot to the LLM result object. For country always use proper country codes (e.g., DE, FR, IT, AT etc.).')
def search_jobs_on_linkedin(
        llm_result_id: int,
        location: str,
        keyword: str,
        country: str,
        experience_level: str,
        job_type:str,
        company: str,
        remote: str,
        location_radius: str,
        time_range: str = 'Past month'
):
    url = "https://api.brightdata.com/datasets/v3/trigger"

    headers = {
        "Authorization": f"Bearer {os.getenv('BRIGHTDATA_API_KEY')}",
        "Content-Type": "application/json",
    }

    params = {
    	"dataset_id": "gd_lpfll7v5hcqtkxl6l",
    	"include_errors": "true",
    	"type": "discover_new",
    	"discover_by": "keyword",
        "limit_per_input": "5"
    }

    data = [
    	{
            "location": location,
            "keyword": keyword,
            "country": country,
            "time_range": time_range,
            "job_type": job_type,
            "experience_level": experience_level,
            "remote": remote,
            "company": company,
            "location_radius": location_radius
        },
    ]

    response = requests.post(url, headers=headers, params=params, json=data)

    response.raise_for_status()

    snapshot_id = response.json()['snapshot_id']

    snapshot = Snapshot(
        snapshot_id = snapshot_id,
        ready = False,
        llm_result_id = llm_result_id,
        data = {}
    )
    snapshot.save()

    return "Successfully created snapshot!"


@tool('search_jobs_glassdoor', description='Search for jobs on Glassdoor by multiple parameters. Returns snapshot_id. Use the llm_result_id to attach the snapshot to the LLM result object. For country always use proper country codes (e.g., DE, FR, IT, AT etc.).')
def search_jobs_on_glassdoor(
        llm_result_id: int,
        location: str,
        keyword: str,
        country: str
):
    url = "https://api.brightdata.com/datasets/v3/trigger"

    headers = {
        "Authorization": f"Bearer {os.getenv('BRIGHTDATA_API_KEY')}",
        "Content-Type": "application/json",
    }

    params = {
    	"dataset_id": "gd_lpfbbndm1xnopbrcr0",
    	"include_errors": "true",
    	"type": "discover_new",
    	"discover_by": "keyword",
        "limit_per_input": "5"
    }

    data = [
    	{
            "location": location,
            "keyword": keyword,
            "country": country
        },
    ]

    response = requests.post(url, headers=headers, params=params, json=data)

    response.raise_for_status()

    snapshot_id = response.json()['snapshot_id']

    snapshot = Snapshot(
        snapshot_id = snapshot_id,
        ready = False,
        llm_result_id = llm_result_id,
        data = {}
    )
    snapshot.save()

    return "Successfully created snapshot!"


@tool('set_results_title', description="Set the title of the LLM result object in the database for asynchronous processing. Choose a fitting title.")
def set_results_title(llm_result_id: int, title: str) -> str:
    llm_result = LLMResult.objects.get(id=llm_result_id)
    llm_result.title = title
    llm_result.save()

    return "Success"


def search_jobs_with_agent(llm_result_id: int, prompt: str) -> str:
    agent = create_agent(
        model='gpt-4.1-mini',
        tools=[search_jobs_on_linkedin, search_jobs_on_glassdoor]
    )

    response = agent.invoke({
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant for finding job listings via LinkedIn and Glassdoor based on user prompts.'},
            {'role': 'user', 'content': f"The id of the LLM result is: {llm_result_id}. Always use the tool for setting the title for the given result ID first. Always pass the result ID when calling tools. User request: {prompt}"}
        ]
    })

    return response['messages'][-1].content


def is_ready(snapshot_id: str) -> bool:
    url = f'https://api.brightdata.com/datasets/v3/progress/{snapshot_id}'

    headers = {
        "Authorization": f"Bearer {os.getenv('BRIGHTDATA_API_KEY')}",
        "Content-Type": "application/json",
    }

    return requests.get(url, headers=headers).json()['status'] == 'ready'
    

def get_data(snapshot_id: str) -> dict:
    url = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format=json"

    headers = {
        "Authorization": f"Bearer {os.getenv('BRIGHTDATA_API_KEY')}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    return response.json()

