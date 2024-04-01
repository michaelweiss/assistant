import json
import numpy as np
import os

from embeddings_utils import get_embedding, cosine_similarity

class VectorDatabase:
    def __init__(self):
        self.index = {}

    def load(self, path):
        """
        Load the database from a file.
        """
        with open(path, "r") as file:
            # Each line is a json object with a document and a vector
            # Example: {"document": "content", "vector": [1, 2, 3]}
            for line in file:
                record = json.loads(line)
                self.index[record["document"]] = record["vector"]

    def save(self, path):
        """
        Save the database to a file.
        """
        with open(path, "w") as file:
            # Each line is a json object with a document and a vector
            for document, vector in self.index.items():
                record = {"document": document, "vector": vector}
                file.write(json.dumps(record) + "\n")
            
    def upsert(self, document, vector):
        """
        Upsert (insert or update) a record into the database.
        """
        self.index[document] = vector

    def query(self, vector, top_k=3):
        """
        Query the database.
        """
        # Find the top top_k closest vectors
        # Assumes that the vectors are normalized
        results = [(doc, cosine_similarity(vec, vector))
            for doc, vec in self.index.items()]
        # Sort the results by similarity
        results = sorted(results, key=lambda r: r[1], reverse=True)
        # Return the corresponding documents and their scores
        return results[:top_k]
    
    def delete(self, document):
        """
        Delete a record from the database.
        """
        del self.index[document]

if __name__ == "__main__":
    from embeddings_utils import get_embedding

    python_facts = [
        "Python is a high-level, interpreted programming language.",
        "Python was created by Guido van Rossum and first released in 1991.",
        "Python is known for its simplicity and readability of code.",
        "Python has a large and active community of developers.",
        "Python supports multiple programming paradigms, including procedural, object-oriented, and functional programming.",
        "Indentation is significant in Python and is used to define blocks of code.",
        "Python has a comprehensive standard library with built-in modules for various tasks.",
        "Popular web frameworks like Django and Flask are built using Python.",
        "Python is used in a wide range of applications, including web development, data analysis, artificial intelligence, and more.",
    ]
    
    db = VectorDatabase()
    if os.path.exists("data/python_facts.json"):
        db.load("data/python_facts.json")
    else:
        for fact in python_facts:
            db.upsert(fact, get_embedding(fact))
        db.save("data/python_facts.json")
    query = "Is Python a compiled language?"
    results = db.query(get_embedding(query), top_k=5)
    print(f"Query: {query}")
    print("Results:")
    for result in results:
        print(f"{result[0], result[1]}")