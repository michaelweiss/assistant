import openai
import numpy as np

# Get the embedding for a text
def get_embedding(text, model="text-embedding-3-large"):
    return openai.embeddings.create(input = [text], model=model).data[0].embedding

# Compute the cosine similarity between two vectors
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))