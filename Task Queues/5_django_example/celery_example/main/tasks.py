# NOTE: New File

import os

from celery import shared_task  # Here we used shared_task
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()


class Movie(BaseModel):
    title: str
    release_year: int
    director: str
    genre: str


@shared_task(bind=True, name="myapp.movie_info")
def movie_info(self, prompt: str):
    resp = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that provides movie information in a structured way."},
            {"role": "user", "content": prompt},
        ],
        response_format=Movie,
    )
    movie = Movie.model_validate_json(resp.choices[0].message.content)
    return movie.model_dump()

