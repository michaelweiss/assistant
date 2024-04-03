import openai
import numpy as np

# Get the embedding for a text
# Here we are still using the "old" text-embedding-ada-002 model, but you can use any model 
# you want, such as the new text-embedding-3-small model
def get_embedding(text, model="text-embedding-ada-002"):
    return openai.embeddings.create(input = [text], model=model).data[0].embedding

# Compute the cosine similarity between two vectors
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))