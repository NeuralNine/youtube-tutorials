from pathlib import Path

import modal

from .common import app
from .moshi import Moshi


frontend = Path(__file__).with_name('frontend')
image = modal.Image.debian_slim(python_version='3.11').pip_install('fastapi').add_local_dir(frontend, '/assets')


@app.function(image=image, timeout=600)
@modal.concurrent(max_inputs=100)
@modal.asgi_app()
def web():
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles

    webapp = FastAPI()

    webapp.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
        allow_credentials=True
    )

    webapp.mount('/', StaticFiles(directory='/assets', html=True))

    return webapp
