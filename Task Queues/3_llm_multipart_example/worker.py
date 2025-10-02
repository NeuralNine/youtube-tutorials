import os
import time
import random

from celery import Celery, chord, group
from openai import OpenAI
from pydantic import BaseModel

app = Celery(
    'movie_info',
    broker = os.getenv('CELERY_BROKER_URL'),
    backend = os.getenv('CELERY_BACKEND_URL')
)

client = OpenAI()

class MoviePartA(BaseModel):
    title: str
    release_year: int

class MoviePartB(BaseModel):
    director: str
    genre: str

class MoviePartC(BaseModel):
    actors: list[str]


@app.task
def movie_info_a(prompt):
    response = client.beta.chat.completions.parse(
        model = 'gpt-4o-mini',
        messages = [
            {'role': 'system', 'content': 'You are an assistant that provides movie information in a structured way.'},
            {'role': 'user', 'content': prompt}
        ],
        response_format = MoviePartA
    )

    movie_part_a = MoviePartA.model_validate_json(response.choices[0].message.content)

    return movie_part_a.model_dump()


@app.task
def movie_info_b(prompt):
    response = client.beta.chat.completions.parse(
        model = 'gpt-4o-mini',
        messages = [
            {'role': 'system', 'content': 'You are an assistant that provides movie information in a structured way.'},
            {'role': 'user', 'content': prompt}
        ],
        response_format = MoviePartB
    )

    movie_part_b = MoviePartB.model_validate_json(response.choices[0].message.content)

    return movie_part_b.model_dump()


@app.task
def movie_info_c(prompt):
    response = client.beta.chat.completions.parse(
        model = 'gpt-4o-mini',
        messages = [
            {'role': 'system', 'content': 'You are an assistant that provides movie information in a structured way.'},
            {'role': 'user', 'content': prompt}
        ],
        response_format = MoviePartC
    )

    movie_part_c = MoviePartC.model_validate_json(response.choices[0].message.content)

    return movie_part_c.model_dump()


@app.task
def combine_parts(parts):
    merged = {}

    for part in parts:
        merged.update(part)

    return merged

