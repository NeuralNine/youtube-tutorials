import time

from celery import group, chord

from worker import movie_info_a, movie_info_b, movie_info_c, combine_parts

prompt = 'Tell me about the movie Shutter Island.'

header = group(
    movie_info_a.s(prompt),
    movie_info_b.s(prompt),
    movie_info_c.s(prompt)
)

result = chord(header)(combine_parts.s())

combined = result.get()

print(combined)

