import os
import random

import torch
from PIL import Image
from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

device = 'cuda' if torch.cuda.is_available() else 'cpu'

model = SentenceTransformer(
    'jinaai/jina-clip-v2',
    trust_remote_code=True,
    truncate_dim=1024,
    device=device
)

if not os.path.exists('image_store'):
    client = QdrantClient(path='image_store')

    images = [os.path.join('images', f) for f in os.listdir('images')]
    embeddings = [model.encode(image, normalize_embeddings=True, device=device) for image in images]
    
    client.recreate_collection(
        collection_name='images',
        vectors_config=VectorParams(size=len(embeddings[0]), distance=Distance.COSINE)
    )

    client.upsert(
        collection_name='images',
        points=[
            PointStruct(id=i, vector=embeddings[i], payload={'path': images[i]})
            for i in range(len(images))
        ]
    )

client = QdrantClient(path='image_store')

print('Done')

search_query = input('Enter search query:')
embedded_query = model.encode(search_query, normalize_embeddings=True, device=device)

results = client.query_points(collection_name='images', query=embedded_query, limit=5).points

print([r.payload['path'] for r in results])

