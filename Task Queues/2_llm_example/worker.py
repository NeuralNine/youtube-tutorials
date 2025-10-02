import os
import time
import random

from celery import Celery
from openai import OpenAI
from pydantic import BaseModel

app = Celery(
    'movie_info',
    broker = os.getenv('CELERY_BROKER_URL'),
    backend = os.getenv('CELERY_BACKEND_URL')
)

client = OpenAI()

class Movie(BaseModel):
    title: str
    release_year: int
    director: str
    genre: str


@app.task
def movie_info(prompt):
    response = client.beta.chat.completions.parse(
        model = 'gpt-4o-mini',
        messages = [
            {'role': 'system', 'content': 'You are an assistant that provides movie information in a structured way.'},
            {'role': 'user', 'content': prompt}
        ],
        response_format = Movie
    )

    movie = Movie.model_validate_json(response.choices[0].message.content)

    return movie.model_dump()

