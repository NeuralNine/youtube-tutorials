import os
import uuid
import random

import torch
from PIL import Image
from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue

from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__, static_folder='images', static_url_path='/images')

device = 'cuda' if torch.cuda.is_available() else 'cpu'

model = SentenceTransformer(
    'jinaai/jina-clip-v2',
    trust_remote_code=True,
    truncate_dim=1024,
    device=device
)

client = QdrantClient(path='image_store')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['image_file']
    tags = request.form.get('image_tags', '')

    image_path = os.path.join('images', file.filename)

    file.save(image_path)

    image_embedding = model.encode(image_path, normalize_embeddings=True, device=device)
    
    client.upsert(
        collection_name='images',
        points=[PointStruct(id=uuid.uuid4(), vector=image_embedding, payload={'path': image_path, 'tags': tags})]
    )

    return "Success"


@app.route('/search_query', methods=['POST'])
def search_query():
    search_query = request.form['query']
    embedded_query = model.encode(search_query, normalize_embeddings=True, device=device)

    tag_filter = Filter(must=[FieldCondition(key='tags', match=MatchValue(value=search_query))])
    tag_results = client.query_points(collection_name='images', query=embedded_query, query_filter=tag_filter, limit=5).points

    results = client.query_points(collection_name='images', query=embedded_query, limit=5-len(tag_results)).points

    final_results = tag_results

    for r in results:
        if r not in final_results:
            final_results.append(r)
    
    return render_template('index.html', results=[r.payload['path'] for r in final_results])


if __name__ == '__main__':
    app.run(debug=False)

